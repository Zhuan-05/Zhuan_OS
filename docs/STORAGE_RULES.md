# Storage Rules

- JSONL is append-only source of truth.
- JSONL files live under `data/events/events-YYYY-MM.jsonl`.
- SQLite lives at `data/zhuan_os.db` and can be rebuilt from JSONL.
- `data/index_state.json` is generated local index state.
- Markdown output belongs to the rendering layer and is not implemented in Phase 1A.
- Do not store secrets in Git.
- Do not blindly track local media, generated SQLite, generated JSONL, or Telegram captures.