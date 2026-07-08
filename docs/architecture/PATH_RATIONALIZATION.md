# Zhuan_OS Path Rationalization Map

This document records the approved root path rationalization map for `D:\Zhuan_OS`.

Scope:
- `D:\Zhuan_OS` is the system/code/operation root.
- `D:\Zhuan_Vault` is the human-readable memory root.
- This map is documentation only. It does not authorize moving, deleting, or renaming old folders.

Hard rules:
- No old folder may be moved without explicit approval.
- `08_Logs`, `logs`, `data`, and inbox/private captures must not be blindly committed.
- Do not read, print, or commit secret values.
- Do not migrate old folders as part of documentation-only phases.

## Current Root Classification

| Current Path | Content Role | Target Path | Recommended Action | Risk | Reason |
|---|---|---|---|---|---|
| `apps` | System apps | `apps` | Keep at root | Low | Telegram bot and web dashboard are runnable system apps. |
| `core` | Shared system code | `core` | Keep at root | Low | Event Bus, schema, storage, indexing, query, and recovery code. |
| `scripts` | Operational scripts | `scripts` | Keep at root | Low | Health check, validation, rebuild, dashboard startup, and test commands. |
| `tests` | Test suite | `tests` | Keep at root | Low | Repository verification layer. |
| `data` | Local generated/runtime data | `data` | Keep at root, keep generated files ignored | High | JSONL and SQLite are local runtime data. Do not blindly commit database, index state, or event files. |
| `docs` | Mixed documentation | `docs/*` | Reorganize later | Medium | Should be split into architecture, operation, agents, prompts, templates, and legacy. |
| `90_Archive` | Archive bucket | `90_Archive` | Keep at root | Medium | Target root includes archive, but contents need manual review before use. |
| `.git` | Git metadata | `.git` | Keep internal | High | Never modify manually. |
| `.agents` | Agent config/rules | `docs/agents` or hidden local state | Manual review | Medium | Empty at inspection time, but agent rules may become operational. |
| `.codex` | Codex config/cache | `docs/agents` or hidden local state | Manual review | Medium | Empty at inspection time. Avoid committing generated tool state. |
| `.obsidian` | Obsidian local state | Ignore or archive later | Manual review | High | Zhuan_OS should not behave as a Vault long-term. |
| `00_Command_Center` | Command/control docs | `docs/operation` | Move later after approval | Medium | Likely system operation documentation, not root code. |
| `00_Inbox` | Old inbox/vault-like folder | `D:\Zhuan_Vault` or `90_Archive` | Manual review | High | May contain human memory or private captures. |
| `01_Inbox` | Duplicate inbox/vault-like folder | `D:\Zhuan_Vault` or `90_Archive` | Manual review | High | Duplicate with `00_Inbox`; content role must be confirmed first. |
| `02_AI_Agents` | Agent documentation | `docs/agents` | Move later after approval | Medium | System docs, not root code. |
| `03_Workflows` | Workflow documentation | `docs/operation` | Move later after approval | Medium | Operational docs. |
| `04_Prompts` | Prompt library | `docs/prompts` | Move later after approval | Medium | Duplicate with `prompts`. |
| `05_Templates` | Templates | `docs/templates` | Move later after approval | Medium | Template material, not runtime code. |
| `06_Projects` | Project notes | `D:\Zhuan_Vault` or `docs/legacy` | Manual review | High | May be human-readable memory. |
| `07_Principles` | Principles/memory | `D:\Zhuan_Vault` | Move later after approval | High | Human-readable memory belongs in the Vault. |
| `08_Logs` | Captures, media, logs | Ignore locally or archive later | Do not move yet | High | Private captures/media. Must not be blindly committed. |
| `09_References` | Reference material | `D:\Zhuan_Vault` or `docs/legacy` | Manual review | High | May contain PDFs, notes, or assets. |
| `logs` | System/dev logs or old docs | `docs/operation` or ignored local logs | Manual review | Medium | Duplicate risk with `08_Logs`; classify before moving. |
| `prompts` | System prompts | `docs/prompts` | Move later after approval | Low-Medium | Duplicate with `04_Prompts`. |
| `README.md` | Project entry documentation | `README.md` | Keep at root | Low | Human and agent entry point. |
| `AGENTS.md` | Agent instructions | `AGENTS.md` | Keep at root | Medium | Root operational rules; stage only after source review. |
| `CLAUDE.md` | Agent instructions | `CLAUDE.md` | Keep at root | Medium | Root operational rules; stage only after source review. |
| `.gitignore` | Git safety rules | `.gitignore` | Keep at root | Low | Controls secret/generated/local-only paths. |
| `.gitattributes` | Git attributes | `.gitattributes` | Keep at root | Low | Repository text/binary behavior. |

