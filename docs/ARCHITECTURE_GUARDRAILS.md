# Architecture Guardrails

- D:\Zhuan_OS is the system and code root.
- D:\Zhuan_Vault is the human-readable memory root.
- Do not create D:\Zhuan_System.
- Inputs enter through the Event Bus before downstream indexing or rendering.
- JSONL event files are the append-only source of truth.
- SQLite is a rebuildable query index, not the source of truth.
- Markdown rendering is a separate output layer and is not coupled to storage in Phase 1A.
- Telegram Bot will call shared Event Bus functions in a later phase.
- Website will read SQLite in a later phase and must not scan the full vault on normal load.
- Secrets, local databases, JSONL captures, and media captures must not be blindly pushed to Git.