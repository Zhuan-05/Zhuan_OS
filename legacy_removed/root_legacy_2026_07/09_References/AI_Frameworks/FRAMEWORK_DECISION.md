# AI Framework Decision

## Framework Notes

- OpenAI Agents SDK = lightweight agent app framework.
- LangGraph = durable, stateful, human-in-the-loop orchestration.
- Microsoft Agent Framework = enterprise .NET/Python agent framework.
- CrewAI = role-based multi-agent automation.
- AutoGen = maintenance mode; avoid for new Zhuan_OS core.

## Current Decision

Do not adopt a complex framework yet.

Use:

- Codex for repository execution.
- Claude Code for fast worker tasks.
- ChatGPT for thinking.
- `AGENTS.md` for durable operating rules.

Revisit frameworks only when Zhuan_OS has repeated workflows that need orchestration, memory, state, or human approval gates.
