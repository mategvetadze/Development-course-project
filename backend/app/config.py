from functools import lru_cache
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    database_url: str = ""
    admin_token: str = ""
    posthog_key: str = ""
    posthog_host: str = "https://eu.i.posthog.com"
    cors_origins: str = "http://localhost:3000,http://127.0.0.1:3000"
    app_env: Literal["development", "test", "preview", "production"] = "development"
    internal_anonymous_ids: str = ""

    def analytics_context(self, anonymous_id: str) -> dict:
        internal_ids = {value.strip() for value in self.internal_anonymous_ids.split(",") if value.strip()}
        return {"environment": self.app_env, "is_internal": anonymous_id in internal_ids}

    @property
    def cors_origin_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
