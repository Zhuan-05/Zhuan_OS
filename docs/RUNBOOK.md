# Runbook

## Validate Events

```powershell
python D:\Zhuan_OS\scripts\validate_events.py
```

## Rebuild SQLite Index

```powershell
python D:\Zhuan_OS\scripts\rebuild_index.py
```

## Run Tests

```powershell
python -m unittest discover D:\Zhuan_OS\tests
```

Phase 1A creates the foundation only. It does not migrate old Markdown logs, refactor the bot, build the dashboard, implement Bot Assistant, or implement MCP.