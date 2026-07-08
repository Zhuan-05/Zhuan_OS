from __future__ import annotations

import importlib
import sys
from pathlib import Path
from typing import Any, Callable

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from core.query.events_query import get_recent_events
from core.recovery.recovery import recover_index, validate_events_dir

REQUIRED_MODULES = [
    "core.schema.event",
    "core.schema.validators",
    "core.event_bus.bus",
    "core.storage.jsonl_store",
    "core.indexing.sqlite_index",
    "core.query.events_query",
    "core.recovery.recovery",
]


def _check(name: str, action: Callable[[], str]) -> dict[str, Any]:
    try:
        detail = action()
        return {"name": name, "ok": True, "detail": detail}
    except Exception as exc:
        return {"name": name, "ok": False, "detail": str(exc)}


def run_health_check(root: str | Path = ROOT) -> dict[str, Any]:
    base = Path(root)
    events_dir = base / "data" / "events"
    db_path = base / "data" / "zhuan_os.db"
    dashboard_app = base / "apps" / "web-dashboard" / "app.py"
    checks: list[dict[str, Any]] = []

    checks.append(
        _check(
            "events_dir_exists",
            lambda: "events directory exists" if events_dir.exists() else (_raise(FileNotFoundError(events_dir))),
        )
    )

    def validate_events() -> str:
        report = validate_events_dir(events_dir)
        if not report["ok"]:
            raise RuntimeError(f"{len(report['errors'])} validation issue(s)")
        return f"validated {report['files']} event file(s)"

    checks.append(_check("events_validate", validate_events))

    def rebuild_sqlite() -> str:
        report = recover_index(events_dir, db_path)
        if not report["ok"]:
            raise RuntimeError("event validation failed; SQLite rebuild skipped")
        return f"rebuilt SQLite with {report['rebuild']['indexed']} event row(s)"

    checks.append(_check("sqlite_rebuild", rebuild_sqlite))

    def query_recent() -> str:
        events = get_recent_events(db_path, limit=5, include_test=False)
        return f"query layer read {len(events)} recent non-test event(s)"

    checks.append(_check("query_recent_events", query_recent))

    checks.append(
        _check(
            "dashboard_app_exists",
            lambda: "dashboard app exists" if dashboard_app.exists() else (_raise(FileNotFoundError(dashboard_app))),
        )
    )

    def import_core_modules() -> str:
        for module_name in REQUIRED_MODULES:
            importlib.import_module(module_name)
        return f"imported {len(REQUIRED_MODULES)} core module(s)"

    checks.append(_check("core_modules_import", import_core_modules))

    return {"ok": all(check["ok"] for check in checks), "checks": checks}


def _raise(exc: Exception) -> str:
    raise exc


def format_summary(result: dict[str, Any]) -> str:
    lines = ["HEALTH CHECK", "============"]
    for check in result["checks"]:
        status = "PASS" if check["ok"] else "FAIL"
        lines.append(f"{status} {check['name']}: {check['detail']}")
    lines.append("------------")
    lines.append("PASS summary: Zhuan_OS is operational." if result["ok"] else "FAIL summary: Zhuan_OS needs attention.")
    return "\n".join(lines)


def main() -> int:
    result = run_health_check(ROOT)
    print(format_summary(result))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
