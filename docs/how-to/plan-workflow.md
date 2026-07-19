---
title: Plan a declarative workflow
description: Validate typed steps, gates, hooks, conditions, and safe dependency waves without executing them.
---

# Plan a declarative workflow

Author a JSON workflow that declares capabilities and gives every step an ID,
type, action, dependencies, optional bounded condition, isolation mode, and
approval owner where applicable. Hooks target exact steps and use only declared
capabilities.

```bash
python3 skills/ai-sdlc-workflow/scripts/workflow.py . \
  --workflow workflows/release.json --validate

python3 skills/ai-sdlc-workflow/scripts/workflow.py . \
  --workflow workflows/release.json --plan \
  --context workflow-context.json \
  --concurrency 4 --isolation-supported --write
```

The planner writes complete TOON plus JSON and Markdown under
`_ai_sdlc/workflows/<workflow-id>/`. It never executes actions, hooks, or
approvals. Independent steps share a wave only when their types and isolation
are safe and the host explicitly supports isolation and concurrency. Otherwise
the plan contains deterministic sequential waves and exact fallback reasons.

Treat `executable: false` as a context blocker: at least one condition could
not be evaluated from explicit input.
