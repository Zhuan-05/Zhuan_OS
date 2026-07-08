from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from core.recovery.recovery import recover_index


def main() -> int:
    events_dir = ROOT / "data" / "events"
    db_path = ROOT / "data" / "zhuan_os.db"
    report = recover_index(events_dir, db_path)
    if not report["ok"]:
        print("ERROR: event validation failed; SQLite rebuild skipped")
        return 1
    print(f"OK: rebuilt {db_path} with {report['rebuild']['indexed']} event row(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())