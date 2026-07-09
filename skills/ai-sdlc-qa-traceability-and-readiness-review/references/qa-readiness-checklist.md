# QA Readiness Checklist

Review whether:

- all meaningful requirements have coverage;
- core business flows are covered;
- high-risk areas are covered;
- negative cases are included;
- edge cases are included where needed;
- permissions are tested;
- integrations are tested where applicable;
- data validations are covered;
- expected results are specific;
- test steps are executable;
- assumptions are marked;
- open questions are actionable;
- launch blockers are identified;
- duplicates or low-value cases exist;
- automation candidates are identified.

## Traceability Matrix Structure

Use:

| Requirement ID | Requirement Summary | Test Case IDs | Test Type | Priority | Coverage Status | Open Questions |
|---|---|---|---|---|---|---|

Coverage statuses:

- Covered
- Partially Covered
- Not Covered
- Blocked
- Needs Clarification

## Readiness Scale

- 1-3: Too incomplete for QA execution
- 4-6: Basic coverage exists, but major gaps remain
- 7-8: Good enough for structured QA planning and early execution
- 9-10: Strong test suite ready for QA execution and stakeholder review

## Final Review Output

Explain:

- why the score was given;
- what is well covered;
- what is missing;
- what is risky;
- what must be clarified before testing starts.

## When To Load This Reference

Load after QA strategy and test-case synthesis when you need to verify whether
requirements are actually covered and whether QA execution can begin.

## Traceability Rules

- Every meaningful requirement should map to one or more test cases.
- Every high-risk workflow should map to smoke or regression coverage.
- Every permission rule should have at least one allowed and one denied scenario.
- Every accepted assumption should be visible in either test notes or
  decision-log trace.

## Readiness Evidence Table

| Evidence Area | Required Signal | Present? | Gap | Impact |
|---|---|---|---|---|
| Requirements | IDs or clear requirement statements |  |  |  |
| Test Cases | executable steps and expected results |  |  |  |
| Suites | smoke/regression/UAT grouping |  |  |  |
| Risks | high-risk areas covered |  |  |  |
| Blockers | open questions and dependencies |  |  |  |
| Automation | candidates or rationale |  |  |  |

## Quick Flow Guidance

In `--quick-flow`, produce the matrix and the top readiness gaps. Focus on
launch-critical missing coverage instead of exhaustive scoring.

## Full Flow Guidance

In `--full-flow`, inspect requirements, test cases, suites, assumptions,
decision-log entries, and validation evidence before scoring readiness.

## Decision Log Guidance

Record readiness decisions when QA proceeds with partial coverage, blocked
coverage, manual-only checks, or accepted risk.

## Quality Bar

A strong readiness review makes it clear what QA can execute now, what remains
blocked, and which missing tests create real release risk.
