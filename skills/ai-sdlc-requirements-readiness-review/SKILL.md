---
name: ai-sdlc-requirements-readiness-review
description: Use after PRFAQ and BRD creation to run a strict final quality review, identify gaps or contradictions, and assign a readiness score before design or development starts.
---

# ai-sdlc-requirements-readiness-review: Requirements Readiness Review

> Internal AI SDLC skill, not client-facing by default.
> Every rule below is important to follow. None of it can be skipped.
> Before producing the final artifact, confirm required inputs, target audience, missing facts, output format, and constraints when they are unclear.
> Do not invent missing information. Ask concise clarification questions when required inputs are absent.

## 0. Skill Card

- Skill name: `ai-sdlc-requirements-readiness-review`
- Primary audience: BA
- Supporting audience: PM, Delivery, QA
- Audience tags: BA, PM, QA
- SDLC stage: Requirements quality gate
- Purpose: Run the final gate on a PRFAQ package and business requirements document before they are treated as ready for alignment or handoff.
- Output: Readiness score, blockers, contradictions, and required clarifications before design or development

### 0.1 Required Inputs

- PRFAQ, BRD, PRD, or equivalent requirements artifact.
- Target delivery context or initiative goal.
- Known acceptance, scope, or stakeholder constraints.

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

- Read `references/readiness-checklist.md` when the task needs the detailed structure, checklist, or examples for this skill.

## Purpose

Run the final gate on a PRFAQ package and business requirements document before they are treated as ready for alignment or handoff.

## Use When

- Discovery and synthesis are complete enough to review as a package.
- The user needs an explicit judgment about quality, risk, and remaining gaps.

## Do Not Use When

- Core discovery is still missing.
- The PRFAQ or BRD has not been created yet.

## Workflow

1. Review the package against the quality checklist.
2. Flag unclear customer value, weak business case, oversized MVP, or non-testable requirements directly.
3. Identify contradictions, missing dependencies, and unresolved questions.
4. Assign a readiness score from 1 to 10.
5. Explain what is strong, what is weak, what must be clarified next, and what should happen before design or development.

## Review Rules

- Be strict.
- Do not let assumptions pass as facts.
- Do not allow feature lists without customer pain or business value.
- Do not allow PRFAQ finalization if target customer, problem, alternative, value proposition, business objective, MVP, success metrics, risks, or dependencies remain too unclear.

## Checklist

Use `references/readiness-checklist.md`.

## Completion Criteria

- Score is justified.
- Strengths and weaknesses are specific.
- Remaining open questions are actionable.
- The review makes a clear recommendation about readiness for next steps.
