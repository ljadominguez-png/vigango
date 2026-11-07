"""Provide signed, short-lived access tokens for ViganGo sessions."""

import os
from datetime import datetime, timedelta, timezone
from uuid import UUID

import jwt

ALGORITHM = "HS256"
ISSUER = "vigango"
AUDIENCE = "vigango-api"
ACCESS_TOKEN_MINUTES = 15


# Report missing or unsafe JWT signing configuration.
class JWTConfigurationError(RuntimeError):
    pass


# Report an invalid or expired access token.
class InvalidAccessToken(ValueError):
    pass


# Read the JWT signing secret from the environment.
def get_jwt_secret_key() -> str:
    key = os.environ.get("JWT_SECRET_KEY", "")

    if len(key.encode("utf-8")) < 32:
        raise JWTConfigurationError("JWT_SECRET_KEY must be at least 32 bytes.")

    return key


# Create a signed access token for an authenticated user.
def create_access_token(user_id: UUID) -> str:
    now = datetime.now(timezone.utc)

    claims = {
        "sub": str(user_id),
        "iss": ISSUER,
        "aud": AUDIENCE,
        "iat": now,
        "nbf": now,
        "exp": now + timedelta(minutes=ACCESS_TOKEN_MINUTES),
        "token_type": "access",
    }

    return jwt.encode(
        claims,
        get_jwt_secret_key(),
        algorithm=ALGORITHM,
    )


# Verify an access token and return the authenticated user's UUID.
def decode_access_token(token: str) -> UUID:
    if not token.strip():
        raise InvalidAccessToken("Access token is required.")

    key = get_jwt_secret_key()

    try:
        claims = jwt.decode(
            token,
            key,
            algorithms=[ALGORITHM],
            issuer=ISSUER,
            audience=AUDIENCE,
            options={
                "require": [
                    "sub",
                    "iss",
                    "aud",
                    "iat",
                    "nbf",
                    "exp",
                    "token_type",
                ]
            },
        )

    except jwt.InvalidTokenError as exc:
        raise InvalidAccessToken("Invalid or expired access token.") from exc

    if claims.get("token_type") != "access":
        raise InvalidAccessToken("Token is not an access token.")

    try:
        return UUID(claims["sub"])

    except (ValueError, TypeError, AttributeError) as exc:
        raise InvalidAccessToken("Token subject is invalid.") from exc
