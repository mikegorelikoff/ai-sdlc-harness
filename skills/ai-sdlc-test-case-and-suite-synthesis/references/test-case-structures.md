# Test Case Structures

## Detailed Test Case Table

Use this structure:

| Test Case ID | Title | Requirement ID | User Role | Priority | Test Type | Preconditions | Test Data | Steps | Expected Result | Actual Result | Status | Automation Candidate | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|

## Execution Rules

- Use IDs like `TC-001`, `TC-002`.
- Use priorities like `P0`, `P1`, `P2`, `P3`.
- Use explicit test types such as Functional, Negative, Boundary, Permission, Integration, API, UI, Workflow, Regression, Smoke, UAT, Security, Performance, Accessibility.

## Suite Expectations

Generate separate suites for:

- Smoke
- Regression
- UAT

## Coverage Expectations

Include relevant cases for:

- functional behavior;
- positive flows;
- negative and invalid behavior;
- boundary and edge cases;
- permissions and unauthorized access;
- workflows and E2E;
- API behavior;
- integrations;
- UI and UX;
- data validation;
- state transitions;
- notifications;
- security and privacy;
- non-functional scenarios.

## Quality Bar

- Avoid vague steps such as "verify it works".
- Avoid vague expected results such as "system works correctly".
- Tie every case to a requirement, role, rule, workflow, or risk.

## When To Load This Reference

Load when the user needs executable test cases or named suites rather than only
a strategy. Use it after QA gap review and test strategy when possible.

## Suite Table

| Suite | Purpose | Included Test Case IDs | Entry Criteria | Exit Criteria | Owner |
|---|---|---|---|---|---|

## Case Writing Rules

- Preconditions must describe data/state, not vague setup.
- Steps should be executable by a tester or automatable by an engineer.
- Expected result must be observable.
- Priority should reflect launch/business risk, not author preference.
- Automation candidate should be based on stability and value.

## Coverage Matrix

| Requirement ID | Test Case IDs | Suite | Coverage Status | Gap |
|---|---|---|---|---|

Coverage statuses:

- Covered
- Partial
- Not covered
- Blocked
- Manual only

## Quick Flow Guidance

In `--quick-flow`, synthesize a compact high-value suite and label coverage gaps
instead of expanding every edge case.

## Full Flow Guidance

In `--full-flow`, verify traceability to requirements, roles, workflows, risks,
and decision-log assumptions. Missing expected results should block final cases.

## Decision Log Guidance

Record decisions for suite boundaries, manual-only coverage, skipped test types,
and accepted gaps.
