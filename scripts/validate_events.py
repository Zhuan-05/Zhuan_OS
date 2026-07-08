from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from core.recovery.recovery import validate_events_dir


def main() -> int:
    events_dir = ROOT / "data" / "events"
    report = validate_events_dir(events_dir)
    if report["ok"]:
        print(f"OK: validated {report['files']} event file(s) in {events_dir}")
        return 0
    print(f"ERROR: found {len(report['errors'])} event validation issue(s) in {events_dir}")
    for error in report["errors"]:
        print(f"line {error['line']}: {error['error']}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())