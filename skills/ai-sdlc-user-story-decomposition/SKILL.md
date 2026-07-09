---
name: ai-sdlc-user-story-decomposition
description: Use when the delivery gap review is complete and you need to convert a clarified initiative package into epics, user stories, acceptance criteria, scenario coverage, and priority signals tied to business value.
---

# ai-sdlc-user-story-decomposition: User Story Decomposition

> Internal AI SDLC skill, not client-facing by default.
> Every rule below is important to follow. None of it can be skipped.
> Before producing the final artifact, confirm required inputs, target audience, missing facts, output format, and constraints when they are unclear.
> Do not invent missing information. Ask concise clarification questions when required inputs are absent.

## 0. Skill Card

- Skill name: `ai-sdlc-user-story-decomposition`
- Primary audience: BA
- Supporting audience: PM, QA, Dev
- Audience tags: BA, PM, QA, Dev
- SDLC stage: Story decomposition
- Purpose: Turn a clarified delivery package into implementable, actor-based user stories with acceptance logic and scenario coverage.
- Output: Epics, user stories, acceptance criteria, scenario coverage, and priority signals

### 0.1 Required Inputs

- Clarified delivery package or gap-reviewed requirements.
- Actors, workflows, and business outcomes.
- MVP, priority, or release constraints.

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

- Read `references/story-structures.md` when the task needs the detailed structure, checklist, or examples for this skill.

## Purpose

Turn a clarified delivery package into implementable, actor-based user stories with acceptance logic and scenario coverage.

## Use When

- The upstream package is clear enough to decompose.
- The user needs stories, acceptance criteria, and scenario coverage for delivery planning.

## Do Not Use When

- The input package still has blocking gaps.
- The task only needs a high-level product narrative rather than delivery artifacts.

## Workflow

1. Identify actors, goals, and outcomes.
2. Group related work into epics or capability areas when useful.
3. Write stories in actor-value form.
4. Add acceptance criteria and negative or edge scenarios where they materially affect delivery.
5. Capture dependencies, assumptions, open questions, and priority for each story cluster.

## Story Rules

- Every story must name a concrete actor.
- Every story must state the user or business outcome it supports.
- Do not accept stories that are only UI elements or technical tasks without user/business value.
- Add failure, edge, and exception scenarios where omission would create delivery risk.
- Keep priorities tied to MVP scope, not personal preference.

## Structures

Use `references/story-structures.md`.

## Completion Criteria

- Stories cover the main actor journeys.
- Acceptance criteria are testable.
- Dependencies and open questions are visible.
- The story set is consistent with MVP scope and business goals.
