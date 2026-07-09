# Backlog Structures

## Feature Table

Use:

| Feature ID | Epic ID | Feature Name | Description | User Role | Business Value | Priority | MVP / Post-MVP | Dependencies | Risks | Open Questions |
|---|---|---|---|---|---|---|---|---|---|---|

## Story Table

Use:

| Story ID | Epic ID | Feature ID | User Role | User Story | Business Value | Priority | MVP / Post-MVP | Acceptance Criteria Summary | Dependencies | Assumptions | Open Questions |
|---|---|---|---|---|---|---|---|---|---|---|---|

## Acceptance Summary Table

Use:

| Story ID | Acceptance Criterion ID | Given | When | Then | Notes |
|---|---|---|---|---|---|

## Cross-Functional Task Tables

Technical and other tasks:

| Task ID | Parent Story / Feature | Task Type | Task Description | Owner Role | Dependencies | Priority | Notes |
|---|---|---|---|---|---|---|---|

Design tasks:

| Design Task ID | Related Epic / Feature / Story | Design Task | Required Output | Owner Role | Dependencies | Priority | Open Questions |
|---|---|---|---|---|---|---|---|

QA tasks:

| QA Task ID | Related Epic / Feature / Story | QA Task | Test Type | Priority | Dependencies | Notes |
|---|---|---|---|---|---|---|

Analytics tasks:

| Analytics Task ID | Related Goal / Feature / Story | Event or Metric | Description | Properties | Destination | Owner Role | Priority |
|---|---|---|---|---|---|---|---|

Operations tasks:

| Ops Task ID | Related Feature / Process | Operational Task | Owner Role | Required Before Launch? | Dependencies | Notes |
|---|---|---|---|---|---|---|

Compliance tasks:

| Compliance Task ID | Area | Task | Related Feature / Story | Owner Role | Required Before Launch? | Risk If Not Done | Open Questions |
|---|---|---|---|---|---|---|---|

## Decomposition Discipline

- Keep backlog items outcome-oriented.
- Keep task items linked to a planning artifact, not floating standalone.
- Flag anything that is too large to estimate.

## When To Load This Reference

Load this after goals/capabilities/epics are available and the work must become
features, user stories, acceptance summaries, and cross-functional tasks.

## Decomposition Order

1. Confirm goals, capabilities, and epics.
2. Split each epic into feature-sized outcomes.
3. Split features into user stories.
4. Add acceptance summaries for each story.
5. Add technical/design/QA/analytics/ops/compliance tasks.
6. Add dependencies and risks.
7. Mark items that are not ready for estimation.

## Sizing Heuristics

Split an item when:

- it has more than one primary actor;
- it has multiple independent workflow outcomes;
- it mixes UI/API/data/ops work with separate release risk;
- acceptance criteria cannot fit into a focused scenario set;
- it has hidden dependencies that can be delivered separately.

Keep an item together when:

- splitting would create artificial work with no independent value;
- the same actor, trigger, and outcome are shared;
- the acceptance criteria form one coherent behavior.

## Ready For Backlog Table

| Item ID | Type | Ready? | Missing Info | Blocker? | Next Action |
|---|---|---|---|---|---|

Use readiness states:

- Ready
- Ready with assumptions
- Needs clarification
- Too large
- Blocked

## Quick Flow Guidance

In `--quick-flow`, produce the backlog with explicit assumptions and mark
uncertain fields as `TBD` only when they are not delivery-blocking. Prefer
progress over questions for priority, rough dependencies, and task owner role.

## Full Flow Guidance

In `--full-flow`, ask questions or block when any story lacks actor, outcome,
acceptance summary, dependency, MVP status, or business value.

## Decision Log And Traceability

Record decisions for:

- MVP vs post-MVP placement;
- splitting or merging epics/features/stories;
- priority changes;
- accepted assumptions;
- deferred cross-functional work.

Trace every task to a story, feature, epic, or goal. No floating tasks.

## Quality Bar

A strong backlog can be handed to delivery, design, QA, and engineering without
requiring them to rediscover scope. The backlog should reveal ambiguity instead
of hiding it in broad stories.
