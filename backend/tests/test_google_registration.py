"""Test Google registration and returning account behavior."""

from unittest.mock import MagicMock
from uuid import uuid4

import pytest
from app.database import get_db
from app.main import app
from app.models import User
from app.routers import auth as auth_router
from app.services.google_config import get_google_client_id
from app.services.google_identity import (
    GoogleIdentity,
    GoogleVerificationUnavailable,
    InvalidGoogleToken,
)
from app.services.tokens import decode_access_token
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session


# Provide a mock database and verified Google identity for testing.
@pytest.fixture
def google_client(monkeypatch):
    fake_db = MagicMock(spec=Session)
    fake_db.scalar.return_value = None

    # Simulate PostgreSQL assigning a user ID.
    def assign_user_id(user):
        user.id = uuid4()

    fake_db.refresh.side_effect = assign_user_id

    # Simulate successful Google identity verification.
    def fake_verify(token, client_id):
        assert token == "sample-token"
        assert client_id == "test-client-id"

        return GoogleIdentity(
            google_id="google-user-123",
            email="tester@gmail.com",
            picture_url="https://example.com/avatar.png",
        )

    monkeypatch.setattr(
        auth_router,
        "verify_google_token",
        fake_verify,
    )

    app.dependency_overrides[get_db] = lambda: fake_db
    app.dependency_overrides[get_google_client_id] = lambda: "test-client-id"

    try:
        with TestClient(app) as client:
            yield client, fake_db
    finally:
        app.dependency_overrides.pop(get_db, None)
        app.dependency_overrides.pop(get_google_client_id, None)


# Verify new Google users are registered successfully.
def test_register_new_google_user(google_client):
    client, fake_db = google_client

    response = client.post(
        "/api/v1/auth/google",
        json={
            "id_token": "sample-token",
            "username": "google_tester",
        },
    )

    assert response.status_code == 201
    assert response.json()["email"] == "tester@gmail.com"
    assert "password_hash" not in response.json()
    assert "google_id" not in response.json()

    user = fake_db.add.call_args.args[0]

    assert user.google_id == "google-user-123"
    assert user.password_hash is None

    # New Google users are signed in immediately.
    assert response.json()["token_type"] == "bearer"
    assert decode_access_token(response.json()["access_token"]) == user.id

    fake_db.commit.assert_called_once()


# Verify returning Google users do not create duplicate accounts.
def test_return_existing_google_user(google_client):
    client, fake_db = google_client

    from app.models import User

    existing_user = User(
        id=uuid4(),
        username="google_tester",
        email="tester@gmail.com",
        google_id="google-user-123",
        password_hash=None,
    )

    fake_db.scalar.return_value = existing_user

    response = client.post(
        "/api/v1/auth/google",
        json={"id_token": "sample-token"},
    )

    assert response.status_code == 200
    assert response.json()["username"] == "google_tester"
    assert decode_access_token(response.json()["access_token"]) == existing_user.id

    fake_db.add.assert_not_called()


# Verify Google sign-in reports missing JWT configuration without a token.
def test_google_sign_in_missing_signing_secret(google_client, monkeypatch):
    client, fake_db = google_client

    fake_db.scalar.return_value = User(
        id=uuid4(),
        username="google_tester",
        email="tester@gmail.com",
        google_id="google-user-123",
        password_hash=None,
    )

    monkeypatch.delenv("JWT_SECRET_KEY", raising=False)

    response = client.post(
        "/api/v1/auth/google",
        json={"id_token": "sample-token"},
    )

    assert response.status_code == 503
    assert "access_token" not in response.json()


# Verify matching emails are not automatically linked.
def test_reject_existing_email(google_client):
    client, fake_db = google_client

    fake_db.scalar.side_effect = [
        None,
        uuid4(),
    ]

    response = client.post(
        "/api/v1/auth/google",
        json={
            "id_token": "sample-token",
            "username": "google_tester",
        },
    )

    assert response.status_code == 409
    fake_db.add.assert_not_called()


# Verify duplicate usernames are rejected.
def test_reject_existing_username(google_client):
    client, fake_db = google_client

    fake_db.scalar.side_effect = [
        None,
        None,
        uuid4(),
    ]

    response = client.post(
        "/api/v1/auth/google",
        json={
            "id_token": "sample-token",
            "username": "google_tester",
        },
    )

    assert response.status_code == 409
    fake_db.add.assert_not_called()


# Verify new accounts require a username.
def test_new_google_user_requires_username(google_client):
    client, fake_db = google_client

    response = client.post(
        "/api/v1/auth/google",
        json={"id_token": "sample-token"},
    )

    assert response.status_code == 422
    fake_db.add.assert_not_called()


# Verify invalid Google credentials are rejected.
def test_reject_invalid_google_token(google_client, monkeypatch):
    client, fake_db = google_client

    # Simulate the Google verifier rejecting the token.
    def reject_token(*args, **kwargs):
        raise InvalidGoogleToken("Invalid token")

    monkeypatch.setattr(
        auth_router,
        "verify_google_token",
        reject_token,
    )

    response = client.post(
        "/api/v1/auth/google",
        json={"id_token": "invalid-token"},
    )

    assert response.status_code == 401
    fake_db.add.assert_not_called()


# Verify temporary Google verification failures return HTTP 503.
def test_google_verification_unavailable(google_client, monkeypatch):
    client, fake_db = google_client

    # Simulate a temporary verification service failure.
    def unavailable(*args, **kwargs):
        raise GoogleVerificationUnavailable("Unavailable")

    monkeypatch.setattr(
        auth_router,
        "verify_google_token",
        unavailable,
    )

    response = client.post(
        "/api/v1/auth/google",
        json={"id_token": "sample-token"},
    )

    assert response.status_code == 503
    fake_db.add.assert_not_called()


# Verify registration fails safely when OAuth is not configured.
def test_google_client_id_not_configured(google_client):
    client, fake_db = google_client

    app.dependency_overrides[get_google_client_id] = lambda: ""

    response = client.post(
        "/api/v1/auth/google",
        json={"id_token": "sample-token"},
    )

    assert response.status_code == 503
    fake_db.add.assert_not_called()
