# QA Plan Template

Use this structure when the change needs explicit QA evidence in `qa.md`.

## Minimal Shape

- Change summary: what changed and where regression risk sits
- Acceptance scenarios: observable supported behavior
- Regression targets: existing paths that must remain stable
- Risk notes: risky dependencies, workflows, or rollout concerns
- Validation commands: deterministic automated checks
- Manual checks: exploratory or operator-facing verification
- Signoff: pass/fail or remaining gaps

## Prompts

- Which user-visible or operator-visible behavior would regress first?
- Which acceptance path still needs human verification even if tests exist?
- Which focused command gives the highest-value automated signal?
- Which scenario belongs in `test-cases.md` versus `qa.md`?

## When To Load This Reference

Load when a change needs explicit QA evidence, release validation, regression
thinking, or manual verification notes. Use it for both code-facing and
product-facing QA planning.

## Expanded QA Plan Shape

| Section | What To Include | Common Mistake |
|---|---|---|
| Change Summary | changed behavior and affected surfaces | implementation-only summary |
| Acceptance Scenarios | user/operator-observable outcomes | vague "works" checks |
| Regression Targets | existing flows that must stay stable | only testing the new path |
| Risk Notes | dependencies, data, permissions, rollout | hiding assumptions |
| Validation Commands | deterministic automated checks | commands without purpose |
| Manual Checks | exploratory or UX/operator checks | duplicating automated tests |
| Signoff | pass/fail/gaps and owner | no residual risk |

## Quick Flow Guidance

In `--quick-flow`, produce a lean QA plan with the highest-value commands and
manual checks. Mark broader validation as residual risk when it is not justified
by the change size.

## Full Flow Guidance

In `--full-flow`, verify acceptance scenarios, regression targets, test-case
coverage, decision-log assumptions, and validation evidence before signoff.

## Decision Log Guidance

Record decisions when QA accepts a manual workaround, defers coverage, narrows
regression scope, or accepts a risk due to time/environment constraints.

## Quality Bar

A good QA plan tells another tester what changed, what matters, how to validate
it, and what risk remains. It should not be a generic checklist detached from
the actual feature.
