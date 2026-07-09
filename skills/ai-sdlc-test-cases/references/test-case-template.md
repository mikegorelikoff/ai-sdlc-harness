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
