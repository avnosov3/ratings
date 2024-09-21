from functools import lru_cache
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from src.models.accommodation import Accommodation
from src.repositories.accommodation import AccommodationRepository, get_accommodation_repository


class AccommodationService:
    def __init__(
        self,
        accommodation_repository: AccommodationRepository,
    ) -> None:
        self.accommodation_repository = accommodation_repository

    async def get_accommodation(
        self,
        accommodation_id: UUID,
        session: AsyncSession,
    ) -> Accommodation:
        return await self.accommodation_repository.get_accommodation(accommodation_id, session)

    async def get_accommodations(
        self,
        session: AsyncSession,
        offset: int = 0,
        limit: int = 1000,
    ) -> list[Accommodation]:
        return await self.accommodation_repository.get_all(session, offset, limit)

    async def get_expanded_accommodation(
        self,
        accommodation_id: UUID,
        session: AsyncSession,
    ) -> Accommodation:
        return await self.accommodation_repository.get_expanded_accommodation(accommodation_id, session)


@lru_cache
def get_accommodation_service() -> AccommodationService:
    return AccommodationService(get_accommodation_repository())
