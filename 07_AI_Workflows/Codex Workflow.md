# Codex Workflow

## Purpose

Define how Codex should work with this vault.

## Default Reading Order

1. `_Context/SYSTEM_CONTEXT.md`
2. `_Context/ACTIVE_CONTEXT.md`
3. `_Context/ROUTING_RULES.md`
4. Relevant project, learning, decision, or review file

## Rules

- Work only within the requested scope.
- Do not access `D:\Zhuan_Vault` unless explicitly asked.
- Do not scan private folders.
- Do not initialize Git, commit, or push without explicit confirmation.
- Prefer small, reversible, testable changes.
- Log meaningful vault changes in `_Agent/CHANGELOG.md`.

## Task Pattern

1. Identify context.
2. Check boundaries.
3. Make the smallest useful change.
4. Verify result.
5. Report what changed and what remains.