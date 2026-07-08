# Claude Code Setup

Use Claude Code as a worker agent for scoped implementation, review, and debugging tasks.

## Default Role

Claude Code should act as a repo-aware worker:

- Read instructions before editing.
- Keep changes small and reversible.
- Avoid broad refactors unless asked.
- Report files changed, checks run, and open risks.

## Handoff Pattern

Give Claude Code:

1. The exact repo path.
2. The task objective.
3. Files or directories in scope.
4. Safety boundaries.
5. Required output format.

## Worker Prompts

- `prompts/claude-code/01-worker-check.md`
- `prompts/claude-code/02-small-task.md`
