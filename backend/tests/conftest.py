"""Share test configuration used by every backend test module."""

import pytest


# Provide a test-only JWT signing key so endpoints that issue tokens work in every test.
@pytest.fixture(autouse=True)
def jwt_signing_key(monkeypatch):
    monkeypatch.setenv(
        "JWT_SECRET_KEY",
        "test-only-signing-secret-0123456789-abcdef",
    )
