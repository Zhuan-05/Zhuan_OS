# Verification Ladder

Use the lowest level that matches the real risk.

## Level 0: Casual

Examples:

- Simple wording.
- Quick explanation.
- Brainstorming with no action.

Required verification:

- Basic reasoning.

Required AI/tool:

- ChatGPT or Marvis.

Zhuan confirmation required:

- No.

Tool routing:

- Marvis for reminders and routing.
- ChatGPT for quick thinking.

## Level 1: Low-Risk

Examples:

- Small Markdown edit.
- Simple command explanation.
- Minor local note update.

Required verification:

- Read back changed file or inspect status.

Required AI/tool:

- Claude Code, Codex, or ChatGPT.

Zhuan confirmation required:

- No, unless files will be deleted or pushed.

Tool routing:

- Claude Code Flash for fast implementation.
- Codex if repo state matters.

## Level 2: Medium-Risk

Examples:

- Code edit.
- Git staging.
- Repo restructuring without secrets.
- Workflow documentation updates.

Required verification:

- `git status --short`.
- Diff/stat review.
- Targeted tests or manual check.

Required AI/tool:

- Codex preferred.

Zhuan confirmation required:

- Required before commit or push if not already requested.

Tool routing:

- Codex Pro for repo/Git-sensitive work.
- Claude Code Flash can draft but should hand off if risk grows.

## Level 3: High-Risk

Examples:

- Private data paths.
- Git cleanup.
- Dependency or config changes.
- Security-sensitive code.
- Large file movement.

Required verification:

- Read-only precheck.
- Route-level status summary.
- Secret-safe scan by filename or field name only.
- Explicit before/after Git status.

Required AI/tool:

- Codex with red-team review.

Zhuan confirmation required:

- Yes.

Tool routing:

- Codex Pro only.
- ChatGPT may red-team the plan.
- Marvis may remind or route only.

## Level 4: Critical

Examples:

- History rewrite.
- Force push.
- Production config.
- Credential rotation.
- Irreversible deletion.

Required verification:

- Written plan.
- Backup or rollback path.
- Explicit risk statement.
- Step-by-step approval.
- Post-action audit.

Required AI/tool:

- Codex plus Zhuan final approval.

Zhuan confirmation required:

- Yes, immediately before action.

Tool routing:

- Codex Pro executes only after explicit approval.
- ChatGPT may review the plan.
- Claude Code Flash and Marvis do not execute critical actions.
