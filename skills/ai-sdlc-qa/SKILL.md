---
name: ai-sdlc-qa
description: AI SDLC QA workflow. Use when Codex is asked for QA planning, acceptance validation, regression scope, exploratory checks, smoke tests, release verification, or change-focused manual validation evidence.
---

# AI SDLC QA

## Purpose

Produce QA acceptance, regression, manual-check, and signoff evidence for AI SDLC changes and record it in `specs/NNN-feature-name/qa.md` when the work is medium or large.

## Inputs

- Read the active spec files: `requirements.md`, `test-cases.md`, `design.md`, and existing `qa.md`.
- Collect the changed files or diff when QA is based on an implementation.
- Collect validation output from `$ai-sdlc-validation` when checks have already run.
- Collect release context, user roles, provider names, asset symbols, endpoints, or UI surfaces affected by the change.
- Read `references/qa-plan-template.md` when the QA plan needs reusable acceptance or regression wording.

## Steps

1. Define the change boundary in one sentence.
2. Rank QA risks by user impact, money/asset impact, security impact, provider impact, and regression likelihood.
3. Write acceptance scenarios with actor, setup, action, expected result, evidence type, and risk.
4. Write regression targets for existing behavior that must remain stable.
5. Separate automated validation from manual or exploratory checks.
6. Record exact validation commands and outcomes when already run.
7. Mark unrun checks as planned or skipped with a concrete reason and residual risk.
8. Update `qa.md` for medium or large work.
9. Use `$ai-sdlc-test-cases` when the missing artifact is scenario-to-test automation design.
10. Use `$ai-sdlc-validation` when commands need to be selected or executed.

## Output Spec

Use this format:

```text
QA plan:
- Change boundary: one sentence.

Acceptance scenarios:
- QA-001:
  Actor: role or system.
  Setup: required state.
  Action: user/API/system action.
  Expected result: observable result.
  Evidence: automated test | manual check | not yet covered.
  Risk: high | medium | low and reason.

Regression targets:
- Existing behavior and why it is at risk.

Validation evidence:
- command -> passed | failed | skipped: reason.

Manual checks:
- Check, environment, expected result, and owner if known.

Signoff:
- Ready | blocked | partial, with reason.
```

Quality gate:

- Pass when every acceptance scenario has actor, setup, action, expected result, evidence, and risk.
- Fail when a scenario says only "verify it works", when skipped validation has no reason, or when the plan claims a pass without executed evidence.

## Examples

Valid QA scenario:

```text
- QA-001:
  Actor: operations user.
  Setup: organization has BitGo configured with one enterprise wallet.
  Action: open the custodian setup endpoint.
  Expected result: response includes the BitGo enterprise ID and wallet display label without exposing secrets.
  Evidence: transport test plus manual API response review.
  Risk: high because incorrect wallet scope can block settlement operations.
```

Invalid counter-example:

```text
Acceptance scenarios:
- Test the endpoint.
```

Reject this because it lacks setup, action, expected result, evidence, and risk.

## Edge Cases

- State `blocked` when no environment, fixture, credentials, or sample payload exists for a manual check.
- Do not mark manual QA as passed from code inspection alone.
- Mark flaky or nondeterministic evidence as partial and name the unstable dependency.
- Use redacted examples for provider payloads; never include secrets or production-only values.
- Keep QA signoff separate from developer validation when acceptance requires human workflow review.

## Scope Boundary

- Do not implement automated tests; use `$ai-sdlc-test-cases` to design tests and normal coding workflow to implement them.
- Do not select broad test suites by default; use `$ai-sdlc-validation`.
- Do not approve product scope; use `$ai-sdlc-ba` for unresolved business decisions.
- Do not claim release readiness when validation, manual checks, or signoff are incomplete.
