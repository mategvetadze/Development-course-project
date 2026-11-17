"""Real PostgreSQL regressions. Run: python -m unittest discover -s tests -v.

Requires TEST_DATABASE_URL pointing to a disposable loopback careercards_test* DB.
Each test creates and drops its own schema; no production schema is touched.
"""
import os
import threading
import unittest
from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager
from pathlib import Path
from unittest.mock import patch
from uuid import uuid4

import psycopg
from psycopg.conninfo import conninfo_to_dict, make_conninfo
from fastapi.testclient import TestClient

BASE_URL = os.environ.get("TEST_DATABASE_URL", "")
if not BASE_URL:
    raise RuntimeError("Set TEST_DATABASE_URL to a disposable local PostgreSQL database")
info = conninfo_to_dict(BASE_URL)
if info.get("host") not in ("127.0.0.1", "localhost", "::1") or not info.get("dbname", "").startswith("careercards_test"):
    raise RuntimeError("Tests require a loopback careercards_test* database")
os.environ.update(DATABASE_URL=BASE_URL, ADMIN_TOKEN="test-admin", POSTHOG_KEY="")

from app.config import get_settings
from app.db import get_conn
from app.main import app
from app.routers import decide

ROOT = Path(__file__).resolve().parents[1]
CARD = dict(role="Engineer", company="Example", field="IT", source="Example",
            source_url="https://example.com/job", students_ok=True, experience="None",
            hours="Part time", pay="", deadline="2027-01-01")


