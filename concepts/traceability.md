# Traceability

Traceability is the ability to explain why an artifact, implementation choice,
test, or review result exists. The AI assistant produces traceability by linking
artifact metadata, decision logs, lifecycle state, validation evidence, and
source artifact IDs.

In this library, traceability is not stored in one file. It is built from a
small set of linked records.

## Traceability Sources

- `decision-log.md` records durable decisions.
- `state.toon` records lifecycle stage status and transition references.
- `artifact_metadata` records artifact path, skill, flow mode, status, owner,
  trace IDs, related artifacts, validation, and metatags.
- `specs-index.toon` exposes feature and artifact summaries for fast lookup.
- Artifact bodies hold detailed requirements, scenarios, designs, validation
  evidence, and blockers.
- Validation reports and code-review artifacts link implementation evidence back
  to requirements and test IDs.

## Common IDs

The AI preserves or produces stable IDs when possible:

- `REQ-###` for requirements;
- `AC-###` for acceptance criteria;
- `US-###` for user stories;
- `TC-###` for test cases;
- `TASK-###` for implementation tasks;
- `RISK-###` for risks;
- `DEC-###` for decisions;
- `EPIC-###` for epics.

## Minimum Bar

The AI produces enough traceability for a feature to answer:

- which artifacts define the expected behavior;
- which decisions shaped the scope;
- which tests or validation commands prove the behavior;
- which skill produced or last materially changed each artifact;
- whether the current lifecycle stage is complete, blocked, skipped, or active.

The AI reads `specs-index.toon` first, then opens only the artifacts needed for
the current question.

## AI Reading Behavior

When traceability matters, the AI reads in this order:

1. Workspace `specs-index.toon` to find the feature and relevant artifacts.
2. Feature `state.toon` to understand lifecycle status.
3. `decision-log.md` to understand durable choices.
4. Selected artifact metadata to confirm status, skill, trace IDs, and related
   files.
5. Selected artifact body for detailed requirements, tests, or evidence.

This order keeps token usage low while preserving enough context for rigorous
work.

## AI Production Behavior

When the AI creates or updates an artifact, it produces traceability by:

- adding or preserving stable IDs in the body;
- filling `artifact_metadata.trace_ids`;
- linking related artifacts in metadata;
- adding decision-log rows for material choices;
- updating state transition `decision_ref` values;
- adding validation evidence when checks were run;
- refreshing specs indexes.

## AI Failure Modes

The AI must not:

- produce artifacts that cannot be connected back to requirements, decisions, or
  validation;
- claim a test covers a requirement without a visible ID or evidence link;
- mark lifecycle stages done while traceability is missing in full flow;
- rely on chat-only context for durable decisions.
