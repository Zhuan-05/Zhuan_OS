from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any

from core.storage.jsonl_store import read_events


def _create_schema(conn: sqlite3.Connection) -> None:
    conn.execute("drop table if exists events")
    conn.execute(
        """
        create table events (
            event_id text primary key,
            schema_version integer not null,
            occurred_at text not null,
            ingested_at text not null,
            source text not null,
            type text not null,
            payload_json text not null,
            asset_refs_json text not null,
            privacy text not null,
            status text not null,
            metadata_json text not null,
            idempotency_key text
        )
        """
    )
    conn.execute("create index events_type_idx on events(type)")
    conn.execute("create index events_occurred_at_idx on events(occurred_at)")


def index_event(conn: sqlite3.Connection, event: dict[str, Any]) -> None:
    conn.execute(
        """
        insert into events (
            event_id, schema_version, occurred_at, ingested_at, source, type,
            payload_json, asset_refs_json, privacy, status, metadata_json, idempotency_key
        ) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            event["event_id"],
            event["schema_version"],
            event["occurred_at"],
            event["ingested_at"],
            event["source"],
            event["type"],
            json.dumps(event["payload"], ensure_ascii=False, sort_keys=True),
            json.dumps(event["asset_refs"], ensure_ascii=False, sort_keys=True),
            event["privacy"],
            event["status"],
            json.dumps(event["metadata"], ensure_ascii=False, sort_keys=True),
            event["idempotency_key"],
        ),
    )


def rebuild_sqlite(events_dir: str | Path, db_path: str | Path) -> dict[str, Any]:
    database = Path(db_path)
    database.parent.mkdir(parents=True, exist_ok=True)
    indexed = 0
    conn = sqlite3.connect(database)
    try:
        _create_schema(conn)
        for event in read_events(events_dir):
            index_event(conn, event)
            indexed += 1
        conn.commit()
    finally:
        conn.close()
    return {"db_path": str(database), "indexed": indexed}