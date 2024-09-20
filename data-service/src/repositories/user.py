from functools import lru_cache

from sqlalchemy.ext.asyncio import AsyncSession
from src.models.user import User

from .base import BaseRepository


class UserRepository(BaseRepository):
    def __init__(self, model: User):
        super().__init__(model)

    async def create_user(
        self,
        in_user: dict,
        session: AsyncSession,
        commit: bool = True,
    ) -> User:
        return await self.create(in_user, session, commit)


@lru_cache()
def get_user_repository() -> UserRepository:
    return UserRepository(User)
