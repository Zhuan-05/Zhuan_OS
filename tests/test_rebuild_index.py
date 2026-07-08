import sqlite3
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from core.indexing.sqlite_index import rebuild_sqlite
from core.schema.event import build_event
from core.storage.jsonl_store import append_event


class RebuildIndexTests(unittest.TestCase):
    def test_rebuild_sqlite_creates_expected_rows(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            events_dir = base / "events"
            db_path = base / "zhuan_os.db"
            append_event(build_event(source="test", type="quick_capture", payload={"text": "one"}), events_dir)
            append_event(build_event(source="test", type="decision_log", payload={"text": "two"}), events_dir)

            report = rebuild_sqlite(events_dir, db_path)

            self.assertEqual(report["indexed"], 2)
            conn = sqlite3.connect(db_path)
            try:
                rows = conn.execute("select type, source from events order by ingested_at").fetchall()
            finally:
                conn.close()
            self.assertEqual(rows, [("quick_capture", "test"), ("decision_log", "test")])


if __name__ == "__main__":
    unittest.main()