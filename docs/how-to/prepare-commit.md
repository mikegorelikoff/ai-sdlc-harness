---
title: Prepare a commit
description: Stage one coherent task with current validation and SDD traceability.
---

# Prepare a commit

Run this procedure from a **consumer repository** with the commit-prep skill
installed. In a harness source checkout, replace `.agents/skills/` with the
logical source root `skills/`.

## Confirm task completion

The reviewed task checkbox in `tasks.md`, generated plan projections,
implementation, tests, and validation evidence must agree. Later tasks may
remain pending when the commit is explicitly scoped with `--task TNNN`.

## Inspect before staging

Run `git status --short --branch`, `git diff --stat`, and the full relevant diff. Classify every path as related, unrelated, or unclear. Never use broad staging to hide that decision.

## Run readiness

```bash
python3 .agents/skills/ai-sdlc-commit-prep/scripts/check_commit_ready.py \
  --quick-flow --spec specs/NNN-feature --task TNNN
```

Expected success is `Commit readiness checks passed.` and exit code zero. A
non-zero result lists blocking paths or gates; fix the cause and rerun rather
than bypassing it. The helper validates repository evidence but does not prove
that every command claimed in prose actually ran—execute current tests on the
exact staged revision and retain their output or receipt.

Validate branch/spec alignment, SDD gates, staged scope, and current checks. Fix every `git diff --check` issue.

## Validate the message

Use Conventional Commit syntax and include `Spec: specs/NNN-feature`,
`Task: TNNN`, business context, implementation details, a reviewer-visible
test path, and exact `Validation:` outcomes. For a multi-task commit, list the
completed task IDs separated by commas. Validate with
`validate_commit_msg.py --require-traceability`; the validator rejects missing
or non-canonical task references. Commit non-interactively, then report the
hash and remaining working-tree state.
