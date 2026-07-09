---
name: ai-sdlc-goal-capability-and-epic-mapping
description: Use when planning inputs are clear enough and you need to map business goals, roles, capabilities, and outcome-oriented epics before detailed backlog decomposition.
---

# ai-sdlc-goal-capability-and-epic-mapping: Goal Capability And Epic Mapping

> Internal AI SDLC skill, not client-facing by default.
> Every rule below is important to follow. None of it can be skipped.
> Before producing the final artifact, confirm required inputs, target audience, missing facts, output format, and constraints when they are unclear.
> Do not invent missing information. Ask concise clarification questions when required inputs are absent.

## 0. Skill Card

- Skill name: `ai-sdlc-goal-capability-and-epic-mapping`
- Primary audience: PM
- Supporting audience: BA, Delivery
- Audience tags: PM, BA
- SDLC stage: Planning architecture
- Purpose: Turn a clarified initiative package into a structured planning model of goals, roles, capabilities, and epics.
- Output: Goal-to-capability map and outcome-oriented epics

### 0.1 Required Inputs

- Clear business goals and target users.
- Validated initiative scope or PRFAQ/BRD input.
- Known outcomes, constraints, and priority signals.

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

- Read `references/mapping-structures.md` when the task needs the detailed structure, checklist, or examples for this skill.

## Purpose

Turn a clarified initiative package into a structured planning model of goals, roles, capabilities, and epics.

## Use When

- The planning gap review is complete enough to proceed.
- The team needs structured planning layers before writing features and stories.

## Do Not Use When

- Business outcomes or MVP boundaries are still unclear.
- The task only needs a lightweight feature list.

## Workflow

1. Define business goals and success criteria.
2. Identify users, roles, and actors with their planning-relevant needs.
3. Map the main product capabilities.
4. Group capabilities into outcome-oriented epics.
5. Capture dependencies, risks, and open questions at each level.

## Mapping Rules

- Every goal should connect to at least one capability or required operational/compliance need.
- Every capability should support a user need, business goal, or delivery necessity.
- Every epic should have a clear outcome and be decomposable into smaller units.
- Do not allow miscellaneous or generic buckets that hide scope.

## Structures

Use `references/mapping-structures.md`.

## Completion Criteria

- Goals, roles, capabilities, and epics are explicit.
- The planning structure supports downstream feature/story decomposition.
- Weakly justified or over-broad planning areas are challenged and corrected.
