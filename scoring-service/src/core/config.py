from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    BASE_DIR: str = Path(__file__).resolve().parents[2].as_posix()

    model_config = SettingsConfigDict(env_file=f"{BASE_DIR}/.env", extra="ignore")

    REDIS_HOST: str
    REDIS_PORT: str
    CACHE_LIFETIME: int = 60 * 5
    CACHE_ENABLED: bool

    DATA_SERVICE_ULR: str = "http://localhost:8000"


settings = Settings()
