from collections.abc import Iterator
from contextlib import contextmanager

import psycopg
from psycopg.rows import dict_row

from app.config import get_settings


@contextmanager
def get_conn() -> Iterator[psycopg.Connection]:
    settings = get_settings()
    if not settings.database_url:
        raise RuntimeError("DATABASE_URL is not set")
    try:
        with psycopg.connect(settings.database_url, row_factory=dict_row, connect_timeout=10) as conn:
            yield conn
    except psycopg.OperationalError:
        raise RuntimeError("Database unavailable; please try again") from None
