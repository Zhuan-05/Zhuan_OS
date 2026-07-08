from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from core.event_bus.bus import append_event
from core.storage.jsonl_store import month_file_for

SAFE_TEST_TEXT = "MANUAL_HEALTH_CHECK_EVENT"


def create_manual_health_event(root: str | Path = ROOT) -> dict[str, str]:
    base = Path(root)
    events_dir = base / "data" / "events"
    event = append_event(
        source="manual_test",
        type="quick_capture",
        payload={"text": SAFE_TEST_TEXT},
        events_dir=events_dir,
        metadata={"purpose": "health_check"},
    )
    event_file = month_file_for(event["occurred_at"], events_dir)
    return {"event_id": event["event_id"], "file_path": str(event_file)}


def format_result(result: dict[str, Any]) -> str:
    return f"event_id={result['event_id']}\nfile_path={result['file_path']}"


def main() -> int:
    result = create_manual_health_event(ROOT)
    print(format_result(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
