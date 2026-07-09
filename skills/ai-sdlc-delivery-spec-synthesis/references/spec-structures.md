# Spec Structures

## Core Sections

Use a structured delivery spec with sections such as:

1. Executive Summary
2. Background and Input Package Summary
3. Delivery Goal
4. In Scope
5. Out of Scope
6. Actors and Roles
7. Assumptions
8. Open Questions
9. End-to-End Workflows
10. Functional Requirements
11. Business Rules
12. Data Requirements
13. Non-Functional Requirements
14. Dependencies
15. Operational and Support Considerations
16. Launch or Rollout Constraints
17. Success Measures

## Functional Requirements Table

Capture:

- Requirement ID
- Actor
- Requirement
- Business Value
- Priority
- Acceptance Criteria
- Dependencies
- Assumptions
- Open Questions

## Spec Discipline

- Tie every major requirement cluster back to stories or actor workflows.
- Keep delivery blockers and unresolved decisions explicit.
- Treat ambiguous areas as open questions, not hidden assumptions.

## When To Load This Reference

Load when stories, PRFAQ, BRD, or discovery notes need to become a delivery spec
for cross-functional handoff. This is a refinement artifact, not the developer
implementation SDD unless implementation is explicitly in scope.

## Input Checklist

Look for:

- source package or story set;
- actor and role definitions;
- workflows and state transitions;
- business rules and exceptions;
- data requirements;
- integrations and dependencies;
- MVP/out-of-scope boundaries;
- decision-log rows.

## Requirement Detail Table

| Requirement ID | Actor/System | Requirement | Source | Priority | Acceptance Ref | Decision Ref | Open Issue |
|---|---|---|---|---|---|---|---|

## Workflow Detail Table

| Workflow ID | Trigger | Actor | Steps | End State | Exceptions | Related Requirements |
|---|---|---|---|---|---|---|

## Rule Table

| Rule ID | Rule | Applies To | Source | Failure Behavior | Decision Ref |
|---|---|---|---|---|---|

## Quick Flow Guidance

In `--quick-flow`, synthesize a usable delivery spec with assumptions clearly
marked. Use `TBD` only for non-blocking detail, not for core actor/rule/outcome
definitions.

## Full Flow Guidance

In `--full-flow`, verify that every major requirement maps to a source story,
workflow, or decision. Ask when data ownership, permission, failure behavior, or
MVP boundary is unclear.

## Decision Log Guidance

Record decisions for:

- requirement inclusion/exclusion;
- accepted assumptions;
- rule interpretation;
- workflow exception handling;
- operational or rollout constraints.

## Quality Bar

A strong delivery spec gives engineering, design, QA, analytics, and operations
the same understanding of scope. It should expose unresolved decisions instead
of smoothing them over.
