# Test Case Template

Use this structure when the user asks for a visible test plan or when the
behavior is non-trivial enough that explicit scenario naming matters.

## Minimal Case Shape

- Case: short behavior-focused title
- Layer: unit, service, transport, or integration
- Setup: relevant fixtures, state, and collaborators
- Trigger: exact call, request, or event
- Expected: precise observable outcome
- Notes: edge-condition or risk rationale when useful

## Scenario Buckets

- Happy path: the main supported business flow
- Boundary: min/max values, empty values, rounding edges, stale state, missing
  optional data
- Negative: invalid input, missing records, domain conflicts, provider errors
- Authorization: wrong org, wrong role, disabled account, missing permission
- Workflow: duplicate events, retries, already-resolved state, race windows

## Mapping Into Tests

- Prefer one scenario per test when the behavior is sharp and observable.
- Group closely related table-driven variants only when the assertion shape is
  the same.
- Make the test name mention the trigger and the expected outcome.
- Assert the externally visible behavior first, then the critical side effects.

## When To Load This Reference

Load when turning requirements, acceptance criteria, QA risks, or code behavior
into concrete test scenarios. Use it before writing tests or visible test plans.

## Detailed Case Table

| Case ID | Requirement/AC | Layer | Scenario | Setup | Trigger | Expected Result | Risk Covered | Automation |
|---|---|---|---|---|---|---|---|---|

## Expected Result Rules

Expected results should name:

- returned status or error;
- persisted state;
- emitted event/message;
- visible UI or API response;
- side effect that must happen;
- side effect that must not happen.

Avoid:

- "works correctly";
- "verify success";
- "no issues";
- expected results that require reading implementation internals.

## Quick Flow Guidance

In `--quick-flow`, produce the highest-value cases first: happy path, strongest
negative path, permission boundary, and the most likely regression.

## Full Flow Guidance

In `--full-flow`, map every meaningful requirement or AC to at least one case,
and identify uncovered requirements explicitly.

## Decision Log Guidance

Record decisions for coverage exclusions, manual-only cases, accepted risk, or
ambiguous expected behavior resolved by assumption.
