from posthog import Posthog
import logging

from app.config import get_settings

_client: Posthog | None = None
logger = logging.getLogger(__name__)


def get_posthog() -> Posthog | None:
    global _client
    settings = get_settings()
    if not settings.posthog_key:
        return None
    if _client is None:
        _client = Posthog(settings.posthog_key, host=settings.posthog_host)
    return _client


def capture(distinct_id: str, event: str, properties: dict | None = None) -> None:
    try:
        client = get_posthog()
        if client is None:
            return
        client.capture(distinct_id, event, properties or {})
        client.flush()
    except Exception:
        # The database write has committed; analytics must not turn it into a 500.
        logger.warning("Analytics delivery failed for %s", event, exc_info=True)
