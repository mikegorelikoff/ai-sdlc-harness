---
name: ai-sdlc-backlog-decomposition-and-task-planning
description: Use when goals, capabilities, and epics are defined and you need to decompose them into features, user stories, acceptance summaries, and cross-functional delivery tasks.
---

# ai-sdlc-backlog-decomposition-and-task-planning: Backlog Decomposition And Task Planning

> Internal AI SDLC skill, not client-facing by default.
> Every rule below is important to follow. None of it can be skipped.
> Before producing the final artifact, confirm required inputs, target audience, missing facts, output format, and constraints when they are unclear.
> Do not invent missing information. Ask concise clarification questions when required inputs are absent.

## 0. Skill Card

- Skill name: `ai-sdlc-backlog-decomposition-and-task-planning`
- Primary audience: PM
- Supporting audience: BA, QA, Dev Lead, Delivery
- Audience tags: PM, BA, QA, Dev
- SDLC stage: Backlog decomposition
- Purpose: Convert planning structure into a delivery-oriented backlog with cross-functional work represented explicitly.
- Output: Features, user stories, acceptance summaries, and cross-functional delivery tasks

### 0.1 Required Inputs

- Defined goals, capabilities, and epics.
- MVP or release boundary.
- Known dependencies, constraints, and cross-functional needs.

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

- Read `references/backlog-structures.md` when the task needs the detailed structure, checklist, or examples for this skill.

## Purpose

Convert planning structure into a delivery-oriented backlog with cross-functional work represented explicitly.

## Use When

- Goals, roles, capabilities, and epics are mature enough to decompose.
- The team needs features, stories, and task breakdowns rather than only planning themes.

## Do Not Use When

- The planning structure is still unstable.
- The task only needs high-level epic framing.

## Workflow

1. Break epics into features.
2. Break features into user stories with business value and acceptance summaries.
3. Add technical, QA, design, analytics, operations, and compliance tasks where relevant.
4. Capture dependencies, assumptions, open questions, and estimation-readiness signals.
5. Keep items small enough to estimate and sequence.

## Decomposition Rules

- Stories must have a concrete actor and outcome.
- Features must be testable at a high level.
- Do not hide complex backend, integration, QA, analytics, or operational work inside a single story.
- Split items that are too large or mix unrelated workflows.
- Keep cross-functional tasks linked to a feature, story, or planning need.

## Structures

Use `references/backlog-structures.md`.

## Completion Criteria

- Features and stories are specific enough for refinement.
- Cross-functional tasks are visible instead of being implicit.
- Oversized or non-estimable items are flagged for splitting or spikes.
