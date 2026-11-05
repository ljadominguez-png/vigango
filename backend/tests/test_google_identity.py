"""Test Google ID token verification and identity validation."""

import pytest
from app.services import google_identity
from google.auth.exceptions import TransportError

CLIENT_ID = "test-client.apps.googleusercontent.com"


# Verify that valid Google claims produce a trusted identity.
def test_verify_valid_google_token(monkeypatch):
    def fake_verify(token, request, audience):
        assert token == "sample-token"
        assert audience == CLIENT_ID

        return {
            "sub": "google-user-123",
            "email": "tester@gmail.com",
            "email_verified": True,
            "picture": "https://example.com/avatar.png",
        }

    monkeypatch.setattr(
        google_identity.google_id_token,
        "verify_oauth2_token",
        fake_verify,
    )

    identity = google_identity.verify_google_token("sample-token", CLIENT_ID)

    assert identity.google_id == "google-user-123"
    assert identity.email == "tester@gmail.com"
    assert identity.picture_url == "https://example.com/avatar.png"


# Verify that invalid Google tokens are rejected.
def test_reject_invalid_google_token(monkeypatch):
    def fake_verify(*args, **kwargs):
        raise ValueError("Invalid token")

    monkeypatch.setattr(
        google_identity.google_id_token,
        "verify_oauth2_token",
        fake_verify,
    )

    with pytest.raises(google_identity.InvalidGoogleToken):
        google_identity.verify_google_token("invalid-token", CLIENT_ID)


# Verify that an unverified email cannot be trusted.
def test_reject_unverified_email(monkeypatch):
    def fake_verify(*args, **kwargs):
        return {
            "sub": "google-user-123",
            "email": "tester@example.com",
            "email_verified": False,
        }

    monkeypatch.setattr(
        google_identity.google_id_token,
        "verify_oauth2_token",
        fake_verify,
    )

    with pytest.raises(google_identity.InvalidGoogleToken):
        google_identity.verify_google_token("sample-token", CLIENT_ID)


# Verify that an identity without Google's stable ID is rejected.
def test_reject_missing_google_id(monkeypatch):
    def fake_verify(*args, **kwargs):
        return {
            "email": "tester@gmail.com",
            "email_verified": True,
        }

    monkeypatch.setattr(
        google_identity.google_id_token,
        "verify_oauth2_token",
        fake_verify,
    )

    with pytest.raises(google_identity.InvalidGoogleToken):
        google_identity.verify_google_token("sample-token", CLIENT_ID)


# Verify that token verification cannot run without a client ID.
def test_reject_missing_client_id():
    with pytest.raises(ValueError):
        google_identity.verify_google_token("sample-token", "")


# Verify that Google transport failures are reported separately.
def test_google_verification_unavailable(monkeypatch):
    def fake_verify(*args, **kwargs):
        raise TransportError("Network unavailable")

    monkeypatch.setattr(
        google_identity.google_id_token,
        "verify_oauth2_token",
        fake_verify,
    )

    with pytest.raises(google_identity.GoogleVerificationUnavailable):
        google_identity.verify_google_token("sample-token", CLIENT_ID)
