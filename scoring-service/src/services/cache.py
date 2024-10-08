import pickle
from abc import ABC, abstractmethod
from functools import wraps
from typing import Annotated, Any, Callable, Optional, Union

from fastapi import Depends
from redis.asyncio import ConnectionPool as AsyncConnectionPool
from redis.asyncio.client import Redis as AsyncRedis

from src.core.config import settings


class AbstractCache(ABC):
    def __init__(self, cache_instance):
        self.cache = cache_instance

    @abstractmethod
    async def get(self, key: str):
        pass

    @abstractmethod
    async def set(self, key: str, value: Union[bytes, str], expire: int):
        pass

    @abstractmethod
    async def close(self):
        pass


class CacheRedis(AbstractCache):
    async def get(self, key: str) -> Optional[dict]:
        return await self.cache.get(key)

    async def set(self, key: str, value: Union[bytes, str], expire: int):
        await self.cache.set(name=key, value=value, ex=expire)

    async def close(self):
        await self.cache.close()


async def get_cache() -> CacheRedis:
    pool = AsyncConnectionPool.from_url(f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}")
    redis = AsyncRedis(connection_pool=pool)
    cache = CacheRedis(redis)
    try:
        yield cache
    finally:
        await cache.close()


CacheDependancy = Annotated[CacheRedis, Depends(get_cache)]


def cache_handler(name: str, expire: Optional[int] = settings.CACHE_LIFETIME) -> Callable[[Any], Any]:
    def decorator(func: Callable) -> Callable[[Any], Any]:
        @wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            if not settings.CACHE_ENABLED:
                return await func(*args, **kwargs)
            cache = getattr(args[0], "cache", None)

            if cache is None:
                raise ValueError("class does not have redis")

            key = hash(f"{name}{str(args[1:])}{kwargs}")

            item = await cache.get(key)
            if item:
                return pickle.loads(item)

            result = await func(*args, **kwargs)
            if result:
                await cache.set(key=key, value=pickle.dumps(result), expire=expire)

            return result

        return wrapper

    return decorator
