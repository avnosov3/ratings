from functools import lru_cache
from uuid import UUID

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.review import Locale, Review, Source

from .base import BaseRepository


class ReviewRepository(BaseRepository):
    def __init__(self, model: Review):
        super().__init__(model)

    async def get_review(
        self,
        review_id: UUID,
        session: AsyncSession,
    ) -> Review:
        return await self.get_by_id(review_id, session)

    async def get_reviews(
        self,
        session: AsyncSession,
    ) -> list[Review]:
        return await self.get_all(session)

    async def create_review(
        self,
        in_review: dict,
        session: AsyncSession,
        commit: bool = True,
    ) -> Review:
        return await self.create(in_review, session, commit)

    async def get_reviews_by_accommodation(
        self,
        accommodation_id: UUID,
        session: AsyncSession,
    ) -> list[Review]:
        result = await session.execute(select(Review).where(Review.accommodation_id == accommodation_id))
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

    async def create_locale(
        self,
        in_locale: dict,
        session: AsyncSession,
        commit: bool = True,
    ) -> Locale:
        return await self.create(in_locale, session, commit)


@lru_cache()
def get_locale_repository() -> LocaleRepository:
    return LocaleRepository(Locale)


class SourceRepository(BaseRepository):
    def __init__(self, model: Source):
        super().__init__(model)

    async def create_source(
        self,
        in_source: dict,
        session: AsyncSession,
        commit: bool = True,
    ) -> Source:
        return await self.create(in_source, session, commit)


@lru_cache()
def get_source_repository() -> SourceRepository:
    return SourceRepository(Source)
