"""Disposable HTTP integration fixture. TEST_DATABASE_URL safety checks are shared
with the API tests. Run from backend: python tests/live_server.py
Then opt into app/tests/integration.test.mjs. No live analytics are configured.
"""
import os
import sys
from pathlib import Path
from uuid import uuid4

import psycopg
import uvicorn
from psycopg.conninfo import make_conninfo

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
os.environ["CORS_ORIGINS"] = "http://127.0.0.1:55441"
from test_api import BASE_URL, ROOT, app, get_conn, get_settings


if __name__ == "__main__":
    schema = "live_test_" + uuid4().hex
    with psycopg.connect(BASE_URL, autocommit=True) as conn:
        conn.execute(f'create schema "{schema}"')
    os.environ["DATABASE_URL"] = make_conninfo(BASE_URL, options=f"-c search_path={schema}")
    get_settings.cache_clear()
    try:
        with get_conn() as conn:
            conn.execute((ROOT / "sql/schema.sql").read_text())
        uvicorn.run(app, host="127.0.0.1", port=55440, log_level="warning")
    finally:
        with psycopg.connect(BASE_URL, autocommit=True) as conn:
            conn.execute(f'drop schema "{schema}" cascade')
