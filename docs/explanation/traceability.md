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

## Executable delivery graph

`ai-sdlc-delivery-graph` turns stable anchors into a deterministic generated
projection. Feature-scoped IDs avoid collisions, exact file-and-line anchors
explain every node and edge, and Git commit bodies connect implementation tasks
to commits and release tags. Rebuilding the same repository state produces the
same graph and fingerprint.

The graph derives only conservative relationships: task references trace to
requirements, test references verify requirements, explicit component and
evidence declarations connect implementation and proof, commits implement
tasks, and tags release commits. It never adds a link based on wording alone.

Gap queries expose requirements without task or test coverage, tasks and tests
without requirement links, and disconnected lifecycle nodes. Trace queries
walk semantic links in either direction so a reviewer can move from a customer
criterion to its task, commit, and release without artifact declaration edges
creating misleading shortcuts.
