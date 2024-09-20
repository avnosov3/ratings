from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from src.models.base import Base


class AbstractRepository(ABC):
    def __init__(self, model: Base):
        self.model = model

    @abstractmethod
    async def get_by_id(self, obj_id: UUID, session: AsyncSession) -> Optional[Base]:
        pass

    @abstractmethod
    async def get_all(
        self,
        session: AsyncSession,
    ) -> list[Base]:
        pass

    @abstractmethod
    async def create(
        self,
        in_obj: dict,
        session: AsyncSession,
    ) -> Base:
        pass

    @abstractmethod
    async def update(
        self,
        db_obj: Base,
        in_obj: dict,
        session: AsyncSession,
    ) -> Base:
        pass

    @abstractmethod
    async def delete(
        self,
        db_obj: Base,
        session: AsyncSession,
    ) -> Base:
        pass

    @abstractmethod
    async def get_by_attribute(
        self,
        attr_name: str,
        attr_value: str,
        session: AsyncSession,
    ) -> Base:
        pass
