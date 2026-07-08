from __future__ import annotations

import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from core.indexing.sqlite_index import rebuild_sqlite
from core.schema.event import build_event
from core.storage.jsonl_store import append_event


APP_PATH = Path("D:/Zhuan_OS/apps/web-dashboard/app.py")


def load_dashboard_module():
    spec = importlib.util.spec_from_file_location("web_dashboard_app", APP_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class WebDashboardTests(unittest.TestCase):
    def test_app_module_loads_when_started_outside_repo_root(self):
        script = (
            "import runpy; "
            f"runpy.run_path({str(APP_PATH)!r}, run_name='web_dashboard_import_check')"
        )
        with tempfile.TemporaryDirectory() as tmp:
            result = subprocess.run(
                [sys.executable, "-c", script],
                cwd=tmp,
                capture_output=True,
                text=True,
                timeout=10,
            )

        self.assertEqual(result.returncode, 0, result.stderr)
    def test_missing_database_returns_clear_read_only_message(self):
        app = load_dashboard_module()
        with tempfile.TemporaryDirectory() as tmp:
            missing_db = Path(tmp) / "missing.db"
            response = app.build_response("/", db_path=missing_db)

        self.assertEqual(response.status, 200)
        self.assertIn("SQLite database not found", response.body)
        self.assertIn("read-only", response.body.lower())

    def test_empty_database_is_handled_gracefully(self):
        app = load_dashboard_module()
        with tempfile.TemporaryDirectory() as tmp:
            events_dir = Path(tmp) / "events"
            db_path = Path(tmp) / "zhuan_os.db"
            events_dir.mkdir()
            rebuild_sqlite(events_dir, db_path)

            response = app.build_response("/", db_path=db_path)

        self.assertEqual(response.status, 200)
        self.assertIn("No events found", response.body)

    def test_dashboard_reads_events_through_query_layer(self):
        app = load_dashboard_module()
        fake_recent = [{"event_id": "visible-1", "type": "quick_capture", "source": "telegram", "occurred_at": "2026-07-08T01:00:00+00:00", "payload": {"text": "safe sample"}}]
        fake_query = mock.Mock()
        fake_query.get_recent_events.return_value = fake_recent
        fake_query.get_today_events.return_value = []
        fake_query.get_events_by_type.return_value = []
        fake_query.search_events.return_value = []

        with mock.patch.object(app, "events_query", fake_query):
            response = app.build_response("/?include_test=1", db_path=Path("sample.db"))

        self.assertIn("safe sample", response.body)
        fake_query.get_recent_events.assert_called_once_with(Path("sample.db"), limit=20, include_test=True)
        fake_query.get_today_events.assert_called_once()

    def test_dashboard_displays_real_events_from_temp_sqlite(self):
        app = load_dashboard_module()
        with tempfile.TemporaryDirectory() as tmp:
            events_dir = Path(tmp) / "events"
            db_path = Path(tmp) / "zhuan_os.db"
            event = build_event(
                source="telegram",
                type="decision_log",
                payload={"text": "safe dashboard sample"},
                occurred_at="2026-07-08T02:00:00+00:00",
            )
            append_event(event, events_dir)
            rebuild_sqlite(events_dir, db_path)

            response = app.build_response("/?type=decision_log&search=dashboard", db_path=db_path)

        self.assertEqual(response.status, 200)
        self.assertIn("safe dashboard sample", response.body)
        self.assertIn("decision_log", response.body)

    def test_dashboard_source_does_not_scan_vault(self):
        source = APP_PATH.read_text(encoding="utf-8")
        self.assertNotIn("Zhuan_Vault", source)
        self.assertNotIn("os.walk", source)
        self.assertNotIn("rglob", source)


if __name__ == "__main__":
    unittest.main()


