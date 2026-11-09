"""Authenticate local ViganGo accounts using stored password hashes."""

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models import User
from app.services.password import hash_password, verify_password

# Placeholder hash checked when an account has no local password.
DUMMY_PASSWORD_HASH = hash_password("vigango-timing-placeholder")


# Find an account and validate its local password.
def authenticate_local_user(
    db: Session,
    email: str,
    password: str,
) -> User | None:
    user = db.scalar(select(User).where(func.lower(User.email) == email.lower()))

    # Hash the password anyway so response times do not reveal registered emails.
    if user is None or user.password_hash is None:
        verify_password(password, DUMMY_PASSWORD_HASH)
        return None

    if not verify_password(password, user.password_hash):
        return None

    return user
