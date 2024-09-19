from datetime import datetime
from typing import TYPE_CHECKING, Optional
from uuid import UUID

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, SmallInteger, String, Text
from sqlalchemy.dialects.postgresql import JSON, UUID as POSTGRES_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import ALL_DELETE, CASCADE, Base

if TYPE_CHECKING:
    from .review import Review

ACCOMMODATION_TYPE_LEN = 64
ACCOMMODATION_NAME_LEN = 256
ACCOMMODATION_SLUG_LEN = 512
ACCOMMODATION_ZIP_CODE_LEN = 16
ACCOMMODATION_STREET_LEN = 1028
ACCOMMODATION_PHONE_LEN = 32
ACCOMMODATION_EMAIL_LEN = 512
ACCOMMODATION_URL_LEN = 1028

FILE_TITLE_LEN = 256

HOLIDAY_TYPE__NAME_LEN = 256

AMENITY_NAME_LEN = 256

DOMAIN_NAME_LEN = 256

THEME_NAME_LEN = 256

DISTANCE_NAME_LEN = 64

AWARD_TYPE_LEN = 16


class Accommodation(Base):
    __tablename__ = "accommodation"

    type: Mapped[str] = mapped_column(
        String(ACCOMMODATION_TYPE_LEN),
        nullable=False,
    )
    name: Mapped[str] = mapped_column(
        String(ACCOMMODATION_NAME_LEN),
        unique=True,
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        nullable=False,
    )
    slug: Mapped[str] = mapped_column(
        String(ACCOMMODATION_SLUG_LEN),
        unique=True,
        nullable=False,
    )
    stars: Mapped[int] = mapped_column(
        SmallInteger,
        nullable=False,
    )
    zip_code: Mapped[str] = mapped_column(
        String(ACCOMMODATION_ZIP_CODE_LEN),
        nullable=False,
    )
    street: Mapped[str] = mapped_column(
        String(ACCOMMODATION_STREET_LEN),
        nullable=False,
    )
    phone: Mapped[str] = mapped_column(
        String(ACCOMMODATION_PHONE_LEN),
        unique=True,
        nullable=False,
    )
    email: Mapped[str] = mapped_column(
        String(ACCOMMODATION_EMAIL_LEN),
        unique=True,
        nullable=False,
    )
    url: Mapped[str] = mapped_column(
        String(ACCOMMODATION_URL_LEN),
        nullable=False,
    )
    is_bookable: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )
    latitude: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )
    longitude: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )
    zoover_gold_award: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )
    zoover_silver_award: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )
    default_price: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )
    facts: Mapped[dict] = mapped_column(
        JSON,
        default={},
        nullable=False,
    )

    files: Mapped[list["File"]] = relationship(
        "File",
        back_populates="accommodation",
        cascade=ALL_DELETE,
    )
    holiday_types: Mapped[list["HolidayType"]] = relationship(
        "HolidayType",
        secondary="accommodation__holiday_type",
        back_populates="accommodations",
    )
    amenities: Mapped[list["Amenity"]] = relationship(
        "Amenity",
        secondary="accommodation__amenity",
        back_populates="accommodations",
    )
    domains: Mapped[list["Domain"]] = relationship(
        "Domain",
        secondary="accommodation__domain",
        back_populates="accommodations",
    )
    themes: Mapped[list["Theme"]] = relationship(
        "Theme",
        secondary="accommodation__theme",
        back_populates="accommodations",
    )
    distances: Mapped[list["Distance"]] = relationship(
        "Distance",
        secondary="accommodation__distance",
        back_populates="accommodations",
    )
    award_links: Mapped[list["AccommodationAward"]] = relationship(
        "AccommodationAward",
        back_populates="accommodation",
    )
    reviews: Mapped[Optional[list["Review"]]] = relationship(
        "Review",
        back_populates="accommodation",
        cascade=ALL_DELETE,
    )

    def __repr__(self):
        return f"Accommodation(id={self.id} name={self.name:.20s})"


class File(Base):
    __tablename__ = "file"

    source_url: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    rotation_degrees: Mapped[Optional[int]] = mapped_column(
        Boolean,
        nullable=True,
    )
    title: Mapped[str] = mapped_column(
        String(FILE_TITLE_LEN),
        nullable=False,
    )
    is_top: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )
    is_default: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    accommodation_id: Mapped[UUID] = mapped_column(
        POSTGRES_UUID,
        ForeignKey("accommodation.id", ondelete=CASCADE),
    )
    accommodation: Mapped[Accommodation] = relationship(
        Accommodation,
        back_populates="files",
    )

    def __repr__(self):
        return f"File(id={self.id} title={self.title:.20s})"


class HolidayType(Base):
    __tablename__ = "holiday_type"

    name: Mapped[str] = mapped_column(
        String(HOLIDAY_TYPE__NAME_LEN),
        unique=True,
        nullable=False,
    )

    accommodations: Mapped[list[Accommodation]] = relationship(
        Accommodation,
        secondary="accommodation__holiday_type",
        back_populates="holiday_types",
    )

    def __repr__(self):
        return f"HolidayType(id={self.id} name={self.name:.20s})"


