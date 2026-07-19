---
layout: default
title: Navigate a new request
description: Turn an unstructured delivery request into one evidence-backed required action and relevant optional actions.
kicker: How-to · Routing
permalink: /how-to/navigate-request/
nav_order: 14
---

## Provide intent, not a workflow guess

```text
Use ai-sdlc-navigator --quick-flow.
We need to rotate the signing keys without interrupting active sessions.
Inspect the repository and recommend the next required action.
```

Add the feature slug when resuming known work. Otherwise let the navigator inspect Git state, specs indexes, active lifecycle state, installed modules, project context, and policy.

## Evaluate the recommendation

A valid result includes detected context, exactly one ranked required action, relevant optional actions, reasons, exact commands, expected artifacts, and blockers. Confirm that the evidence paths actually exist and are current.

## Handle a blocker

Do not jump to a later skill when the required predecessor is missing. Resolve the decision, artifact, or repository state—or use a quick-flow assumption only when the risk is low and the same assumption is recorded durably.

Re-run navigation after completing the action. Workflow handoffs and navigator recommendations should converge on the same next lifecycle need.