## Proposed Final Root Structure

```text
D:\Zhuan_OS
|-- apps
|-- core
|-- data
|-- scripts
|-- tests
|-- docs
|   |-- architecture
|   |-- operation
|   |-- agents
|   |-- prompts
|   |-- templates
|   `-- legacy
|-- launchers
|-- 90_Archive
|-- README.md
|-- AGENTS.md
|-- CLAUDE.md
|-- .gitignore
`-- .gitattributes
```

## Duplicate And Collision Findings

| Duplicate / Collision | Finding | Recommended Resolution |
|---|---|---|
| `04_Prompts` vs `prompts` | Two prompt routes exist at root. | Consolidate later into `docs/prompts` after manual review. |
| `08_Logs` vs `logs` | Both look log-like, but likely have different privacy levels. | Treat `08_Logs` as private/local capture output. Classify `logs` before moving or committing. |
| `00_Inbox` vs `01_Inbox` | Two inbox routes exist at root. | Manual review. Do not move or commit blindly. |
| `docs` vs command/control docs | `00_Command_Center`, `02_AI_Agents`, `03_Workflows`, and `05_Templates` overlap with docs. | Move system docs into `docs/*` only after explicit approval. |
| Windows case/collision risk | Windows paths are case-insensitive by default. | Avoid plans that rely on case-only distinctions such as `templates` vs `Templates`. |

## Unsafe Paths That Must Not Be Blindly Committed

Do not blindly stage or commit:

- `data/`
- `data/*.db`
- `data/index_state.json`
- `data/events/*.jsonl`
- `08_Logs/`
- `08_Logs/telegram_inbox/`
- `08_Logs/telegram_media/`
- `logs/` until classified
- `00_Inbox/`
- `01_Inbox/`
- inbox/private captures
- media files such as `*.jpg`, `*.jpeg`, `*.png`, `*.mp4`, `*.mov`
- `.env`
- `.env.*`
- `.venv/`
- `__pycache__/`
- `.obsidian/workspace.json`
- `.obsidian/workspace-mobile.json`

Safe example exception:

- `.env.example` may be committed only when it contains placeholders and no secret values.

## Staged Migration Sequence

### Step 1: Create docs subfolders

Create only structural documentation folders:

```text
docs/architecture
docs/operation
docs/agents
docs/prompts
docs/templates
docs/legacy
```

No old folders move in this step.

### Step 2: Move system docs only

Move only clearly system-facing documentation after explicit approval:

- architecture docs to `docs/architecture`
- runbooks and operation checklists to `docs/operation`
- agent setup/rules docs to `docs/agents`
- prompt docs to `docs/prompts`
- template docs to `docs/templates`

Do not move memory, private captures, vault-like notes, media, or logs in this step.

### Step 3: Leave private logs untouched

Do not move, delete, rename, or stage:

- `08_Logs/`
- `logs/` until classified
- `data/`
- `00_Inbox/`
- `01_Inbox/`
- private captures
- media files

### Step 4: Archive old duplicated folders

After manual review and explicit approval, stale duplicates may be routed to:

- `docs/legacy` for old system documentation
- `90_Archive` for old system routes that must remain available but not active
- `D:\Zhuan_Vault` for human-readable memory that belongs outside the system/code root

### Step 5: Update README path map

After the structure is real, update `README.md` with:

- active root map
- local-only paths
- do-not-commit paths
- migration status
- current operator commands

## Approval Rules

- No old folder may be moved without explicit approval.
- No old folder may be deleted without explicit approval.
- No old folder may be renamed without explicit approval.
- No old folder may be archived without explicit approval.
- `08_Logs`, `logs`, `data`, and inbox/private captures must not be blindly committed.
- A migration command plan is not permission to execute migration.

## Exact Next Command Plan

These commands are the next safe planning checks. Do not run migration commands until explicitly approved.

