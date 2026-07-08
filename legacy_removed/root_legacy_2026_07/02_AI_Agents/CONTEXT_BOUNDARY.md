# Context Boundary

Purpose: define what each AI tool may know by default and how private data is handled.

## Default Context

ChatGPT may know:

- Zhuan's stated goals, decisions, and non-private workflow context.
- Summaries of projects and problems.
- Redacted errors, logs, and file paths when needed.

Codex may know:

- Repository files in the explicitly targeted workspace.
- Git status, tests, build output, and code context needed for execution.

Claude Code may know:

- The bounded task context needed for a worker job.
- Specific files Zhuan approves for the task.

Marvis may know:

- High-level task state, reminders, routing notes, and non-private summaries.

Zhuan may know:

- Everything Zhuan chooses to inspect.
- Final decision context.
- Risk trade-offs and verification results.

## Current Context vs Storage Context

Current context belongs in `D:\Zhuan_OS`:

- Today's task.
- Active decisions.
- AI prompts and rules.
- Execution notes.
- Review loops.

Storage context belongs in `D:\Zhuan_Vault`:

- References.
- Old projects.
- Study files.
- Media.
- Archives.

Private storage belongs in `D:\Zhuan_Vault\01_Private`:

- Private identity, finance, education, account-reference, and personal files.
- Not normal AI context.

## Private Data

Do not share by default:

- Identity documents.
- Finance records.
- Account credentials.
- API keys, tokens, passwords, seed phrases, cookies, or private keys.
- Raw contents from `D:\Zhuan_Vault\01_Private`.

## Zhuan_Private_Vault

`D:\Zhuan_Vault\01_Private` is private storage. It is not normal AI context.

Rules:

- Do not open private files unless Zhuan explicitly approves the exact task.
- Use route-level summaries before file-level details.
- Never print private filenames or contents unless Zhuan explicitly asks.
- Parent `D:\Zhuan_Vault` must not track this folder.

## Summary-First Rule

For sensitive material, ask for or produce a summary first:

1. Route or category.
2. Risk type.
3. What decision is needed.
4. Whether deeper access is necessary.

Only inspect deeper content after explicit approval.

## Explicit Approval Rule

Private file access requires all of:

- Clear target.
- Clear reason.
- Minimum necessary scope.
- No secret value output.
- Confirmation before any modification.