class AccommodationHolidayType(Base):
    __tablename__ = "accommodation__holiday_type"

    accommodation_id: Mapped[UUID] = mapped_column(
        POSTGRES_UUID,
        ForeignKey("accommodation.id", ondelete=CASCADE),
        primary_key=True,
    )
    holiday_type_id: Mapped[UUID] = mapped_column(
        POSTGRES_UUID,
        ForeignKey("holiday_type.id", ondelete=CASCADE),
        primary_key=True,
    )


class Amenity(Base):
    __tablename__ = "amenity"

    name: Mapped[str] = mapped_column(
        String(AMENITY_NAME_LEN),
        unique=True,
        nullable=False,
    )

    accommodations: Mapped[list[Accommodation]] = relationship(
        Accommodation,
        secondary="accommodation__amenity",
        back_populates="amenities",
    )

    def __repr__(self):
        return f"Amenity(id={self.id} name={self.name:.20s})"


class AccommodationAmenity(Base):
    __tablename__ = "accommodation__amenity"

    accommodation_id: Mapped[UUID] = mapped_column(
        POSTGRES_UUID,
        ForeignKey("accommodation.id", ondelete=CASCADE),
        primary_key=True,
    )
    amenity_id: Mapped[UUID] = mapped_column(
        POSTGRES_UUID,
        ForeignKey("amenity.id", ondelete=CASCADE),
        primary_key=True,
    )


class Domain(Base):
    __tablename__ = "domain"

    name: Mapped[str] = mapped_column(
        String(DOMAIN_NAME_LEN),
        unique=True,
        nullable=False,
    )

    accommodations: Mapped[list[Accommodation]] = relationship(
        Accommodation,
        secondary="accommodation__domain",
        back_populates="domains",
    )

    def __repr__(self):
        return f"Domain(id={self.id} name={self.name:.20s})"


class AccommodationDomain(Base):
    __tablename__ = "accommodation__domain"

    accommodation_id: Mapped[UUID] = mapped_column(
        POSTGRES_UUID,
        ForeignKey("accommodation.id", ondelete=CASCADE),
        primary_key=True,
    )
    domain_id: Mapped[UUID] = mapped_column(
        POSTGRES_UUID,
        ForeignKey("domain.id", ondelete=CASCADE),
        primary_key=True,
    )


class Theme(Base):
    __tablename__ = "theme"

    name: Mapped[str] = mapped_column(
        String(THEME_NAME_LEN),
        unique=True,
        nullable=False,
    )
    is_static: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    accommodations: Mapped[list[Accommodation]] = relationship(
        Accommodation,
        secondary="accommodation__theme",
        back_populates="themes",
    )

    def __repr__(self):
        return f"Theme(id={self.id} name={self.name:.20s})"


class AccommodationTheme(Base):
    __tablename__ = "accommodation__theme"

    accommodation_id: Mapped[UUID] = mapped_column(
        POSTGRES_UUID,
        ForeignKey("accommodation.id", ondelete=CASCADE),
        primary_key=True,
    )
    theme_id: Mapped[UUID] = mapped_column(
        POSTGRES_UUID,
        ForeignKey("theme.id", ondelete=CASCADE),
        primary_key=True,
    )


class Distance(Base):
    __tablename__ = "distance"

    name: Mapped[str] = mapped_column(
        String(DISTANCE_NAME_LEN),
        nullable=False,
    )

    accommodations: Mapped[list[Accommodation]] = relationship(
        Accommodation,
        secondary="accommodation__distance",
        back_populates="distances",
    )

    def __repr__(self):
        return f"Distance(id={self.id} name={self.name:.20s})"


class AccommodationDistance(Base):
    __tablename__ = "accommodation__distance"

    accommodation_id: Mapped[UUID] = mapped_column(
        POSTGRES_UUID,
        ForeignKey("accommodation.id", ondelete=CASCADE),
        primary_key=True,
    )
    distance_id: Mapped[UUID] = mapped_column(
        POSTGRES_UUID,
        ForeignKey("distance.id", ondelete=CASCADE),
        primary_key=True,
    )


class Award(Base):
    __tablename__ = "award"

    rank: Mapped[int] = mapped_column(
        SmallInteger,
        nullable=False,
    )
    type: Mapped[str] = mapped_column(
        String(AWARD_TYPE_LEN),
        nullable=False,
    )
    is_region: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
    )

    accommodation_links: Mapped[list["AccommodationAward"]] = relationship(
        "AccommodationAward",
        back_populates="award",
    )

    def __repr__(self):
        return f"Award(id={self.id} type={self.type})"


class AccommodationAward(Base):
    __tablename__ = "accommodation__award"

    accommodation_id: Mapped[UUID] = mapped_column(
        POSTGRES_UUID,
        ForeignKey("accommodation.id", ondelete=CASCADE),
        primary_key=True,
    )
    award_id: Mapped[UUID] = mapped_column(
        POSTGRES_UUID,
        ForeignKey("award.id", ondelete=CASCADE),
        primary_key=True,
    )
    year: Mapped[int] = mapped_column(
        SmallInteger,
        nullable=False,
    )

    accommodation: Mapped[Accommodation] = relationship(
        Accommodation,
        back_populates="award_links",
    )
    award: Mapped[Award] = relationship(
        Award,
        back_populates="accommodation_links",
    )

    def __repr__(self):
        return f"AccommodationAward(id={self.id} year={self.year})"
