"""Test user registration against an isolated PostgreSQL database."""

import os
from uuid import uuid4

import pytest
from app.database import get_db
from app.main import app
from app.models import User
from app.services.password import verify_password
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, select
from sqlalchemy.engine import make_url
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
