---
name: ai-sdlc-prfaq-package-synthesis
description: Use when working-backwards discovery is complete and you need to synthesize a PRFAQ, FAQ package, and business requirements document tied to business value, scenarios, and testable acceptance logic.
---

# ai-sdlc-prfaq-package-synthesis: PRFAQ Package Synthesis

> Internal AI SDLC skill, not client-facing by default.
> Every rule below is important to follow. None of it can be skipped.
> Before producing the final artifact, confirm required inputs, target audience, missing facts, output format, and constraints when they are unclear.
> Do not invent missing information. Ask concise clarification questions when required inputs are absent.

## 0. Skill Card

- Skill name: `ai-sdlc-prfaq-package-synthesis`
- Primary audience: PM
- Supporting audience: BA, Delivery
- Audience tags: PM, BA
- SDLC stage: PRFAQ / business requirements synthesis
- Purpose: Convert validated discovery notes into a decision-ready PRFAQ package and business requirements document.
- Output: PRFAQ, FAQ package, and BRD-style requirements summary

### 0.1 Required Inputs

- Completed working-backwards discovery notes.
- Customer problem, target audience, and business value.
- Known MVP boundaries, risks, and success metrics.

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

- Read `references/prfaq-package-structures.md` when the task needs the detailed structure, checklist, or examples for this skill.

## Purpose

Convert validated discovery notes into a decision-ready PRFAQ package and business requirements document.

## Use When

- Discovery minimums are met: target customer, problem, alternative, value proposition, business objective, MVP, success metrics, risks, and dependencies are materially captured.
- The user needs a PRFAQ, FAQ package, and BRD from clarified discovery inputs.
- The initiative is ready for narrative synthesis, not more interviewing.

## Do Not Use When

- Core discovery is still missing or contradictions remain unresolved.
- The user only needs a lightweight summary rather than a full PRFAQ package.
- The task is delivery decomposition or backlog planning rather than product definition.

## Workflow

1. Start from validated discovery notes and separate facts, assumptions, decisions made, and open questions.
2. Draft the press release in customer-facing language tied to the value proposition and MVP.
3. Build the FAQ package to address stakeholder, customer, business, operational, and launch questions.
4. Produce the BRD with business goals, scope boundaries, scenarios, requirements, and acceptance logic.
5. Keep unresolved items explicit instead of smoothing them into confident language.
6. Hand off to `ai-sdlc-requirements-readiness-review` when the package is complete.

## Synthesis Rules

- Do not invent customer pain, metrics, or business case details missing from discovery.
- Keep MVP boundaries consistent across the press release, FAQ, and BRD.
- Tie requirements to business value, actor intent, and observable outcomes.
- Mark assumptions and open questions clearly wherever certainty is still limited.
- Use testable acceptance logic rather than generic feature labels.

## Structures

Use `references/prfaq-package-structures.md` for document sections and output shape.

## Completion Criteria

- Press release reflects the validated customer problem, value proposition, and MVP.
- FAQ package covers the main stakeholder and launch questions without hiding gaps.
- BRD links business goals, scope, scenarios, requirements, and acceptance criteria.
- Assumptions, dependencies, risks, and open questions remain visible.
- The package is ready for a strict readiness review.
