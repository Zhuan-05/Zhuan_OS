# Query Layer Dashboard

`apps/web-dashboard` is a minimal read-only web surface over the SQLite query index.

## Contract

The dashboard must read events through `core.query.events_query`. It must not scan the Vault and must not write to JSONL, SQLite, Markdown, or Vault paths.

Default database path:

```text
D:\Zhuan_OS\data\zhuan_os.db
```

## Supported Views

- Recent Events: `get_recent_events(...)`
- Today Events: `get_today_events(...)`
- Event Type Filter: `get_events_by_type(...)`
- Keyword Search: `search_events(...)`

By default, the query layer excludes `source="test"`. The dashboard exposes an `include_test=1` checkbox for debugging.

## Missing or Empty Database

A missing SQLite index should show a clear read-only message instead of crashing. An empty index should render empty states.

## Run

```powershell
python D:\Zhuan_OS\apps\web-dashboard\app.py
```

Then open:

```text
http://127.0.0.1:8765
```
