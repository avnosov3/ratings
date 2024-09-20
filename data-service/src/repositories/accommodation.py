from functools import lru_cache
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from src.models.accommodation import Accommodation, Amenity, File

from .base import BaseRepository


class AccommodationRepository(BaseRepository):
    def __init__(self, model: Accommodation):
        super().__init__(model)

    async def get_expanded_accommodation(
        self,
        accommodation_id: UUID,
        session: AsyncSession,
    ) -> Accommodation:
        result = await session.execute(
            select(Accommodation)
            .options(selectinload(Accommodation.files), selectinload(Accommodation.amenities))
            .where(Accommodation.id == accommodation_id),
        )
        accommodation = result.scalars().first()
        return accommodation


@lru_cache()
def get_accommodation_repository() -> AccommodationRepository:
    return AccommodationRepository(Accommodation)


class FileRepository(BaseRepository):
    def __init__(self, model: File):
        super().__init__(model)


@lru_cache()
def get_file_repository() -> FileRepository:
    return FileRepository(File)


class AmenityRepository(BaseRepository):
    def __init__(self, model: Amenity):
        super().__init__(model)


@lru_cache()
def get_amenity_repository() -> AmenityRepository:
    return AmenityRepository(Amenity)
