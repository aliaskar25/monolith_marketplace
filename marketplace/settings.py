from functools import lru_cache
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",  # ignore extra env keys like COMPOSE_PROFILES, API_PORT, DB_HOST_PORT
    )

    app_env: str = "dev"
    api_prefix: str = "/api"

    # Database
    postgres_db: str = "marketplace"
    postgres_user: str = "marketplace"
    postgres_password: str = "marketplace"
    postgres_host: str = "db"
    postgres_port: int = 5432
    database_url: Optional[str] = None

    @property
    def sqlalchemy_async_url(self) -> str:
        if self.database_url:
            return self.database_url
        return (
            f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()  # type: ignore[call-arg]


settings = get_settings()
