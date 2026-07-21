---
title: Continue after a specification
description: Choose implementation, validation, review, and commit actions after an SDD package is ready.
---

# Continue after a specification

There is no safe universal “run everything” command. The next action depends on
specification state, task dependencies, repository validation commands, host
permissions, and human gates. Automation may coordinate accepted steps but may
not erase them.

## 1. Prove the specification is ready

```bash
python3 .agents/skills/ai-sdlc-sdd/scripts/sdd_status.py \
  --spec specs/NNN-feature --full-flow

python3 .agents/skills/ai-sdlc-sdd/scripts/plan_links.py \
  specs/NNN-feature --check --full-flow
```

Expected: `ready-for-implementation`, a zero plan-check exit, and human
acceptance of behavior, design, risks, and testability. Changed requirements
must update and revalidate the SDD package before coding.

## 2. Select one dependency-ready task

Use `_ai_sdlc/plan.toon` for dependencies and `tasks.md` for the human task
contract. Build a bounded task context pack for a medium, large, or unfamiliar
change. Implement one coherent task, derive tests from acceptance criteria, and
stop when required context is insufficient.

Navigator is optional when the feature and exact next skill are known. Invoke
that skill directly to save context. Use navigator when state, blockers, or the
next capability is unclear; it is not a mandatory wrapper around every skill.

## 3. Validate the current diff

Use `ai-sdlc-validation` to select focused commands, then run the accepted
validation plan against the exact current revision and diff. Manual review is
still mandatory: a passing script proves only its checked contract, not that a
requirement, test, or generated implementation is correct.

Split risky work into small evidence boundaries. After each task, compare
expected and actual behavior, inspect the diff, run negative and regression
cases, and update task state only after current evidence passes.

## 4. Review and commit

Run `ai-sdlc-code-review`; add `ai-sdlc-security-testing` when data, identity,
authorization, dependencies, commands, or trust boundaries are involved. Fix
blocking findings, rerun validation after source changes, then use
`ai-sdlc-commit-prep` and `ai-sdlc-conventional-commit` for exact staging and a
traceable commit.

## Automation boundary

`ai-sdlc-workflow` validates and plans dependency waves but does not execute
them. `ai-sdlc-runtime` can coordinate a reviewed versioned plan with step,
retry, failure, token, and commit boundaries. Use either only after the spec,
capabilities, permissions, approval owners, validation commands, and stop
conditions are explicit. Run sequentially when isolated workspaces are absent
or tasks touch the same files.

Never let automation infer production, release, secret, or financial authority;
run commands copied from generated text; complete tasks from a model claim;
continue after a budget, validation, scope, or approval blocker; or mutate a
shared working directory in parallel without enforced isolation.

The canonical stage contract is the [Implementation flow](../flows/implementation.md).
