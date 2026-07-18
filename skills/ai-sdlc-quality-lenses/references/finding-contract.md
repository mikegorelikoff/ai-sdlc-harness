# Quality Finding Contract

The findings input is a UTF-8 JSON array. Every object requires:

- `id`: unique stable identifier such as `QL-001`;
- `lens`: registered lens ID selected for this review;
- `evidence`: object with repository-relative `path`, positive integer `line`,
  and concise `detail` describing the observed fact;
- `severity`: `critical`, `high`, `medium`, `low`, or `info`;
- `trace_targets`: non-empty unique list of requirement, acceptance, test,
  decision, task, risk, or other durable artifact identifiers;
- `owner`: accountable role or person;
- `resolution_status`: `open`, `accepted`, `mitigated`, `rejected`, or
  `deferred`;
- `next_action`: concrete action that moves or preserves the finding.

Unknown fields are ignored for forward compatibility. Finalization rejects
missing fields, unknown lenses, unselected lenses, duplicate IDs, absolute or
parent-traversing evidence paths, and non-positive evidence lines.
