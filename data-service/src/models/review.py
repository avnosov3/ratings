from datetime import datetime
from typing import TYPE_CHECKING, Optional
from uuid import UUID

from sqlalchemy import JSON, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID as POSTGRES_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import CASCADE, SET_NULL, Base

if TYPE_CHECKING:
    from .accommodation import Accommodation
    from .user import User

REVIEW_TITLE_LEN = 128
REVIEW_TRAVEL_DATE_LEN = 8
REVIEW_TRAVEL_PARTY_LEN = 128
REVIEW_STATUS_LEN = 16

LOCALE_CODE_LEN = 5

SOURCE_NAME_LEN = 64
SCORE_ASPECT__NAME_LEN = 64


class Review(Base):
    __tablename__ = "review"

    title: Mapped[Optional[str]] = mapped_column(
        String(REVIEW_TITLE_LEN),
        nullable=True,
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
    travel_date: Mapped[Optional[str]] = mapped_column(
        String(REVIEW_TRAVEL_DATE_LEN),
        nullable=True,
    )
    travel_party: Mapped[Optional[str]] = mapped_column(
        String(REVIEW_TRAVEL_PARTY_LEN),
        nullable=True,
    )
    general_score: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )
    status: Mapped[str] = mapped_column(
        String(REVIEW_STATUS_LEN),
        nullable=False,
    )
    text: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    zoover_review_id: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )
    score_aspects: Mapped[dict] = mapped_column(
        JSON,
        default={},
        nullable=False,
    )

    accommodation_id: Mapped[UUID] = mapped_column(
        POSTGRES_UUID,
        ForeignKey("accommodation.id", ondelete=CASCADE),
    )
    accommodation: Mapped["Accommodation"] = relationship(
        "Accommodation",
        back_populates="reviews",
    )
    user_id: Mapped[UUID] = mapped_column(
        POSTGRES_UUID,
        ForeignKey("user.id", ondelete=CASCADE),
    )
    user: Mapped["User"] = relationship(
        "User",
        back_populates="reviews",
    )
    locale_id: Mapped[Optional[UUID]] = mapped_column(
        POSTGRES_UUID,
        ForeignKey("locale.id", ondelete=SET_NULL),
        nullable=True,
    )
    locale: Mapped[Optional["Locale"]] = relationship(
        "Locale",
        back_populates="reviews",
    )
    source_id: Mapped[Optional[UUID]] = mapped_column(
        POSTGRES_UUID,
        ForeignKey("source.id", ondelete=SET_NULL),
    )
    source: Mapped[Optional["Source"]] = relationship(
        "Source",
        back_populates="reviews",
    )

    def __repr__(self):
        return f"Review(id={self.id} title={self.title:.20s})"


class Locale(Base):
    __tablename__ = "locale"

    code: Mapped[str] = mapped_column(
        String(LOCALE_CODE_LEN),
        unique=True,
        nullable=False,
    )

    reviews: Mapped[Optional[list[Review]]] = relationship(
        "Review",
        back_populates="locale",
    )

    def __repr__(self):
        return f"Locale(id={self.id} code={self.code:.20s})"


class Source(Base):
    __tablename__ = "source"

    name: Mapped[str] = mapped_column(
        String(SOURCE_NAME_LEN),
        unique=True,
        nullable=False,
    )

    reviews: Mapped[Optional[list[Review]]] = relationship(
        "Review",
        back_populates="source",
    )

    def __repr__(self):
        return f"Source(id={self.id} name={self.name:.20s})"
