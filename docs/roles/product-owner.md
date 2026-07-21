---
title: Product owner guide
description: Refine, order, and accept backlog outcomes within delegated product authority.
---

# Product owner guide

This guide uses responsibility assignment matrix (RACI) and minimum viable product (MVP).

## Why you should care

The harness can connect intended value to stories, tasks, tests, and acceptance
evidence. Your review keeps that trace useful for decisions rather than creating
documents for their own sake.

## Role convention

Here, Product Manager owns broader customer strategy and outcome trade-offs.
Product Owner is the locally delegated day-to-day authority for backlog clarity,
ordering, and increment acceptance. A team may combine the roles, but its RACI
must name one accountable person for each gate. This convention is not a claim
that every organization uses the Scrum definition.

## Where you participate

Review requirements readiness, refine and order stories, approve the minimum
viable product slice within delegation, reject ambiguity, inspect changed scope,
and accept or reject the delivered outcome.

## Inputs and outputs

Inputs: product goal, actors, rules, acceptance criteria, dependencies, risks,
and delivery evidence. Outputs: ordered ready backlog, scope decisions, accepted
criteria, release-slice decision, and post-implementation accept/reject record.

## Decisions you own

Own backlog ordering, day-to-day story readiness, and product acceptance only
within explicit delegation. Escalate strategy, budget, legal, security, or
cross-product trade-offs outside that authority.

## Common mistakes

- Accepting a story that has a solution but no user value or observable result.
- Allowing priority numbers without an organization rubric and rationale.
- Treating code completion as product acceptance.
- Ignoring a changed requirement after downstream evidence exists.

## Example workflow

Run backlog gap review; reject one ambiguous story; approve actor, value,
Given/When/Then criteria, dependencies, and ordering; review the release slice;
after implementation query requirement → task → code/commit → test/evidence;
observe the behavior; then [record product acceptance](../how-to/record-product-acceptance.md)
as a revision-bound canonical decision-log row.

## Review checklist

- Each story has actor, value, observable acceptance, exclusions, and owner.
- Priority has criteria, confidence, rationale, and decision reference.
- Dependencies and MVP exclusions are visible.
- Changed intent reopened affected artifacts and tests.
- Product behavior was demonstrated on the accepted revision.
- Acceptance status links to evidence and an accountable human decision.
