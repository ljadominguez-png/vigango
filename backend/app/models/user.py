import uuid
from typing import TYPE_CHECKING
from datetime import datetime

from sqlalchemy import (
    BigInteger,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Identity,
    Text,
    UniqueConstraint,
    Uuid,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.listing import Listing

class User(Base):
    """
    App account: username, email, and a way to sign in.

    Email accounts store a password_hash made by the backend (argon2),
    never the plain password. Google accounts have no password, so
    password_hash is None and google_id holds Google's stable user ID.
    Every account must have at least one of the two.
    Never return password_hash in an API response.
    """

    __tablename__ = "users"
    __table_args__ = (
        CheckConstraint(
            "password_hash is not null or google_id is not null",
            name="users_login_method_check",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid, primary_key=True, server_default=func.gen_random_uuid()
    )
    username: Mapped[str] = mapped_column(Text, unique=True, nullable=False)
    email: Mapped[str] = mapped_column(Text, unique=True, nullable=False)
    password_hash: Mapped[str | None] = mapped_column(Text)  # None for Google-only accounts
    google_id: Mapped[str | None] = mapped_column(Text, unique=True)  # Google's stable user ID
    image_url: Mapped[str | None] = mapped_column(Text)  # profile picture URL, optional
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    favorites: Mapped[list["Favorite"]] = relationship(
        back_populates="user", cascade="all, delete-orphan", passive_deletes=True
    )


class Favorite(Base):
    """A user saving a listing. One row per (user, listing)."""

    __tablename__ = "favorites"
    __table_args__ = (UniqueConstraint("user_id", "listing_id"),)

    id: Mapped[int] = mapped_column(BigInteger, Identity(always=True), primary_key=True)
    user_id: Mapped[uuid.UUID] = mapped_column(
        Uuid, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    listing_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("listings.id", ondelete="CASCADE"), nullable=False
    )
    saved_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    user: Mapped["User"] = relationship(back_populates="favorites")
    listing: Mapped["Listing"] = relationship(back_populates="favorites")