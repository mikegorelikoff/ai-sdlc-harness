---
layout: default
title: Adopt an existing project
description: Introduce the harness to an established repository without overwriting its conventions or inventing missing context.
kicker: Tutorial · Established codebase
permalink: /tutorials/existing-project/
nav_order: 4
---

An established repository already has a delivery system, even if much of it is implicit. Adoption starts by observing that system and recording evidence, not by imposing a generic workflow.

## 1. Install additively

Use the installer in merge-safe mode and review the resulting diff. Keep existing project instructions, CI, templates, and ownership rules authoritative unless the team explicitly changes them.

## 2. Build evidence-backed context

Run `ai-sdlc-project-context --quick-flow`. The profiler should cite paths for architecture, test commands, language versions, code ownership, security boundaries, and delivery conventions. Unknown facts remain unknown.

## 3. Confirm the control plane

Inspect `specs-index.toon`, active `state.toon`, decision logs, and Git status. If the repository has no active AI SDLC feature, start a new feature for the first real change rather than backfilling fictional history.

## 4. Choose a pilot

Pick a bounded, valuable change with an informed reviewer. Use the navigator to select the entry point, then compare its recommendation with the repository context. Record any policy adjustment as a decision.

## 5. Learn before expanding

After the pilot, run a retrospective. Separate observations from proposals. Adopt only improvements that have evidence, an owner, and an explicit decision; do not let a retrospective silently rewrite team policy.

The result is an incremental adoption path: existing practice remains visible, new evidence contracts add continuity, and the team can expand usage based on measured value.
