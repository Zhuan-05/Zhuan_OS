import sys
import tempfile
import unittest
from pathlib import Path

APP_DIR = Path(__file__).resolve().parent
ROOT_DIR = APP_DIR.parents[1]
sys.path.insert(0, str(APP_DIR))
sys.path.insert(0, str(ROOT_DIR))

from core.event_bus.bus import append_event
from core.indexing.sqlite_index import rebuild_sqlite
from query_adapter import (
    format_recent_events,
    format_search_results,
    short_preview,
    format_today_events,
    get_recent_message,
    get_search_message,
    get_today_message,
)


class TelegramQueryAdapterTests(unittest.TestCase):
    def _sample_db(self):
        temp = tempfile.TemporaryDirectory()
        base = Path(temp.name)
        events_dir = base / "events"
        db_path = base / "zhuan_os.db"
        append_event(
            source="telegram_bot",
            type="quick_capture",
            payload={"text": "short safe note"},
            events_dir=events_dir,
            occurred_at="2026-07-08T03:00:00+00:00",
        )
        append_event(
            source="web_dashboard",
            type="decision_log",
            payload={"decision_question": "Choose safe option", "ai_response": "x" * 200},
            events_dir=events_dir,
            occurred_at="2026-07-08T04:00:00+00:00",
        )
        append_event(
            source="test",
            type="quick_capture",
            payload={"text": "hidden test event"},
            events_dir=events_dir,
            occurred_at="2026-07-08T05:00:00+00:00",
        )
        rebuild_sqlite(events_dir, db_path)
        return temp, db_path

    def test_recent_message_uses_sqlite_and_excludes_test_events(self):
        temp, db_path = self._sample_db()
        with temp:
            message = get_recent_message(db_path=db_path, limit=10)

        self.assertIn("Recent Events", message)
        self.assertIn("short safe note", message)
        self.assertIn("decision_log", message)
        self.assertNotIn("hidden test event", message)

    def test_today_message_limits_to_ten_items(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            events_dir = base / "events"
            db_path = base / "zhuan_os.db"
            for index in range(12):
                append_event(
                    source="telegram_bot",
                    type="quick_capture",
                    payload={"text": f"today item {index}"},
                    events_dir=events_dir,
                    occurred_at=f"2026-07-08T{index:02d}:00:00+00:00",
                )
            rebuild_sqlite(events_dir, db_path)
            message = get_today_message(db_path=db_path, timezone="+08:00", limit=10)

        self.assertIn("Today Events", message)
        self.assertNotIn("today item 0", message)
        self.assertIn("today item 11", message)

    def test_search_message_requires_keyword_and_searches_sqlite(self):
        temp, db_path = self._sample_db()
        with temp:
            missing = get_search_message("", db_path=db_path)
            found = get_search_message("safe", db_path=db_path, limit=10)

        self.assertIn("Usage: /search keyword", missing)
        self.assertIn("Search Results", found)
        self.assertIn("short safe note", found)

    def test_short_preview_collapses_and_truncates_text(self):
        preview = short_preview("private   value\n" + "x" * 200, limit=40)

        self.assertLessEqual(len(preview), 40)
        self.assertIn("private value", preview)
        self.assertNotIn("\n", preview)

    def test_formatters_do_not_dump_long_payloads(self):
        long_text = "private " + "x" * 300
        message = format_recent_events([
            {"occurred_at": "2026-07-08T00:00:00+00:00", "type": "quick_capture", "payload": {"text": long_text}}
        ])

        self.assertIn("private", message)
        self.assertLess(len(message), 220)
        self.assertNotIn("x" * 120, message)

    def test_source_does_not_scan_vault_or_write_files(self):
        source = (APP_DIR / "query_adapter.py").read_text(encoding="utf-8")
        self.assertNotIn("Zhuan_Vault", source)
        self.assertNotIn("os.walk", source)
        self.assertNotIn("rglob", source)
        self.assertNotIn("write_text", source)
        self.assertNotIn("open(", source)


if __name__ == "__main__":
    unittest.main()
