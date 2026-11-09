"""Test local account authentication and invalid credentials."""

from unittest.mock import MagicMock
from uuid import uuid4

import pytest
from app.models import User
from app.services import login
from app.services.login import DUMMY_PASSWORD_HASH, authenticate_local_user
from app.services.password import hash_password
from sqlalchemy.orm import Session


# Provide an account with a valid local password hash.
@pytest.fixture
def local_user():
    return User(
        id=uuid4(),
        username="traveler",
        email="traveler@example.com",
        password_hash=hash_password("ExamplePassword123!"),
    )


# Accept the correct account password.
def test_login_valid_password(local_user):
    db = MagicMock(spec=Session)
    db.scalar.return_value = local_user

    result = authenticate_local_user(
        db,
        "traveler@example.com",
        "ExamplePassword123!",
    )

    assert result is local_user


# Reject an incorrect account password.
def test_login_wrong_password(local_user):
    db = MagicMock(spec=Session)
    db.scalar.return_value = local_user

    result = authenticate_local_user(
        db,
        "traveler@example.com",
        "WrongPassword123!",
    )

    assert result is None


# Reject login attempts for nonexistent accounts.
def test_login_unknown_account():
    db = MagicMock(spec=Session)
    db.scalar.return_value = None

    result = authenticate_local_user(
        db,
        "unknown@example.com",
        "ExamplePassword123!",
    )

    assert result is None


# Reject password authentication for Google-only accounts.
def test_login_google_only_account():
    db = MagicMock(spec=Session)
    db.scalar.return_value = User(
        id=uuid4(),
        username="google_traveler",
        email="google@example.com",
        google_id="google-user-123",
        password_hash=None,
    )

    result = authenticate_local_user(
        db,
        "google@example.com",
        "ExamplePassword123!",
    )

    assert result is None


# Check a placeholder hash for accounts without a local password so login timing
# does not reveal which emails are registered.
@pytest.mark.parametrize(
    "stored_user",
    [
        None,
        User(
            id=uuid4(),
            username="google_traveler",
            email="google@example.com",
            google_id="google-user-123",
            password_hash=None,
        ),
    ],
)
def test_login_without_password_still_hashes(monkeypatch, stored_user):
    db = MagicMock(spec=Session)
    db.scalar.return_value = stored_user

    verify = MagicMock(return_value=True)
    monkeypatch.setattr(login, "verify_password", verify)

    result = authenticate_local_user(
        db,
        "google@example.com",
        "ExamplePassword123!",
    )

    assert result is None
    verify.assert_called_once_with("ExamplePassword123!", DUMMY_PASSWORD_HASH)
