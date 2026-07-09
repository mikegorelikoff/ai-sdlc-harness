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
