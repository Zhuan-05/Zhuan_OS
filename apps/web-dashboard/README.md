# Zhuan OS Web Dashboard

Minimal dashboard for the V1 Event Bus SQLite read model. The main dashboard is read-only; `/decision` is a controlled Event Bus write path for AI-assisted decision logs.

## Run locally

```powershell
python D:\Zhuan_OS\apps\web-dashboard\app.py
```

Open `http://127.0.0.1:8765`.

## Rules

- Reads `D:\Zhuan_OS\data\zhuan_os.db` by default.
- Uses `core.query.events_query` for all event reads.
- Does not scan `D:\Zhuan_Vault`.
- The main `/` dashboard does not write JSONL, SQLite, Markdown, or Vault files.
- `/decision` appends a `decision_log` Event Bus event and rebuilds SQLite after a successful AI response.
- Default view excludes `source="test"`; enable the checkbox to include test events.

## Views

- Recent Events
- Today Events
- Event Type Filter
- Keyword Search

This is intentionally a skeleton. UI polish, auth, deployment, and richer filters are later phases.


## AI 7-Layer Decision

Open:

```text
http://127.0.0.1:8765/decision
```

The page accepts `decision_question`, `context`, `options`, `constraints`, and `urgency`.

AI provider/config:

- Uses an OpenAI-compatible Chat Completions request.
- Reads API key from `OPENAI_API_KEY` first, then `AI_API_KEY`.
- Optional model override: `OPENAI_MODEL`.
- If no key is present, the page shows a clear error and does not save an event.

Successful submissions save a `decision_log` event with `source="web_dashboard"` into `D:\Zhuan_OS\data\events`, then rebuild `D:\Zhuan_OS\data\zhuan_os.db`.
