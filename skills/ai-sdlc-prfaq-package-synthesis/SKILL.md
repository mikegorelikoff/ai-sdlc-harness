---
name: ai-sdlc-prfaq-package-synthesis
description: Use when working-backwards discovery is complete and you need to synthesize a PRFAQ, FAQ package, and business requirements document tied to business value, scenarios, and testable acceptance logic.
---

# PRFAQ Package Synthesis

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
