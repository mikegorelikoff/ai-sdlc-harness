---
title: Context and quality
description: Why bounded evidence-backed context and reusable review lenses improve continuity without flooding the model.
---

More context is not automatically better context. Large indiscriminate reads consume attention, preserve stale assumptions, and make important constraints harder to find.

## Bounded project memory

Project context summarizes architecture, commands, policy, ownership, and delivery conventions with source anchors and drift identity. Compact indexes route the assistant to the smallest relevant artifact ranges before broad reads.

## Reusable quality lenses

A lens names a review perspective—testability, accessibility, operability, security, consistency—and defines what evidence a finding needs. Findings carry severity, trace targets, owner, resolution status, and next action.

## Quality without authority confusion

Context describes current evidence. Lenses evaluate it. Neither silently changes the underlying requirement or policy. That separation keeps repeated reviews consistent while preserving the responsible owner’s decision authority.

## Context contract v3

Project memory is intentionally broad; implementation context should be narrow.
Context contract v3 maps repository ownership, source-to-test topology, stack,
commands, and feature traces, then selects a task pack from explicit task paths,
tags, and conditional selector rules.

Every candidate has a priority, per-source cap, and explanation. Allocation is
deterministic and cannot exceed the pack budget. Exact content ranges carry
current hashes; skipped candidates retain exclusion reasons. Secret-named
paths, symlinks, generated output, binaries, oversized files, configured globs,
and credential-like assignments are removed before content is returned.

A pack also compares saved project-context identity with current repository
evidence and intersects selected paths with non-fresh evidence ledger records.
Missing freshness sources produce warnings, not optimistic assumptions. The
result is small enough for one task but still explains what was omitted and why.

Good context reduces tokens by increasing selectivity, not by deleting the evidence needed to challenge a conclusion.

For prerequisite teaching and exercises, start with
[Context, verification, and evidence](../learn/context-and-verification.md).
