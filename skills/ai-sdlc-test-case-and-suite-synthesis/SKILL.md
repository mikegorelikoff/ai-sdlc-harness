---
name: ai-sdlc-test-case-and-suite-synthesis
description: Use when QA scope and strategy are defined and you need to generate detailed, executable test cases plus smoke, regression, and user acceptance suites tied to requirements, roles, workflows, and risks.
---

# Test Case And Suite Synthesis

## Purpose

Generate the detailed QA artifacts used for structured execution.

## Use When

- Requirements are clear enough to test.
- Scope and strategy decisions are already defined.
- The team needs detailed cases and explicit suite groupings.

## Do Not Use When

- Core expected behavior is still unclear.
- Strategy and risk priorities are not yet defined.

## Workflow

1. Create detailed cases only for relevant product surfaces.
2. Cover positive, negative, boundary, permission, workflow, and data conditions as applicable.
3. Add API, UI, integration, notification, state, security, privacy, and non-functional cases only where the system actually has those surfaces.
4. Produce separate smoke, regression, and UAT groupings.
5. Keep each case tied to a requirement, role, workflow, rule, or risk.

## Case Rules

- Steps must be explicit and executable.
- Expected results must be specific.
- Every case should be traceable to a requirement, workflow, role, or risk.
- Do not create generic cases that could apply to any system.
- Mark automation candidacy explicitly.

## Structures

Use `references/test-case-structures.md`.

## Completion Criteria

- Core business flows are covered.
- Negative and edge cases are included where material.
- Separate smoke, regression, and UAT suites exist.
- The cases are executable without hidden interpretation.
