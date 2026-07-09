---
name: ai-sdlc-test-case-and-suite-synthesis
description: Use when QA scope and strategy are defined and you need to generate detailed, executable test cases plus smoke, regression, and user acceptance suites tied to requirements, roles, workflows, and risks.
---

# ai-sdlc-test-case-and-suite-synthesis: Test Case And Suite Synthesis

> Internal AI SDLC skill, not client-facing by default.
> Every rule below is important to follow. None of it can be skipped.
> Before producing the final artifact, confirm required inputs, target audience, missing facts, output format, and constraints when they are unclear.
> Do not invent missing information. Ask concise clarification questions when required inputs are absent.

## 0. Skill Card

- Skill name: `ai-sdlc-test-case-and-suite-synthesis`
- Primary audience: QA
- Supporting audience: BA, Dev, PM
- Audience tags: QA, BA, Dev, PM
- SDLC stage: Detailed test design
- Purpose: Generate the detailed QA artifacts used for structured execution.
- Output: Executable test cases plus smoke, regression, and UAT suites

### 0.1 Required Inputs

- QA scope and strategy.
- Requirements, workflows, roles, rules, and risks.
- Known test data, environment, and automation constraints.

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

- Read `references/test-case-structures.md` when the task needs the detailed structure, checklist, or examples for this skill.

## Purpose

Generate the detailed QA artifacts used for structured execution.

## Use When

- Requirements are clear enough to test.
- Scope and strategy decisions are already defined.
- The team needs detailed cases and explicit suite groupings.

## Do Not Use When

- Core expected behavior is still unclear.
- Strategy and risk priorities are not yet defined.

## Workflow

1. Create detailed cases only for relevant product surfaces.
2. Cover positive, negative, boundary, permission, workflow, and data conditions as applicable.
3. Add API, UI, integration, notification, state, security, privacy, and non-functional cases only where the system actually has those surfaces.
4. Produce separate smoke, regression, and UAT groupings.
5. Keep each case tied to a requirement, role, workflow, rule, or risk.

## Case Rules

- Steps must be explicit and executable.
- Expected results must be specific.
- Every case should be traceable to a requirement, workflow, role, or risk.
- Do not create generic cases that could apply to any system.
- Mark automation candidacy explicitly.

## Structures

Use `references/test-case-structures.md`.

## Completion Criteria

- Core business flows are covered.
- Negative and edge cases are included where material.
- Separate smoke, regression, and UAT suites exist.
- The cases are executable without hidden interpretation.
