from datetime import datetime
from enum import Enum
from functools import lru_cache
from typing import Optional
from uuid import UUID

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.review import Locale, Review, Source

from .base import BaseRepository


class TimeFrame(str, Enum):
    NEWER_THEN_TWO_YEARS = "newer_than_2_years"
    OLDER_THEN_TWO_YEARS = "older_than_2_years"


class ReviewRepository(BaseRepository):
    def __init__(self, model: Review):
        super().__init__(model)

    async def get_reviews_by_accommodation(
        self,
        accommodation_id: UUID,
        session: AsyncSession,
        status: Optional[str] = None,
        time_frame: Optional[str] = None,
        offset: int = 0,
        limit: int = 1000,
    ) -> list[Review]:
        query = select(Review).where(Review.accommodation_id == accommodation_id)
        if status is not None:
            query = query.where(Review.status == status)

        if time_frame is not None:
            two_years_ago = datetime.utcnow().replace(year=datetime.utcnow().year - 2)
            time_frame_mapper = {
                TimeFrame.NEWER_THEN_TWO_YEARS: Review.created_at >= two_years_ago,
                TimeFrame.OLDER_THEN_TWO_YEARS: Review.created_at < two_years_ago,
            }
            query = query.where(time_frame_mapper[time_frame])

        query = query.offset(offset).limit(limit)

        result = await session.execute(query)
        reviews = result.scalars().all()
        return reviews

    async def get_review_by_accommodation(
        self,
        accommodation_id: UUID,
        review_id: UUID,
        session: AsyncSession,
    ) -> Review:
        result = await session.execute(
            select(Review).where(
                and_(
                    Review.accommodation_id == accommodation_id,
                    Review.id == review_id,
                ),
            ),
        )
        review = result.scalars().first()
        return review


@lru_cache()
def get_review_repository() -> ReviewRepository:
    return ReviewRepository(Review)


class LocaleRepository(BaseRepository):
    def __init__(self, model: Locale):
        super().__init__(model)


@lru_cache()
def get_locale_repository() -> LocaleRepository:
    return LocaleRepository(Locale)


class SourceRepository(BaseRepository):
    def __init__(self, model: Source):
        super().__init__(model)


@lru_cache()
def get_source_repository() -> SourceRepository:
    return SourceRepository(Source)
