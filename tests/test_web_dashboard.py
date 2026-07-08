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


class DecisionPageTests(unittest.TestCase):
    def test_decision_get_page_renders_form(self):
        app = load_dashboard_module()

        response = app.build_response("/decision")

        self.assertEqual(response.status, 200)
        self.assertIn("AI 7-Layer Decision", response.body)
        for field in ["decision_question", "context", "options", "constraints", "urgency"]:
            self.assertIn(field, response.body)

    def test_missing_ai_key_is_handled_without_crashing(self):
        app = load_dashboard_module()
        body = "decision_question=Choose+A&context=Safe+context&options=A+or+B&constraints=low+risk&urgency=today"

        response = app.build_decision_response(
            "POST",
            body,
            ai_client=lambda form: (_ for _ in ()).throw(app.MissingAIKeyError("OPENAI_API_KEY or AI_API_KEY is missing")),
        )

        self.assertEqual(response.status, 200)
        self.assertIn("AI key is missing", response.body)
        self.assertIn("Decision was not saved", response.body)

    def test_decision_event_payload_shape_is_valid_and_indexed(self):
        app = load_dashboard_module()
        form = {
            "decision_question": "Which safe option should I choose?",
            "context": "Synthetic context only",
            "options": "Option A; Option B",
            "constraints": "No private data",
            "urgency": "today",
        }
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            result = app.save_decision_event(
                form,
                {
                    "ai_response": "Synthetic 7-layer analysis",
                    "seven_layer_sections": {title: f"sample {title}" for title in app.SEVEN_LAYER_TITLES},
                },
                events_dir=base / "events",
                db_path=base / "zhuan_os.db",
            )

            events = list(app.read_events(base / "events"))
            self.assertEqual(len(events), 1)
            event = events[0]
            self.assertEqual(event["event_id"], result["event_id"])
            self.assertEqual(event["type"], "decision_log")
            self.assertEqual(event["source"], "web_dashboard")
            payload = event["payload"]
            for key in ["decision_question", "context", "options", "constraints", "urgency", "ai_response", "seven_layer_sections"]:
                self.assertIn(key, payload)
            self.assertEqual(set(payload["seven_layer_sections"].keys()), set(app.SEVEN_LAYER_TITLES))
            indexed = app.events_query.get_events_by_type(base / "zhuan_os.db", "decision_log", include_test=True)
            self.assertEqual(len(indexed), 1)

    def test_decision_post_saves_event_with_mock_ai(self):
        app = load_dashboard_module()
        body = "decision_question=Choose+A&context=Safe+context&options=A+or+B&constraints=low+risk&urgency=today"
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            response = app.build_decision_response(
                "POST",
                body,
                events_dir=base / "events",
                db_path=base / "zhuan_os.db",
                ai_client=lambda form: {
                    "ai_response": "Mock analysis",
                    "seven_layer_sections": {title: f"mock {title}" for title in app.SEVEN_LAYER_TITLES},
                },
            )

            events = list(app.read_events(base / "events"))

        self.assertEqual(response.status, 200)
        self.assertIn("Decision saved", response.body)
        self.assertEqual(events[0]["type"], "decision_log")
        self.assertEqual(events[0]["payload"]["decision_question"], "Choose A")

    def test_decision_source_does_not_scan_vault_or_write_random_files(self):
        source = APP_PATH.read_text(encoding="utf-8")
        self.assertNotIn("Zhuan_Vault", source)
        self.assertNotIn("os.walk", source)
        self.assertNotIn("rglob", source)
        self.assertNotIn("open(\"", source)
        self.assertNotIn("write_text", source)


if __name__ == "__main__":
    unittest.main()


