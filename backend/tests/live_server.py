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


@app.get("/test/state/{anonymous_id}")
def test_state(anonymous_id: str):
    # Test-fixture-only route; app.main does not expose it in deployment.
    with get_conn() as conn:
        decisions = conn.execute("select count(*) as n from decisions where anonymous_id=%s", (anonymous_id,)).fetchone()["n"]
        completions = conn.execute("select id::text, ms_total, qualifies, environment from card_set_completions where anonymous_id=%s",
                                   (anonymous_id,)).fetchall()
        events = conn.execute("select event, properties from analytics_outbox where distinct_id=%s", (anonymous_id,)).fetchall()
    return {"decisions": decisions, "completions": completions, "events": events}


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
