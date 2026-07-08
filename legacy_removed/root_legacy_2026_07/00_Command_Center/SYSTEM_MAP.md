# System Map

## Roles

- ChatGPT = thinking interface.
- Codex = repo execution agent.
- Claude Code = fast worker.
- Marvis = task routing and assistant layer.
- Zhuan_Vault = storage vault.
- Zhuan_Private_Vault = private online storage.
- Zhuan = final judge.

## Flow

1. ChatGPT clarifies thinking and strategy.
2. Codex executes inside repositories.
3. Claude Code handles focused worker tasks.
4. Marvis helps route tasks and maintain lightweight operating context.
5. Zhuan_Vault stores durable references.
6. Zhuan_Private_Vault stores private material.
7. Zhuan decides what is true, useful, and worth keeping.

## Control Layer

- OKR: `00_Command_Center/OKR.md`
- Token Budget Policy: `02_AI_Agents/TOKEN_BUDGET_POLICY.md`
- Permission Matrix: `02_AI_Agents/PERMISSION_MATRIX.md`
- Context Boundary: `02_AI_Agents/CONTEXT_BOUNDARY.md`
- Emergency Stop: `02_AI_Agents/EMERGENCY_STOP.md`
- Verification Ladder: `03_Workflows/Verification/VERIFICATION_LADDER.md`
- Handoff Protocol: `03_Workflows/Handoff/HANDOFF_PROTOCOL.md`
- Model Scorecard: `08_Logs/model-scorecard.md`

## Control Rule

AI tools may assist, but Zhuan owns final judgment, approval, and responsibility.

## Five Engineering Stack

### Prompt Engineering

Lives in `04_Prompts/` and `02_AI_Agents/Agent_Rules/`.

Purpose: shape AI answers so they are direct, safe, and useful.

### Context Engineering

Lives in `02_AI_Agents/CONTEXT_BOUNDARY.md` and `02_AI_Agents/TOKEN_BUDGET_POLICY.md`.

Purpose: give each tool enough context, not all context.

### Harness Engineering

Lives in `02_AI_Agents/PERMISSION_MATRIX.md`, `02_AI_Agents/EMERGENCY_STOP.md`, and `03_Workflows/Verification/VERIFICATION_LADDER.md`.

Purpose: control permissions, verification, and stop conditions.

### Loop Engineering

Lives in `00_Command_Center/TODAY.md`, `03_Workflows/Review/REVIEW_WORKFLOW.md`, and `08_Logs/weekly-judgment-scorecard.md`.

Purpose: force Before AI, After AI, judgment, verification, action, and review.

### OKR

Lives in `00_Command_Center/OKR.md`.

Purpose: make Zhuan_OS measurable instead of just organized.
