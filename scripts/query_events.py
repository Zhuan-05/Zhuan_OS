from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from core.query.events_query import get_events_by_type, get_recent_events, get_today_events, search_events


def main() -> int:
    parser = argparse.ArgumentParser(description="Read events from the Zhuan_OS SQLite query index.")
    parser.add_argument("--db", default=str(ROOT / "data" / "zhuan_os.db"))
    parser.add_argument("--limit", type=int, default=20)
    parser.add_argument("--include-test", action="store_true")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--type", dest="event_type")
    group.add_argument("--today", action="store_true")
    group.add_argument("--search")
    parser.add_argument("--timezone", default="+08:00")
    args = parser.parse_args()

    if args.event_type:
        events = get_events_by_type(args.db, args.event_type, limit=args.limit, include_test=args.include_test)
    elif args.today:
        events = get_today_events(args.db, timezone=args.timezone, include_test=args.include_test)
    elif args.search:
        events = search_events(args.db, args.search, limit=args.limit, include_test=args.include_test)
    else:
        events = get_recent_events(args.db, limit=args.limit, include_test=args.include_test)

    print(json.dumps(events, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())