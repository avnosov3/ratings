from functools import lru_cache
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from src.models.accommodation import Accommodation, Amenity, File

from .base import BaseRepository


class AccommodationRepository(BaseRepository):
    def __init__(self, model: Accommodation):
        super().__init__(model)

    async def get_accommodation(
        self,
        accommodation_id: UUID,
        session: AsyncSession,
    ) -> Accommodation:
        return await self.get_by_id(accommodation_id, session)

    async def get_accommodations(
        self,
        session: AsyncSession,
    ) -> list[Accommodation]:
        return await self.get_all(session)

    async def create_accommodation(
        self,
        in_accommodation: dict,
        session: AsyncSession,
        commit: bool = True,
    ) -> Accommodation:
        return await self.create(in_accommodation, session, commit)


@lru_cache()
def get_accommodation_repository() -> AccommodationRepository:
    return AccommodationRepository(Accommodation)


class FileRepository(BaseRepository):
    def __init__(self, model: File):
        super().__init__(model)

    async def create_file(
        self,
        in_file: dict,
        session: AsyncSession,
        commit: bool = True,
    ) -> File:
        return await self.create(in_file, session, commit)


@lru_cache()
def get_file_repository() -> FileRepository:
    return FileRepository(File)


class AmenityRepository(BaseRepository):
    def __init__(self, model: Amenity):
        super().__init__(model)

    async def create_amenity(
        self,
        in_amenity: dict,
        session: AsyncSession,
        commit: bool = True,
    ) -> Amenity:
        return await self.create(in_amenity, session, commit)


@lru_cache()
def get_amenity_repository() -> AmenityRepository:
    return AmenityRepository(Amenity)
