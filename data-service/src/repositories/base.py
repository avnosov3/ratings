from uuid import UUID

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.base import Base

from .abstract import AbstractRepository


class BaseRepository(AbstractRepository):
    def __init__(self, model: Base):
        super().__init__(model=model)

    async def get_by_id(
        self,
        obj_id: UUID,
        session: AsyncSession,
    ) -> Base:
        return await session.get(self.model, obj_id)

    async def get_all(
        self,
        session: AsyncSession,
    ) -> list[Base]:
        objs = await session.scalars(select(self.model))
        return objs.all()

    async def create(
        self,
        in_obj: dict,
        session: AsyncSession,
        commit: bool = True,
    ) -> Base:
        obj = self.model(**in_obj)
        session.add(obj)
        if commit:
            await session.commit()
            await session.refresh(obj)
        return obj

    async def update(
        self,
        db_obj: Base,
        in_obj: dict,
        session: AsyncSession,
        commit: bool = True,
    ) -> Base:
        for field in jsonable_encoder(db_obj):
            if field in in_obj:
                setattr(db_obj, field, in_obj[field])
        session.add(db_obj)
        if commit:
            await session.commit()
            await session.refresh(db_obj)
        return db_obj

    async def delete(
        self,
        db_obj: Base,
        session: AsyncSession,
        commit: bool = True,
    ) -> Base:
        await session.delete(db_obj)
        if commit:
            await session.commit()
        return db_obj

    async def get_by_attribute(
        self,
        attr_name: str,
        attr_value: str,
        session: AsyncSession,
    ) -> Base:
        attr = getattr(self.model, attr_name)
        obj_db = await session.execute(select(self.model).where(attr == attr_value))
        return obj_db.scalars().first()
