"""Identify authenticated users from signed JWT access tokens."""

from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
)
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.services.tokens import (
    InvalidAccessToken,
    JWTConfigurationError,
    decode_access_token,
)

bearer_scheme = HTTPBearer(auto_error=False)


# Verify the bearer token and retrieve its associated user.
def get_current_user(
    credentials: Annotated[
        HTTPAuthorizationCredentials | None,
        Depends(bearer_scheme),
    ],
    db: Annotated[Session, Depends(get_db)],
) -> User:

    unauthorized = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or missing authentication credentials.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if credentials is None:
        raise unauthorized

    try:
        user_id = decode_access_token(credentials.credentials)

    except InvalidAccessToken as exc:
        raise unauthorized from exc

    except JWTConfigurationError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Authentication service is unavailable.",
        ) from exc

    user = db.get(User, user_id)

    if user is None:
        raise unauthorized

    return user
