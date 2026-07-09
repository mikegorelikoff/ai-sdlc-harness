---
name: ai-sdlc-test-scope-and-strategy-design
description: Use when requirements are testable enough and you need to define QA scope, coverage priorities, test strategy, suite intent, test data needs, environment dependencies, and risk-based execution focus.
---

# ai-sdlc-test-scope-and-strategy-design: Test Scope And Strategy Design

> Internal AI SDLC skill, not client-facing by default.
> Every rule below is important to follow. None of it can be skipped.
> Before producing the final artifact, confirm required inputs, target audience, missing facts, output format, and constraints when they are unclear.
> Do not invent missing information. Ask concise clarification questions when required inputs are absent.

## 0. Skill Card

- Skill name: `ai-sdlc-test-scope-and-strategy-design`
- Primary audience: QA
- Supporting audience: BA, PM, Dev Lead
- Audience tags: QA, BA, PM, Dev
- SDLC stage: QA strategy
- Purpose: Turn a clarified delivery package into a structured QA scope and strategy.
- Output: QA scope, coverage priorities, suite strategy, data needs, and risk-based execution plan

### 0.1 Required Inputs

- Testable requirements or delivery specification.
- Known risks, roles, workflows, and integrations.
- Release, environment, data, or dependency constraints.

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

- Read `references/test-strategy-structures.md` when the task needs the detailed structure, checklist, or examples for this skill.

## Purpose

Turn a clarified delivery package into a structured QA scope and strategy.

## Use When

- The requirements gap review is complete enough to proceed.
- The team needs a disciplined test scope and QA approach before detailed test cases.

## Do Not Use When

- Blocking requirements gaps remain unresolved.
- The task only needs raw test cases without any strategy layer.

## Workflow

1. Define in-scope and out-of-scope areas.
2. Identify critical roles, flows, integrations, and business rules.
3. Prioritize test types and coverage based on launch risk.
4. Define smoke, regression, and UAT suite intent.
5. Capture test data, environment, dependency, and defect severity expectations.

## Strategy Rules

- Do not mark everything critical.
- Tie priorities to business risk, launch impact, compliance, revenue, or operational exposure.
- Keep assumptions, environment dependencies, and unknown thresholds explicit.
- Include only relevant test types for the product surface involved.

## Structures

Use `references/test-strategy-structures.md`.

## Completion Criteria

- Scope boundaries are explicit.
- High-risk areas and critical paths are prioritized.
- Required suites, data, and environment needs are identified.
- The QA plan is detailed enough to drive case synthesis.
