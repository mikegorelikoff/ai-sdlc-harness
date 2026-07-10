# Decision Log

`decision-log.md` captures durable choices that affect scope, behavior,
validation, implementation, rollout, or traceability. The AI assistant produces
or updates decision rows whenever a skill makes, accepts, changes, or depends on
a material decision.

A decision is not merely an action item or an unanswered question. It records a
choice between meaningful alternatives whose outcome affects delivery. Open
questions remain in artifacts until a choice is proposed or accepted.

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

Do not add a new row for formatting changes, routine script execution, or facts
that are already authoritative source evidence and involve no choice.

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

## Decision Status Lifecycle

| Status | Meaning | May downstream work rely on it? |
| --- | --- | --- |
| `proposed` | A concrete option is awaiting authority or evidence | Only as an explicit risk/assumption |
| `accepted` | The accountable owner or authorized workflow adopted it | Yes |
| `rejected` | The option must not be treated as current intent | No |
| `superseded` | A later decision replaced it | Follow the replacing decision |

When superseding, preserve the original row and add the new `DEC-###` reference
to its context or affected artifacts. This keeps historical reasoning auditable.

## ID Allocation And Updates

Decision IDs are feature-local, stable, and monotonically allocated. Before
creating a row, inspect the existing log and choose the next unused `DEC-###`.
If the same decision is being clarified without changing its meaning, update
the existing row. If the selected option, scope, or authority changes, create a
new decision and supersede the old one.

Deterministic helpers upsert a row by ID and require the canonical nine-column
shape. This avoids duplicate decisions caused by retries.

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

### Example

```markdown
| DEC-004 | 2026-07-10 | accepted | Product | Retry failed payments for 72 hours | Discovery showed recoverable issuer failures and support cost | 24h; 72h; manual-only — 72h selected | delivery-spec.md; qa.md | REQ-012; AC-019; TC-044 |
```

The row states the outcome, evidence, alternatives, ownership, affected files,
and proof links. “Use recommended retry behavior” would be too vague to recover
the decision later.

## Cross-Workspace Decisions

Refinement and implementation keep separate decision logs because they have
different authorities. When an implementation constraint changes product scope,
record the technical choice in the implementation log and link or add the
scope-impact decision in refinement. Do not copy an accepted row into both logs
without clarifying which record owns the decision.

## AI Failure Modes

The AI must not:

- bury material decisions only in prose;
- proceed in quick flow with a skipped predecessor without decision or assumption
  trace;
- treat proposed decisions as accepted;
- delete old decision rows to simplify the table;
- update artifact metadata or state decision references without keeping
  `decision-log.md` consistent.
