# Event Bus

The V1 Event Bus accepts structured events and appends them to monthly JSONL files under `data/events`.

## Public Entry Points

- `core.schema.event.build_event`: builds a schema-shaped event dictionary.
- `core.schema.validators.validate_event`: returns validation errors without mutating input.
- `core.event_bus.bus.append_event`: builds and appends one event through the shared bus.
- `core.storage.jsonl_store.append_event`: validates and appends one JSON line.
- `core.storage.jsonl_store.read_events`: streams events from JSONL files.

Phase 1A does not refactor the Telegram bot. Bot integration happens later through `core.event_bus.bus.append_event`.