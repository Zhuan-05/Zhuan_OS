from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

APP_DIR = Path(__file__).resolve().parent
ROOT_DIR = APP_DIR.parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from core.event_bus.bus import append_event as append_bus_event
from core.indexing.sqlite_index import rebuild_sqlite


@dataclass(frozen=True)
class EventBusConfig:
    events_dir: Path = ROOT_DIR / "data" / "events"
    db_path: Path = ROOT_DIR / "data" / "zhuan_os.db"


DEFAULT_EVENT_BUS_CONFIG = EventBusConfig()

_CAPTURE_TYPE_MAP = {
    "capture": "quick_capture",
    "quick_capture": "quick_capture",
    "study": "study_log",
    "assignment": "study_log",
    "decision": "decision_log",
    "mistake": "mistake_log",
    "principle": "principle_log",
    "review": "review_log",
}

_FLOW_TYPE_MAP = {
    "quick_capture": "quick_capture",
    "study_log": "study_log",
    "assignment_project": "study_log",
    "decision": "decision_log",
    "mistake": "mistake_log",
    "principle": "principle_log",
    "review": "review_log",
    "before_ai": "quick_capture",
    "conversation_log": "quick_capture",
}


def event_type_for_capture(category: str) -> str:
    return _CAPTURE_TYPE_MAP.get(category, "quick_capture")


def event_type_for_flow(flow_name: str) -> str:
    return _FLOW_TYPE_MAP.get(flow_name, "quick_capture")


def _merge_metadata(metadata: dict[str, Any] | None, **defaults: Any) -> dict[str, Any]:
    merged = {key: value for key, value in defaults.items() if value is not None}
    if metadata:
        merged.update(metadata)
    return merged


def record_capture_event(
    text: str,
    *,
    category: str = "capture",
    config: EventBusConfig = DEFAULT_EVENT_BUS_CONFIG,
    occurred_at: str | None = None,
    metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    payload: dict[str, Any] = {"text": text.strip()}
    if category != "capture":
        payload["category"] = category
    event = append_bus_event(
        source="telegram_bot",
        type=event_type_for_capture(category),
        payload=payload,
        events_dir=config.events_dir,
        occurred_at=occurred_at,
        metadata=_merge_metadata(metadata, category=category),
    )
    rebuild_sqlite(config.events_dir, config.db_path)
    return event


def record_flow_event(
    flow_name: str,
    answers: list[str],
    *,
    config: EventBusConfig = DEFAULT_EVENT_BUS_CONFIG,
    metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    event = append_bus_event(
        source="telegram_bot",
        type=event_type_for_flow(flow_name),
        payload={"flow": flow_name, "answers": [answer.strip() for answer in answers]},
        events_dir=config.events_dir,
        metadata=_merge_metadata(metadata, flow=flow_name),
    )
    rebuild_sqlite(config.events_dir, config.db_path)
    return event