# Research Contract

Use `ai-sdlc-research-input/v1` with:

- `topic`;
- `scope`: `internal`, `external`, or `mixed`;
- questions: unique `id`, `question`, non-empty `trace_targets`;
- sources: unique `id`, `title`, `locator`, `type`, ISO `accessed_at`,
  `credibility`, and `notes`;
- findings: unique `id`, `statement`, non-empty registered `source_ids`,
  confidence (`high`, `medium`, `low`), non-empty `limitations`, and
  `trace_targets`;
- open questions: unique `id`, `question`, `owner`, and `next_action`.

Full flow requires at least two sources representing at least two source types.
External and mixed scope additionally require at least one direct HTTP(S)
locator gathered through internet research.
