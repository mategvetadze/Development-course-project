from functools import lru_cache
from typing import Literal
from urllib.parse import urlsplit

from pydantic import Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from psycopg.conninfo import conninfo_to_dict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore", hide_input_in_errors=True)

    database_url: str = Field(default="", repr=False)
    admin_token: str = Field(default="", repr=False)
    posthog_key: str = Field(default="", repr=False)
    posthog_host: str = "https://eu.i.posthog.com"
    cors_origins: str = "http://localhost:3000,http://127.0.0.1:3000"
    app_env: Literal["development", "test", "preview", "production"] = "development"
    internal_anonymous_ids: str = ""

    @model_validator(mode="after")
    def production_configuration(self):
        if self.app_env != "production":
            return self
        try:
            database = conninfo_to_dict(self.database_url)
        except Exception:
            raise ValueError("Invalid production database configuration") from None
        if not database.get("host") or database.get("sslmode") not in ("require", "verify-ca", "verify-full"):
            raise ValueError("Production DATABASE_URL must specify a hosted database and TLS")
        if len(self.admin_token) < 32 or self.admin_token.lower().startswith(("replace", "changeme", "example")):
            raise ValueError("Production ADMIN_TOKEN must be a random secret of at least 32 characters")
        if not self.posthog_key:
            raise ValueError("Production POSTHOG_KEY is required")
        for origin in self.cors_origin_list + [self.posthog_host]:
            parsed = urlsplit(origin)
            if parsed.scheme != "https" or not parsed.hostname or parsed.username or parsed.password or parsed.query or parsed.fragment or parsed.path not in ("", "/"):
                raise ValueError("Production service origins must be HTTPS origins without credentials or paths")
        if not self.cors_origin_list:
            raise ValueError("Production CORS_ORIGINS must name the frontend HTTPS origin")
        return self

    def analytics_context(self, anonymous_id: str) -> dict:
        internal_ids = {value.strip() for value in self.internal_anonymous_ids.split(",") if value.strip()}
        return {"environment": self.app_env, "is_internal": anonymous_id in internal_ids}

    @property
    def cors_origin_list(self) -> list[str]:
        return [o.strip().rstrip("/") for o in self.cors_origins.split(",") if o.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
