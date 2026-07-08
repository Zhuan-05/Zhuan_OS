# Telegram Bot Path Map

This document records the Telegram Bot path dependencies during and after Sprint C1.

## Current App Paths

```text
Telegram Bot: D:\Zhuan_OS\apps\zhuan-telegram-bot
Website Dashboard: D:\Zhuan_OS\apps\web-dashboard
```

These names are preserved in Sprint C1. Do not rename them in this sprint.

## Future App Paths

A later rename sprint may change paths to Python-friendly names:

```text
Telegram Bot: D:\Zhuan_OS\apps\telegram_bot
Website Dashboard: D:\Zhuan_OS\apps\web_dashboard
```

Do not perform this rename until tests, launchers, imports, and docs are updated together.

## Event Bus Dependency

Telegram Bot captures must call shared Event Bus/storage functions through the bot adapter layer.

Required shared modules:

```text
core.schema.event
core.schema.validators
core.event_bus.bus
core.storage.jsonl_store
core.indexing.sqlite_index
core.query.events_query
```

The bot must keep these adapter files:

```text
apps\zhuan-telegram-bot\event_adapter.py
apps\zhuan-telegram-bot\query_adapter.py
```

## Source Of Truth

JSONL event logs are the append-only source of truth:

```text
D:\Zhuan_OS\data\events\events-YYYY-MM.jsonl
```

## SQLite Query Index

SQLite is a rebuildable query index:

```text
D:\Zhuan_OS\data\zhuan_os.db
```

Telegram Today, Recent, and Search must read through:

```text
core.query.events_query
```

The bot should not scan `D:\Zhuan_Vault` and should not query SQLite through scattered raw SQL in handlers.

## Environment Rule

The bot may read `.env` through the existing app setup. Do not print `.env` values, bot tokens, API keys, or user IDs in logs or docs.

Safe example files such as `.env.example` may be committed only when they contain placeholders and no secret values.

## Local Legacy Helper Output

Event Bus JSONL remains primary. Optional legacy Markdown fallback is local helper output only.

After Sprint C1, Telegram Bot must not require root `D:\Zhuan_OS\08_Logs` for normal operation, and it must not write directly to:

```text
D:\Zhuan_OS\legacy_removed
```

If local helper captures are needed, they should stay under active local workspace paths such as:

```text
D:\Zhuan_OS\agent_workspace\inbox
```

These helper captures are not source of truth and must not be blindly committed.

## Must Not Write Directly

Telegram Bot must not write directly to:

```text
D:\Zhuan_Vault
D:\Zhuan_OS\legacy_removed
D:\Zhuan_OS\data\zhuan_os.db outside shared index functions
D:\Zhuan_OS\data\events outside shared Event Bus/storage functions
```