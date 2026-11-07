"""Test JWT creation, verification, expiration, and tampering."""

from datetime import datetime, timedelta, timezone
from uuid import uuid4

import jwt
import pytest
from app.services.tokens import (
    ALGORITHM,
    AUDIENCE,
    ISSUER,
    InvalidAccessToken,
    JWTConfigurationError,
    create_access_token,
    decode_access_token,
)


# Supply a temporary signing key for isolated unit tests.
@pytest.fixture
def signing_secret(monkeypatch):
    key = "local-test-secret-not-for-production-0123456789"
    monkeypatch.setenv("JWT_SECRET_KEY", key)
    return key


# Generate signed test tokens with customizable claims.
def signed_token(key, **overrides):
    now = datetime.now(timezone.utc)

    claims = {
        "sub": str(uuid4()),
        "iss": ISSUER,
        "aud": AUDIENCE,
        "iat": now,
        "nbf": now,
        "exp": now + timedelta(minutes=15),
        "token_type": "access",
    }

    claims.update(overrides)

    return jwt.encode(
        claims,
        key,
        algorithm=ALGORITHM,
    )


# Verify that a created token identifies the correct user.
def test_create_and_decode_access_token(signing_secret):
    user_id = uuid4()

    token = create_access_token(user_id)
    decoded_id = decode_access_token(token)

    assert decoded_id == user_id


# Reject an access token after its expiration.
def test_reject_expired_token(signing_secret):
    token = signed_token(
        signing_secret,
        exp=datetime.now(timezone.utc) - timedelta(seconds=1),
    )

    with pytest.raises(InvalidAccessToken):
        decode_access_token(token)


# Reject a token signed with an unauthorized key.
def test_reject_invalid_signature(signing_secret):
    token = signed_token("wrong-key-with-at-least-32-characters")

    with pytest.raises(InvalidAccessToken):
        decode_access_token(token)


# Reject tokens intended for another application.
def test_reject_wrong_audience(signing_secret):
    token = signed_token(
        signing_secret,
        aud="another-api",
    )

    with pytest.raises(InvalidAccessToken):
        decode_access_token(token)


# Reject tokens issued by another service.
def test_reject_wrong_issuer(signing_secret):
    token = signed_token(
        signing_secret,
        iss="another-service",
    )

    with pytest.raises(InvalidAccessToken):
        decode_access_token(token)


# Reject tokens that are not access tokens.
def test_reject_wrong_token_type(signing_secret):
    token = signed_token(
        signing_secret,
        token_type="refresh",
    )

    with pytest.raises(InvalidAccessToken):
        decode_access_token(token)


# Reject tokens without a valid user UUID.
def test_reject_invalid_subject(signing_secret):
    token = signed_token(
        signing_secret,
        sub="not-a-valid-uuid",
    )

    with pytest.raises(InvalidAccessToken):
        decode_access_token(token)


# Refuse to sign tokens without a configured secret.
def test_reject_missing_secret(monkeypatch):
    monkeypatch.delenv("JWT_SECRET_KEY", raising=False)

    with pytest.raises(JWTConfigurationError):
        create_access_token(uuid4())
