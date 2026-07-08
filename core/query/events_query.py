from __future__ import annotations

import json
import sqlite3
from datetime import datetime, time, timedelta, timezone as dt_timezone
from pathlib import Path
from typing import Any


def _connect_readonly(db_path: str | Path) -> sqlite3.Connection:
    path = Path(db_path)
    if not path.exists():
        raise FileNotFoundError(f"SQLite database not found: {path}")
    uri = path.resolve().as_uri() + "?mode=ro"
    conn = sqlite3.connect(uri, uri=True)
    conn.row_factory = sqlite3.Row
    return conn


def _limit(value: int) -> int:
    if value < 1:
        return 1
    return min(value, 500)


def _decode_json(value: str) -> Any:
    return json.loads(value) if value else None


def _row_to_event(row: sqlite3.Row) -> dict[str, Any]:
    return {
        "event_id": row["event_id"],
        "schema_version": row["schema_version"],
        "occurred_at": row["occurred_at"],
        "ingested_at": row["ingested_at"],
        "source": row["source"],
        "type": row["type"],
        "payload": _decode_json(row["payload_json"]),
        "asset_refs": _decode_json(row["asset_refs_json"]),
        "privacy": row["privacy"],
        "status": row["status"],
        "metadata": _decode_json(row["metadata_json"]),
        "idempotency_key": row["idempotency_key"],
    }


def _test_filter(include_test: bool) -> str:
    return "" if include_test else " and source != 'test'"


def _fetch_events(
    db_path: str | Path,
    where_sql: str,
    params: tuple[Any, ...],
    *,
    limit: int,
    include_test: bool,
    order_sql: str = "occurred_at desc, ingested_at desc",
) -> list[dict[str, Any]]:
    sql = f"select * from events where {where_sql}{_test_filter(include_test)} order by {order_sql} limit ?"
    conn = _connect_readonly(db_path)
    try:
        rows = conn.execute(sql, (*params, _limit(limit))).fetchall()
        return [_row_to_event(row) for row in rows]
    finally:
        conn.close()


def get_recent_events(db_path: str | Path, limit: int = 20, include_test: bool = False) -> list[dict[str, Any]]:
    return _fetch_events(db_path, "1 = 1", (), limit=limit, include_test=include_test)


def get_events_by_type(
    db_path: str | Path,
    event_type: str,
    limit: int = 50,
    include_test: bool = False,
) -> list[dict[str, Any]]:
    return _fetch_events(db_path, "type = ?", (event_type,), limit=limit, include_test=include_test)


def _parse_timezone_offset(value: str) -> dt_timezone:
    if len(value) != 6 or value[0] not in "+-" or value[3] != ":":
        raise ValueError("timezone must look like +08:00 or -05:30")
    sign = 1 if value[0] == "+" else -1
    hours = int(value[1:3])
    minutes = int(value[4:6])
    return dt_timezone(sign * timedelta(hours=hours, minutes=minutes))


def get_today_events(
    db_path: str | Path,
    timezone: str = "+08:00",
    include_test: bool = False,
) -> list[dict[str, Any]]:
    tz = _parse_timezone_offset(timezone)
    today = datetime.now(tz).date()
    start_local = datetime.combine(today, time.min, tzinfo=tz)
    end_local = start_local + timedelta(days=1)
    start_utc = start_local.astimezone(dt_timezone.utc).isoformat()
    end_utc = end_local.astimezone(dt_timezone.utc).isoformat()
    return _fetch_events(
        db_path,
        "datetime(occurred_at) >= datetime(?) and datetime(occurred_at) < datetime(?)",
        (start_utc, end_utc),
        limit=500,
        include_test=include_test,
        order_sql="occurred_at asc, ingested_at asc",
    )


def search_events(
    db_path: str | Path,
    keyword: str,
    limit: int = 50,
    include_test: bool = False,
) -> list[dict[str, Any]]:
    pattern = f"%{keyword}%"
    return _fetch_events(
        db_path,
        "(payload_json like ? or metadata_json like ? or type like ?)",
        (pattern, pattern, pattern),
        limit=limit,
        include_test=include_test,
    )