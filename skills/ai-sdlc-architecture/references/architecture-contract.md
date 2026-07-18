# Architecture Contract

Use `ai-sdlc-architecture-input/v1` with `context` and arrays for:

- constraints: `id`, `statement`, `trace_targets`;
- components: `name`, `responsibility`, `dependencies`;
- interfaces: `name`, `from`, `to`, `contract`, `trace_targets`;
- decisions: `id`, `statement`, `rationale`, non-empty `alternatives`,
  non-empty `consequences`, `trace_targets`;
- risks: `id`, `statement`, `mitigation`, `owner`, `trace_targets`;
- validation: `check`, `evidence`, `status` (`planned`, `passed`, `failed`).

All identifiers must be unique within their collection. Full flow requires at
least one decision, risk, and validation check.
