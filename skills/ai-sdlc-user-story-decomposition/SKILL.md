---
name: ai-sdlc-user-story-decomposition
description: Use when the delivery gap review is complete and you need to convert a clarified initiative package into epics, user stories, acceptance criteria, scenario coverage, and priority signals tied to business value.
---

# User Story Decomposition

## Purpose

Turn a clarified delivery package into implementable, actor-based user stories with acceptance logic and scenario coverage.

## Use When

- The upstream package is clear enough to decompose.
- The user needs stories, acceptance criteria, and scenario coverage for delivery planning.

## Do Not Use When

- The input package still has blocking gaps.
- The task only needs a high-level product narrative rather than delivery artifacts.

## Workflow

1. Identify actors, goals, and outcomes.
2. Group related work into epics or capability areas when useful.
3. Write stories in actor-value form.
4. Add acceptance criteria and negative or edge scenarios where they materially affect delivery.
5. Capture dependencies, assumptions, open questions, and priority for each story cluster.

## Story Rules

- Every story must name a concrete actor.
- Every story must state the user or business outcome it supports.
- Do not accept stories that are only UI elements or technical tasks without user/business value.
- Add failure, edge, and exception scenarios where omission would create delivery risk.
- Keep priorities tied to MVP scope, not personal preference.

## Structures

Use `references/story-structures.md`.

## Completion Criteria

- Stories cover the main actor journeys.
- Acceptance criteria are testable.
- Dependencies and open questions are visible.
- The story set is consistent with MVP scope and business goals.
