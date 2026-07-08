from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    events_dir = ROOT / "data" / "events"
    db_path = ROOT / "data" / "zhuan_os.db"
    print(f"events_dir_exists={events_dir.exists()}")
    print(f"sqlite_index_exists={db_path.exists()}")
    print("backup_check is a placeholder guardrail for Phase 1A; no backup is created here.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())