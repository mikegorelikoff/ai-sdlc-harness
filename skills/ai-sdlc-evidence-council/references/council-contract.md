# Evidence Council Contract

Use `ai-sdlc-evidence-council-input/v1` with:

- `topic`, `mode` (`simulated` or `independent`);
- authority: `owner` and non-empty feature-relative `authoritative_artifacts`;
- panel: unique `id`, `role`, `execution` matching mode, and unique
  `execution_id` (required for independent mode);
- evidence: unique `id`, feature-relative `path`, positive `line`, `detail`,
  and non-empty `trace_targets`;
- agreements: `id`, `statement`, `reviewers`, `evidence_ids`;
- conflicts: `id`, `statement`, at least two `positions`, `reviewers`,
  `evidence_ids`, `owner`, `next_action`;
- proposals: `id`, `statement`, `reviewers`, `evidence_ids`, `owner`, status
  (`proposed`, `deferred`, `rejected`, `review-needed`), and `next_action`;
- unresolved questions: `id`, `question`, `reviewers`, `evidence_ids`, `owner`, `next_action`.

All reviewer and evidence references must resolve. Council cannot emit an
`accepted` proposal status.
