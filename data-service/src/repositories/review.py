from functools import lru_cache

from src.models.review import Locale, Review, Source

from .base import BaseRepository


class ReviewRepository(BaseRepository):
    def __init__(self, model: Review):
        super().__init__(model)


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
