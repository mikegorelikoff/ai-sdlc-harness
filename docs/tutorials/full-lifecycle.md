---
title: Run the full lifecycle
description: Follow a product change from customer problem through backlog, engineering delivery, QA readiness, release evidence, and learning.
---

Use full lifecycle work when the problem is still ambiguous, several roles must align, or the change carries meaningful product or operational risk.

## Discover and work backwards

Start with `ai-sdlc-working-backwards-discovery --full-flow`. Clarify the customer, problem, promised outcome, business value, constraints, success measures, and disconfirming evidence. Synthesize the result into a PRFAQ/BRD package and run requirements readiness before planning.

## Shape delivery

Map goals to capabilities and outcome-oriented epics. Review the package for backlog gaps, decompose stories, define acceptance summaries, slice releases, and check readiness. The output is not merely a list of tickets: every slice remains tied to customer and business outcomes.

## Design QA before implementation

Review requirements for testability. Define risk-based QA scope, environments, test data, suite intent, and explicit cases. Finish with traceability and readiness so missing rules become visible before code makes them expensive.

## Build from an SDD

Synthesize the implementation specification: requirements, design, cases, QA, tasks, decision log, and linked plans. Branch from the agreed base, implement one bounded task at a time, and keep plan status aligned with evidence.

## Validate, review, and release

Run focused validation, code review, and security testing where risk calls for it. Prepare auditable commits and preserve exact commands/outcomes. After release, analyze change impact and capture retrospective proposals without automatically changing policy.

At every boundary, the handoff contract answers four questions: what happened, what blocks progress, what must happen next, and what is optional.
