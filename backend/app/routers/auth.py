"""Handle user registration requests through the authentication API."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.schemas.auth import RegisterRequest, UserResponse
from app.services.password import hash_password

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
    existing_user = db.scalar(
        select(User.id).where(
            (User.username == data.username) | (User.email == data.email)
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
