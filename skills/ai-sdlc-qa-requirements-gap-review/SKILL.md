---
name: ai-sdlc-qa-requirements-gap-review
description: Use when stories, specs, BRDs, APIs, workflows, or equivalent delivery artifacts exist and you need to review them for testability, missing business rules, unclear behavior, scope ambiguity, and QA blocking gaps before generating tests.
---

# ai-sdlc-qa-requirements-gap-review: QA Requirements Gap Review

> Internal AI SDLC skill, not client-facing by default.
> Every rule below is important to follow. None of it can be skipped.
> Before producing the final artifact, confirm required inputs, target audience, missing facts, output format, and constraints when they are unclear.
> Do not invent missing information. Ask concise clarification questions when required inputs are absent.

## 0. Skill Card

- Skill name: `ai-sdlc-qa-requirements-gap-review`
- Primary audience: QA
- Supporting audience: BA, PM, Dev
- Audience tags: QA, BA, PM, Dev
- SDLC stage: Pre-QA requirements review
- Purpose: Review the incoming delivery package and determine whether it is specific enough to support rigorous test design.
- Output: QA-blocking gaps, missing business rules, ambiguity, and testability risks

### 0.1 Required Inputs

- Stories, specs, BRDs, APIs, workflows, or equivalent delivery artifacts.
- Target product surface and user roles.
- Known acceptance criteria, rules, and release constraints.

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

- Read `references/qa-gap-review-framework.md` when the task needs the detailed structure, checklist, or examples for this skill.

## Purpose

Review the incoming delivery package and determine whether it is specific enough to support rigorous test design.

## Use When

- The team already has stories, specs, APIs, workflows, or equivalent artifacts.
- The next task is defining test scope, strategy, and detailed test cases.
- There is a risk that the package is good for product or delivery discussions but still weak for QA execution.

## Do Not Use When

- No meaningful requirements artifacts exist yet.
- The task is original product discovery rather than downstream QA design.

## Workflow

1. Inspect the available artifacts and identify what is present versus missing.
2. Check whether requirements are testable, specific, measurable, and role-aware.
3. Identify missing acceptance criteria, business rules, failure behavior, scope boundaries, permissions, dependencies, and data rules.
4. Ask only the clarifying questions needed, in small batches.
5. Do not move to strategy or test-case synthesis until the minimum QA bar is met.

## Review Rules

- Do not treat polished prose as proof of testability.
- Call out vague phrases like "it should work", "admin has access", or "system validates input" directly.
- Separate facts from assumptions and open questions.
- Flag what blocks QA execution versus what can be deferred.

## Framework

Use `references/qa-gap-review-framework.md`.

## Completion Criteria

- Core actors, flows, and expected outcomes are clear enough to test.
- Missing acceptance logic and business rules are either clarified or explicitly marked.
- The package is specific enough to support scope and test design without inventing behavior.
