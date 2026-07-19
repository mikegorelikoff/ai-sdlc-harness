---
title: Implementation flow
description: Move from accepted delivery evidence through task branching, SDD, bounded tasks, validation, review, and traceable commits.
---

# Implementation flow

Implementation belongs under `specs/<feature>/`. It consumes accepted
refinement evidence when available, but owns a separate contract for how the
repository will deliver and verify the change.

## Entry signals

- Accepted delivery specification and QA readiness for a full feature.
- A clear, low-risk behavior change that needs a proportionate SDD.
- A reproducible bug whose expected behavior is already authoritative.
- A review, validation, or security request that can reuse an existing spec.

## Exact implementation contract

| Stage ID | Predecessor / entry | Accountable owner | Required input | Exact capability | Artifact / result | Exit gate | Next consumer / handoff | Reopen condition |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `branch` | Accepted request or refinement handoff; documented base exists. | Repository owner | Repository root, branch policy, clean-tree evidence, feature slug. | `ai-sdlc-branching` | Verified `feature/<slug>` task branch and branch evidence. | Base refreshed, task branch checked out, tree clean, branch/spec identity aligned. | `sdd`, or a named read-only review stage when no write is required. | Wrong/stale base, dirty unrelated files, protected branch, or identity mismatch. |
| `sdd` | `branch` | Dev/Architecture with BA/QA inputs | Accepted delivery evidence or bounded behavior request, repository constraints, feature slug. | `ai-sdlc-sdd` | Complete `specs/<feature>/` requirements, design, test cases, QA, tasks, decisions, and plans. | Clarify, checklist, plan-link, analyze, and validation gates pass; human accepts behavior/design. | `task_context` for the first ready task. | Behavior changes, design contradiction, untestable requirement, or rejected decision. |
| `task_context` | Accepted `sdd` task, or evidence-backed existing contract for direct review. | Dev | Task/AC/TC IDs, repository topology, ownership/test evidence, exclusions, token budget. | `ai-sdlc-project-context` | Fresh project context and optional `_ai_sdlc/context/task-packs/<task>.{toon,json,md}`. | Selected sources are explained, fresh, in budget, and secrets/generated noise are excluded. | `implement`, `validate`, or `review` according to the requested task. | Source drift, stale pack, missing ownership/test topology, or unsafe selected path. |
| `implement` | `sdd` + `task_context` | Dev | One ready task, linked AC/TC, accepted design, bounded context. | Host coding agent within declared task scope | Code, tests, and bounded working-tree diff linked to the task. | Tests are derived first; requested behavior is present; task remains open until trusted validation passes. | `validate`. | Scope expansion, changed acceptance, implementation blocker, or failing trusted regression. |
| `validate` | `implement`, or direct validation-only request with an authoritative contract. | Dev/QA | Current diff/target, AC/TC, QA scope, exact environment constraints. | `ai-sdlc-validation` | Exact command outcomes, coverage mapping, skipped checks, and residual-risk handoff. | Required focused checks pass and evidence is current for the same diff. | `review`, or `implement` when a failure requires repair. | Source changes after validation, failed/skipped required check, or stale environment evidence. |
| `review` | Current `validate` evidence, or direct read-only review request. | Reviewer/Security | Diff or target, accepted spec, tests, validation, threat/context evidence. | `ai-sdlc-code-review` and risk-triggered `ai-sdlc-security-testing` | Evidence-ranked findings and complete review/security handoff. | Blocking findings are fixed, owned, or explicitly accepted by authorized humans. | `commit_prep`, or the exact producing stage named by a finding. | New high finding, changed diff, contract mismatch, or missing abuse/threat path. |
| `commit_prep` | Completed task + current `validate`/`review` evidence. | Dev/Repository owner | Branch/spec/task identity, scoped files, SDD gates, test evidence, commit policy. | `ai-sdlc-commit-prep` + `ai-sdlc-conventional-commit` | Staged bounded change and traceable commit with Spec/Task/validation evidence. | Staging contains no unrelated files; message and task evidence pass; commit succeeds. | `release_handoff` or the next explicitly ready task. | Unrelated staged file, stale validation, incomplete task/plan, or missing traceability. |
| `release_handoff` | Accepted `commit_prep` evidence and release candidate. | Release/Delivery | Commit/build identity, rollout, monitor, rollback, owners, waivers, residual risk. | `ai-sdlc-validation` plus accountable release handoff | Accepted release evidence and `ai-sdlc-handoff/v1` to the release owner. | Required release checks, owners, rollout/monitor/rollback, and residual risk are accepted. | Release execution and later `ai-sdlc-retrospective`. | Stale build/evidence, expired waiver, unowned dependency, failed rollout, or rollback trigger. |

## Small change versus medium/large change

A typo, log text fix, or test-only correction may use a small path with focused
validation and no new SDD. Observable behavior, API, architecture, data,
security, multi-component work, or meaningful rollout risk requires the SDD
package before implementation. The navigator can recommend the earliest missing
evidence but does not decide accountable product risk.

Create and verify the task branch before SDD writes. The specification is
repository-tracked delivery work, not disposable routing output. A read-only
review can enter later without creating a branch only when it performs no
repository mutation.

## One task, one evidence boundary

Tasks are bounded by output, AC/TC references, dependencies, validation, and
commit requirements. Marking a task complete is the final reflection of current
evidence—not an instruction to the system. If work expands, update the spec and
plan before continuing.

## Review-only and validation-only entry

You do not need to rerun discovery or rewrite a valid spec to review a diff.
Enter directly at code review, security testing, or validation, cite the
available contract, and report gaps to the owner. A review finding may reopen
SDD, QA, BA, or product work depending on what is missing.

For durable multi-task execution, see the runtime branch in
[Control-plane flows](control-plane.md).
