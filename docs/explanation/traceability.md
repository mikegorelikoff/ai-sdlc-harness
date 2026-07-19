---
title: Traceability
description: How customer outcomes, requirements, decisions, tests, tasks, validation, and commits remain connected.
---

Traceability answers “why does this exist?” and “what proves it works?” without requiring the original author or assistant to reconstruct intent from a diff.

## Stable anchors

Acceptance criteria, test cases, tasks, and decisions use stable IDs such as `AC-003`, `TC-003`, `T002`, and `DEC-004`. Plans connect those anchors with dependencies, status, and validation order.

## Bidirectional reasoning

Forward traceability shows how a requirement becomes design, implementation, and tests. Backward traceability shows why a test, file, or task exists. Both are necessary: forward-only maps can hide orphan implementation, while backward-only maps can hide untested requirements.

## Evidence at completion

A task closes only when code or documentation, relevant tests, and validation support its linked criteria. Commit messages name the spec and exact checks. Release readiness can then identify missing coverage mechanically rather than relying on confidence language.

Trace links should remain small and meaningful. Linking everything to everything creates a graph that is complete on paper and useless in practice.
