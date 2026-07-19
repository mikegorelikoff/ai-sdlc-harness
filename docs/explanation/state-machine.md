---
layout: default
title: Feature state machine
description: How lifecycle stages, active skills, skips, blockers, and artifact evidence prevent ambiguous workflow progress.
kicker: Explanation · State
permalink: /explanation/state-machine/
nav_order: 34
---

Chat history is a poor source of delivery state. It is incomplete, host-specific, and easily lost. Each feature therefore has a repository-local `state.toon` that describes lifecycle progress independently of any conversation.

## Stages and transitions

Stages map to skills and expected artifacts. `check` evaluates whether a transition is allowed, `begin` records active work, and `complete` requires artifact evidence. Only one lifecycle skill is active at a time.

## Quick and full behavior

Full flow blocks when predecessors, decisions, or artifacts are missing. Quick flow may skip a predecessor only for low-risk work with an explicit assumption or decision reference. The same reasoning belongs in the decision log, so the skip survives the chat.

## Recovery

Change impact can identify stale downstream work and propose a reopen. Reopen operations preserve prior evidence and resume from the earliest affected stage. The state machine is not a progress dashboard alone; it protects causal order.
