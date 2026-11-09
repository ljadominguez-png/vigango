"""Test user registration against an isolated PostgreSQL database."""

import os
from uuid import uuid4

import pytest
from app.database import get_db
from app.main import app
from app.models import User
from app.routers import auth as auth_router
from app.services.google_config import get_google_client_id
from app.services.google_identity import GoogleIdentity
from app.services.password import verify_password
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, func, select
from sqlalchemy.engine import make_url
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session


# Provide a PostgreSQL test session with automatic transaction rollback.
@pytest.fixture
def postgres_client():
    url = os.environ.get("TEST_DATABASE_URL")

    if not url:
        pytest.skip("TEST_DATABASE_URL is not configured")

    parsed = make_url(url)

    # Restrict testing to our local disposable PostgreSQL database.
    if (
        parsed.drivername != "postgresql+psycopg"
        or parsed.host != "127.0.0.1"
        or parsed.port != 55432
        or parsed.database != "vigango_test"
        or parsed.username != "vigango_test"
        or parsed.query
    ):
        pytest.fail("Unsafe test database configuration")

    engine = create_engine(url, pool_pre_ping=True)

    try:
        User.__table__.create(bind=engine, checkfirst=True)

        with engine.connect() as connection:
            transaction = connection.begin()

            # Replace the real database dependency with the test session.
            def override_get_db():
                with Session(
                    bind=connection,
                    join_transaction_mode="create_savepoint",
                ) as db:
                    yield db

            app.dependency_overrides[get_db] = override_get_db

            try:
                with TestClient(app) as client:
                    yield client, connection
            finally:
                app.dependency_overrides.pop(get_db, None)
                transaction.rollback()
    finally:
        engine.dispose()


# Verify registration stores a user with a hashed password.
def test_register_persists_user(postgres_client):
    client, connection = postgres_client

    username = f"test_{uuid4().hex[:12]}"
    email = f"{username}@example.com"
    password = "ExamplePassword123!"

    response = client.post(
        "/api/v1/auth/register",
        json={
            "username": username,
            "email": email,
            "password": password,
        },
    )

    assert response.status_code == 201
    assert response.json()["username"] == username
    assert "password_hash" not in response.json()

    stored_hash = connection.execute(
        select(User.password_hash).where(User.username == username)
    ).scalar_one()

    assert stored_hash != password
    assert verify_password(password, stored_hash)


# Verify duplicate usernames and emails are rejected.
def test_register_rejects_duplicates(postgres_client):
    client, _ = postgres_client

    username = f"test_{uuid4().hex[:12]}"
    email = f"{username}@example.com"

    first_response = client.post(
        "/api/v1/auth/register",
        json={
            "username": username,
            "email": email,
            "password": "ExamplePassword123!",
        },
    )

    assert first_response.status_code == 201

    duplicate_username = client.post(
        "/api/v1/auth/register",
        json={
            "username": username,
            "email": "different@example.com",
            "password": "ExamplePassword123!",
        },
    )

    assert duplicate_username.status_code == 409

    duplicate_email = client.post(
        "/api/v1/auth/register",
        json={
            "username": f"other_{uuid4().hex[:12]}",
            "email": email,
            "password": "ExamplePassword123!",
        },
    )

    assert duplicate_email.status_code == 409


# Verify that Google-only accounts can be stored without passwords.
def test_google_only_user_can_be_stored(postgres_client):
    _, connection = postgres_client

    identifier = uuid4().hex

    new_user = User(
        username=f"google_{identifier[:12]}",
        email=f"google_{identifier}@example.com",
        password_hash=None,
        google_id=f"google-sub-{identifier}",
    )

    with Session(
        bind=connection,
        join_transaction_mode="create_savepoint",
    ) as db:
        db.add(new_user)
        db.flush()

        stored_user = db.scalar(
            select(User).where(User.google_id == new_user.google_id)
        )

        assert stored_user is not None
        assert stored_user.password_hash is None
        assert stored_user.google_id == new_user.google_id

        db.commit()


