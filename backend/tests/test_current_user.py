"""Test JWT-protected endpoints and authentication failures."""

from unittest.mock import MagicMock
from uuid import uuid4

import pytest
from app.database import get_db
from app.main import app
from app.models import User
from app.services.tokens import create_access_token
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session


# Provide a test client with isolated database and JWT configuration.
@pytest.fixture
def protected_client(monkeypatch):
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


# Allow a valid bearer token to retrieve its associated account.
def test_get_current_user_success(protected_client):
    client, db = protected_client
    user_id = uuid4()

    db.get.return_value = User(
        id=user_id,
        username="traveler",
        email="traveler@example.com",
        password_hash="test-hash",
    )

    token = create_access_token(user_id)

    response = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert response.json()["id"] == str(user_id)
    assert response.json()["username"] == "traveler"
    assert "password_hash" not in response.json()
    assert "google_id" not in response.json()

    db.get.assert_called_once_with(User, user_id)


# Reject requests without an authorization header.
def test_get_current_user_missing_token(protected_client):
    client, db = protected_client

    response = client.get("/api/v1/auth/me")

    assert response.status_code == 401
    db.get.assert_not_called()


# Reject malformed JWT access tokens.
def test_get_current_user_invalid_token(protected_client):
    client, db = protected_client

    response = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": "Bearer invalid.jwt.token"},
    )

    assert response.status_code == 401
    db.get.assert_not_called()


# Reject authorization schemes other than Bearer.
def test_get_current_user_wrong_scheme(protected_client):
    client, db = protected_client

    response = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": "Basic invalid"},
    )

    assert response.status_code == 401
    db.get.assert_not_called()


# Reject valid tokens for accounts that no longer exist.
def test_get_current_user_deleted_account(protected_client):
    client, db = protected_client

    db.get.return_value = None

    token = create_access_token(uuid4())

    response = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 401


# Report missing JWT configuration without exposing the secret.
def test_get_current_user_missing_secret(protected_client, monkeypatch):
    client, db = protected_client

    token = create_access_token(uuid4())

    monkeypatch.delenv("JWT_SECRET_KEY", raising=False)

    response = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 503
    db.get.assert_not_called()
