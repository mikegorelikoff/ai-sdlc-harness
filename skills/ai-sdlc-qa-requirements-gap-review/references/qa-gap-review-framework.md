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
