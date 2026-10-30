"""
Import every model here so SQLAlchemy knows about all tables and
relationships. Use it like:  from app.models import Listing, Category
"""
from app.models.area import Area
from app.models.category import Category
from app.models.listing import (
    EventSchedule,
    Listing,
    ListingImage,
    ListingStats,
    OperatingHour,
)
from app.models.tag import Tag, listing_tags
from app.models.user import Favorite, User

__all__ = [
    "Area",
    "Category",
    "EventSchedule",
    "Favorite",
    "Listing",
    "ListingImage",
    "ListingStats",
    "OperatingHour",
    "Tag",
    "User",
    "listing_tags",
]