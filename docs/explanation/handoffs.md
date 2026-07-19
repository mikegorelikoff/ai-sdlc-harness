---
layout: default
title: Workflow handoffs
description: How every durable workflow communicates result, blockers, required next work, and optional opportunities.
kicker: Explanation · Continuity
permalink: /explanation/handoffs/
nav_order: 38
---

A workflow is not complete when it produces a file; it is complete when the next participant can understand the outcome and continue safely.

## The common contract

The handoff contains `result`, `blockers`, `next_required`, and `next_optional`. Every action explains its reason, exact command, and expected artifact. Required work is separated from useful but non-blocking improvement.

## Why exact commands matter

Skill names and flags are public workflow contracts. An exact command reduces routing ambiguity, preserves quick/full intent, and lets deterministic helpers validate the same transition.

## Relationship to navigation

The navigator infers next actions from current repository state. A workflow handoff knows what just happened. When both use the same state, policy, capability registry, and artifact contracts, their recommendations should agree.

Handoffs keep delivery continuous across roles, assistants, sessions, and context compaction without turning the conversation transcript into a dependency.
