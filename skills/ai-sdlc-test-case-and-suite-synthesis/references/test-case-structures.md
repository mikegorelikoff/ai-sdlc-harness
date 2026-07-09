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
