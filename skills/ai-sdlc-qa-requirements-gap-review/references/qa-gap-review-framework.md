# QA Gap Review Framework

Run this before test strategy or test-case synthesis.

## Inputs

Possible inputs:

- user stories
- acceptance criteria
- delivery spec
- BRD
- PRFAQ
- API documentation
- workflow diagrams
- business rules
- existing test cases
- defect history

## Review Dimensions

Check whether the package clearly defines:

- scope and out-of-scope boundaries;
- user roles and permissions;
- happy paths and failure paths;
- business rules and validations;
- state transitions;
- integration behavior;
- notifications;
- data rules;
- environment dependencies;
- non-functional expectations;
- launch-critical flows.

## Mandatory Blocking Questions

If any of these remain too vague, block test-case synthesis and ask follow-ups:

- What is the expected result for each core workflow?
- Which roles can perform, view, edit, approve, or reject each action?
- What business rules decide valid versus invalid behavior?
- What happens when validation, permissions, integration, or status transitions fail?
- What is in MVP versus deferred?
- Which flows are truly launch-critical?

## Output Shape

Return:

- confirmed facts;
- assumptions;
- unclear or conflicting requirements;
- QA blockers;
- clarifying questions;
- a short go/no-go judgment for moving into test design.

## When To Load This Reference

Load before designing test strategy or test cases when requirements may be too
vague to test. This protects QA from inventing expected behavior.

## Gap Severity

| Severity | Meaning | QA Action |
|---|---|---|
| Blocker | Expected result cannot be known | stop and ask |
| High | Tests can be drafted but risk is significant | isolate and escalate |
| Medium | Test with explicit assumption | record assumption |
| Low | Minor clarification | proceed with note |

## QA Gap Matrix

| Dimension | Evidence Needed | Gap Found | Severity | Question/Action |
|---|---|---|---|---|
| Role/Permission | who can do what |  |  |  |
| Expected Result | observable output/state |  |  |  |
| Rule | validation or domain rule |  |  |  |
| Failure | error/retry/rollback behavior |  |  |  |
| Data | required inputs and state |  |  |  |
| Integration | external dependency behavior |  |  |  |
| Non-functional | performance, reliability, accessibility |  |  |  |

## Quick Flow Guidance

In `--quick-flow`, identify only blockers and high-risk assumptions that affect
test design. Proceed with clearly labeled assumptions for minor gaps.

## Full Flow Guidance

In `--full-flow`, require expected results for core workflows, negative paths,
permissions, integrations, and launch-critical behavior before test-case
synthesis.

## Decision Log Guidance

Record accepted testing assumptions, deferred coverage, narrowed scope, and any
requirement interpretation that determines expected results.
