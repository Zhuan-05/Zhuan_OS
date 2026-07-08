# Operation Checklist

This checklist keeps Zhuan_OS runnable without touching `D:\Zhuan_Vault`.

## Run all tests and checks

```powershell
powershell -ExecutionPolicy Bypass -File D:\Zhuan_OS\scripts\run_all_tests.ps1
```

This runs:

```powershell
python -m unittest discover D:\Zhuan_OS\tests
python D:\Zhuan_OS\scripts\validate_events.py
python D:\Zhuan_OS\scripts\rebuild_index.py
python D:\Zhuan_OS\scripts\health_check.py
```

## Create a safe test event

```powershell
python D:\Zhuan_OS\scripts\create_test_event.py
```

The script creates a `manual_test` / `quick_capture` event with safe test text and prints only `event_id` plus the event file path.

## Validate event logs

```powershell
python D:\Zhuan_OS\scripts\validate_events.py
```

## Rebuild SQLite

```powershell
python D:\Zhuan_OS\scripts\rebuild_index.py
```

SQLite is a rebuildable query index. JSONL remains the append-only source of truth.

## Start dashboard

```powershell
powershell -ExecutionPolicy Bypass -File D:\Zhuan_OS\scripts\start_dashboard.ps1
```

Then open:

```text
http://127.0.0.1:8765
```



## AI 7-layer decision page

Start the dashboard, then open:

```text
http://127.0.0.1:8765/decision
```

Configuration is environment-only:

```text
OPENAI_API_KEY=...
# or
AI_API_KEY=...
```

Optional model override:

```text
OPENAI_MODEL=gpt-4o-mini
```

Do not commit API keys. If the key is missing, the page should show a clear error and should not save a decision event.

A successful submission creates a `decision_log` Event Bus event with `source="web_dashboard"`, then rebuilds SQLite. The page must not scan `D:\Zhuan_Vault`.

## Telegram capture stability

Telegram text capture writes to the Event Bus first. The JSONL event log is the source of truth and SQLite is rebuilt as a query index.

Legacy Markdown fallback is enabled by default:

```text
LEGACY_MARKDOWN_FALLBACK=true
```

Disable fallback only after Event Bus confidence is high:

```text
LEGACY_MARKDOWN_FALLBACK=false
```

If Event Bus writing fails, the bot must report the failure clearly. Logs may include `event_id`, event `type`, and `source`, but must not include message bodies, bot tokens, or `.env` values.

## Local-only and ignored files

These are operational/runtime files and should remain local-only:

- `data/`
- `data/events/*.jsonl`
- `data/*.db`
- `data/index_state.json`
- `08_Logs/`
- `.env`
- `.env.*`
- `.venv/`
- `__pycache__/`
- media files such as `*.jpg`, `*.jpeg`, `*.png`, `*.mp4`, `*.mov`

## Do not commit

Do not commit:

- `data/`
- `08_Logs/`
- `.env`
- `.venv`
- `__pycache__`
- media files

Safe example files such as `.env.example` may be committed when reviewed for placeholders only.
