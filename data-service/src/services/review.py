from functools import lru_cache
from typing import Annotated, Optional
from uuid import UUID

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.review import Review
from src.repositories.review import ReviewRepository, get_review_repository


class ReviewService:
    def __init__(
        self,
        review_repository: ReviewRepository,
    ) -> None:
        self.review_repository = review_repository

    async def get_reviews_by_accommodation(
        self,
        accommodation_id: UUID,
        session: AsyncSession,
        status: Optional[str] = None,
        time_frame: Optional[str] = None,
        offset: int = 0,
        limit: int = 1000,
    ) -> list[Review]:
        return await self.review_repository.get_reviews_by_accommodation(
            accommodation_id,
            session,
            status,
            time_frame,
            offset,
            limit,
        )

    async def get_review_by_accommodation(
        self,
        accommodation_id: UUID,
        review_id: UUID,
        session: AsyncSession,
    ) -> Review:
        return await self.review_repository.get_review_by_accommodation(accommodation_id, review_id, session)


@lru_cache
def get_review_service() -> ReviewService:
    return ReviewService(get_review_repository())


ReviewServiceDependancy = Annotated[ReviewService, Depends(get_review_service)]
