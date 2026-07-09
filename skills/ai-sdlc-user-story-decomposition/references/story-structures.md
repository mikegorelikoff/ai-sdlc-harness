# Story Structures

## Story Format

Write stories as:

`As a [user role], I want to [action/capability], so that [value/outcome].`

## Acceptance Criteria

Use when needed:

`Given [context]`
`When [action]`
`Then [expected result]`

## For Each Story or Story Cluster Capture

- actor;
- goal;
- business value;
- priority;
- dependencies;
- assumptions;
- open questions;
- linked scenarios.

## Scenario Coverage

Include:

- primary flow;
- alternate flows;
- negative flows;
- failure or retry flows;
- admin/support flows when relevant;
- rollback/cancellation paths when relevant.

## Blocking Rule

If a story cannot be written without inventing a key business rule or actor behavior, stop and mark that gap explicitly.

## When To Load This Reference

Load when a clarified delivery package needs to become user stories with
acceptance criteria and scenario coverage. Use it after a gap review when
possible.

## Story Splitting Heuristics

Split stories by:

- actor or permission boundary;
- workflow trigger;
- independent business outcome;
- state transition;
- integration boundary;
- positive vs high-risk negative behavior;
- launch-critical vs post-MVP scope.

Avoid splitting by implementation layer alone unless the layer can be delivered
and validated independently.

## Story Detail Table

| Story ID | Epic ID | Actor | Story | Value | Priority | MVP | Dependencies | Risks | Open Questions |
|---|---|---|---|---|---|---|---|---|---|

## Acceptance Criteria Table

| AC ID | Story ID | Given | When | Then | Rule Covered | Notes |
|---|---|---|---|---|---|---|

## Scenario Coverage Table

| Scenario ID | Story ID | Type | Trigger | Expected Outcome | Covered By AC |
|---|---|---|---|---|---|

Types:

- Primary
- Alternate
- Negative
- Permission
- Boundary
- Failure/retry
- Support/admin

## Quick Flow Guidance

In `--quick-flow`, draft the best story set with explicit assumptions and mark
open questions at the story or AC level. Do not stop for every missing detail.

## Full Flow Guidance

In `--full-flow`, do not finalize stories without actor, value, acceptance
criteria, dependencies, and MVP status. Ask when a missing rule would change the
story split or expected result.

## Decision Log Guidance

Record story split/merge choices, MVP exclusions, accepted assumptions, and
business rules inferred from weak source material.

## Quality Bar

A strong story set is ready for delivery planning and QA strategy: each story is
small enough to validate, valuable enough to justify, and explicit enough that
test cases can be derived without guessing.
