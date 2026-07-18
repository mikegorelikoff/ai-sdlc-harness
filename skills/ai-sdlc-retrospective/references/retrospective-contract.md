# Retrospective Contract

Use schema `ai-sdlc-retrospective-input/v1` with separate arrays:

- `observations`: `id`, `category` (`worked`, `friction`, `escape`, `surprise`),
  `statement`, and evidence object containing feature-relative `path`, positive
  `line`, and non-empty `detail`;
- `proposals`: `id`, non-empty `based_on` observation IDs, `target`, `change`,
  `owner`, `status` (`proposed`, `accepted`, `rejected`, `deferred`), optional
  `decision_ref`, and `next_action`.

Observation statements describe what happened. Proposal changes describe what
should change. An accepted proposal requires `decision_ref`; other statuses may
leave it empty.
