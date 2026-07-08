import sqlite3
import sys
import tempfile
import unittest
from pathlib import Path

APP_DIR = Path(__file__).resolve().parent
ROOT_DIR = APP_DIR.parents[1]
sys.path.insert(0, str(APP_DIR))
sys.path.insert(0, str(ROOT_DIR))

from core.storage.jsonl_store import read_events
from event_adapter import EventBusConfig, event_type_for_capture, record_capture_event


class TelegramEventAdapterTests(unittest.TestCase):
    def test_quick_capture_creates_valid_event_jsonl_and_sqlite_row(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            config = EventBusConfig(events_dir=base / "events", db_path=base / "zhuan_os.db")

            event = record_capture_event(
                "plain fake capture",
                config=config,
                occurred_at="2026-07-08T00:00:00+00:00",
                metadata={"test": True},
            )

            events = list(read_events(config.events_dir))
            self.assertEqual(len(events), 1)
            self.assertEqual(events[0]["event_id"], event["event_id"])
            self.assertEqual(events[0]["type"], "quick_capture")
            self.assertEqual(events[0]["payload"], {"text": "plain fake capture"})

            conn = sqlite3.connect(config.db_path)
            try:
                rows = conn.execute("select type, source from events").fetchall()
            finally:
                conn.close()
            self.assertEqual(rows, [("quick_capture", "telegram_bot")])

    def test_event_type_mapping_for_bot_categories(self):
        cases = {
            "capture": "quick_capture",
            "study": "study_log",
            "assignment": "study_log",
            "decision": "decision_log",
            "mistake": "mistake_log",
            "principle": "principle_log",
            "review": "review_log",
        }

        for category, expected in cases.items():
            with self.subTest(category=category):
                self.assertEqual(event_type_for_capture(category), expected)


if __name__ == "__main__":
    unittest.main()