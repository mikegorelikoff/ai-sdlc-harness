<!-- public-docs-canonical: ../docs/index.md -->

> **Internal, non-canonical design note.** The maintained public documentation starts at [AI SDLC Harness docs](../docs/index.md). This file is retained for repository history and maintainer context only.

# Workflow Handoff Contract

Every AI SDLC workflow returns a normalized post-workflow handoff directly in
the assistant response. The contract separates what happened from what must or
may happen next.

Schema `ai-sdlc-handoff/v1` contains:

- `result`: `complete`, `partial`, or `blocked`;
- `summary`: concise outcome;
- `blockers`: explicit unresolved conditions;
- `next_required`: exactly one skill, reason, command, and expected artifact;
- `next_optional`: zero or more actions with the same fields.

Use `skills/_shared/ai_sdlc_handoff.py` to validate and render Markdown or TOON.
The emitter is read-only: the owning workflow completes artifacts and state
before producing its handoff. When the next required action is unclear, use
`ai-sdlc-navigator` and then emit the selected action.
