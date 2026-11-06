"""Verify Google ID tokens and extract trusted account identities."""

from dataclasses import dataclass

from google.auth.exceptions import GoogleAuthError, TransportError
from google.auth.transport.requests import Request
from google.oauth2 import id_token as google_id_token


# Store identity information extracted from a verified Google token.
@dataclass(frozen=True)
class GoogleIdentity:
    google_id: str
    email: str
    picture_url: str | None = None


# Report invalid Google tokens or untrusted account claims.
class InvalidGoogleToken(Exception):
    pass


# Report temporary failures communicating with Google's verification service.
class GoogleVerificationUnavailable(Exception):
    pass


# Verify a Google ID token against the application's OAuth client ID.
def verify_google_token(token: str, client_id: str) -> GoogleIdentity:
    if not client_id.strip():
        raise ValueError("Google OAuth client ID is required.")

    if not token.strip():
        raise InvalidGoogleToken("Google ID token is required.")

    try:
        claims = google_id_token.verify_oauth2_token(
            token,
            Request(),
            audience=client_id,
        )

    except TransportError as exc:
        raise GoogleVerificationUnavailable(
            "Google token verification is temporarily unavailable."
        ) from exc

    except (ValueError, GoogleAuthError) as exc:
        raise InvalidGoogleToken("Invalid Google ID token.") from exc

    google_id = claims.get("sub")
    email = claims.get("email")
    email_verified = claims.get("email_verified")

    if (
        not isinstance(google_id, str)
        or not google_id.strip()
        or not isinstance(email, str)
        or not email.strip()
        or not (email_verified is True or email_verified == "true")
    ):
        raise InvalidGoogleToken("Google token does not contain a verified identity.")

    picture = claims.get("picture")

    return GoogleIdentity(
        google_id=google_id,
        email=email,
        picture_url=picture if isinstance(picture, str) and picture else None,
    )
