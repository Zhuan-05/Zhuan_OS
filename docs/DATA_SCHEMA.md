# Data Schema

V1 event fields:

- `event_id`
- `schema_version`
- `occurred_at`
- `ingested_at`
- `source`
- `type`
- `payload`
- `asset_refs`
- `privacy`
- `status`
- `metadata`
- `idempotency_key`

Allowed event types:

- `quick_capture`
- `study_log`
- `decision_log`
- `mistake_log`
- `principle_log`
- `review_log`

`payload` is event-type-specific. Phase 1A validates shape and core routing fields only.