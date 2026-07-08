# Query Layer

The query layer is the read model for future dashboard code. Website code should call `core.query.events_query` instead of scanning `D:\Zhuan_Vault` or writing raw SQL in UI modules.

## Functions

- `get_recent_events(db_path, limit=20, include_test=False)`
- `get_events_by_type(db_path, event_type, limit=50, include_test=False)`
- `get_today_events(db_path, timezone="+08:00", include_test=False)`
- `search_events(db_path, keyword, limit=50, include_test=False)`

By default, all query functions exclude events where `source = "test"` so smoke-test events do not appear in normal dashboard views.

## Rules

- Query functions open SQLite in read-only mode.
- JSON fields are decoded before being returned to callers.
- SQLite is still rebuildable from JSONL and is not the source of truth.
- Dashboard code must not scan the full vault during normal load.

## CLI

```powershell
python D:\Zhuan_OS\scripts\query_events.py --limit 20
python D:\Zhuan_OS\scripts\query_events.py --type quick_capture
python D:\Zhuan_OS\scripts\query_events.py --today --timezone +08:00
python D:\Zhuan_OS\scripts\query_events.py --search keyword
```