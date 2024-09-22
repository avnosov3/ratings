from typing import Annotated, Generator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

from src.core.config import settings


def get_async_engine(db_url: str) -> AsyncEngine:
    return create_async_engine(url=db_url, echo=settings.ECHO_ENABLED)


def get_async_session_maker(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(engine, expire_on_commit=False)


async def get_async_session() -> Generator[AsyncSession, None, None]:
    engine = get_async_engine(settings.DATABASE_URL)
    async_session = get_async_session_maker(engine)

    async with async_session() as session:
        yield session


AsyncSessionDependency = Annotated[AsyncSession, Depends(get_async_session)]
