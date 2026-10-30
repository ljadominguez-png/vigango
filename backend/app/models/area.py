from sqlalchemy import BigInteger, Double, Identity, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Area(Base):
    """Towns in Metro Vigan: Vigan City, Bantay, Caoayan, Santa, ..."""

    __tablename__ = "areas"

    id: Mapped[int] = mapped_column(BigInteger, Identity(always=True), primary_key=True)
    name: Mapped[str] = mapped_column(Text, unique=True, nullable=False)
    center_lat: Mapped[float | None] = mapped_column(Double)
    center_lng: Mapped[float | None] = mapped_column(Double)

    listings: Mapped[list["Listing"]] = relationship(back_populates="area")