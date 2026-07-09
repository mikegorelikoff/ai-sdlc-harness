---
name: ai-sdlc-delivery-spec-synthesis
description: Use when stories and clarified delivery context are ready and you need to produce a structured delivery specification that engineering and cross-functional teams can use for implementation planning and handoff.
---

# ai-sdlc-delivery-spec-synthesis: Delivery Spec Synthesis

> Internal AI SDLC skill, not client-facing by default.
> Every rule below is important to follow. None of it can be skipped.
> Before producing the final artifact, confirm required inputs, target audience, missing facts, output format, and constraints when they are unclear.
> Do not invent missing information. Ask concise clarification questions when required inputs are absent.

## 0. Skill Card

- Skill name: `ai-sdlc-delivery-spec-synthesis`
- Primary audience: BA
- Supporting audience: Dev, QA, PM, Delivery
- Audience tags: BA, Dev, QA, PM
- SDLC stage: Delivery specification
- Purpose: Convert the clarified package and story set into a structured delivery specification.
- Output: Structured delivery specification for engineering and cross-functional planning

### 0.1 Required Inputs

- Approved or clarified stories and delivery context.
- Business rules, acceptance criteria, and dependencies.
- Known implementation constraints or system boundaries.

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

- Read `references/spec-structures.md` when the task needs the detailed structure, checklist, or examples for this skill.

## Purpose

Convert the clarified package and story set into a structured delivery specification.

## Use When

- The gap review is complete.
- The story set is mature enough to serve as a reliable input.
- The team needs a delivery-oriented spec, not just narrative discovery.

## Do Not Use When

- Stories are still missing key actor behavior or acceptance logic.
- The team only needs a lightweight story list.

## Workflow

1. Start from the validated stories and upstream package.
2. Synthesize scope, roles, workflows, business rules, data needs, NFRs, and dependencies.
3. Keep assumptions and open questions explicit instead of smoothing them over.
4. Organize the document for delivery handoff rather than executive storytelling.

## Spec Rules

- Keep the spec consistent with the story set and MVP boundaries.
- Do not re-invent requirements that contradict the input package.
- Call out unresolved rules, missing owners, and dependency risks directly.
- Go deep enough for delivery planning, but do not drift into code design unless the business-level spec genuinely requires it.

## Structures

Use `references/spec-structures.md`.

## Completion Criteria

- Scope, actors, and workflows are explicit.
- Requirements are traceable to stories and business value.
- Dependencies, assumptions, and open questions are visible.
- The document is usable as a delivery handoff artifact.
