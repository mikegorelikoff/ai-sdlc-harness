---
name: ai-sdlc-delivery-package-gap-review
description: Use when a PRFAQ, BRD, or equivalent discovery package exists and you need to review it for delivery gaps, contradictions, missing business rules, and insufficient implementation handoff detail before writing user stories or specs.
---

# ai-sdlc-delivery-package-gap-review: Delivery Package Gap Review

> Internal AI SDLC skill, not client-facing by default.
> Every rule below is important to follow. None of it can be skipped.
> Before producing the final artifact, confirm required inputs, target audience, missing facts, output format, and constraints when they are unclear.
> Do not invent missing information. Ask concise clarification questions when required inputs are absent.

## 0. Skill Card

- Skill name: `ai-sdlc-delivery-package-gap-review`
- Primary audience: BA
- Supporting audience: PM, Delivery, Dev Lead, QA
- Audience tags: BA, PM, QA, Dev
- SDLC stage: Pre-delivery gap review
- Purpose: Review an upstream discovery package and decide whether it is specific enough to decompose into delivery artifacts.
- Output: Delivery gaps, contradictions, missing business rules, and handoff blockers

### 0.1 Required Inputs

- PRFAQ, BRD, PRD, discovery package, or equivalent artifact.
- Expected delivery outcome and target users.
- Known business rules, workflows, and constraints.

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

- Read `references/gap-review-framework.md` when the task needs the detailed structure, checklist, or examples for this skill.

## Purpose

Review an upstream discovery package and decide whether it is specific enough to decompose into delivery artifacts.

## Use When

- The user already has a PRFAQ, BRD, discovery notes, or similar package.
- The next task is user stories, acceptance criteria, or a delivery specification.
- There is a risk that the input package is strong narratively but still weak operationally.

## Do Not Use When

- No meaningful discovery package exists yet.
- The task is to do original customer/problem discovery rather than downstream delivery clarification.

## Workflow

1. Inspect the input package and identify what is present versus missing.
2. Separate facts from assumptions and open questions.
3. Identify missing delivery-critical detail such as business rules, role behavior, failure paths, dependencies, and scope boundaries.
4. Ask only the clarifying questions needed, in small batches.
5. Do not move to story decomposition until the minimum delivery bar is met.

## Review Rules

- Do not assume a polished PRFAQ equals delivery readiness.
- Call out contradictions between customer narrative, MVP, metrics, and proposed scope.
- Flag missing ownership, unresolved dependencies, and ambiguous workflows directly.
- Capture what can remain open versus what blocks decomposition.

## Framework

Use `references/gap-review-framework.md`.

## Completion Criteria

- Core actors and outcomes are clear.
- Delivery blockers are identified and either clarified or explicitly left open with impact.
- The package is specific enough to support story decomposition without fiction.
