from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

SCHEMA_VERSION = 1
EVENT_TYPES = {
    "quick_capture",
    "study_log",
    "decision_log",
    "mistake_log",
    "principle_log",
    "review_log",
}
PRIVACY_LEVELS = {"personal", "private", "public"}
STATUSES = {"active", "archived", "deleted"}
REQUIRED_FIELDS = {
    "event_id",
    "schema_version",
    "occurred_at",
    "ingested_at",
    "source",
    "type",
    "payload",
    "asset_refs",
    "privacy",
    "status",
    "metadata",
    "idempotency_key",
}


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def build_event(
    *,
    source: str,
    type: str,
    payload: dict[str, Any],
    occurred_at: str | None = None,
    asset_refs: list[dict[str, Any]] | None = None,
    privacy: str = "personal",
    status: str = "active",
    metadata: dict[str, Any] | None = None,
    idempotency_key: str | None = None,
) -> dict[str, Any]:
    now = utc_now_iso()
    return {
        "event_id": str(uuid4()),
        "schema_version": SCHEMA_VERSION,
        "occurred_at": occurred_at or now,
        "ingested_at": now,
        "source": source,
        "type": type,
        "payload": payload,
        "asset_refs": asset_refs or [],
        "privacy": privacy,
        "status": status,
        "metadata": metadata or {},
        "idempotency_key": idempotency_key,
    }