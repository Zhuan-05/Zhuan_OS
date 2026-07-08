from __future__ import annotations

import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from core.indexing.sqlite_index import rebuild_sqlite
from core.query.events_query import get_recent_events
from core.storage.jsonl_store import read_events


ROOT = Path("D:/Zhuan_OS")
HEALTH_PATH = ROOT / "scripts" / "health_check.py"
CREATE_EVENT_PATH = ROOT / "scripts" / "create_test_event.py"
RUN_ALL_TESTS_PATH = ROOT / "scripts" / "run_all_tests.ps1"
START_DASHBOARD_PATH = ROOT / "scripts" / "start_dashboard.ps1"
CHECKLIST_PATH = ROOT / "docs" / "OPERATION_CHECKLIST.md"


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class OperationalScriptsTests(unittest.TestCase):
    def test_required_operational_files_exist(self):
        for path in [HEALTH_PATH, CREATE_EVENT_PATH, RUN_ALL_TESTS_PATH, START_DASHBOARD_PATH, CHECKLIST_PATH]:
            self.assertTrue(path.exists(), f"missing {path}")

    def test_create_test_event_uses_event_bus_and_prints_no_payload(self):
        module = load_module(CREATE_EVENT_PATH, "create_test_event_script")
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            result = module.create_manual_health_event(root)
            events = list(read_events(root / "data" / "events"))

        self.assertEqual(len(events), 1)
        self.assertEqual(events[0]["source"], "manual_test")
        self.assertEqual(events[0]["type"], "quick_capture")
        self.assertEqual(events[0]["payload"], {"text": "MANUAL_HEALTH_CHECK_EVENT"})
        self.assertEqual(result["event_id"], events[0]["event_id"])
        self.assertIn("events-", result["file_path"])
        printed = module.format_result(result)
        self.assertIn(result["event_id"], printed)
        self.assertIn("file_path=", printed)
        self.assertNotIn("MANUAL_HEALTH_CHECK_EVENT", printed)

    def test_health_check_reports_pass_without_payload_content(self):
        create_module = load_module(CREATE_EVENT_PATH, "create_test_event_for_health")
        health_module = load_module(HEALTH_PATH, "health_check_script")
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "apps" / "web-dashboard").mkdir(parents=True)
            (root / "apps" / "web-dashboard" / "app.py").write_text("# dashboard", encoding="utf-8")
            create_module.create_manual_health_event(root)
            rebuild_sqlite(root / "data" / "events", root / "data" / "zhuan_os.db")
            result = health_module.run_health_check(root)

        self.assertTrue(result["ok"], result)
        names = {check["name"] for check in result["checks"]}
        self.assertIn("events_dir_exists", names)
        self.assertIn("events_validate", names)
        self.assertIn("sqlite_rebuild", names)
        self.assertIn("query_recent_events", names)
        self.assertIn("dashboard_app_exists", names)
        summary = health_module.format_summary(result)
        self.assertIn("PASS", summary)
        self.assertNotIn("MANUAL_HEALTH_CHECK_EVENT", summary)

    def test_ps1_scripts_contain_expected_commands(self):
        run_all = RUN_ALL_TESTS_PATH.read_text(encoding="utf-8")
        start_dashboard = START_DASHBOARD_PATH.read_text(encoding="utf-8")
        self.assertIn("python -m unittest discover D:\\Zhuan_OS\\tests", run_all)
        self.assertIn("python D:\\Zhuan_OS\\scripts\\validate_events.py", run_all)
        self.assertIn("python D:\\Zhuan_OS\\scripts\\rebuild_index.py", run_all)
        self.assertIn("python D:\\Zhuan_OS\\scripts\\health_check.py", run_all)
        self.assertIn("python D:\\Zhuan_OS\\apps\\web-dashboard\\app.py", start_dashboard)

    def test_health_check_cli_runs_from_outside_repo_root(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = subprocess.run(
                [sys.executable, str(HEALTH_PATH)],
                cwd=tmp,
                capture_output=True,
                text=True,
                timeout=20,
            )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("HEALTH CHECK", result.stdout)
        self.assertNotIn("MANUAL_HEALTH_CHECK_EVENT", result.stdout)


if __name__ == "__main__":
    unittest.main()
