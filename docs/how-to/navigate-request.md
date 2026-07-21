---
title: Navigate a new request
description: Turn an unstructured delivery request into one evidence-backed required action and relevant optional actions.
---

## Provide intent, not a workflow guess

```text
Use ai-sdlc-navigator --quick-flow.
We need to rotate the signing keys without interrupting active sessions.
Inspect the repository and recommend the next required action.
```

Add the feature slug when resuming known work. Otherwise let the navigator inspect Git state, specs indexes, active lifecycle state, installed modules, project context, and policy.

Navigator is optional when the exact installed skill and lifecycle state are
known. Invoke that skill directly to save context. Use navigator for an unclear
entry point, a resumed feature, conflicting state, or a blocker. Direct
invocation does not waive predecessor, permission, validation, or approval
gates.

## Evaluate the recommendation

A valid result includes detected context, exactly one ranked required action, relevant optional actions, reasons, exact commands, expected artifacts, and blockers. Confirm that the evidence paths actually exist and are current.

Inspect `skill_roots` when availability is disputed. It includes repository
source, project-scoped, and executing packaged/global roots when present. If a
host was open during installation, start a new session to refresh its own
registry; a correct direct filesystem report does not prove the host refreshed.

## Handle a blocker

Do not jump to a later skill when the required predecessor is missing. Resolve the decision, artifact, or repository state—or use a quick-flow assumption only when the risk is low and the same assumption is recorded durably.

Re-run navigation after completing the action. Workflow handoffs and navigator recommendations should converge on the same next lifecycle need.
