# Agent Workspace

This folder is for local AI/Codex working materials that support Zhuan_OS operation.

Subfolders:
- `inbox/` - local operational inbox and non-source-of-truth helper captures.
- `plans/` - implementation and migration plans.
- `reports/` - audit and verification reports.
- `reviews/` - review notes and checkpoints.

Rules:
- Event Bus JSONL remains the source of truth under `data/events/`.
- SQLite remains a rebuildable query index under `data/zhuan_os.db`.
- Human-readable long-term memory belongs in `D:\Zhuan_Vault`, not here.
- Do not store secrets here.