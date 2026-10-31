"""Test user registration without writing to the real database."""

from unittest.mock import MagicMock
from uuid import uuid4

import pytest
from app.database import get_db
from app.main import app
from app.services.password import verify_password
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session


# Provide an isolated mock database session for registration tests.
@pytest.fixture
def registration_client():
    fake_db = MagicMock(spec=Session)
    fake_db.scalar.return_value = None

    # Simulate the database assigning a new user ID.
    def assign_user_id(user):
        user.id = uuid4()

    fake_db.refresh.side_effect = assign_user_id

    app.dependency_overrides[get_db] = lambda: fake_db

    try:
        with TestClient(app) as client:
            yield client, fake_db
    finally:
        app.dependency_overrides.pop(get_db, None)


# Verify successful registration and secure password storage.
def test_register_success(registration_client):
    client, fake_db = registration_client

    response = client.post(
        "/api/v1/auth/register",
        json={
            "username": "tester",
            "email": "tester@example.com",
            "password": "ExamplePassword123!",
        },
    )

    assert response.status_code == 201
    assert response.json()["username"] == "tester"
    assert "password_hash" not in response.json()

    user = fake_db.add.call_args.args[0]

    assert user.password_hash != "ExamplePassword123!"
    assert verify_password("ExamplePassword123!", user.password_hash)

    fake_db.commit.assert_called_once()


# Verify that an existing account cannot register again.
def test_register_duplicate_user(registration_client):
    client, fake_db = registration_client
    fake_db.scalar.return_value = uuid4()

    response = client.post(
        "/api/v1/auth/register",
        json={
            "username": "tester",
            "email": "tester@example.com",
            "password": "ExamplePassword123!",
        },
    )

    assert response.status_code == 409
    fake_db.add.assert_not_called()


# Verify that invalid email addresses are rejected.
def test_register_invalid_email(registration_client):
    client, fake_db = registration_client

    response = client.post(
        "/api/v1/auth/register",
        json={
            "username": "tester",
            "email": "invalid-email",
            "password": "ExamplePassword123!",
        },
    )

    assert response.status_code == 422
    fake_db.add.assert_not_called()
