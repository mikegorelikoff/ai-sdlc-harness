# Release And Readiness Structures

## Dependency Table

Use:

| Dependency ID | Backlog Item | Depends On | Dependency Type | Owner | Needed By | Risk If Delayed | Mitigation |
|---|---|---|---|---|---|---|---|

## Risk Table

Use:

| Risk ID | Risk | Category | Related Backlog Items | Likelihood | Impact | Mitigation | Owner | Early Warning Signal |
|---|---|---|---|---|---|---|---|---|

## Prioritization Table

Use:

| Backlog Item ID | Item Type | Summary | Business Value | Urgency | Risk Reduction | Dependency Impact | Effort Placeholder | Priority | Rationale |
|---|---|---|---|---|---|---|---|---|---|

## Scope Slicing Table

Use:

| Backlog Item ID | Summary | Scope Category | Reason | Risk If Excluded | Manual Workaround | Launch Blocker? |
|---|---|---|---|---|---|---|

## Release Slice Table

Use:

| Release Slice | Objective | Included Backlog Items | Excluded Items | Success Criteria | Risks | Dependencies |
|---|---|---|---|---|---|---|

## Sequencing Table

Use:

| Sequence | Backlog Item ID | Item Summary | Reason for Position | Can Run in Parallel? | Blocks | Blocked By |
|---|---|---|---|---|---|---|

## Milestone Table

Use:

| Milestone | Objective | Key Backlog Items | Exit Criteria | Dependencies | Risks |
|---|---|---|---|---|---|

## Estimation Readiness Table

Use:

| Backlog Item ID | Summary | Estimation Readiness | Reason | Clarification Needed | Suggested Next Step |
|---|---|---|---|---|---|

## Spike Table

Use:

| Spike ID | Topic | Question to Answer | Related Backlog Items | Owner Role | Output Expected | Timebox Placeholder | Decision Enabled |
|---|---|---|---|---|---|---|---|

## Definition Of Ready Table

Use:

| Backlog Item ID | Ready? | Missing Information | Blocking Questions | Required Action |
|---|---|---|---|---|

## Definition Of Done Table

Use:

| Done Criteria | Applies To | Required Before Launch? | Owner Role | Notes |
|---|---|---|---|---|

## Traceability Matrix

Use:

| Business Goal ID | Business Goal | Epic IDs | Feature IDs | Story IDs | Task IDs | Coverage Status | Notes |
|---|---|---|---|---|---|---|---|

## JIRA-Ready View

Use:

| Issue Type | Summary | Description | Parent | Priority | Labels | Acceptance Criteria | Dependencies | Notes |
|---|---|---|---|---|---|---|---|---|

## Readiness Discipline

- If capacity or dates are unknown, produce logical sequencing instead of fake sprint dates.
- If items are too large to estimate, flag them explicitly.
- If business goals lack backlog coverage, mark them as blocked or partially covered.

## When To Load This Reference

Load when a backlog exists and the next question is release shape, sequencing,
dependency management, estimation readiness, or whether the backlog is ready for
delivery planning.

## Release Slicing Order

1. Identify launch objective and non-negotiable outcomes.
2. Mark hard dependencies and blockers.
3. Separate must-have, should-have, could-have, and won't-have.
4. Identify risk-reduction spikes.
5. Sequence items by dependency, value, risk, and learning.
6. Produce release slices with success criteria.
7. Mark estimation readiness and remaining questions.

## Slicing Heuristics

Prefer earlier slices for items that:

- unlock other teams;
- reduce major feasibility risk;
- validate key assumptions;
- enable smoke/UAT paths;
- create operational readiness.

Defer items that:

- are cosmetic without launch impact;
- depend on unresolved policy/vendor decisions;
- can be handled manually for MVP;
- do not map to a launch goal.

## Quick Flow Guidance

In `--quick-flow`, avoid fake dates and capacity. Produce logical slices and
explicit assumptions. Ask only if the launch objective or must-have scope is
unclear.

## Full Flow Guidance

In `--full-flow`, require dependency, risk, DoR, DoD, and traceability checks
before declaring readiness. Ask questions for missing blockers, owners, launch
criteria, or estimation inputs.

## Decision Log Guidance

Record decisions for:

- launch slice composition;
- deferred scope;
- accepted manual workaround;
- risk accepted without spike;
- sequencing tradeoff;
- definition-of-ready or definition-of-done change.

## Readiness Verdict

Use one of:

- Ready for delivery planning.
- Ready with assumptions.
- Needs backlog refinement.
- Needs dependency resolution.
- Not ready for release slicing.

Always include the top three reasons and the next action.
