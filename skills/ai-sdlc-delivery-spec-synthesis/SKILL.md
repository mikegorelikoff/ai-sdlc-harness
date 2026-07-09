---
name: ai-sdlc-delivery-spec-synthesis
description: Use when stories and clarified delivery context are ready and you need to produce a structured delivery specification that engineering and cross-functional teams can use for implementation planning and handoff.
---

# Delivery Spec Synthesis

## Purpose

Convert the clarified package and story set into a structured delivery specification.

## Use When

- The gap review is complete.
- The story set is mature enough to serve as a reliable input.
- The team needs a delivery-oriented spec, not just narrative discovery.

## Do Not Use When

- Stories are still missing key actor behavior or acceptance logic.
- The team only needs a lightweight story list.

## Workflow

1. Start from the validated stories and upstream package.
2. Synthesize scope, roles, workflows, business rules, data needs, NFRs, and dependencies.
3. Keep assumptions and open questions explicit instead of smoothing them over.
4. Organize the document for delivery handoff rather than executive storytelling.

## Spec Rules

- Keep the spec consistent with the story set and MVP boundaries.
- Do not re-invent requirements that contradict the input package.
- Call out unresolved rules, missing owners, and dependency risks directly.
- Go deep enough for delivery planning, but do not drift into code design unless the business-level spec genuinely requires it.

## Structures

Use `references/spec-structures.md`.

## Completion Criteria

- Scope, actors, and workflows are explicit.
- Requirements are traceable to stories and business value.
- Dependencies, assumptions, and open questions are visible.
- The document is usable as a delivery handoff artifact.
