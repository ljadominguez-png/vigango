"""Handle user registration requests through the authentication API."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.schemas.auth import (
    GoogleAuthRequest,
    LoginRequest,
    RegisterRequest,
    TokenResponse,
    UserResponse,
)
from app.services.google_config import get_google_client_id
from app.services.google_identity import (
    GoogleVerificationUnavailable,
    InvalidGoogleToken,
    verify_google_token,
)
from app.services.login import authenticate_local_user
from app.services.password import hash_password
from app.services.tokens import (
    JWTConfigurationError,
    create_access_token,
)

router = APIRouter(
    prefix="/api/v1/auth",
    tags=["Authentication"],
)


# Register a new user with a securely hashed password..
@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register_user(
    data: RegisterRequest, db: Annotated[Session, Depends(get_db)]
) -> User:
    # Check usernames and emails without case sensitivity.
    existing_user = db.scalar(
        select(User.id).where(
            (func.lower(User.username) == data.username.lower())
            | (func.lower(User.email) == data.email.lower())
        )
    )

    if existing_user is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username or email already registered",
        )

    new_user = User(
        username=data.username,
        email=data.email,
        password_hash=hash_password(data.password),
    )

    try:
        db.add(new_user)
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username or email already registered",
        ) from exc

    db.refresh(new_user)

    return new_user


# Register or retrieve a user using a verified Google identity.
@router.post(
    "/google",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register_google_user(
    data: GoogleAuthRequest,
    response: Response,
    db: Annotated[Session, Depends(get_db)],
    client_id: Annotated[str, Depends(get_google_client_id)],
) -> User:

    if not client_id:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Google sign-in is not configured.",
        )

    try:
        identity = verify_google_token(
            data.id_token,
            client_id,
        )
    except InvalidGoogleToken as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Google identity token.",
        ) from exc

    except GoogleVerificationUnavailable as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Google identity verification unavailable.",
        ) from exc

    # Find returning users using Google's stable account ID.
    existing_user = db.scalar(select(User).where(User.google_id == identity.google_id))

    if existing_user is not None:
        response.status_code = status.HTTP_200_OK
        return existing_user

    # Prevent automatic linking to an existing email account.
    existing_email = db.scalar(
        select(User.id).where(func.lower(User.email) == identity.email.lower())
    )

    if existing_email is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An account with this email already exists.",
        )

    if data.username is None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="Username is required for new Google accounts.",
        )

    # Check whether another user already owns the username.
    existing_username = db.scalar(
        select(User.id).where(func.lower(User.username) == data.username.lower())
    )

    if existing_username is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already registered.",
        )

    new_user = User(
        username=data.username,
        email=identity.email,
        google_id=identity.google_id,
        password_hash=None,
        image_url=identity.picture_url,
    )

    try:
        db.add(new_user)
        db.commit()

    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Account conflicts with an existing user.",
        ) from exc

    db.refresh(new_user)

    return new_user


# Authenticate local credentials and issue a signed JWT access token.
@router.post(
    "/login",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
)
def login_user(
    data: LoginRequest,
    db: Annotated[Session, Depends(get_db)],
) -> TokenResponse:

    # Verify the supplied email and password.
    user = authenticate_local_user(
        db,
        data.email,
        data.password,
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create an access token after successful authentication.
    try:
        access_token = create_access_token(user.id)

    except JWTConfigurationError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Authentication service is unavailable.",
        ) from exc

    return TokenResponse(
        access_token=access_token,
    )
