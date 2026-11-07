"""Test validation of email/password login requests."""

import pytest
from app.schemas.auth import LoginRequest
from pydantic import ValidationError


# Accept correctly formatted login credentials.
def test_login_accepts_valid_credentials():
    data = LoginRequest(
        email="traveler@example.com",
        password="ExamplePassword123!",
    )

    assert data.email == "traveler@example.com"


# Reject improperly formatted email addresses.
def test_login_rejects_invalid_email():
    with pytest.raises(ValidationError):
        LoginRequest(
            email="invalid-email",
            password="ExamplePassword123!",
        )


# Reject login requests with empty passwords.
def test_login_rejects_empty_password():
    with pytest.raises(ValidationError):
        LoginRequest(
            email="traveler@example.com",
            password="",
        )
