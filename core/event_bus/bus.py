from __future__ import annotations

from pathlib import Path
from typing import Any

from core.schema.event import build_event
from core.storage.jsonl_store import append_event as append_jsonl_event


def append_event(
    *,
    source: str,
    type: str,
    payload: dict[str, Any],
    events_dir: str | Path,
    occurred_at: str | None = None,
    asset_refs: list[dict[str, Any]] | None = None,
    privacy: str = "personal",
    status: str = "active",
    metadata: dict[str, Any] | None = None,
    idempotency_key: str | None = None,
) -> dict[str, Any]:
    event = build_event(
        source=source,
        type=type,
        payload=payload,
        occurred_at=occurred_at,
        asset_refs=asset_refs,
        privacy=privacy,
        status=status,
        metadata=metadata,
        idempotency_key=idempotency_key,
    )
    append_jsonl_event(event, events_dir)
    return event