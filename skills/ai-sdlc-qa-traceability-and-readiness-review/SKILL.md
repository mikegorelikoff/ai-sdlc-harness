---
name: ai-sdlc-qa-traceability-and-readiness-review
description: Use after QA strategy and test-case synthesis to build the requirements-to-test traceability matrix, identify missing coverage and test blockers, and score readiness for QA execution.
---

# QA Traceability And Readiness Review

## Purpose

Run the final QA gate on the generated test pack before execution starts.

## Use When

- Test scope, strategy, and cases exist as a package.
- The team needs a clear statement of readiness, missing coverage, and blockers.

## Do Not Use When

- The QA gap review or test-case synthesis is still incomplete.
- Detailed cases do not yet exist.

## Workflow

1. Build the requirements-to-test traceability matrix.
2. Identify uncovered, partially covered, blocked, or unclear requirements.
3. Compile assumptions, open questions, environment blockers, and testing risks.
4. Review smoke, regression, and UAT coverage for launch fitness.
5. Assign a QA readiness score and explain what must be clarified before execution.

## Review Rules

- Be strict.
- Call out non-testable requirements directly.
- Call out duplicated or low-value tests if they dilute coverage quality.
- Distinguish between blocking and non-blocking gaps.
- Keep launch blockers explicit.

## Checklist

Use `references/qa-readiness-checklist.md`.

## Completion Criteria

- Traceability matrix is complete enough to expose coverage gaps.
- Missing or blocked coverage is visible.
- Risks and open questions are actionable.
- The readiness score is justified and useful for planning.
