from __future__ import annotations

from pathlib import Path
from typing import Any

from core.indexing.sqlite_index import rebuild_sqlite
from core.storage.jsonl_store import validate_event_file


def validate_events_dir(events_dir: str | Path) -> dict[str, Any]:
    root = Path(events_dir)
    reports = [validate_event_file(path) for path in sorted(root.glob("events-*.jsonl"))] if root.exists() else []
    errors = [error for report in reports for error in report["errors"]]
    return {"ok": not errors, "files": len(reports), "errors": errors, "reports": reports}


def recover_index(events_dir: str | Path, db_path: str | Path) -> dict[str, Any]:
    validation = validate_events_dir(events_dir)
    if not validation["ok"]:
        return {"ok": False, "validation": validation, "rebuild": None}
    rebuild = rebuild_sqlite(events_dir, db_path)
    return {"ok": True, "validation": validation, "rebuild": rebuild}