---
title: Delivery manager guide
description: Coordinate dependencies, handoffs, decisions, and impediments without replacing role accountability.
---

# Delivery manager guide

This guide uses quality assurance (QA).

## Why you should care

The harness exposes blockers and artifact state across roles. Delivery
management turns that evidence into sequencing and escalation rather than
another reporting layer.

## Where you participate

Coordinate lifecycle entry, dependencies, owners, review gates, environment
readiness, change impact, release sequencing, and handoffs across product,
analysis, engineering, QA, security, and platform teams.

## Inputs and outputs

Inputs: goals, ready backlog, dependency graph, capacity, risks, state, and
blockers. Outputs: sequenced delivery plan, named owners, escalation decisions,
handoff status, and current readiness view.

## Decisions you own

Own coordination and delivery recommendations within local authority. Do not
approve product scope, technical correctness, quality, security, or release risk
for their accountable owners.

## Common mistakes

- Marking a stage complete to improve status reporting.
- Treating every project as needing the full 18-stage path.
- Hiding blocked or stale evidence behind a target date.
- Allowing two unnamed groups to be “accountable.”

## Example workflow

Use navigator and delivery graph to find the earliest missing producer; choose a
proportionate flow; name one accountable owner per gate; sequence dependencies;
track blocker age and decisions; after a change, reopen stale stages; hand off
only when evidence and owner acceptance are current.

## Review checklist

- Every gate has one named accountable owner.
- Dependencies and critical environments have owners and dates.
- Blockers identify the decision required and safest provisional behavior.
- Stale evidence is reopened instead of cosmetically refreshed.
- Ceremony and correction effort are measured.
- Handoff includes next action, expected artifact, and residual risk.
