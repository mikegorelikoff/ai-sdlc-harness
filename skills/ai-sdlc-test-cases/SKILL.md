---
name: ai-sdlc-test-cases
description: AI SDLC test-case-driven testing workflow. Use when Codex is asked to derive test cases, create a test plan, expand coverage, or write tests from explicit scenarios before implementing unit, service, transport, or integration tests.
---

# AI SDLC Test Cases

## Purpose

Derive executable AI SDLC test scenarios before implementation, link each scenario to the spec, and define verifiable outcomes, automation commands, execution order, and human decisions without leaving open TODOs.

## Inputs

- Read the active `requirements.md`, `design.md`, and existing `test-cases.md` for medium or large work.
- Read `qa.md` when acceptance or manual validation already exists.
- Collect the changed behavior, contract, bug, regression risk, endpoint, provider, asset, or workflow under test.
- Collect existing test files for the affected package when implementing tests.
- Read `references/test-case-template.md` when the scenario matrix needs reusable wording.
- Collect known fixtures, mocks, seeded data, and unavailable dependencies.

## Steps

1. Write `In scope` and `Out of scope` before generating scenarios.
2. Check every proposed test case against `Out of scope`; delete any test case that tests excluded behavior.
3. Define the behavior under test in one sentence.
4. Identify the spec reference each scenario proves using an acceptance-criteria ID, requirement ID, or Markdown section anchor.
5. Create scenario IDs using `TC-001`, `TC-002`, and continuing sequence.
6. Include happy path, boundary values, null or missing inputs, negative validation, authorization, state-transition, retry, idempotency, concurrency, and provider-failure cases when relevant.
7. Map each scenario to exactly one primary layer: unit, service, transport, integration, QA/manual, or not automated.
8. Write a verifiable outcome for every scenario using one of these forms:
   - shell command whose exit code proves the outcome
   - numbered checklist of observable facts a human can tick without interpretation
   - before/after diff or data pair that proves the behavior changed correctly
9. Write an automation path for every scenario using one of these forms:
   - script path plus exact invocation
   - CI step name
   - `Manual — automate by YYYY-MM-DD — blocker: concrete blocker`
10. Replace open TODOs with `Decisions required`; each decision must include Question, Options A/B/C, Recommended default, Owner, and Blocking yes/no.
11. Replace decorative layer descriptions with `Execution order`; each layer must include run condition, what it blocks, and failure action.
12. Update `specs/NNN-feature-name/test-cases.md` for medium or large work.
13. Implement tests only after the scenario matrix contains spec refs, verifiable outcomes, automation paths, execution order, and structured decisions.
14. Name tests so a reviewer can trace each test back to a scenario ID or spec reference.

## Output Spec

Use this format:

```text
Scope:
- In scope:
  - Behavior, contract, endpoint, workflow, or artifact covered.
- Out of scope:
  - Behavior, contract, endpoint, workflow, or artifact deliberately excluded.

Scenario matrix:
| ID | Spec ref | Scenario | Setup | Trigger | Verifiable outcome | Layer | Automation |
| --- | --- | --- | --- | --- | --- | --- | --- |
| TC-001 | AC-001 or `requirements.md#acceptance-criteria` | Scenario name | Fixture/state | Action | Command, checklist, or before/after pair | unit/service/transport/integration/QA/manual | script path + invocation, CI step, or manual blocker |

Automation plan:
- TC-001: exact command or CI step, target file if new, expected pass condition.

Execution order:
1. Layer: run condition; blocks: later layer or release gate; failure action: stop, fix, rerun, or escalate.

Decisions required:
- Question: decision needed.
  Options:
  A. Option A
  B. Option B
  C. Option C
  Recommended default: option and reason.
  Owner: role or person.
  Blocking: yes | no.
```

Quality gate:

- Pass when every scenario has scope fit, spec ref, setup, trigger, verifiable outcome, layer, concrete automation path, and execution-order placement.
- Pass when every manual scenario uses `Manual — automate by YYYY-MM-DD — blocker: reason`.
- Pass when every unresolved item is a structured decision with options and recommended default.
- Fail when any scenario lacks a spec ref, uses prose-only expected outcomes, says only `Manual review`, contains `TODO`, or leaves layer mapping as descriptive text instead of execution order.

## Examples

Valid executable scenario:

```text
Scenario matrix:
| ID | Spec ref | Scenario | Setup | Trigger | Verifiable outcome | Layer | Automation |
| --- | --- | --- | --- | --- | --- | --- | --- |
| TC-003 | `requirements.md#acceptance-criteria` | Reject unsupported provider asset | BitGo wallet fixture contains BTC only | Submit a USDC transfer request | `GOCACHE=/tmp/ai-sdlc-go-cache go test ./internal/service -run TestRejectUnsupportedProviderAsset -count=1` exits 0 and asserts no transfer row is created | service | `.codex/skills/ai-sdlc-validation/scripts/validation_plan.py internal/service/transfer_service.go`; implement `TestRejectUnsupportedProviderAsset` |

Execution order:
1. Service tests: run after scenario matrix is approved; blocks transport tests; failure action: fix service validation and rerun focused service test.

Decisions required:
- Question: Should unsupported provider assets return 400 validation error or 409 conflict?
  Options:
  A. 400 validation error
  B. 409 conflict
  C. Provider-specific 502
  Recommended default: A, because the request is invalid before provider submission.
  Owner: Delivery Manager
  Blocking: yes
```

Invalid counter-example:

```text
| TC-003 |  | Test bad inputs | Existing tests | Run tests | Service rejects bad data | service | Manual review |
```

Reject this because it has no spec ref, the outcome is prose-only, and `Manual review` has no blocker or automation date.

## Edge Cases

- Mark expected behavior as a structured decision when the spec is silent and code behavior is inconsistent.
- Prefer lower-layer tests when they prove the behavior without full integration setup.
- Use integration tests only when provider adapters, HTTP contracts, migrations, or cross-package behavior must be exercised together.
- Mark flaky or external-service-dependent scenarios as manual only with `Manual — automate by YYYY-MM-DD — blocker: reason`.
- Do not invent provider responses; use documented fixtures, existing mocks, or a structured decision with a recommended default.
- Do not output `TODO`, `TBD`, `manual review`, or `needs confirmation` as a final gap.

## Scope Boundary

- Do not claim QA signoff; use `$ai-sdlc-qa`.
- Do not choose final validation command execution; use `$ai-sdlc-validation`.
- Do not implement production behavior from this skill alone; use `$ai-sdlc-sdd` and approved `tasks.md`.
- Do not add broad snapshot tests when focused assertions can prove the behavior.
