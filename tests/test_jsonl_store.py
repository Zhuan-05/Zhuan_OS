import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from core.schema.event import build_event
from core.storage.jsonl_store import append_event, read_events, validate_event_file


class JsonlStoreTests(unittest.TestCase):
    def test_append_event_creates_one_jsonl_line(self):
        with tempfile.TemporaryDirectory() as tmp:
            events_dir = Path(tmp) / "events"
            event = build_event(
                source="test",
                type="quick_capture",
                payload={"text": "one"},
                occurred_at="2026-07-08T00:00:00+00:00",
            )

            path = append_event(event, events_dir)

            self.assertTrue(path.exists())
            self.assertEqual(len(path.read_text(encoding="utf-8").splitlines()), 1)

    def test_append_event_does_not_overwrite_old_lines(self):
        with tempfile.TemporaryDirectory() as tmp:
            events_dir = Path(tmp) / "events"
            first = build_event(
                source="test",
                type="quick_capture",
                payload={"text": "one"},
                occurred_at="2026-07-08T00:00:00+00:00",
            )
            second = build_event(
                source="test",
                type="study_log",
                payload={"text": "two"},
                occurred_at="2026-07-08T00:00:01+00:00",
            )

            path = append_event(first, events_dir)
            append_event(second, events_dir)

            lines = path.read_text(encoding="utf-8").splitlines()
            self.assertEqual(len(lines), 2)
            self.assertEqual([event["payload"]["text"] for event in read_events(events_dir)], ["one", "two"])

    def test_validate_event_file_reports_corrupt_jsonl_line(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "events-2026-07.jsonl"
            path.write_text('{"event_id":"ok"}\nnot-json\n', encoding="utf-8")

            report = validate_event_file(path)

            self.assertFalse(report["ok"])
            self.assertEqual(report["errors"][0]["line"], 2)


if __name__ == "__main__":
    unittest.main()