# Verify that accounts cannot exist without a login method.
def test_user_requires_login_method(postgres_client):
    _, connection = postgres_client

    identifier = uuid4().hex

    invalid_user = User(
        username=f"invalid_{identifier[:12]}",
        email=f"invalid_{identifier}@example.com",
        password_hash=None,
        google_id=None,
    )

    with Session(
        bind=connection,
        join_transaction_mode="create_savepoint",
    ) as db:
        db.add(invalid_user)

        with pytest.raises(IntegrityError):
            db.flush()

        db.rollback()


# Provide a verified Google identity without contacting Google.
@pytest.fixture
def trusted_google_identity(monkeypatch):
    identifier = uuid4().hex

    identity = GoogleIdentity(
        google_id=f"google-sub-{identifier}",
        email=f"google_{identifier}@example.com",
        picture_url="https://example.com/avatar.png",
    )

    # Simulate successful verification of a Google ID token.
    def fake_verify(token: str, client_id: str) -> GoogleIdentity:
        assert token == "integration-test-token"
        assert client_id == "integration-test-client"
        return identity

    monkeypatch.setattr(
        auth_router,
        "verify_google_token",
        fake_verify,
    )

    app.dependency_overrides[get_google_client_id] = lambda: "integration-test-client"

    try:
        yield identity
    finally:
        app.dependency_overrides.pop(get_google_client_id, None)


# Verify Google registration persists an account in PostgreSQL.
def test_google_registration_persists_user(postgres_client, trusted_google_identity):
    client, connection = postgres_client
    identity = trusted_google_identity

    response = client.post(
        "/api/v1/auth/google",
        json={
            "id_token": "integration-test-token",
            "username": f"traveler_{uuid4().hex[:12]}",
        },
    )

    assert response.status_code == 201
    assert "google_id" not in response.json()
    assert "password_hash" not in response.json()

    stored = connection.execute(
        select(User.google_id, User.email, User.password_hash).where(
            User.google_id == identity.google_id
        )
    ).one()

    assert stored.google_id == identity.google_id
    assert stored.email == identity.email
    assert stored.password_hash is None


# Verify returning Google users do not create duplicate accounts.
def test_google_registration_returns_existing_user(
    postgres_client, trusted_google_identity
):
    client, connection = postgres_client
    identity = trusted_google_identity

    first = client.post(
        "/api/v1/auth/google",
        json={
            "id_token": "integration-test-token",
            "username": f"traveler_{uuid4().hex[:12]}",
        },
    )

    assert first.status_code == 201

    second = client.post(
        "/api/v1/auth/google",
        json={"id_token": "integration-test-token"},
    )

    assert second.status_code == 200
    assert second.json()["id"] == first.json()["id"]

    count = connection.execute(
        select(func.count())
        .select_from(User)
        .where(User.google_id == identity.google_id)
    ).scalar_one()

    assert count == 1


# Verify Google cannot automatically claim an existing email account.
def test_google_registration_rejects_existing_email(
    postgres_client, trusted_google_identity
):
    client, connection = postgres_client
    identity = trusted_google_identity

    local_account = client.post(
        "/api/v1/auth/register",
        json={
            "username": f"local_{uuid4().hex[:12]}",
            "email": identity.email,
            "password": "ExamplePassword123!",
        },
    )

    assert local_account.status_code == 201

    response = client.post(
        "/api/v1/auth/google",
        json={
            "id_token": "integration-test-token",
            "username": f"google_{uuid4().hex[:12]}",
        },
    )

    assert response.status_code == 409

    stored_google_id = connection.execute(
        select(User.google_id).where(User.email == identity.email)
    ).scalar_one()

    assert stored_google_id is None


