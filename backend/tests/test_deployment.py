import unittest
from unittest.mock import patch
import os

from pydantic import ValidationError

from app.config import Settings
import test_api as base


PRODUCTION = dict(app_env="production", database_url="postgresql://user:synthetic-password@db.example.test/app?sslmode=require",
                  admin_token="synthetic-admin-token-with-at-least-32-characters", posthog_key="phc_synthetic-test-only",
                  cors_origins="https://example.test")


class ConfigurationTests(unittest.TestCase):
    def test_valid_production_settings(self):
        self.assertEqual(Settings(_env_file=None, **PRODUCTION).app_env, "production")

    def test_production_rejects_missing_or_unsafe_configuration_without_echoing_secrets(self):
        for field, value in (("database_url", ""), ("database_url", "postgresql://u:p@db.example.test/app"),
                             ("admin_token", "replace-with-long-random-token"), ("admin_token", "short"),
                             ("posthog_key", ""), ("cors_origins", "*"),
                             ("cors_origins", "http://localhost:3000"), ("posthog_host", "http://example.test")):
            with self.subTest(field=field, value=value):
                with self.assertRaises(ValidationError) as error:
                    Settings(_env_file=None, **{**PRODUCTION, field: value})
                self.assertNotIn("synthetic-password", str(error.exception))


class ReadinessTests(base.DatabaseTestCase):
    def test_readiness_checks_database_and_required_schema(self):
        ready = self.client.get("/health/ready")
        self.assertEqual(ready.status_code, 200, ready.text)
        with patch.dict(os.environ, {"DATABASE_URL": ""}):
            base.get_settings.cache_clear()
            self.assertEqual(self.client.get("/health/ready").status_code, 503)
        base.get_settings.cache_clear()
        with base.get_conn() as conn:
            conn.execute("drop table analytics_outbox")
        self.assertEqual(self.client.get("/health/ready").status_code, 503)
        self.assertEqual(self.client.get("/health").status_code, 200)

    def test_analytics_diagnostics_are_protected_and_show_real_backlog(self):
        self.publish()
        self.assertEqual(self.client.get("/api/admin/analytics").status_code, 404)
        status = self.client.get("/api/admin/analytics", headers={"X-Admin-Token": "test-admin"})
        self.assertEqual(status.status_code, 200, status.text)
        self.assertEqual(status.json()["pending"], 1)
        self.assertFalse(status.json()["configured"])
        self.assertNotIn("test-admin", status.text)
