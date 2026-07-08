from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Iterator

from core.schema.validators import validate_event


def month_file_for(occurred_at: str, events_dir: str | Path) -> Path:
    dt = datetime.fromisoformat(occurred_at.replace("Z", "+00:00"))
    return Path(events_dir) / f"events-{dt:%Y-%m}.jsonl"


def append_event(event: dict[str, Any], events_dir: str | Path) -> Path:
    errors = validate_event(event)
    if errors:
        raise ValueError("invalid event: " + "; ".join(errors))
    path = month_file_for(event["occurred_at"], events_dir)
    path.parent.mkdir(parents=True, exist_ok=True)
    line = json.dumps(event, ensure_ascii=False, sort_keys=True)
    with path.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write(line + "\n")
    return path


def read_events(events_dir: str | Path) -> Iterator[dict[str, Any]]:
    root = Path(events_dir)
    if not root.exists():
        return
    for path in sorted(root.glob("events-*.jsonl")):
        with path.open("r", encoding="utf-8") as handle:
            for line in handle:
                if line.strip():
                    yield json.loads(line)


def validate_event_file(path: str | Path) -> dict[str, Any]:
    event_path = Path(path)
    errors: list[dict[str, Any]] = []
    parsed: list[tuple[int, dict[str, Any]]] = []
    if not event_path.exists():
        return {"ok": False, "path": str(event_path), "checked": 0, "errors": [{"line": 0, "error": "file not found"}]}

    with event_path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            try:
                value = json.loads(line)
            except json.JSONDecodeError as exc:
                errors.append({"line": line_number, "error": f"invalid JSON: {exc.msg}"})
                continue
            if not isinstance(value, dict):
                errors.append({"line": line_number, "error": "event line must be a JSON object"})
                continue
            parsed.append((line_number, value))

    for line_number, event in parsed:
        for error in validate_event(event):
            errors.append({"line": line_number, "error": error})

    return {"ok": not errors, "path": str(event_path), "checked": len(parsed), "errors": errors}