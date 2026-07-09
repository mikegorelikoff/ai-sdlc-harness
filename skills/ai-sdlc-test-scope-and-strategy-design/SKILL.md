---
name: ai-sdlc-test-scope-and-strategy-design
description: Use when requirements are testable enough and you need to define QA scope, coverage priorities, test strategy, suite intent, test data needs, environment dependencies, and risk-based execution focus.
---

# Test Scope And Strategy Design

## Purpose

Turn a clarified delivery package into a structured QA scope and strategy.

## Use When

- The requirements gap review is complete enough to proceed.
- The team needs a disciplined test scope and QA approach before detailed test cases.

## Do Not Use When

- Blocking requirements gaps remain unresolved.
- The task only needs raw test cases without any strategy layer.

## Workflow

1. Define in-scope and out-of-scope areas.
2. Identify critical roles, flows, integrations, and business rules.
3. Prioritize test types and coverage based on launch risk.
4. Define smoke, regression, and UAT suite intent.
5. Capture test data, environment, dependency, and defect severity expectations.

## Strategy Rules

- Do not mark everything critical.
- Tie priorities to business risk, launch impact, compliance, revenue, or operational exposure.
- Keep assumptions, environment dependencies, and unknown thresholds explicit.
- Include only relevant test types for the product surface involved.

## Structures

Use `references/test-strategy-structures.md`.

## Completion Criteria

- Scope boundaries are explicit.
- High-risk areas and critical paths are prioritized.
- Required suites, data, and environment needs are identified.
- The QA plan is detailed enough to drive case synthesis.
