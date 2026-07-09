---
name: ai-sdlc-qa
description: AI SDLC QA workflow. Use when Codex is asked for QA planning, acceptance validation, regression scope, exploratory checks, smoke tests, release verification, or change-focused manual validation evidence.
---

# ai-sdlc-qa: QA Planning And Evidence

> Internal AI SDLC skill, not client-facing by default.
> Every rule below is important to follow. None of it can be skipped.
> Before producing the final artifact, confirm required inputs, target audience, missing facts, output format, and constraints when they are unclear.
> Do not invent missing information. Ask concise clarification questions when required inputs are absent.

## 0. Skill Card

- Skill name: `ai-sdlc-qa`
- Primary audience: QA
- Supporting audience: BA, Dev, PM
- Audience tags: QA, BA, Dev, PM
- SDLC stage: QA planning and refinement
- Purpose: Produce QA acceptance, regression, manual-check, and signoff evidence for AI SDLC changes and place QA refinement artifacts under `specs-refiniment/<feature-name>/<file.md>` when writing files.
- Output: QA acceptance plan, regression targets, manual checks, validation evidence, and residual risks

### 0.1 Required Inputs

- Requirements, stories, delivery spec, `specs-refiniment/<feature-name>/<file.md>` QA context, or changed implementation context.
- Acceptance criteria, changed files, or release-sensitive behavior.
- Validation output if already run.

### 0.2 Clarification Rules

- Ask concise questions before finalizing when role, artifact, requirements, scope, audience, or constraints are unclear.
- If optional information is missing, mark it as `TBD`, `Not provided`, or `Assumption` instead of inventing it.
- Separate confirmed facts from assumptions and open questions.
- Do not proceed to downstream synthesis when a required upstream artifact or decision is missing.

### 0.3 Output Rules

- Keep output structured with headings and bullets.
- Make findings, gaps, risks, and blockers explicit.
- Tie recommendations to evidence from the provided artifact, `specs-refiniment/<feature-name>/<file.md>` workspace, or user context.
- Include role ownership when the output creates follow-up work for BA, QA, Dev, PM, or Delivery.

### 0.4 Artifact Routing

- When writing or updating files, place PM, BA, QA, Delivery, discovery, planning, refinement, and readiness artifacts at `specs-refiniment/<feature-name>/<file.md>`.
- Use the path pattern `specs-refiniment/<feature-name>/<file.md>`; choose a stable feature slug when known, otherwise use `tbd-<short-topic>` for `<feature-name>`.
- Do not write this skill's output into `specs/`; that folder is reserved for developer implementation SDD artifacts.
- If the user explicitly asks to convert a refined artifact into developer implementation work, hand off to `$ai-sdlc-sdd`.

## References

- Read `references/qa-plan-template.md` when the task needs the detailed structure, checklist, or examples for this skill.

## Purpose

Produce QA acceptance, regression, manual-check, and signoff evidence for AI SDLC changes. Return the QA plan as an internal refinement artifact and place it under `specs-refiniment/<feature-name>/<file.md>` when writing files.

## Inputs

- Read the relevant requirements, stories, delivery spec, existing `specs-refiniment/<feature-name>/<file.md>` QA notes, test cases, and release context.
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
8. Write or update the QA artifact under `specs-refiniment/<feature-name>/<file.md>` when file output is requested.
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
