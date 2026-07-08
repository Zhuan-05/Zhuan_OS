from __future__ import annotations

import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

from core.indexing.sqlite_index import rebuild_sqlite
from core.query.events_query import (
    get_events_by_type,
    get_recent_events,
    get_today_events,
    search_events,
)
from core.schema.event import build_event
from core.storage.jsonl_store import append_event


class EventsQueryTests(unittest.TestCase):
    def build_db(self) -> tuple[tempfile.TemporaryDirectory, Path]:
        temp = tempfile.TemporaryDirectory()
        base = Path(temp.name)
        events_dir = base / "events"
        db_path = base / "zhuan_os.db"
        today_utc = datetime.now(timezone.utc).replace(hour=1, minute=0, second=0, microsecond=0)
        yesterday_utc = today_utc - timedelta(days=1)

        events = [
            build_event(
                source="telegram_bot",
                type="quick_capture",
                payload={"text": "alpha dashboard note"},
                occurred_at=today_utc.isoformat(),
            ),
            build_event(
                source="telegram_bot",
                type="study_log",
                payload={"text": "beta study note"},
                occurred_at=(today_utc + timedelta(minutes=1)).isoformat(),
            ),
            build_event(
                source="test",
                type="quick_capture",
                payload={"text": "SMOKE_TEST_EVENT_BUS_DO_NOT_KEEP"},
                occurred_at=(today_utc + timedelta(minutes=2)).isoformat(),
            ),
            build_event(
                source="telegram_bot",
                type="review_log",
                payload={"text": "old review note"},
                occurred_at=yesterday_utc.isoformat(),
            ),
        ]
        for event in events:
            append_event(event, events_dir)
        rebuild_sqlite(events_dir, db_path)
        return temp, db_path

    def test_recent_events_excludes_test_source_by_default(self):
        temp, db_path = self.build_db()
        try:
            events = get_recent_events(db_path, limit=10)
        finally:
            temp.cleanup()

        self.assertEqual([event["source"] for event in events], ["telegram_bot", "telegram_bot", "telegram_bot"])
        self.assertEqual(events[0]["payload"]["text"], "beta study note")
        self.assertNotIn("SMOKE_TEST_EVENT_BUS_DO_NOT_KEEP", [event["payload"]["text"] for event in events])

    def test_recent_events_can_include_test_source(self):
        temp, db_path = self.build_db()
        try:
            events = get_recent_events(db_path, limit=10, include_test=True)
        finally:
            temp.cleanup()

        self.assertIn("test", [event["source"] for event in events])

    def test_get_events_by_type_filters_type_and_excludes_test_source(self):
        temp, db_path = self.build_db()
        try:
            events = get_events_by_type(db_path, "quick_capture", limit=10)
        finally:
            temp.cleanup()

        self.assertEqual(len(events), 1)
        self.assertEqual(events[0]["type"], "quick_capture")
        self.assertEqual(events[0]["source"], "telegram_bot")

    def test_get_today_events_uses_timezone_and_excludes_old_events(self):
        temp, db_path = self.build_db()
        try:
            events = get_today_events(db_path, timezone="+00:00", include_test=True)
        finally:
            temp.cleanup()

        texts = [event["payload"]["text"] for event in events]
        self.assertIn("alpha dashboard note", texts)
        self.assertIn("beta study note", texts)
        self.assertNotIn("old review note", texts)

    def test_search_events_matches_payload_keyword(self):
        temp, db_path = self.build_db()
        try:
            events = search_events(db_path, "dashboard", limit=10)
        finally:
            temp.cleanup()

        self.assertEqual(len(events), 1)
        self.assertEqual(events[0]["payload"], {"text": "alpha dashboard note"})


if __name__ == "__main__":
    unittest.main()