# Verify Google registration rejects an occupied username.
def test_google_registration_rejects_existing_username(
    postgres_client, trusted_google_identity
):
    client, connection = postgres_client
    identity = trusted_google_identity

    username = f"taken_{uuid4().hex[:12]}"

    local_account = client.post(
        "/api/v1/auth/register",
        json={
            "username": username,
            "email": f"local_{uuid4().hex}@example.com",
            "password": "ExamplePassword123!",
        },
    )

    assert local_account.status_code == 201

    response = client.post(
        "/api/v1/auth/google",
        json={
            "id_token": "integration-test-token",
            "username": username,
        },
    )

    assert response.status_code == 409

    count = connection.execute(
        select(func.count())
        .select_from(User)
        .where(User.google_id == identity.google_id)
    ).scalar_one()

    assert count == 0


# Reject usernames that differ only by letter casing.
def test_register_rejects_case_variant_username(postgres_client):
    client, _ = postgres_client

    identifier = uuid4().hex[:12]
    username = f"Traveler_{identifier}"

    first = client.post(
        "/api/v1/auth/register",
        json={
            "username": username,
            "email": f"first_{identifier}@example.com",
            "password": "ExamplePassword123!",
        },
    )

    assert first.status_code == 201

    duplicate = client.post(
        "/api/v1/auth/register",
        json={
            "username": username.lower(),
            "email": f"second_{identifier}@example.com",
            "password": "ExamplePassword123!",
        },
    )

    assert duplicate.status_code == 409


# Reject email addresses that differ only by letter casing.
def test_register_rejects_case_variant_email(postgres_client):
    client, _ = postgres_client

    identifier = uuid4().hex[:12]
    email = f"Traveler_{identifier}@example.com"

    first = client.post(
        "/api/v1/auth/register",
        json={
            "username": f"first_{identifier}",
            "email": email,
            "password": "ExamplePassword123!",
        },
    )

    assert first.status_code == 201

    duplicate = client.post(
        "/api/v1/auth/register",
        json={
            "username": f"second_{identifier}",
            "email": email.lower(),
            "password": "ExamplePassword123!",
        },
    )

    assert duplicate.status_code == 409


# Verify PostgreSQL rejects case-variant usernames directly.
def test_database_rejects_case_variant_username(postgres_client):
    _, connection = postgres_client
    identifier = uuid4().hex

    with Session(
        bind=connection,
        join_transaction_mode="create_savepoint",
    ) as db:
        db.add(
            User(
                username=f"Traveler_{identifier[:12]}",
                email=f"first_{identifier}@example.com",
                google_id=f"google-first-{identifier}",
                password_hash=None,
            )
        )
        db.flush()

        db.add(
            User(
                username=f"traveler_{identifier[:12]}",
                email=f"second_{identifier}@example.com",
                google_id=f"google-second-{identifier}",
                password_hash=None,
            )
        )

        with pytest.raises(IntegrityError):
            db.flush()

        db.rollback()


# Verify PostgreSQL rejects case-variant emails directly.
def test_database_rejects_case_variant_email(postgres_client):
    _, connection = postgres_client
    identifier = uuid4().hex

    with Session(
        bind=connection,
        join_transaction_mode="create_savepoint",
    ) as db:
        db.add(
            User(
                username=f"first_{identifier[:12]}",
                email=f"Traveler_{identifier}@example.com",
                google_id=f"google-first-{identifier}",
                password_hash=None,
            )
        )
        db.flush()

        db.add(
            User(
                username=f"second_{identifier[:12]}",
                email=f"traveler_{identifier}@example.com",
                google_id=f"google-second-{identifier}",
                password_hash=None,
            )
        )

        with pytest.raises(IntegrityError):
            db.flush()

        db.rollback()


# Configure a temporary JWT signing key for integration tests.
@pytest.fixture
def jwt_test_key(monkeypatch):
    monkeypatch.setenv(
        "JWT_SECRET_KEY",
        "local-integration-test-secret-0123456789abcdef",
    )


