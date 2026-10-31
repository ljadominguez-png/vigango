"""Test validation rules for authentication request schemas."""

import pytest
from app.schemas.auth import RegisterRequest
from pydantic import ValidationError


# Verify that registration rejects an invalid email address.
def test_register_rejects_invalid_email():
    with pytest.raises(ValidationError):
        RegisterRequest(
            username="tester",
            email="not-an-email",
            password="a-long-test-password",
        )
