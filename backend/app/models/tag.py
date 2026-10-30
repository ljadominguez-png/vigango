from sqlalchemy import BigInteger, Column, ForeignKey, Identity, Table, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

# Join table (many-to-many between listings and tags)
listing_tags = Table(
    "listing_tags",
    Base.metadata,
    Column(
        "listing_id",
        BigInteger,
        ForeignKey("listings.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "tag_id",
        BigInteger,
        ForeignKey("tags.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)


class Tag(Base):
    """Keywords such as 'empanada', 'kalesa', 'pottery', 'free entry'."""

    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(BigInteger, Identity(always=True), primary_key=True)
    name: Mapped[str] = mapped_column(Text, unique=True, nullable=False)

    listings: Mapped[list["Listing"]] = relationship(
        secondary=listing_tags, back_populates="tags"
    )