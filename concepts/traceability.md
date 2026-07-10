# Traceability

Traceability is the ability to explain why an artifact, implementation choice,
test, or review result exists. The AI assistant produces traceability by linking
artifact metadata, decision logs, lifecycle state, validation evidence, and
source artifact IDs.

In this library, traceability is not stored in one file. It is built from a
small set of linked records.

Traceability is directional. Upstream records explain intent; downstream
records prove decomposition, implementation, and validation. A useful chain can
be traversed in both directions: from a goal to its tests, or from a failed test
back to the requirement and decision that created it.

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

The runtime also recognizes `GOAL-###`, `CAP-###`, `WF-###`, `BR-###`,
`SC-###`, `NFR-###`, and `DEP-###` when artifacts use more detailed goal,
capability, workflow, business-rule, scenario, non-functional, or dependency
catalogs. `T###` remains supported by SDD task plans.

IDs are stable within a feature. Do not renumber them merely to make tables
contiguous; supersede or deprecate records while preserving references.

## Minimum Bar

The AI produces enough traceability for a feature to answer:

- which artifacts define the expected behavior;
- which decisions shaped the scope;
- which tests or validation commands prove the behavior;
- which skill produced or last materially changed each artifact;
- whether the current lifecycle stage is complete, blocked, skipped, or active.

The AI reads `specs-index.toon` first, then opens only the artifacts needed for
the current question.

## Traceability Graph

```text
GOAL-001
  -> CAP-002
    -> EPIC-003
      -> US-014
        -> REQ-021 / BR-006
          -> AC-031
            -> TC-044
              -> suite: regression
                -> validation evidence / defect / signoff

DEC-004 -------> REQ-021, AC-031, rollout notes
RISK-007 ------> test strategy, TC-044, monitoring requirement
```

Not every feature needs every ID type. The chain must be detailed enough for
the decisions and risks involved, without generating identifiers that no
artifact uses.

## Coverage Dimensions

Traceability reviews should distinguish:

- **requirements coverage:** every material requirement has acceptance evidence;
- **scenario coverage:** happy, negative, boundary, permission, and failure paths;
- **risk coverage:** high-impact risks map to prevention, detection, or tests;
- **decision coverage:** accepted choices appear in affected artifacts;
- **execution coverage:** planned tests map to suites, environments, and results;
- **ownership coverage:** blockers and follow-up work have accountable owners.

A high percentage of linked IDs is not sufficient when the uncovered item is a
critical security, data-loss, compliance, or rollout risk.

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

### Worked Example

Suppose `REQ-012` requires retrying a recoverable payment failure and `DEC-004`
sets the retry window to 72 hours. The delivery spec should link both IDs,
`AC-019` should describe observable retry behavior and stopping conditions, and
`TC-044` should test issuer recovery while a negative case proves permanent
failures are not retried. QA readiness then reports both test IDs and any
environment dependency. A reviewer can recover the whole chain without the
original chat.

## Broken-Link Handling

When an ID is referenced but its defining artifact is missing:

1. Search the workspace index and related-artifact metadata.
2. Check whether the record was renamed, superseded, or migrated.
3. Restore the defining source or update every affected reference deliberately.
4. Record a decision if meaning or accepted scope changed.
5. Rebuild indexes and rerun the relevant traceability/readiness gate.

Do not satisfy the check by removing the downstream ID when the underlying
requirement or risk still exists.

## AI Failure Modes

The AI must not:

- produce artifacts that cannot be connected back to requirements, decisions, or
  validation;
- claim a test covers a requirement without a visible ID or evidence link;
- mark lifecycle stages done while traceability is missing in full flow;
- rely on chat-only context for durable decisions.