# Verify registration, login, and protected profile retrieval.
def test_login_and_me_with_postgres(postgres_client, jwt_test_key):
    client, connection = postgres_client

    identifier = uuid4().hex
    email = f"login_{identifier}@example.com"

    registered = client.post(
        "/api/v1/auth/register",
        json={
            "username": f"login_{identifier[:12]}",
            "email": email,
            "password": "ExamplePassword123!",
        },
    )

    assert registered.status_code == 201

    login = client.post(
        "/api/v1/auth/login",
        json={
            "email": email,
            "password": "ExamplePassword123!",
        },
    )

    assert login.status_code == 200
    assert login.json()["token_type"] == "bearer"
    assert login.json()["id"] == registered.json()["id"]
    assert "password_hash" not in login.json()

    token = login.json()["access_token"]

    profile = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert profile.status_code == 200
    assert profile.json()["id"] == registered.json()["id"]
    assert profile.json()["email"] == email
    assert "password_hash" not in profile.json()
    assert "google_id" not in profile.json()

    stored_user = connection.execute(
        select(User.id).where(User.email == email)
    ).scalar_one()

    assert str(stored_user) == registered.json()["id"]


# Verify real PostgreSQL accounts reject incorrect passwords.
def test_login_rejects_wrong_password_db(postgres_client, jwt_test_key):
    client, _ = postgres_client

    identifier = uuid4().hex
    email = f"wrong_{identifier}@example.com"

    registered = client.post(
        "/api/v1/auth/register",
        json={
            "username": f"wrong_{identifier[:12]}",
            "email": email,
            "password": "ExamplePassword123!",
        },
    )

    assert registered.status_code == 201

    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": email,
            "password": "IncorrectPassword123!",
        },
    )

    assert response.status_code == 401
    assert response.headers["www-authenticate"] == "Bearer"
    assert "access_token" not in response.json()


# Verify Google-only accounts cannot use local password login.
def test_login_rejects_google_only_account_db(
    postgres_client,
    trusted_google_identity,
    jwt_test_key,
):
    client, _ = postgres_client

    identity = trusted_google_identity

    registered = client.post(
        "/api/v1/auth/google",
        json={
            "id_token": "integration-test-token",
            "username": f"google_{uuid4().hex[:12]}",
        },
    )

    assert registered.status_code == 201

    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": identity.email,
            "password": "ExamplePassword123!",
        },
    )

    assert response.status_code == 401
    assert "access_token" not in response.json()


# Verify email lookup works regardless of letter casing.
def test_login_accepts_case_variant_email_db(
    postgres_client,
    jwt_test_key,
):
    client, _ = postgres_client

    identifier = uuid4().hex
    email = f"Traveler_{identifier}@example.com"

    registered = client.post(
        "/api/v1/auth/register",
        json={
            "username": f"traveler_{identifier[:12]}",
            "email": email,
            "password": "ExamplePassword123!",
        },
    )

    assert registered.status_code == 201

    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": email.lower(),
            "password": "ExamplePassword123!",
        },
    )

    assert response.status_code == 200
    assert response.json()["token_type"] == "bearer"


# Verify a returning Google user receives a token that unlocks their profile.
def test_google_sign_in_and_me_with_postgres(
    postgres_client,
    trusted_google_identity,
    jwt_test_key,
):
    client, _ = postgres_client

    identity = trusted_google_identity

    registered = client.post(
        "/api/v1/auth/google",
        json={
            "id_token": "integration-test-token",
            "username": f"google_{uuid4().hex[:12]}",
        },
    )

    assert registered.status_code == 201

    signed_in = client.post(
        "/api/v1/auth/google",
        json={"id_token": "integration-test-token"},
    )

    assert signed_in.status_code == 200
    assert signed_in.json()["id"] == registered.json()["id"]

    profile = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {signed_in.json()['access_token']}"},
    )

    assert profile.status_code == 200
    assert profile.json()["email"] == identity.email
    assert "google_id" not in profile.json()
