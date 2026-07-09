# Test Strategy Structures

## Core Outputs

Define:

- test objective;
- in scope;
- out of scope;
- critical roles;
- critical workflows;
- critical integrations;
- must-test areas;
- nice-to-test areas;
- high-risk areas;
- unchanged but regression-sensitive areas;
- required test types;
- smoke, regression, and UAT suite intent;
- test data strategy;
- environment and dependency needs;
- launch blockers;
- severity and priority expectations.

## Coverage Dimensions

Consider only applicable dimensions:

- functional;
- positive;
- negative;
- boundary and edge cases;
- permissions;
- workflows and E2E;
- integration;
- API;
- UI and UX;
- notifications;
- state transitions;
- security and privacy;
- performance and reliability.

## Strategy Discipline

- If everything is labeled critical, force prioritization.
- If performance or compliance thresholds are unknown, mark them as open questions.
- If environment or third-party dependencies can block testing, make them explicit.

## When To Load This Reference

Load after requirements are testable enough and before detailed test cases are
generated. The strategy defines what deserves coverage and why.

## Risk-Based Prioritization

| Risk Driver | Examples | Testing Implication |
|---|---|---|
| Business criticality | revenue, launch, support | smoke/UAT priority |
| Permission boundary | admin/customer/operator | authorization tests |
| State transition | pending/approved/rejected | workflow and retry tests |
| Integration | provider/API/webhook | contract and failure tests |
| Data sensitivity | PII, money, credentials | security/privacy tests |
| Change complexity | refactor, migration | regression depth |

## Strategy Output Table

| Area | Risk | Test Type | Priority | Owner | Evidence | Open Questions |
|---|---|---|---|---|---|---|

## Suite Design

- Smoke suite: smallest set proving launch-critical paths are alive.
- Regression suite: existing behavior most likely to break.
- UAT suite: stakeholder-readable scenarios proving business value.
- Negative suite: invalid, unauthorized, failed, or conflicting behavior.
- Integration suite: external systems, contracts, webhooks, retries.

## Quick Flow Guidance

In `--quick-flow`, produce a focused strategy with must-test areas and a lean
smoke/regression/UAT split. Avoid exhaustive test taxonomy.

## Full Flow Guidance

In `--full-flow`, verify scope, out-of-scope, roles, risk drivers, dependencies,
test data, environment needs, and coverage expectations before moving to cases.

## Decision Log Guidance

Record decisions about risk acceptance, suite boundaries, excluded test types,
manual-vs-automated strategy, and environment constraints.
