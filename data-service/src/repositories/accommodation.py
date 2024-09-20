from functools import lru_cache

from src.models.accommodation import Accommodation, Amenity, File

from .base import BaseRepository


class AccommodationRepository(BaseRepository):
    def __init__(self, model: Accommodation):
        super().__init__(model)


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
