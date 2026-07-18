# UX Contract

Use `ai-sdlc-ux-input/v1` with:

- `context`;
- actors: unique `id`, `name`, non-empty `goals`, non-empty `needs`;
- journeys: unique `id`, known `actor`, `goal`, ordered non-empty `steps`,
  observable `acceptance`, and `trace_targets`;
- states: `surface`, `state`, `behavior`, `recovery`, and `trace_targets`;
- accessibility: `requirement`, `evidence`, status (`planned`, `passed`,
  `failed`, `blocked`), and `trace_targets`;
- content: optional `surface`, `intent`, and `guidance` notes.

Full flow requires at least one journey, state, and accessibility check.
