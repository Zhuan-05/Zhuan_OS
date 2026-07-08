# Token Budget Policy

## Principle

Zhuan_OS should use just-in-time context, not all context.

Do not load the full Zhuan_OS unless doing a system audit.

The goal:

- Enough context for correctness.
- Not too much context to create noise.
- Preserve token budget.
- Preserve Zhuan's attention.

## Token Levels

### Level 1: Fast Path

Use for small tasks.

Context:

- `TODAY.md`
- `QUICK_COMMANDS.md`
- Relevant file only

Budget: 500 - 3k tokens.

### Level 2: Standard Task

Use for normal study, coding, planning, or review.

Context:

- `TODAY.md`
- `THINKING_PROTOCOL.md`
- Selected workflow
- Target file or task details

Budget: 3k - 8k tokens.

### Level 3: High Risk

Use for Git, private data, delete, push, security, account, or money.

Context:

- `PERMISSION_MATRIX.md`
- `CONTEXT_BOUNDARY.md`
- `VERIFICATION_LADDER.md`
- `EMERGENCY_STOP.md`
- Selected target files/status only

Budget: 8k - 30k tokens.

### Level 4: Audit / Migration

Use for large read-only audits, migrations, and repo cleanup.

Context:

- Full relevant directory scan
- Git status
- Risk files
- Policies

Budget: 30k - 100k+ tokens.

## Tool Routing

### Marvis

- Use low-token daily loop.
- Do not read full Zhuan_OS.
- Do not read private files.
- Use for reminders, routing, and review prompts.

### Claude Code / DeepSeek V4 Flash

- Use for low/medium-risk implementation.
- Read only relevant files.
- Hand off high-risk work to Codex.

### Codex / DeepSeek V4 Pro

- Use for high-risk, repo, Git, security, and architecture.
- Read first.
- Take the smallest safe action.
- No push/delete without approval.

## Compression Rules

When logs become long:

- Summarize weekly.
- Extract principles.
- Archive old detail.
- Keep current active context short.

## Anti-Waste Rules

Do not:

- Load all files by default.
- Paste long history unless needed.
- Ask multiple agents to solve the same low-risk task.
- Use Pro model for small formatting work.
- Use Flash model for high-risk decisions.

## Default Rule

Small task: use Fast Path.

Important task: use Before AI / After AI / Review.

High-risk task: use Verification Ladder and Codex Pro.
