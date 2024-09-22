from unittest.mock import AsyncMock, Mock

import pytest
from httpx import AsyncClient

from src.core.config import settings
from src.main import create_app
from src.services.cache import CacheRedis, get_cache
from src.services.scoring import ScoreService

test_app = create_app()
test_app.dependency_overrides[get_cache] = lambda: Mock(CacheRedis)
settings.CACHE_ENABLED = False


@pytest.fixture
async def client() -> AsyncClient:
    async with AsyncClient(app=test_app, base_url="http://test") as cl:
        yield cl


@pytest.fixture
async def score_service():
    return ScoreService(client=AsyncMock(), cache=AsyncMock())
