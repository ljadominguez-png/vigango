"""Test email/password login responses and JWT issuance."""

from unittest.mock import MagicMock
from uuid import uuid4

import pytest
from app.database import get_db
from app.main import app
from app.models import User
from app.services.password import hash_password
from app.services.tokens import decode_access_token
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session


# Provide an isolated API client and fake database session.
@pytest.fixture
def login_client(monkeypatch):
    db = MagicMock(spec=Session)

    monkeypatch.setenv(
        "JWT_SECRET_KEY",
        "test-only-signing-secret-0123456789-abcdef",
    )

    app.dependency_overrides[get_db] = lambda: db

    try:
        with TestClient(app) as client:
            yield client, db
    finally:
        app.dependency_overrides.pop(get_db, None)


# Verify valid credentials produce a JWT for the correct user.
def test_login_success(login_client):
    client, db = login_client
    user_id = uuid4()

    db.scalar.return_value = User(
        id=user_id,
        username="traveler",
        email="traveler@example.com",
        password_hash=hash_password("ExamplePassword123!"),
    )

    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "traveler@example.com",
            "password": "ExamplePassword123!",
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["token_type"] == "bearer"
    assert set(body) == {"access_token", "token_type"}
    assert decode_access_token(body["access_token"]) == user_id


# Verify incorrect passwords return a generic authentication error.
def test_login_wrong_password(login_client):
    client, db = login_client

    db.scalar.return_value = User(
        id=uuid4(),
        username="traveler",
        email="traveler@example.com",
        password_hash=hash_password("ExamplePassword123!"),
    )

    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "traveler@example.com",
            "password": "WrongPassword123!",
        },
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid email or password."
    assert response.headers["www-authenticate"] == "Bearer"


# Verify unknown accounts cannot authenticate.
def test_login_unknown_account(login_client):
    client, db = login_client
    db.scalar.return_value = None

    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "unknown@example.com",
            "password": "ExamplePassword123!",
        },
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid email or password."


# Verify Google-only accounts cannot log in with a local password.
def test_login_google_only_account(login_client):
    client, db = login_client

    db.scalar.return_value = User(
        id=uuid4(),
        username="google_traveler",
        email="google@example.com",
        google_id="google-user-123",
        password_hash=None,
    )

    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "google@example.com",
            "password": "ExamplePassword123!",
        },
    )

    assert response.status_code == 401


# Verify missing signing configuration never issues an access token.
def test_login_missing_signing_secret(login_client, monkeypatch):
    client, db = login_client

    db.scalar.return_value = User(
        id=uuid4(),
        username="traveler",
        email="traveler@example.com",
        password_hash=hash_password("ExamplePassword123!"),
    )

    monkeypatch.delenv("JWT_SECRET_KEY", raising=False)

    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "traveler@example.com",
            "password": "ExamplePassword123!",
        },
    )

    assert response.status_code == 503
    assert response.json()["detail"] == ("Authentication service is unavailable.")
