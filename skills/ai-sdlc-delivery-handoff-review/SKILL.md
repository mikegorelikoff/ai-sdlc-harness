---
name: ai-sdlc-delivery-handoff-review
description: Use after story and spec synthesis to perform a strict delivery handoff review, identify remaining gaps or contradictions, and score readiness for engineering and cross-functional execution.
---

# ai-sdlc-delivery-handoff-review: Delivery Handoff Review

> Internal AI SDLC skill, not client-facing by default.
> Every rule below is important to follow. None of it can be skipped.
> Before producing the final artifact, confirm required inputs, target audience, missing facts, output format, and constraints when they are unclear.
> Do not invent missing information. Ask concise clarification questions when required inputs are absent.

## 0. Skill Card

- Skill name: `ai-sdlc-delivery-handoff-review`
- Primary audience: Delivery
- Supporting audience: PM, BA, QA, Dev Lead
- Audience tags: PM, BA, QA, Dev
- SDLC stage: Engineering handoff quality gate
- Purpose: Run the final quality gate on the delivery package before it is treated as ready for implementation planning or handoff.
- Output: Handoff readiness score, remaining blockers, contradictions, and execution risks

### 0.1 Required Inputs

- Delivery spec, stories, acceptance criteria, and supporting context.
- Known constraints, dependencies, and ownership expectations.
- Target implementation or planning audience.

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

- Read `references/handoff-checklist.md` when the task needs the detailed structure, checklist, or examples for this skill.

## Purpose

Run the final quality gate on the delivery package before it is treated as ready for implementation planning or handoff.

## Use When

- Stories and spec are complete enough to review as a package.
- The team needs an explicit judgment on readiness and remaining risk.

## Do Not Use When

- The delivery gap review or decomposition work is still incomplete.
- The package does not yet contain both stories and a structured spec.

## Workflow

1. Compare the input package, stories, and spec for consistency.
2. Check coverage of actors, workflows, edge cases, dependencies, business rules, and open questions.
3. Identify what still blocks confident delivery handoff.
4. Assign a readiness score and explain the reasons.
5. State what must be clarified next before implementation starts.

## Review Rules

- Be strict.
- Block handoff if stories and spec contradict each other.
- Block handoff if acceptance criteria are not testable.
- Block handoff if critical dependencies or decisions remain hidden.
- Distinguish between non-blocking gaps and true delivery blockers.

## Checklist

Use `references/handoff-checklist.md`.

## Completion Criteria

- The review identifies concrete strengths and blockers.
- The readiness score is justified.
- Remaining questions are actionable.
- The recommendation is clear enough for delivery planning.
