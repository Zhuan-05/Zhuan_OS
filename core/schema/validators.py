from __future__ import annotations

from datetime import datetime
from typing import Any

from core.schema.event import EVENT_TYPES, PRIVACY_LEVELS, REQUIRED_FIELDS, STATUSES


def _is_iso_datetime(value: Any) -> bool:
    if not isinstance(value, str) or not value:
        return False
    try:
        datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return False
    return True


def validate_event(event: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    missing = sorted(REQUIRED_FIELDS - set(event.keys()))
    if missing:
        errors.append(f"missing required fields: {', '.join(missing)}")

    if event.get("schema_version") != 1:
        errors.append("schema_version must be 1")
    if not isinstance(event.get("event_id"), str) or not event.get("event_id"):
        errors.append("event_id must be a non-empty string")
    if not _is_iso_datetime(event.get("occurred_at")):
        errors.append("occurred_at must be an ISO datetime string")
    if not _is_iso_datetime(event.get("ingested_at")):
        errors.append("ingested_at must be an ISO datetime string")
    if not isinstance(event.get("source"), str) or not event.get("source"):
        errors.append("source must be a non-empty string")
    if event.get("type") not in EVENT_TYPES:
        errors.append("type must be one of: " + ", ".join(sorted(EVENT_TYPES)))
    if not isinstance(event.get("payload"), dict):
        errors.append("payload must be an object")
    if not isinstance(event.get("asset_refs"), list):
        errors.append("asset_refs must be a list")
    if event.get("privacy") not in PRIVACY_LEVELS:
        errors.append("privacy must be one of: " + ", ".join(sorted(PRIVACY_LEVELS)))
    if event.get("status") not in STATUSES:
        errors.append("status must be one of: " + ", ".join(sorted(STATUSES)))
    if not isinstance(event.get("metadata"), dict):
        errors.append("metadata must be an object")
    if event.get("idempotency_key") is not None and not isinstance(event.get("idempotency_key"), str):
        errors.append("idempotency_key must be a string or null")
    return errors