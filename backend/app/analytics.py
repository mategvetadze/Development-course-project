from posthog import Posthog
import logging
from uuid import uuid4

from psycopg.types.json import Jsonb

from app.config import get_settings
from app.db import get_conn

_client: Posthog | None = None
logger = logging.getLogger(__name__)


def get_posthog() -> Posthog | None:
    global _client
    settings = get_settings()
    if not settings.posthog_key:
        return None
    if _client is None:
        _client = Posthog(settings.posthog_key, host=settings.posthog_host,
                          sync_mode=True, timeout=3, max_retries=0, disable_geoip=True)
    return _client


def capture(distinct_id: str, event: str, properties: dict | None = None, *, timestamp=None, event_id=None) -> bool:
    try:
        client = get_posthog()
        if client is None:
            return False
        accepted, _ = client.capture(distinct_id, event, {**(properties or {}), "$insert_id": str(event_id)},
                                     timestamp=timestamp, uuid=event_id)
        client.flush()
        return bool(accepted)
    except Exception:
        # Do not log SDK exceptions: upstream messages may contain credentials.
        logger.warning("Analytics delivery failed for %s; event remains pending", event)
        return False


def enqueue(conn, *, distinct_id, event, properties, timestamp=None, event_id=None):
    """Use the SAME transaction as the business write. Delivery happens later."""
    conn.execute(
        """insert into analytics_outbox(id, distinct_id, event, properties, occurred_at)
           values (%s,%s,%s,%s,coalesce(%s,clock_timestamp()))""",
        (event_id or uuid4(), distinct_id, event, Jsonb(properties), timestamp),
    )


def dispatch_pending(limit=20):
    delivered = 0
    with get_conn() as conn:
        with conn.transaction():
            rows = conn.execute(
                """select * from analytics_outbox
                   where delivered_at is null and next_attempt_at <= clock_timestamp()
                   order by occurred_at, id limit %s for update skip locked""", (limit,),
            ).fetchall()
            for row in rows:
                accepted = capture(distinct_id=row["distinct_id"], event=row["event"],
                                   properties=row["properties"], timestamp=row["occurred_at"], event_id=row["id"])
                if accepted:
                    conn.execute("""update analytics_outbox set delivered_at=clock_timestamp(),
                                 attempts=attempts+1, last_error=null where id=%s""", (row["id"],))
                    delivered += 1
                else:
                    conn.execute("""update analytics_outbox set attempts=attempts+1,
                                 last_error='delivery_not_acknowledged',
                                 next_attempt_at=clock_timestamp() + least(3600, 30*power(2,least(attempts,7))) * interval '1 second'
                                 where id=%s""", (row["id"],))
                    break  # avoid hammering a service during an outage
    return delivered
