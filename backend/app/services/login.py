"""Authenticate local ViganGo accounts using stored password hashes."""

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models import User
from app.services.password import verify_password


# Find an account and validate its local password.
def authenticate_local_user(
    db: Session,
    email: str,
    password: str,
) -> User | None:
    user = db.scalar(select(User).where(func.lower(User.email) == email.lower()))

    if user is None or user.password_hash is None:
        return None

    if not verify_password(password, user.password_hash):
        return None

    return user
