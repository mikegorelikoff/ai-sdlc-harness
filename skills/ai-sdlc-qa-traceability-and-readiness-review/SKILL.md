---
name: ai-sdlc-qa-traceability-and-readiness-review
description: Use after QA strategy and test-case synthesis to build the requirements-to-test traceability matrix, identify missing coverage and test blockers, and score readiness for QA execution.
---

# ai-sdlc-qa-traceability-and-readiness-review: QA Traceability And Readiness Review

> Internal AI SDLC skill, not client-facing by default.
> Every rule below is important to follow. None of it can be skipped.
> Before producing the final artifact, confirm required inputs, target audience, missing facts, output format, and constraints when they are unclear.
> Do not invent missing information. Ask concise clarification questions when required inputs are absent.

## 0. Skill Card

- Skill name: `ai-sdlc-qa-traceability-and-readiness-review`
- Primary audience: QA
- Supporting audience: BA, PM, Delivery, Dev
- Audience tags: QA, BA, PM, Dev
- SDLC stage: QA execution readiness gate
- Purpose: Run the final QA gate on the generated test pack before execution starts.
- Output: Requirements-to-test traceability matrix, coverage gaps, blockers, and readiness score

### 0.1 Required Inputs

- Requirements, QA strategy, and detailed test cases.
- Known release scope and execution constraints.
- Evidence of requirement-to-test coverage.

### 0.2 Clarification Rules

- Ask concise questions before finalizing when role, artifact, requirements, scope, audience, or constraints are unclear.
- If optional information is missing, mark it as `TBD`, `Not provided`, or `Assumption` instead of inventing it.
- Separate confirmed facts from assumptions and open questions.
- Do not proceed to downstream synthesis when a required upstream artifact or decision is missing.

### 0.3 Output Rules

- Keep output structured with headings and bullets.
- Make findings, gaps, risks, and blockers explicit.
- Tie recommendations to evidence from the provided artifact, `specs-refiniment/<feature-name>/<file.md>` workspace, stakeholder context, or user-provided source material.
- Include role ownership when the output creates follow-up work for BA, QA, Dev, PM, or Delivery.

### 0.4 Artifact Routing

- When writing or updating files, place PM, BA, QA, Delivery, discovery, planning, refinement, and readiness artifacts at `specs-refiniment/<feature-name>/<file.md>`.
- Use the path pattern `specs-refiniment/<feature-name>/<file.md>`; choose a stable feature slug when known, otherwise use `tbd-<short-topic>` for `<feature-name>`.
- Do not write this skill's output into `specs/`; that folder is reserved for developer implementation SDD artifacts.
- If the user explicitly asks to convert a refined artifact into developer implementation work, hand off to `$ai-sdlc-sdd`.

## References

- Read `references/qa-readiness-checklist.md` when the task needs the detailed structure, checklist, or examples for this skill.

## Purpose

Run the final QA gate on the generated test pack before execution starts.

## Use When

- Test scope, strategy, and cases exist as a package.
- The team needs a clear statement of readiness, missing coverage, and blockers.

## Do Not Use When

- The QA gap review or test-case synthesis is still incomplete.
- Detailed cases do not yet exist.

## Workflow

1. Build the requirements-to-test traceability matrix.
2. Identify uncovered, partially covered, blocked, or unclear requirements.
3. Compile assumptions, open questions, environment blockers, and testing risks.
4. Review smoke, regression, and UAT coverage for launch fitness.
5. Assign a QA readiness score and explain what must be clarified before execution.

## Review Rules

- Be strict.
- Call out non-testable requirements directly.
- Call out duplicated or low-value tests if they dilute coverage quality.
- Distinguish between blocking and non-blocking gaps.
- Keep launch blockers explicit.

## Checklist

Use `references/qa-readiness-checklist.md`.

## Completion Criteria

- Traceability matrix is complete enough to expose coverage gaps.
- Missing or blocked coverage is visible.
- Risks and open questions are actionable.
- The readiness score is justified and useful for planning.
