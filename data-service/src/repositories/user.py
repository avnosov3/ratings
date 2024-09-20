from functools import lru_cache

from src.models.user import User

from .base import BaseRepository


class UserRepository(BaseRepository):
    def __init__(self, model: User):
        super().__init__(model)


@lru_cache()
def get_user_repository() -> UserRepository:
    return UserRepository(User)
