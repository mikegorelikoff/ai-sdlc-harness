---
name: ai-sdlc-release-slicing-and-backlog-readiness-review
description: Use after backlog decomposition to define prioritization, MVP and release slices, sequencing, readiness, traceability, and JIRA-ready outputs, then score backlog quality for planning and estimation.
---

# ai-sdlc-release-slicing-and-backlog-readiness-review: Release Slicing And Backlog Readiness Review

> Internal AI SDLC skill, not client-facing by default.
> Every rule below is important to follow. None of it can be skipped.
> Before producing the final artifact, confirm required inputs, target audience, missing facts, output format, and constraints when they are unclear.
> Do not invent missing information. Ask concise clarification questions when required inputs are absent.

## 0. Skill Card

- Skill name: `ai-sdlc-release-slicing-and-backlog-readiness-review`
- Primary audience: PM
- Supporting audience: Delivery, BA, QA, Dev Lead
- Audience tags: PM, BA, QA, Dev
- SDLC stage: Release planning / backlog readiness
- Purpose: Run the final planning gate on the backlog package before estimation, roadmap slicing, or execution planning.
- Output: MVP/release slices, sequencing, readiness score, and planning risks

### 0.1 Required Inputs

- Decomposed backlog, features, stories, or task list.
- Priority, MVP, launch, or sequencing constraints.
- Known dependencies and readiness risks.

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

- Read `references/release-and-readiness-structures.md` when the task needs the detailed structure, checklist, or examples for this skill.

## Purpose

Run the final planning gate on the backlog package before estimation, roadmap slicing, or execution planning.

## Use When

- The backlog structure and cross-functional tasks already exist.
- The team needs prioritization, slicing, sequencing, and readiness guidance.

## Do Not Use When

- The backlog is still missing core epics, stories, or task linkage.
- The planning gap review or decomposition work is incomplete.

## Workflow

1. Review dependencies, risks, priorities, and scope boundaries.
2. Separate MVP, stretch, post-MVP, and out-of-scope work.
3. Create release slices, sequencing, milestones, and spike needs.
4. Assess estimation readiness, Definition of Ready, and Definition of Done.
5. Build traceability from business goals to backlog items and provide a JIRA-ready view.
6. Assign a final backlog readiness score and state what blocks planning.

## Review Rules

- Be strict.
- Push back if MVP is overloaded.
- Push back if priorities ignore business value, risk reduction, or dependencies.
- Flag items that are too large to estimate or too vague to schedule.
- Keep blockers, open questions, and launch risks explicit.

## Structures

Use `references/release-and-readiness-structures.md`.

## Completion Criteria

- MVP and release slices are coherent.
- Sequencing is logical even without explicit sprint dates.
- Traceability and readiness gaps are visible.
- The package is strong enough for backlog refinement and planning.
