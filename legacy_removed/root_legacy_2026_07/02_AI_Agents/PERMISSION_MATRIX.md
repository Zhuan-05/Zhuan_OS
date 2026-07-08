# Permission Matrix

Purpose: keep AI tools useful without giving them uncontrolled agency.

## Marvis

Permission level: low.

Allowed actions:

- Summarize Zhuan's stated context.
- Draft plans, checklists, and reminders.
- Help route tasks to ChatGPT, Codex, or Claude Code.

Forbidden actions:

- Delete, move, rename, commit, push, or rewrite history.
- Access private files without explicit approval.
- Decide final priorities for Zhuan.

Requires explicit confirmation:

- Any action that affects files, Git, private data, money, accounts, or long-term commitments.

## Claude Code with DeepSeek V4 Flash

Permission level: low/medium.

Allowed actions:

- Fast worker tasks.
- Small code edits in approved repositories.
- Lightweight file inspection and summaries.
- Draft scripts or docs for review.

Forbidden actions:

- Broad refactors without approval.
- Secret inspection.
- Git push, force push, or history rewrite.
- Private Vault access unless explicitly approved.

Requires explicit confirmation:

- File deletion or movement.
- Git commit.
- Dependency install.
- Changes touching auth, credentials, production config, or private data.
- Any high-risk action must be handed off to Codex.

## Codex with DeepSeek V4 Pro

Permission level: medium/high.

Allowed actions:

- Repository execution.
- Code edits, Git status checks, audits, and verification.
- Controlled staging, commits, and pushes when Zhuan explicitly asks.
- Security-conscious repair plans.

Forbidden actions:

- Reveal secrets or private file contents.
- Touch `D:\Zhuan_Vault` or `D:\Zhuan_Vault\01_Private` unless the task explicitly targets them.
- Force push or clean Git history without explicit approval.
- Delete files without explicit approval.

Requires explicit confirmation:

- Destructive commands.
- History rewrite.
- Push to remote.
- Private file access.
- Production or credential-related changes.

## ChatGPT

Permission level: judgment layer.

Allowed actions:

- Thinking, review, planning, red-team critique, learning support.
- Help Zhuan structure decisions and compare options.
- Draft instructions for Codex, Claude Code, or Marvis.

Forbidden actions:

- Be treated as final truth.
- Encourage passive copy-paste for important decisions.
- Request or expose secrets unnecessarily.

Requires explicit confirmation:

- Advice involving money, private data, account security, legal/medical risk, or irreversible technical action.

## Zhuan

Permission level: final judge.

Allowed actions:

- Final judgment.
- Approval of risk.
- Priority decisions.
- Accept/reject/verify AI output.

Forbidden actions:

- Outsourcing responsibility to AI.
- Skipping review on high-risk work.

Requires explicit confirmation:

- Any irreversible or high-risk AI-assisted action must be consciously approved by Zhuan.
