---
name: ai-sdlc-delivery-handoff-review
description: Use after story and spec synthesis to perform a strict delivery handoff review, identify remaining gaps or contradictions, and score readiness for engineering and cross-functional execution.
---

# Delivery Handoff Review

## Purpose

Run the final quality gate on the delivery package before it is treated as ready for implementation planning or handoff.

## Use When

- Stories and spec are complete enough to review as a package.
- The team needs an explicit judgment on readiness and remaining risk.

## Do Not Use When

- The delivery gap review or decomposition work is still incomplete.
- The package does not yet contain both stories and a structured spec.

## Workflow

1. Compare the input package, stories, and spec for consistency.
2. Check coverage of actors, workflows, edge cases, dependencies, business rules, and open questions.
3. Identify what still blocks confident delivery handoff.
4. Assign a readiness score and explain the reasons.
5. State what must be clarified next before implementation starts.

## Review Rules

- Be strict.
- Block handoff if stories and spec contradict each other.
- Block handoff if acceptance criteria are not testable.
- Block handoff if critical dependencies or decisions remain hidden.
- Distinguish between non-blocking gaps and true delivery blockers.

## Checklist

Use `references/handoff-checklist.md`.

## Completion Criteria

- The review identifies concrete strengths and blockers.
- The readiness score is justified.
- Remaining questions are actionable.
- The recommendation is clear enough for delivery planning.
