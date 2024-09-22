from pathlib import Path

from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    BASE_DIR: str = Path(__file__).resolve().parents[2].as_posix()

    DATABASE_DSN: PostgresDsn
    TEST_DATABASE_DSN: PostgresDsn
    ECHO_ENABLED: bool = False

    @property
    def DATABASE_URL(self):
        return str(self.DATABASE_DSN)

    @property
    def TEST_DATABASE_URL(self):
        return str(self.TEST_DATABASE_DSN)

    model_config = SettingsConfigDict(env_file=f"{BASE_DIR}/.env", extra="ignore")


settings = Settings()
