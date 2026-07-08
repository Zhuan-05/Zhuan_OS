import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from core.schema.event import build_event
from core.schema.validators import validate_event


class EventSchemaTests(unittest.TestCase):
    def test_build_event_contains_required_fields(self):
        event = build_event(
            source="test",
            type="quick_capture",
            payload={"text": "sample capture"},
            idempotency_key="test-1",
        )

        required = {
            "event_id",
            "schema_version",
            "occurred_at",
            "ingested_at",
            "source",
            "type",
            "payload",
            "asset_refs",
            "privacy",
            "status",
            "metadata",
            "idempotency_key",
        }
        self.assertTrue(required.issubset(event.keys()))
        self.assertEqual(event["type"], "quick_capture")
        self.assertEqual(event["payload"], {"text": "sample capture"})

    def test_invalid_event_type_is_rejected(self):
        event = build_event(
            source="test",
            type="quick_capture",
            payload={"text": "sample capture"},
        )
        event["type"] = "unknown_type"

        errors = validate_event(event)

        self.assertTrue(any("type" in error for error in errors))


if __name__ == "__main__":
    unittest.main()