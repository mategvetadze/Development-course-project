from fastapi import APIRouter, Depends, HTTPException
import psycopg

from app.auth import require_admin
from app.config import get_settings
from app.db import get_conn

router = APIRouter(tags=["health"])


@router.get("/health")
def health():
    return {"ok": True, "service": "careercards-backend"}


@router.get("/health/ready")
def ready():
    try:
        with get_conn() as conn:
            conn.execute("select id from cards limit 0")
            conn.execute("select started_at from student_set_sessions limit 0")
            conn.execute("select ms_total, qualifies from card_set_completions limit 0")
            conn.execute("select next_attempt_at from analytics_outbox limit 0")
    except (RuntimeError, psycopg.Error):
        raise HTTPException(status_code=503, detail="Database or required migrations unavailable") from None
    return {"ok": True, "database": "ready", "analytics_configured": bool(get_settings().posthog_key)}


@router.get("/api/admin/analytics", dependencies=[Depends(require_admin)])
def analytics_status():
    try:
        with get_conn() as conn:
            row = conn.execute("""select count(*) filter (where delivered_at is null)::int as pending,
                               count(*) filter (where delivered_at is not null)::int as acknowledged,
                               min(occurred_at) filter (where delivered_at is null) as oldest_pending_at
                               from analytics_outbox""").fetchone()
    except (RuntimeError, psycopg.Error):
        raise HTTPException(status_code=503, detail="Analytics diagnostics unavailable") from None
    return {**row, "configured": bool(get_settings().posthog_key), "environment": get_settings().app_env}
