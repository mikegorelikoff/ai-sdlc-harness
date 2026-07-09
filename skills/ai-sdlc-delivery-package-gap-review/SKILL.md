---
name: ai-sdlc-delivery-package-gap-review
description: Use when a PRFAQ, BRD, or equivalent discovery package exists and you need to review it for delivery gaps, contradictions, missing business rules, and insufficient implementation handoff detail before writing user stories or specs.
---

# Delivery Package Gap Review

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
