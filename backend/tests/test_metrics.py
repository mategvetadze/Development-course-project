"""Lab 5/7 metric regressions against real PostgreSQL, not client clocks."""
from concurrent.futures import ThreadPoolExecutor
from unittest.mock import patch
import os
import json
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from uuid import uuid4

import test_api as base
from app.config import get_settings
from app.db import get_conn


class MetricTests(base.DatabaseTestCase):
    def start(self, cards, anonymous_id="student", **extra):
        result = self.client.post(f'/api/sets/{cards["id"]}/start',
                                  json={"anonymous_id": anonymous_id, **extra})
        self.assertEqual(result.status_code, 200, result.text)
        return result.json()

    def complete(self, cards):
        for i in range(5):
            result = self.send(cards, i, ms_total=1)
            self.assertEqual(result.status_code, 200, result.text)
        return result.json()

    def test_start_is_idempotent_and_server_timing_ignores_forged_client_duration(self):
        cards = self.publish()
        first = self.start(cards)
        self.assertEqual(first["started_at"], self.start(cards)["started_at"])
        with get_conn() as conn:
            conn.execute("update student_set_sessions set started_at=clock_timestamp()-interval '6 minutes'")
        self.complete(cards)
        with get_conn() as conn:
            completion = conn.execute("select * from card_set_completions").fetchone()
        self.assertGreaterEqual(completion["ms_total"], 360000)
        self.assertFalse(completion["qualifies"])
        self.assertEqual(self.completion_events()[0]["properties"]["ms_total"], completion["ms_total"])
        self.assertEqual(self.completion_events()[0]["properties"]["completion_id"], str(completion["id"]))

    def test_concurrent_start_and_reload_preserve_one_start_and_one_completion(self):
        cards = self.publish()
        with ThreadPoolExecutor(2) as pool:
            starts = list(pool.map(lambda _: self.start(cards), range(2)))
        self.assertEqual(starts[0]["started_at"], starts[1]["started_at"])
        self.complete(cards)
        self.start(cards)
        self.send(cards, 4)
        with get_conn() as conn:
            self.assertEqual(conn.execute("select count(*) as n from student_set_sessions").fetchone()["n"], 1)
            self.assertEqual(conn.execute("select count(*) as n from card_set_completions").fetchone()["n"], 1)
        self.assertEqual(len(self.completion_events()), 1)

    def test_legacy_client_without_start_can_finish_but_cannot_fake_qualification(self):
        cards = self.publish()
        self.complete(cards)
        with get_conn() as conn:
            row = conn.execute("select started_at, ms_total, qualifies from card_set_completions").fetchone()
        self.assertEqual(row, {"started_at": None, "ms_total": None, "qualifies": False})

    def test_late_start_cannot_reclassify_preexisting_decisions(self):
        cards = self.publish()
        self.send(cards, 0)
        self.assertIsNone(self.start(cards)["started_at"])
        self.complete(cards)
        with get_conn() as conn:
            self.assertFalse(conn.execute("select qualifies from card_set_completions").fetchone()["qualifies"])

    def test_internal_and_environment_context_is_server_controlled(self):
        cards = self.publish()
        with patch.dict(os.environ, {"INTERNAL_ANONYMOUS_IDS": "student", "APP_ENV": "test"}):
            get_settings.cache_clear()
            started = self.start(cards, is_internal=False, environment="production")
            self.assertEqual(started["analytics"], {"is_internal": True, "environment": "test"})
            self.complete(cards)
        get_settings.cache_clear()
        with get_conn() as conn:
            row = conn.execute("select is_internal, environment from card_set_completions").fetchone()
        self.assertEqual(row, {"is_internal": True, "environment": "test"})

    def test_reconciliation_unique_students_boundary_timezone_and_filters(self):
        start = datetime(2026, 11, 16, tzinfo=timezone(timedelta(hours=4)))
        end = start + timedelta(days=7)
        params = dict(window_start=start, window_end=end, environment="production", include_internal=False,
                      set_id=None, excluded_ids=[])
        def fixture(anon, at, duration, *, internal=False, environment="production"):
            cards = self.publish()
            began = at - timedelta(milliseconds=duration) if duration is not None else None
            with get_conn() as conn:
                conn.execute("insert into student_set_sessions values(%s,%s,%s,%s,%s)",
                             (cards["id"], anon, began, environment, internal))
                conn.execute("""insert into card_set_completions(set_id,anonymous_id,started_at,completed_at,
                             apply_count,skip_count,environment,is_internal) values(%s,%s,%s,%s,5,0,%s,%s)""",
                             (cards["id"], anon, began, at, environment, internal))
            return cards["id"]
        fixture("repeat-student", start, 300000)  # inclusive, exactly five minutes
        chosen = fixture("repeat-student", start + timedelta(hours=1), 200)
        fixture("different-student", end - timedelta(microseconds=1), 100)
        fixture("too-late", start, 300001)
        fixture("sub-ms-late", start, 300000.1)
        fixture("missing-clock", start, None)
        fixture("team", start, 100, internal=True)
        fixture("preview", start, 100, environment="preview")
        fixture("end-exclusive", end, 100)
        fixture("before-window", start - timedelta(microseconds=1), 100)
        query = (base.ROOT / "sql/reconcile.sql").read_text()
        with get_conn() as conn:
            result = conn.execute(query, params).fetchone()
            self.assertEqual(result, {"completion_events": 6, "qualifying_completion_events": 3, "north_star_students": 2})
            self.assertEqual(conn.execute(query, {**params, "set_id": chosen}).fetchone()["north_star_students"], 1)
            self.assertEqual(conn.execute(query, {**params, "excluded_ids": ["repeat-student"]}).fetchone()["north_star_students"], 1)
            self.assertEqual(conn.execute(query, {**params, "include_internal": True}).fetchone()["north_star_students"], 3)
        command = [sys.executable, "-m", "scripts.reconcile", "--from", start.isoformat(), "--to", end.isoformat()]
        executed = subprocess.run(command, cwd=base.ROOT, capture_output=True, text=True, timeout=15)
        self.assertEqual(executed.returncode, 0, executed.stderr)
        self.assertEqual(json.loads(executed.stdout)["north_star_students"], 2)

    def test_user_results_are_isolated_and_invalid_start_does_not_write(self):
        cards = self.publish()
        self.start(cards)
        self.send(cards, 0)
        other = self.client.get(f'/api/sets/{cards["id"]}/decisions', params={"anonymous_id": "other"}).json()
        self.assertEqual(other["choices"], {})
        self.assertFalse(other["session_exists"])
        self.assertEqual(self.client.post(f'/api/sets/{uuid4()}/start', json={"anonymous_id": "student"}).status_code, 404)
        self.assertEqual(self.client.post(f'/api/sets/{cards["id"]}/start', json={"anonymous_id": " "}).status_code, 422)
