---
name: ai-sdlc-requirements-readiness-review
description: Use after PRFAQ and BRD creation to run a strict final quality review, identify gaps or contradictions, and assign a readiness score before design or development starts.
---

# Requirements Readiness Review

## Purpose

Run the final gate on a PRFAQ package and business requirements document before they are treated as ready for alignment or handoff.

## Use When

- Discovery and synthesis are complete enough to review as a package.
- The user needs an explicit judgment about quality, risk, and remaining gaps.

## Do Not Use When

- Core discovery is still missing.
- The PRFAQ or BRD has not been created yet.

## Workflow

1. Review the package against the quality checklist.
2. Flag unclear customer value, weak business case, oversized MVP, or non-testable requirements directly.
3. Identify contradictions, missing dependencies, and unresolved questions.
4. Assign a readiness score from 1 to 10.
5. Explain what is strong, what is weak, what must be clarified next, and what should happen before design or development.

## Review Rules

- Be strict.
- Do not let assumptions pass as facts.
- Do not allow feature lists without customer pain or business value.
- Do not allow PRFAQ finalization if target customer, problem, alternative, value proposition, business objective, MVP, success metrics, risks, or dependencies remain too unclear.

## Checklist

Use `references/readiness-checklist.md`.

## Completion Criteria

- Score is justified.
- Strengths and weaknesses are specific.
- Remaining open questions are actionable.
- The review makes a clear recommendation about readiness for next steps.
