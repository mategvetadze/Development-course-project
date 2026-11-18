"""Read-only, parameterized Lab 7 database ground truth. No analytics counts invented."""
import argparse
from datetime import datetime
import json
from pathlib import Path

from app.db import get_conn

SQL = Path(__file__).resolve().parents[1] / "sql/reconcile.sql"


def timestamp(value):
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise argparse.ArgumentTypeError("Timestamp must include a UTC offset")
    return parsed


def main():
    from uuid import UUID
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--from", dest="window_start", type=timestamp, required=True)
    parser.add_argument("--to", dest="window_end", type=timestamp, required=True)
    parser.add_argument("--environment", choices=("production", "preview", "development", "test"), default="production")
    parser.add_argument("--set-id", type=UUID)
    parser.add_argument("--exclude-id", action="append", dest="excluded_ids", default=[])
    parser.add_argument("--include-internal", action="store_true")
    args = parser.parse_args()
    if args.window_end <= args.window_start:
        parser.error("--to must be after --from")
    with get_conn() as conn:
        conn.execute("set transaction read only")
        result = conn.execute(SQL.read_text(), vars(args)).fetchone()
    print(json.dumps({**result, "window_start": args.window_start.isoformat(),
                      "window_end": args.window_end.isoformat(), "environment": args.environment,
                      "metric_version": "server_v1"}))


if __name__ == "__main__":
    main()
