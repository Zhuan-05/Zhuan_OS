# Zhuan OS Architecture

Zhuan OS is the control repo for AI-assisted work. It keeps policies, prompts, logs, and setup notes in one place so Codex, Claude Code, and future agents operate from the same rules.

## Boundaries

- `D:\Zhuan_OS` is the active operating repo.
- `D:\Zhuan_Vault` is a separate archive and must not be touched by default.
- Obsidian vault files are not edited unless the task explicitly asks for vault work.
- Secrets, tokens, API keys, credentials, and production data are out of scope unless explicitly approved.

## Main Areas

- `docs/`: durable operating documentation.
- `prompts/`: reusable prompts for agent workflows.
- `logs/`: lightweight decision, task, and risk tracking.
- `templates/`: intended home for reusable repo templates, if it does not conflict with an Obsidian template folder.

## Operating Loop

1. Capture the task and constraints.
2. Recon the repo and current state.
3. Plan small, reversible changes.
4. Implement with minimal blast radius.
5. Verify with tests, checks, or explicit reasoning.
6. Log decisions and residual risks when useful.
