from sqlalchemy import BigInteger, Identity, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Category(Base):
    """Heritage, Food, Culture, Recreation, Events, Local Products, Nature, Nightlife."""

    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(BigInteger, Identity(always=True), primary_key=True)
    name: Mapped[str] = mapped_column(Text, unique=True, nullable=False)
    icon: Mapped[str | None] = mapped_column(Text)
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False, server_default="0")

    listings: Mapped[list["Listing"]] = relationship(back_populates="category")