class ApiTests(unittest.TestCase):
    schema_file = ROOT / "sql/schema.sql"

    def setUp(self):
        self.schema = "test_" + uuid4().hex
        with psycopg.connect(BASE_URL, autocommit=True) as conn:
            conn.execute(f'create schema "{self.schema}"')
        os.environ["DATABASE_URL"] = make_conninfo(BASE_URL, options=f"-c search_path={self.schema}")
        get_settings.cache_clear()
        with get_conn() as conn:
            conn.execute(self.schema_file.read_text())
        self.events = []
        def capture(**event):
            self.events.append(event)
        for module in ("app.routers.publish", "app.routers.decide"):
            p = patch(module + ".capture", side_effect=capture)
            p.start()
            self.addCleanup(p.stop)
        self.client = TestClient(app, raise_server_exceptions=False)
        self.addCleanup(self.client.close)

    def tearDown(self):
        with psycopg.connect(BASE_URL, autocommit=True) as conn:
            conn.execute(f'drop schema "{self.schema}" cascade')
        get_settings.cache_clear()

    def publish(self):
        result = self.client.post("/api/publish", headers={"X-Admin-Token": "test-admin"},
                                  json={"cards": [dict(CARD, role=f"Role {i}") for i in range(5)]})
        self.assertEqual(result.status_code, 200, result.text)
        latest = self.client.get("/api/sets/latest").json()
        self.assertEqual(latest["id"], result.json()["set_id"])
        self.assertEqual([c["position"] for c in latest["cards"]], list(range(1, 6)))
        self.assertEqual(latest["cards"][0]["pay"], "Pay: not stated")
        return latest

    def body(self, card_set, i, **extra):
        return dict(set_id=card_set["id"], card_id=card_set["cards"][i]["id"],
                    position=i + 1, decision="apply", anonymous_id="student", ms_on_card=100,
                    ms_total=500, **extra)

    def send(self, card_set, i, **extra):
        body = self.body(card_set, i)
        body.update(extra)
        return self.client.post("/api/decide", json=body)

    def completion_events(self):
        return [e for e in self.events if e["event"] == "student_completes_card_set"]

    def test_publish_decide_reload_summary_and_idempotency(self):
        self.assertIsNone(self.client.get("/api/sets/latest").json())
        cards = self.publish()
        for i in range(5):
            result = self.send(cards, i, decision="skip" if i == 1 else "apply",
                               skip_reason="hours" if i == 1 else None)
            self.assertEqual(result.status_code, 200, result.text)
            self.assertEqual(result.json()["complete"], i == 4)
        summary = result.json()["summary"]
        self.assertEqual([r["role"] for r in summary], ["Role 0", "Role 2", "Role 3", "Role 4"])
        repeated = self.send(cards, 0, decision="skip", skip_reason="other").json()
        self.assertEqual(repeated["decision"], "apply")
        self.assertEqual(repeated["summary"], summary)
        restored = self.client.get(f'/api/sets/{cards["id"]}/decisions', params={"anonymous_id": "student"})
        self.assertEqual(restored.status_code, 200, restored.text)
        self.assertEqual(restored.json()["choices"][cards["cards"][1]["id"]], "skip")
        self.assertEqual(restored.json()["summary"], summary)
        self.assertEqual(len(self.completion_events()), 1)
        self.assertEqual(self.completion_events()[0]["properties"]["apply_count"], 4)
        with get_conn() as conn:
            rows = conn.execute("select ms_total from decisions").fetchall()
        self.assertEqual(len(rows), 5)
        self.assertTrue(all(r["ms_total"] == 500 for r in rows))

    def test_rejects_cross_set_and_wrong_position_without_writes(self):
        first, second = self.publish(), self.publish()
        self.assertEqual(self.send(first, 0, card_id=second["cards"][0]["id"]).status_code, 404)
        self.assertEqual(self.send(first, 0, position=5).status_code, 400)
        self.assertEqual(self.send(first, 0, card_id=str(uuid4())).status_code, 404)
        with get_conn() as conn:
            self.assertEqual(conn.execute("select count(*) as n from decisions").fetchone()["n"], 0)

    def test_database_rejects_cross_set_even_without_api(self):
        first, second = self.publish(), self.publish()
        with self.assertRaises(psycopg.errors.ForeignKeyViolation):
            with get_conn() as conn:
                conn.execute("insert into decisions(set_id,card_id,anonymous_id,decision) values (%s,%s,'x','apply')",
                             (first["id"], second["cards"][0]["id"]))

    def test_concurrent_last_two_decisions_emit_one_completion(self):
        cards = self.publish()
        for i in range(3):
            self.assertEqual(self.send(cards, i).status_code, 200)
        # Hold transactions open at their commit boundary. Without serialization,
        # both requests see only four rows. A serialized writer times out here,
        # commits, and lets the second writer observe all five. No SQL is mocked.
        commit_barrier = threading.Barrier(2)
        real_get_conn = decide.get_conn
        @contextmanager
        def coordinated_connection():
            with real_get_conn() as conn:
                class Connection:
                    def __getattr__(self, name):
                        return getattr(conn, name)
                    @contextmanager
                    def transaction(self):
                        with conn.transaction():
                            yield
                            try:
                                commit_barrier.wait(timeout=1)
                            except threading.BrokenBarrierError:
                                pass
                yield Connection()
        with patch.object(decide, "get_conn", coordinated_connection):
            with ThreadPoolExecutor(2) as pool:
                responses = list(pool.map(lambda i: self.send(cards, i), (3, 4)))
        self.assertEqual([r.status_code for r in responses], [200, 200])
        self.assertEqual(sum(r.json()["complete"] for r in responses), 1)
        self.assertEqual(len(self.completion_events()), 1)
        self.assertEqual(len(self.send(cards, 4).json()["summary"]), 5)

    def test_all_skip_and_concurrent_duplicate(self):
        cards = self.publish()
        with ThreadPoolExecutor(2) as pool:
            responses = list(pool.map(lambda _: self.send(cards, 0, decision="skip", skip_reason="other"), range(2)))
        self.assertEqual([r.status_code for r in responses], [200, 200])
        for i in range(1, 5):
            result = self.send(cards, i, decision="skip", skip_reason="other")
        self.assertEqual(result.json()["summary"], [])
        self.assertEqual(len(self.completion_events()), 1)
        self.assertEqual(sum(e["event"] == "student_decides_card" for e in self.events), 5)

    def test_concurrent_conflicting_duplicates_return_same_saved_choice(self):
        cards = self.publish()
        start = threading.Barrier(2)
        def send(decision):
            start.wait(timeout=5)
            return self.send(cards, 0, decision=decision, skip_reason="other" if decision == "skip" else None)
        with ThreadPoolExecutor(2) as pool:
            results = list(pool.map(send, ("apply", "skip")))
        self.assertEqual([r.status_code for r in results], [200, 200])
        self.assertEqual(results[0].json()["decision"], results[1].json()["decision"])
        with get_conn() as conn:
            rows = conn.execute("select decision from decisions").fetchall()
        self.assertEqual(rows, [{"decision": results[0].json()["decision"]}])
        self.assertEqual(sum(e["event"] == "student_decides_card" for e in self.events), 1)

    def test_publish_auth_and_validation(self):
        self.assertEqual(self.client.post("/api/publish", json={"cards": [CARD] * 5}).status_code, 404)
        self.assertEqual(self.client.post("/api/publish", headers={"X-Admin-Token": "wrong"},
                                          json={"cards": [CARD] * 5}).status_code, 404)
        for field, value in (("deadline", "2027-02-30"), ("source_url", "javascript:alert(1)"),
                             ("role", " ")):
            with self.subTest(field=field):
                result = self.client.post("/api/publish", headers={"X-Admin-Token": "test-admin"},
                                          json={"cards": [dict(CARD, **{field: value})] * 5})
                self.assertEqual(result.status_code, 422, result.text)
        with get_conn() as conn:
            self.assertEqual(conn.execute("select count(*) as n from card_sets").fetchone()["n"], 0)

    def test_decision_validation(self):
        cards = self.publish()
        for extra, expected in (({"decision": "skip"}, 400), ({"position": 0}, 422),
                                ({"ms_on_card": -1}, 422), ({"ms_total": -1}, 422),
                                ({"ms_on_card": 2147483648}, 422),
                                ({"anonymous_id": " "}, 422)):
            with self.subTest(extra=extra):
                self.assertEqual(self.send(cards, 0, **extra).status_code, expected)

    def test_missing_set_and_database_configuration(self):
        self.assertEqual(self.client.get(f"/api/sets/{uuid4()}/decisions",
                                          params={"anonymous_id": "student"}).status_code, 404)
        with patch.dict(os.environ, {"DATABASE_URL": ""}):
            get_settings.cache_clear()
            result = self.client.get("/api/sets/latest")
            self.assertEqual(result.status_code, 503)
            self.assertEqual(result.json()["detail"], "DATABASE_URL is not set")


