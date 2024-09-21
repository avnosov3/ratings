from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    BASE_DIR: str = Path(__file__).resolve().parents[2].as_posix()

    model_config = SettingsConfigDict(env_file=f"{BASE_DIR}/.env", extra="ignore")


settings = Settings()
