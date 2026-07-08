# Quick Commands

## Start Work

- Check `00_Command_Center/TODAY.md`.
- Write one clear next action.
- Pick the smallest reversible step.
- Use `02_AI_Agents/TOKEN_BUDGET_POLICY.md` to choose the right context size.
- Check the Verification Ladder when risk is unclear.

## Codex

- Use Codex for repo edits, Git checks, audits, and verification.
- Keep commands scoped to the target repository.
- Never expose secrets or private file contents.
- Follow the Permission Matrix before staging, committing, pushing, or deleting.

## Review

- Use review mode for risky decisions, Git cleanup, security, and architecture.
- Lead with findings and the smallest safe next action.

## Control Layer Commands

### Choose token level

Open `02_AI_Agents/TOKEN_BUDGET_POLICY.md` before loading broad context or choosing between Marvis, Claude Code, Codex, and ChatGPT.

### Check permissions

Open `02_AI_Agents/PERMISSION_MATRIX.md` before giving an AI tool file, Git, private-data, or account-level authority.

### Check context boundary

Open `02_AI_Agents/CONTEXT_BOUNDARY.md` before sharing private, financial, identity, account, or credential-adjacent information.

### Emergency stop

Open `02_AI_Agents/EMERGENCY_STOP.md` when Git status, file movement, delete behavior, private data, or secret risk is unexpected.

### Choose verification level

Open `03_Workflows/Verification/VERIFICATION_LADDER.md` before medium-risk or higher work.

### Hand off work

Use `03_Workflows/Handoff/HANDOFF_PROTOCOL.md` when moving work between ChatGPT, Codex, Claude Code, Marvis, or Zhuan.

### Score models

Update `08_Logs/model-scorecard.md` after enough real usage to judge accuracy, safety, cost, and best use case.
