---
name: ai-sdlc-backlog-requirements-gap-review
description: Use when PRFAQ, BRD, PRD, product brief, workflow, or equivalent initiative artifacts exist and you need to review them for planning gaps, unclear scope, weak priorities, missing actors, and backlog-blocking ambiguity before decomposing work.
---

# ai-sdlc-backlog-requirements-gap-review: Backlog Requirements Gap Review

> Internal AI SDLC skill, not client-facing by default.
> Every rule below is important to follow. None of it can be skipped.
> Before producing the final artifact, confirm required inputs, target audience, missing facts, output format, and constraints when they are unclear.
> Do not invent missing information. Ask concise clarification questions when required inputs are absent.

## 0. Skill Card

- Skill name: `ai-sdlc-backlog-requirements-gap-review`
- Primary audience: BA
- Supporting audience: PM, Delivery, QA
- Audience tags: BA, PM, QA
- SDLC stage: Pre-backlog planning review
- Purpose: Review the incoming initiative package and determine whether it is specific enough to support backlog decomposition and release planning.
- Output: Backlog-blocking gaps, assumptions, open questions, and readiness decision

### 0.1 Required Inputs

- PRFAQ, BRD, PRD, product brief, workflow, or equivalent artifact.
- Planning goal or target backlog scope.
- Known priority, MVP, or release constraints.

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

- Read `references/planning-gap-review-framework.md` when the task needs the detailed structure, checklist, or examples for this skill.

## Purpose

Review the incoming initiative package and determine whether it is specific enough to support backlog decomposition and release planning.

## Use When

- The team already has discovery or requirements artifacts.
- The next task is planning epics, features, stories, and release slices.
- There is a risk that the initiative is well-described strategically but still weak for backlog planning.

## Do Not Use When

- No meaningful initiative artifacts exist yet.
- The task is original customer/problem discovery rather than planning decomposition.

## Workflow

1. Inspect the available artifacts and identify what is present versus missing.
2. Check whether goals, actors, scope, constraints, and delivery boundaries are clear enough to plan.
3. Identify missing business outcomes, unclear MVP boundaries, overloaded scope, absent priorities, and unresolved dependencies.
4. Ask only the clarifying questions needed, in small batches.
5. Do not move to decomposition until the minimum planning bar is met.

## Review Rules

- Do not treat a polished narrative as a ready backlog.
- Challenge vague phrases like "build the dashboard", "support integrations", or "MVP should include everything important".
- Separate facts from assumptions and open questions.
- Flag what blocks backlog planning versus what can remain open temporarily.

## Framework

Use `references/planning-gap-review-framework.md`.

## Completion Criteria

- Business goals, actors, and launch context are clear enough to plan against.
- MVP boundaries and major planning blockers are either clarified or explicitly marked.
- The package is specific enough to support capability and epic mapping without inventing intent.