class MigrationTests(ApiTests):
    schema_file = ROOT / "tests/fixtures/legacy_schema.sql"

    def setUp(self):
        super().setUp()
        with get_conn() as conn:
            conn.execute((ROOT / "sql/migrations/001_decision_integrity.sql").read_text())

    def test_preserves_legacy_invalid_rows_but_excludes_them_from_completion(self):
        # Recreate the old schema to demonstrate migration against existing bad data.
        with get_conn() as conn:
            conn.execute("alter table decisions drop constraint decisions_card_set_fkey")
        first, second = self.publish(), self.publish()
        with get_conn() as conn:
            conn.execute("insert into decisions(set_id,card_id,anonymous_id,decision) values (%s,%s,'student','apply')",
                         (first["id"], second["cards"][0]["id"]))
            conn.execute("alter table decisions drop column ms_total")
            conn.execute("alter table cards drop constraint cards_set_id_id_key")
        with get_conn() as conn:
            conn.execute((ROOT / "sql/migrations/001_decision_integrity.sql").read_text())
            row = conn.execute("select count(*) as n, max(ms_total) as timing from decisions").fetchone()
            self.assertEqual(row, {"n": 1, "timing": None})
        state = self.client.get(f'/api/sets/{first["id"]}/decisions', params={"anonymous_id": "student"}).json()
        self.assertEqual(state, {"choices": {}, "complete": False, "summary": None})
        self.assertEqual(self.send(first, 0).status_code, 200)
        with self.assertRaises(psycopg.errors.ForeignKeyViolation):
            with get_conn() as conn:
                conn.execute("insert into decisions(set_id,card_id,anonymous_id,decision) values (%s,%s,'new','apply')",
                             (first["id"], second["cards"][0]["id"]))


class AnalyticsTests(unittest.TestCase):
    def test_transport_failure_does_not_fail_committed_operation(self):
        from app.analytics import capture
        for stage in ("capture", "flush"):
            with self.subTest(stage=stage), patch("app.analytics.get_posthog") as client:
                getattr(client.return_value, stage).side_effect = OSError("offline")
                with self.assertLogs("app.analytics", level="WARNING"):
                    capture("student", "student_decides_card", {})


if __name__ == "__main__":
    unittest.main()
