---
name: ai-sdlc-qa-requirements-gap-review
description: Use when stories, specs, BRDs, APIs, workflows, or equivalent delivery artifacts exist and you need to review them for testability, missing business rules, unclear behavior, scope ambiguity, and QA blocking gaps before generating tests.
---

# QA Requirements Gap Review

## Purpose

Review the incoming delivery package and determine whether it is specific enough to support rigorous test design.

## Use When

- The team already has stories, specs, APIs, workflows, or equivalent artifacts.
- The next task is defining test scope, strategy, and detailed test cases.
- There is a risk that the package is good for product or delivery discussions but still weak for QA execution.

## Do Not Use When

- No meaningful requirements artifacts exist yet.
- The task is original product discovery rather than downstream QA design.

## Workflow

1. Inspect the available artifacts and identify what is present versus missing.
2. Check whether requirements are testable, specific, measurable, and role-aware.
3. Identify missing acceptance criteria, business rules, failure behavior, scope boundaries, permissions, dependencies, and data rules.
4. Ask only the clarifying questions needed, in small batches.
5. Do not move to strategy or test-case synthesis until the minimum QA bar is met.

## Review Rules

- Do not treat polished prose as proof of testability.
- Call out vague phrases like "it should work", "admin has access", or "system validates input" directly.
- Separate facts from assumptions and open questions.
- Flag what blocks QA execution versus what can be deferred.

## Framework

Use `references/qa-gap-review-framework.md`.

## Completion Criteria

- Core actors, flows, and expected outcomes are clear enough to test.
- Missing acceptance logic and business rules are either clarified or explicitly marked.
- The package is specific enough to support scope and test design without inventing behavior.
