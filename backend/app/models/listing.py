from datetime import date, datetime, time
from decimal import Decimal
from typing import Optional

from sqlalchemy import (
    BigInteger,
    Boolean,
    CheckConstraint,
    Date,
    DateTime,
    Double,
    ForeignKey,
    Identity,
    Integer,
    Numeric,
    Text,
    Time,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.tag import listing_tags


class Listing(Base):
    """One place, activity, event or product shown in the app."""

    __tablename__ = "listings"
    __table_args__ = (
        CheckConstraint("status in ('draft', 'published', 'hidden')", name="listings_status_check"),
        CheckConstraint("fee_max >= fee_min", name="listings_fee_check"),
    )

    id: Mapped[int] = mapped_column(BigInteger, Identity(always=True), primary_key=True)
    category_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("categories.id"), nullable=False)
    area_id: Mapped[int | None] = mapped_column(BigInteger, ForeignKey("areas.id"))

    title: Mapped[str] = mapped_column(Text, nullable=False)
    short_desc: Mapped[str | None] = mapped_column(Text)
    description: Mapped[str | None] = mapped_column(Text)
    address: Mapped[str | None] = mapped_column(Text)
    latitude: Mapped[float | None] = mapped_column(Double)
    longitude: Mapped[float | None] = mapped_column(Double)

    fee_min: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False, server_default="0")
    fee_max: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False, server_default="0")
    duration_min: Mapped[int | None] = mapped_column(Integer)  # estimated minutes

    is_featured: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default="false")
    status: Mapped[str] = mapped_column(Text, nullable=False, server_default="published")
    contact_info: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    category: Mapped["Category"] = relationship(back_populates="listings")
    area: Mapped[Optional["Area"]] = relationship(back_populates="listings")
    images: Mapped[list["ListingImage"]] = relationship(
        back_populates="listing", cascade="all, delete-orphan", passive_deletes=True
    )
    hours: Mapped[list["OperatingHour"]] = relationship(
        back_populates="listing", cascade="all, delete-orphan", passive_deletes=True
    )
    events: Mapped[list["EventSchedule"]] = relationship(
        back_populates="listing", cascade="all, delete-orphan", passive_deletes=True
    )
    tags: Mapped[list["Tag"]] = relationship(secondary=listing_tags, back_populates="listings")
    favorites: Mapped[list["Favorite"]] = relationship(
        back_populates="listing", cascade="all, delete-orphan", passive_deletes=True
    )
    stats: Mapped[Optional["ListingStats"]] = relationship(
        back_populates="listing",
        uselist=False,
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class ListingStats(Base):
    """
    How many users saved a listing as a favorite.

    Read-only for the app: a database trigger updates favorite_count
    whenever a row is added to or removed from the favorites table.
    Do not change this number from Python code.
    """

    __tablename__ = "listing_stats"

    listing_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("listings.id", ondelete="CASCADE"), primary_key=True
    )
    favorite_count: Mapped[int] = mapped_column(Integer, nullable=False, server_default="0")

    listing: Mapped["Listing"] = relationship(back_populates="stats")


class ListingImage(Base):
    __tablename__ = "listing_images"

    id: Mapped[int] = mapped_column(BigInteger, Identity(always=True), primary_key=True)
    listing_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("listings.id", ondelete="CASCADE"), nullable=False
    )
    image_url: Mapped[str] = mapped_column(Text, nullable=False)
    is_cover: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default="false")

    listing: Mapped["Listing"] = relationship(back_populates="images")


class OperatingHour(Base):
    """Regular weekly schedule. day_of_week: 0 = Sunday ... 6 = Saturday."""

    __tablename__ = "operating_hours"
    __table_args__ = (
        CheckConstraint("day_of_week between 0 and 6", name="operating_hours_day_check"),
        UniqueConstraint("listing_id", "day_of_week"),
    )

    id: Mapped[int] = mapped_column(BigInteger, Identity(always=True), primary_key=True)
    listing_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("listings.id", ondelete="CASCADE"), nullable=False
    )
    day_of_week: Mapped[int] = mapped_column(Integer, nullable=False)
    open_time: Mapped[time | None] = mapped_column(Time)
    close_time: Mapped[time | None] = mapped_column(Time)
    is_closed: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default="false")

    listing: Mapped["Listing"] = relationship(back_populates="hours")


class EventSchedule(Base):
    """Date-based schedule for festivals and one-time or recurring events."""

    __tablename__ = "event_schedules"

    id: Mapped[int] = mapped_column(BigInteger, Identity(always=True), primary_key=True)
    listing_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("listings.id", ondelete="CASCADE"), nullable=False
    )
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date | None] = mapped_column(Date)
    recurrence: Mapped[str | None] = mapped_column(Text)  # e.g. 'yearly', 'every Saturday'
    notes: Mapped[str | None] = mapped_column(Text)

    listing: Mapped["Listing"] = relationship(back_populates="events")