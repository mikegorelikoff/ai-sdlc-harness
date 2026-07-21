---
title: QA engineer guide
description: Design independent, risk-based verification for AI-generated work.
---

# Quality assurance (QA) engineer guide

## Why you should care

Artificial intelligence (AI) can generate code and tests that share the same
mistaken assumption. QA adds
independent evidence that the intended behavior, failure paths, and regression
boundary were actually exercised.

## Where you participate

Review requirements for testability, define strategy and data, synthesize test
cases, validate acceptance and negative paths, assess regression, and provide a
release-readiness recommendation.

## Inputs and outputs

Inputs: actors, workflows, business rules, requirements, risks, environments,
and changed surface. Outputs: strategy, cases, suites, test data, environment
needs, results, defects, traceability, and residual-risk recommendation.

## Decisions you own

Own QA scope and quality-evidence recommendations within local policy. The
product owner accepts outcomes; engineering owns implementation; a release owner
accepts release risk.

## Common mistakes

- Testing only acceptance happy paths.
- Accepting a test name without inspecting assertion and execution output.
- Marking inaccessible performance, accessibility, security, or environment
  coverage as passed.
- Reusing stale evidence after code or requirements change.

## Example workflow

Run requirements gap review, define risk-based strategy, derive cases before
implementation, execute unit/integration/end-to-end and applicable security,
performance, accessibility, recovery, and regression checks, then build the
requirements-to-test matrix and record blocked coverage.

## Review checklist

- Every acceptance criterion has positive and relevant negative coverage.
- Applicable non-functional requirements have measurable evidence.
- Test data and environment prerequisites are explicit.
- Failures are reproducible and not hidden by retries.
- Results identify the exact revision and command.
- Skipped coverage has an owner, reason, and release decision.
