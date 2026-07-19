---
layout: default
title: Recover from change
description: Identify stale downstream artifacts after a requirement, design, or decision changes and reopen only the necessary lifecycle stages.
kicker: How-to · Recovery
permalink: /how-to/recover-change/
nav_order: 18
---

## Name the change signal

Point `ai-sdlc-change-impact` at the changed requirement, decision, design constraint, API contract, or validation result. Include the feature slug and the evidence that establishes what changed.

## Review the impact graph

Inspect linked acceptance criteria, test cases, tasks, plans, QA scope, and release evidence. “File modified” is not enough; impact follows semantic trace links and recorded dependencies.

## Reopen safely

Accept only reopen actions that name the lifecycle stage, stale artifacts, owner, and evidence. Reopening should preserve history and mark superseded conclusions; it must not erase earlier decisions to make state look clean.

## Resume from the earliest affected stage

Run the navigator after the reopen is recorded. It should route to the first required correction, not restart the entire lifecycle or continue from a now-invalid downstream task.
