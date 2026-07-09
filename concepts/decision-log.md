# Decision Log

`decision-log.md` captures durable choices that affect scope, behavior,
validation, implementation, rollout, or traceability. The AI assistant produces
or updates decision rows whenever a skill makes, accepts, changes, or depends on
a material decision.

Every feature workspace should keep its own decision log:

- `specs-refiniment/<feature-name>/decision-log.md` for refinement work;
- `specs/<feature-name>/decision-log.md` for implementation work.

## When To Add A Decision

The AI adds or updates a decision entry when a skill:

- accepts an assumption that changes scope or behavior;
- resolves an open question;
- chooses between meaningful options;
- skips a lifecycle predecessor in quick flow;
- changes artifact routing, ownership, status, validation, or rollout;
- depends on a decision made outside the current artifact.

## Canonical Structure

```markdown
# Decision Log

| ID | Date | Status | Owner | Decision | Context/Evidence | Options Considered | Affected Artifacts | Validation/Trace Links |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| DEC-001 | YYYY-MM-DD | proposed / accepted / superseded / rejected | role or name | concise decision | source facts, artifact links, or evidence | option A; option B; recommended default | affected docs, tasks, code, tests, or rollout notes | requirement IDs, test IDs, validation commands, PRs, commits, or tickets |
```

## Relationship To Other Concepts

- `artifact_metadata.decision_log` points back to the feature decision log.
- `state.toon` stores `decision_ref` values for lifecycle transitions.
- `specs-index.toon` exposes decision-log paths so agents do not search for
  them manually.
- Decision IDs should appear in related artifacts when they materially explain
  scope or validation.

## AI Reading Behavior

Before the AI treats an assumption, scope choice, predecessor skip, or validation
claim as accepted, it checks whether a related `DEC-###` exists. When the specs
index points to a feature decision log, the AI opens that file before searching
for decisions elsewhere.

The AI uses decision rows to understand:

- what was decided;
- who owns or accepted it;
- whether the status is proposed, accepted, superseded, or rejected;
- which artifacts and validations the decision affects;
- whether the current artifact relies on a stale or superseded decision.

## AI Production Behavior

When the AI creates a decision row, it produces:

- a stable `DEC-###` ID;
- date;
- status;
- owner;
- concise decision statement;
- context or evidence;
- options considered when relevant;
- affected artifacts;
- validation or trace links.

When a later skill changes the decision, the AI does not overwrite history
silently. It updates status, adds a superseding decision, or references the new
decision from affected artifacts.

## AI Failure Modes

The AI must not:

- bury material decisions only in prose;
- proceed in quick flow with a skipped predecessor without decision or assumption
  trace;
- treat proposed decisions as accepted;
- delete old decision rows to simplify the table;
- update artifact metadata or state decision references without keeping
  `decision-log.md` consistent.
