# Codex Setup

Use Codex as the execution agent for repository work in `D:\Zhuan_OS`.

## Default Rules

- Work only inside the current repo unless Zhuan explicitly approves otherwise.
- Read local instructions before editing.
- Preserve useful existing files.
- Do not delete files without explicit confirmation.
- Do not touch `D:\Zhuan_Vault`.
- Do not read or print secrets.

## Standard Workflow

1. Confirm current directory.
2. Inspect `git status --short`.
3. Read relevant files before making claims.
4. Create the smallest useful change.
5. Run targeted verification when possible.
6. Summarize changed files, verification, and remaining risk.

## Useful Starting Prompts

- `prompts/codex/01-verify-setup.md`
- `prompts/codex/02-repo-recon.md`
- `prompts/codex/03-safe-repair-plan.md`
- `prompts/codex/04-implement-small-task.md`
- `prompts/codex/05-red-team-review.md`
- `prompts/codex/06-finish-branch.md`
