# Zhuan OS Web Dashboard

Minimal read-only dashboard for the V1 Event Bus SQLite read model.

## Run locally

```powershell
python D:\Zhuan_OS\apps\web-dashboard\app.py
```

Open `http://127.0.0.1:8765`.

## Rules

- Reads `D:\Zhuan_OS\data\zhuan_os.db` by default.
- Uses `core.query.events_query` for all event reads.
- Does not scan `D:\Zhuan_Vault`.
- Does not write JSONL, SQLite, Markdown, or Vault files.
- Default view excludes `source="test"`; enable the checkbox to include test events.

## Views

- Recent Events
- Today Events
- Event Type Filter
- Keyword Search

This is intentionally a skeleton. UI polish, auth, deployment, and richer filters are later phases.
