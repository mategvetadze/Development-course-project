"""Manually drain one outbox batch. Requires the configured project key; no key is printed."""
import argparse
import json

from app.analytics import dispatch_pending
from app.config import get_settings


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--limit", type=int, default=100)
    args = parser.parse_args()
    if not 1 <= args.limit <= 1000:
        parser.error("--limit must be between 1 and 1000")
    if not get_settings().posthog_key:
        parser.error("POSTHOG_KEY is not configured; no delivery attempted")
    print(json.dumps({"acknowledged": dispatch_pending(args.limit)}))
