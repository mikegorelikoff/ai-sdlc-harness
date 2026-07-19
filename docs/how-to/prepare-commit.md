---
title: Prepare a commit
description: Stage one coherent task with current validation and SDD traceability.
---

## Confirm task completion

The task checkbox, machine plan status, implementation, tests, and validation evidence must agree. Later tasks may remain pending when the commit is explicitly scoped with `--task TNNN`.

## Inspect before staging

Run `git status --short --branch`, `git diff --stat`, and the full relevant diff. Classify every path as related, unrelated, or unclear. Never use broad staging to hide that decision.

## Run readiness

```bash
python3 skills/ai-sdlc-commit-prep/scripts/check_commit_ready.py \
  --quick-flow --spec specs/NNN-feature --task TNNN
```

Validate branch/spec alignment, SDD gates, staged scope, and current checks. Fix every `git diff --check` issue.

## Validate the message

Use Conventional Commit syntax and include the spec, business context, implementation details, reviewer-visible test path, and exact validation outcomes. Commit non-interactively, then report the hash and remaining working-tree state.