```powershell
git -C D:\Zhuan_OS status --short --branch
git -C D:\Zhuan_OS diff --cached --name-only
```

If the staged area is non-empty, stop and decide whether to commit or unstage current work before path migration.

Create docs subfolders only when approved:

```powershell
New-Item -ItemType Directory -Force D:\Zhuan_OS\docs\architecture
New-Item -ItemType Directory -Force D:\Zhuan_OS\docs\operation
New-Item -ItemType Directory -Force D:\Zhuan_OS\docs\agents
New-Item -ItemType Directory -Force D:\Zhuan_OS\docs\prompts
New-Item -ItemType Directory -Force D:\Zhuan_OS\docs\templates
New-Item -ItemType Directory -Force D:\Zhuan_OS\docs\legacy
```

Dry-run style review before any move:

```powershell
git -C D:\Zhuan_OS status --short --branch
Get-ChildItem D:\Zhuan_OS -Force -Directory
Get-ChildItem D:\Zhuan_OS\docs -Force
```

Only after explicit approval, move docs route by route with `Move-Item -LiteralPath ...`. Never use broad wildcards for migration.
## Sprint C1 Active Root Reset

Sprint C1 moves old root-level legacy folders out of the active root into:

```text
D:\Zhuan_OS\legacy_removed\root_legacy_2026_07
```

This is a move-only archival reset. It is not deletion, not Vault migration, and not approval to commit private or generated files.

### Future Active Root

```text
D:\Zhuan_OS
|-- apps
|-- core
|-- data
|-- config
|-- scripts
|-- launchers
|-- tests
|-- docs
|-- agent_workspace
|-- legacy_removed
|-- README.md
|-- AGENTS.md
|-- CLAUDE.md
|-- .gitignore
`-- .gitattributes
```

Hidden folders may remain for now:

```text
.git
.obsidian
.agents
.codex
```

### Legacy Folders Moved

These folders are Sprint C1 legacy candidates and should live under `legacy_removed/root_legacy_2026_07/` when present:

```text
00_Command_Center
00_Inbox
01_Inbox
02_AI_Agents
03_Workflows
04_Prompts
05_Templates
06_Projects
07_Principles
08_Logs
09_References
logs
prompts
01_Daily
02_Learning
03_Projects
05_Decision
06_Review
07_AI_Workflows
90_Archive_Index
Templates
_Agent
_Context
```

### Telegram Bot Dependency Map

Telegram Bot active folder:

```text
D:\Zhuan_OS\apps\zhuan-telegram-bot
```

Required runtime dependencies:

```text
D:\Zhuan_OS\core\event_bus
D:\Zhuan_OS\core\schema
D:\Zhuan_OS\core\storage
D:\Zhuan_OS\core\indexing
D:\Zhuan_OS\core\query
D:\Zhuan_OS\data\events
D:\Zhuan_OS\data\zhuan_os.db
```

The bot must continue to write captures through Event Bus first. JSONL event logs remain source of truth. SQLite remains a rebuildable query index. Telegram query buttons must read SQLite through the shared query layer, not raw SQL and not Vault scans.

Optional legacy Markdown fallback is local helper output only. It is not source of truth and must not point into `legacy_removed`.

### Paths That Remain Source Of Truth

```text
D:\Zhuan_OS\data\events\events-YYYY-MM.jsonl
```

### Paths That Remain Rebuildable Indexes

```text
D:\Zhuan_OS\data\zhuan_os.db
D:\Zhuan_OS\data\index_state.json
```

### Deprecated Paths

These root paths are deprecated for active operation:

```text
D:\Zhuan_OS\08_Logs
D:\Zhuan_OS\logs
D:\Zhuan_OS\00_Inbox
D:\Zhuan_OS\01_Inbox
D:\Zhuan_OS\04_Prompts
D:\Zhuan_OS\prompts
```

Do not recreate them for normal operation unless a later sprint explicitly approves a compatibility shim.

### Next Sprint Rename Plan

Do not rename apps in Sprint C1. In a later sprint, after tests are stable and imports are mapped, consider:

```text
apps\zhuan-telegram-bot -> apps\telegram_bot
apps\web-dashboard -> apps\web_dashboard
```

Before that rename sprint:

1. Add import compatibility tests.
2. Update launcher scripts.
3. Update README and operation docs.
4. Run full tests and manual bot smoke checks.
5. Stage by exact file names only.
