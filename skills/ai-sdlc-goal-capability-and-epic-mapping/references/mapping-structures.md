# Mapping Structures

## Business Goals Table

Use:

| Goal ID | Business Goal | Success Metric | Target | Measurement Method | Related Capabilities | Priority |
|---|---|---|---|---|---|---|

## Role Matrix

Use:

| Role | Description | Main Goals | Key Actions | Data Access | Permissions | Success Criteria |
|---|---|---|---|---|---|---|

## Capability Map

Use:

| Capability ID | Capability | Description | User Roles | Business Value | MVP? | Dependencies | Risks | Open Questions |
|---|---|---|---|---|---|---|---|---|

## Epic Table

Use:

| Epic ID | Epic Name | Objective | Business Value | User Roles | Included Capabilities | Priority | Dependencies | Risks | Success Criteria | Open Questions |
|---|---|---|---|---|---|---|---|---|---|---|

## Mapping Discipline

- Force linkage from goals to capabilities.
- Force linkage from capabilities to epics.
- Flag anything that lacks a clear business or operational purpose.

## When To Load This Reference

Load when the initiative is understood but still needs to become an outcome
map: goals, roles, capabilities, and epics. This reference is useful before
backlog decomposition or release slicing.

## Input Checklist

Useful inputs include:

- PRFAQ, BRD, business-context, or discovery summary;
- success metrics or launch objectives;
- known roles and permission boundaries;
- MVP/non-MVP notes;
- dependency, risk, or constraint notes;
- decision-log rows from discovery.

## Mapping Steps

1. Extract business goals first.
2. Identify user/operator roles and their desired outcomes.
3. Group actions into capabilities.
4. Map capabilities to epics.
5. Mark dependencies and risks.
6. Flag goals with no capability coverage.
7. Flag capabilities with no clear goal.

## Traceability Expectations

Use IDs consistently:

- `GOAL-001` for goals.
- `CAP-001` for capabilities.
- `EPIC-001` for epics.

Suggested trace table:

| Goal ID | Capability IDs | Epic IDs | Coverage | Notes |
|---|---|---|---|---|

Coverage values:

- Covered
- Partially covered
- Missing capability
- Missing epic
- Blocked by decision

## Quick Flow Guidance

In `--quick-flow`, create the map from available evidence and mark uncertain
items as assumptions. Do not block unless the primary business goal, target role,
or MVP boundary is unknown.

## Full Flow Guidance

In `--full-flow`, challenge every epic that does not map back to a measurable
goal. Ask questions when goals are slogans, roles are vague, or capabilities are
implementation tasks instead of business abilities.

## Quality Bar

A strong map makes backlog decomposition mechanical: every feature or story can
point to an epic, every epic can point to capabilities, and every capability can
justify itself through a goal or operational need.
