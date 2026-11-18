from concurrent.futures import ThreadPoolExecutor
from threading import Event
from threading import Thread
from unittest.mock import patch
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from datetime import datetime, timezone
from uuid import uuid4
import json
import unittest

from posthog import Posthog

import test_api as base
from app import analytics
from app.db import get_conn


class OutboxTests(base.DatabaseTestCase):
    def finish(self):
        cards = self.publish()
        self.client.post(f'/api/sets/{cards["id"]}/start', json={"anonymous_id": "student"})
        for i in range(5):
            self.assertEqual(self.send(cards, i).status_code, 200)
        return cards

    def test_business_writes_and_timestamped_events_commit_together(self):
        self.finish()
        with get_conn() as conn:
            rows = conn.execute("select * from analytics_outbox").fetchall()
            completion = conn.execute("select * from card_set_completions").fetchone()
        self.assertEqual(len(rows), 7)
        self.assertTrue(all(row["delivered_at"] is None for row in rows))
        event = next(r for r in rows if r["event"] == "student_completes_card_set")
        self.assertEqual(event["occurred_at"], completion["completed_at"])
        self.assertEqual(event["properties"]["completion_id"], str(completion["id"]))
        self.assertEqual(event["properties"]["environment"], "test")

    def test_offline_delivery_retries_same_uuid_and_timestamp_without_failing_writes(self):
        self.finish()
        with patch("app.analytics.capture", return_value=False) as capture:
            self.assertEqual(analytics.dispatch_pending(), 0)
            failed = capture.call_args.kwargs
        with get_conn() as conn:
            self.assertEqual(conn.execute("select count(*) as n from analytics_outbox where delivered_at is null").fetchone()["n"], 7)
            conn.execute("update analytics_outbox set next_attempt_at=clock_timestamp()")
        with patch("app.analytics.capture", return_value=True) as capture:
            self.assertEqual(analytics.dispatch_pending(), 7)
            self.assertEqual(analytics.dispatch_pending(), 0)
            retried = next(c.kwargs for c in capture.call_args_list if c.kwargs["event_id"] == failed["event_id"])
        self.assertEqual(retried, failed)

    def test_two_dispatchers_do_not_send_the_same_locked_events(self):
        self.finish()
        entered, release = Event(), Event()
        def deliver(**kwargs):
            entered.set()
            self.assertTrue(release.wait(timeout=5))
            return True
        with patch("app.analytics.capture", side_effect=deliver) as capture:
            with ThreadPoolExecutor(2) as pool:
                first = pool.submit(analytics.dispatch_pending)
                try:
                    self.assertTrue(entered.wait(timeout=5))
                    second = pool.submit(analytics.dispatch_pending)
                    self.assertEqual(second.result(timeout=3), 0)
                finally:
                    release.set()
                self.assertEqual(first.result(timeout=5), 7)
        self.assertEqual(len({c.kwargs["event_id"] for c in capture.call_args_list}), 7)
        self.assertEqual(capture.call_count, 7)

    def test_failed_publish_rolls_back_cards_and_success_event(self):
        with get_conn() as conn:
            conn.execute("""create function reject_third() returns trigger language plpgsql as $$
                         begin raise exception 'controlled test failure'; end $$""")
            conn.execute("""create trigger reject_third before insert on cards for each row
                         when (new.position=3) execute function reject_third()""")
        response = self.client.post("/api/publish", headers={"X-Admin-Token": "test-admin"}, json={"cards": [base.CARD] * 5})
        self.assertEqual(response.status_code, 500)
        with get_conn() as conn:
            for table in ("card_sets", "cards", "analytics_outbox"):
                self.assertEqual(conn.execute(f"select count(*) as n from {table}").fetchone()["n"], 0)


class TransportTests(unittest.TestCase):
    def test_real_sdk_sync_transport_waits_for_local_receipt_and_keeps_id_and_time(self):
        received = []
        class Handler(BaseHTTPRequestHandler):
            def do_POST(self):
                received.append(json.loads(self.rfile.read(int(self.headers["Content-Length"]))))
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b'{"status":"OK"}')
            def log_message(self, *_):
                pass
        server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        thread = Thread(target=server.serve_forever, daemon=True)
        thread.start()
        at, event_id = datetime(2026, 11, 18, tzinfo=timezone.utc), uuid4()
        client = Posthog("test-only", host=f"http://127.0.0.1:{server.server_port}", sync_mode=True, timeout=2)
        try:
            with patch("app.analytics.get_posthog", return_value=client):
                self.assertTrue(analytics.capture("anonymous-test-id", "student_completes_card_set", {}, timestamp=at, event_id=event_id))
            event = received[0]["batch"][0]
            self.assertEqual(event["uuid"], str(event_id))
            self.assertEqual(event["properties"]["$insert_id"], str(event_id))
            self.assertEqual(event["timestamp"], at.isoformat())
            self.assertEqual(event["distinct_id"], "anonymous-test-id")
            self.assertFalse(event["properties"]["$process_person_profile"])
            self.assertIsNone(event["properties"]["$ip"])
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=3)
