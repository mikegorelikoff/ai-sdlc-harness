---
title: Open, review, and merge a change
description: Turn validated agent-assisted work into an independently reviewed, safely merged change with traceable evidence.
---

# Open, review, and merge a change

This gate applies after implementation and focused validation. An agent may
prepare evidence, but the accountable human decides whether to publish, merge,
release, or roll back a change.

## Prerequisites

- the task branch contains only the intended scope;
- requirements, tests, tasks, decisions, and validation evidence agree;
- required checks pass on the exact commit proposed for merge;
- secrets, generated caches, and unrelated files are absent;
- the repository's contribution, security, and branch-protection rules are
  known.

## 1. Inspect before staging

```bash
git branch --show-current
git status --short
git diff --check
git diff --stat
git diff
```

Read generated code and commands as untrusted proposals. Check boundary cases,
authorization, error handling, dependency changes, data exposure, licensing,
and rollback impact. A passing test does not prove that the test expresses the
correct requirement.

## 2. Stage an explicit scope

Prefer named paths to `git add -A`:

```bash
git add app.py test_app.py specs/001-health-endpoint
git diff --cached --check
git diff --cached --stat
git diff --cached
```

If the staged diff contains an unexpected cache, lock, agent package, secret,
or unrelated edit, unstage it and investigate. Do not discard another person's
work to make the tree look clean.

## 3. Record traceable evidence

The commit or pull request should identify:

- specification and task identifiers;
- acceptance criteria and test cases exercised;
- exact validation commands and outcomes;
- skipped checks and residual risks;
- material human decisions or waivers;
- migration, rollout, and rollback notes when relevant.

Use `ai-sdlc-commit-prep` to assemble this evidence. It does not grant approval
to merge and it does not replace repository policy.

## 4. Publish and open a pull request

Publishing affects an external repository. Verify the remote and obtain the
normal project authority before running:

```bash
git remote -v
git push -u origin HEAD
```

Create the pull request through the project's normal user interface or
approved command-line tool. Request reviewers independent of the implementing
agent. The product owner or delegated outcome owner validates behavior; code,
quality, security, and operations reviewers validate their respective risks.

## 5. Require fresh checks and resolve feedback

Required continuous-integration checks must pass for the current head commit,
not an earlier revision. Treat review comments as new evidence: update the
specification first when intent changed, then update plans, code, tests, and
validation. Never silence a failing check or weaken acceptance merely to make
the pull request green.

## 6. Merge, verify, and recover

Use the repository's approved merge strategy. After merge, verify the target
branch and deployment or release evidence. If production behavior fails,
follow the project's rollback or forward-fix procedure; preserve the failed
evidence and decision trail for diagnosis.

## Review checklist

- [ ] The diff is bounded and understandable without the original chat.
- [ ] Requirement-to-test-to-code traceability is inspectable.
- [ ] Negative and regression cases relevant to the risk passed.
- [ ] No secrets, private prompts, caches, or accidental files are included.
- [ ] Required checks are fresh for the merge commit or pull-request head.
- [ ] An accountable human accepted residual risk.
- [ ] Rollout, observation, and rollback ownership are explicit.

See [Validation](../reference/validation.md), [Prepare a commit](prepare-commit.md), and
[Governance and trust](../operations/governance.md).
