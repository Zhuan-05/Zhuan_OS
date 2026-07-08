from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

APP_DIR = Path(__file__).resolve().parent
ROOT_DIR = APP_DIR.parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from core.query.events_query import get_recent_events, get_today_events, search_events

DEFAULT_DB_PATH = ROOT_DIR / "data" / "zhuan_os.db"
MAX_PREVIEW_CHARS = 72


def short_preview(value: object, limit: int = MAX_PREVIEW_CHARS) -> str:
    single_line = " ".join(str(value).split())
    if len(single_line) <= limit:
        return single_line
    return single_line[: max(0, limit - 3)].rstrip() + "..."


def _compact(value: str, limit: int = MAX_PREVIEW_CHARS) -> str:
    return short_preview(value, limit)


def _payload_preview(payload: Any) -> str:
    if isinstance(payload, dict):
        for key in ("text", "decision_question", "title", "summary", "ai_response"):
            value = payload.get(key)
            if value:
                return _compact(str(value))
        return _compact(json.dumps(payload, ensure_ascii=False, sort_keys=True))
    if payload is None:
        return "(no payload)"
    return _compact(str(payload))


def _event_line(event: dict[str, Any]) -> str:
    occurred_at = str(event.get("occurred_at", ""))[:16].replace("T", " ")
    event_type = str(event.get("type", "unknown"))
    preview = _payload_preview(event.get("payload"))
    return f"- {occurred_at} | {event_type} | {preview}"


def _format_events(title: str, events: list[dict[str, Any]], *, empty: str) -> str:
    if not events:
        return f"{title}\n{empty}"
    lines = [title]
    lines.extend(_event_line(event) for event in events[:10])
    return "\n".join(lines)


def format_recent_events(events: list[dict[str, Any]]) -> str:
    return _format_events("Recent Events", events[:10], empty="No recent events found.")


def format_today_events(events: list[dict[str, Any]]) -> str:
    latest = list(reversed(events[-10:]))
    return _format_events("Today Events", latest, empty="No events found for today.")


def format_search_results(events: list[dict[str, Any]], keyword: str) -> str:
    return _format_events(f"Search Results: {keyword}", events[:10], empty="No matching events found.")


def get_recent_message(*, db_path: str | Path = DEFAULT_DB_PATH, limit: int = 10) -> str:
    try:
        events = get_recent_events(db_path, limit=limit, include_test=False)
    except FileNotFoundError:
        return "Recent Events\nSQLite database not found. Run rebuild_index.py first."
    except Exception as exc:
        return f"Recent Events\nUnable to query SQLite: {exc}"
    return format_recent_events(events)


def get_today_message(*, db_path: str | Path = DEFAULT_DB_PATH, timezone: str = "+08:00", limit: int = 10) -> str:
    try:
        events = get_today_events(db_path, timezone=timezone, include_test=False)
    except FileNotFoundError:
        return "Today Events\nSQLite database not found. Run rebuild_index.py first."
    except Exception as exc:
        return f"Today Events\nUnable to query SQLite: {exc}"
    return format_today_events(events[-limit:])


def get_search_message(keyword: str, *, db_path: str | Path = DEFAULT_DB_PATH, limit: int = 10) -> str:
    clean = keyword.strip()
    if not clean:
        return "Usage: /search keyword"
    try:
        events = search_events(db_path, clean, limit=limit, include_test=False)
    except FileNotFoundError:
        return "Search Results\nSQLite database not found. Run rebuild_index.py first."
    except Exception as exc:
        return f"Search Results\nUnable to query SQLite: {exc}"
    return format_search_results(events, clean)


def get_dashboard_link_message(url: str | None) -> str:
    clean = (url or "").strip()
    if not clean:
        return "Dashboard URL is not configured. You can still use Today, Recent, and Search inside Telegram."
    return f"Dashboard: {clean}"
