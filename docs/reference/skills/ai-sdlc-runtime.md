---
title: Runtime
description: Human-facing operating guide for ai-sdlc-runtime, including inputs, authority, artifacts, modes, helpers, gates, recovery, and handoff.
---

# `ai-sdlc-runtime`

AI SDLC resumable task-runtime workflow. Use when an AI assistant needs to start or resume a versioned delivery run, select dependency-ready work, enforce step, failure, and token budgets, retry safely, persist exact stop reasons, recover state from an append-only journal, or require commit evidence at task boundaries. Supports `--quick-flow` for deterministic local runs and `--full-flow` for strict transition review.

| Lifecycle position | Primary owner | Supporting roles | Module | Output |
| --- | --- | --- | --- | --- |
| Controlled execution | Dev, Delivery | QA, Release, Architecture | `core` | `_ai_sdlc/runs/<run-id>/journal.jsonl`, exact `state.json`, and complete token-efficient `state.toon` |

## Why it exists

Persist task selection and outcomes so interrupted delivery can resume without duplicate work or unsupported completion claims.

## Use it when

AI SDLC resumable task-runtime workflow. Use when an AI assistant needs to start or resume a versioned delivery run, select dependency-ready work, enforce step, failure, and token budgets, retry safely, persist exact stop reasons, recover state from an append-only journal, or require commit evidence at task boundaries. Supports `--quick-flow` for deterministic local runs and `--full-flow` for strict transition review.

If the correct entry point is still unclear, ask the read-only navigator first instead of guessing.

## Do not use it when

- Do not use it without an accepted immutable execution plan. Use `ai-sdlc-workflow` or `ai-sdlc-sdd` instead.
- Do not use it for a bounded one-off task that needs no declared DAG. Use the normal owning implementation workflow instead.


## Who is involved

- **Accountable/primary:** Dev, Delivery.
- **Supporting:** QA, Release, Architecture.
- **Agent:** follows this contract, reports assumptions and blockers, and cannot accept protected decisions for the humans above.

## Before you start

- Versioned run plan, safe run ID, dependency graph, task input fingerprints,
  retry limits, budgets, and commit-boundary flags.
- Exact result fingerprint, token use, commit evidence, and reason when recording.

## Tell your agent

```text
Use ai-sdlc-runtime for <target>.
Choose --quick-flow for bounded assumption-driven progress or --full-flow
for strict verification only as described below.
Read the required evidence,
produce or report `_ai_sdlc/runs/<run-id>/journal.jsonl`, exact `state.json`, and complete token-efficient `state.toon`, preserve human approval boundaries,
and return blockers plus a complete ai-sdlc-handoff/v1.
```

This is an agent instruction, not a shell command. Terminal commands belong in the helper section.

## What the agent reads

- Immutable plan identity and ordered task IDs with dependencies.
- Per-task maximum attempts and commit-boundary requirement.
- Run-level maximum task starts, failures, and recorded tokens.
- Exact outcome evidence for each started task.

## What it may write

- Route each run only to `_ai_sdlc/runs/<run-id>/`.
- Keep journal append-only, JSON recovery state atomically replaceable, and
  TOON state as the complete agent-facing projection.
- Never store runtime records inside a feature spec folder.

## Human checkpoints

- Ask when task outcome, result identity, commit evidence, or stop reason is missing.
- Reject unknown tasks, invalid transitions, dependency cycles, and journal gaps.
- Never mark an unrecorded task complete from conversational confidence.

Humans accept or reject material product, security, QA, policy, rollout, release, and destructive-action decisions; a complete agent handoff is evidence, not approval.

## Flow modes

- Support `--quick-flow` and `--full-flow`; full flow takes precedence.
- Both modes use the same journal, idempotency, dependency, budget, and commit rules.
- Full flow reviews every event, retry, stop reason, and commit boundary.

## Deterministic helpers

Paths beginning with `skills/` below are canonical **source-checkout** forms for maintainers and CI. In a consumer repository, normally tell the installed skill to act; for human diagnosis, use the matching project-scoped `.agents/skills/<skill>/...` path reported by your host. Do not expect source-only `skills/_shared` to exist after installation.

| Helper | Purpose | Direct starting point | Repository effect |
| --- | --- | --- | --- |
| [`runtime.py`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-runtime/scripts/runtime.py) | Run a bounded, journaled, resumable task state machine. | `python3 skills/ai-sdlc-runtime/scripts/runtime.py --help` | May write only through an explicit mutation mode; start with `--help`, check, preview, or emit. |

The owning agent normally runs these helpers. A human uses the direct starting point for diagnosis or reproduction after inspecting `--help` and repository policy.

### Contract-provided usage

```bash
python3 skills/ai-sdlc-runtime/scripts/runtime.py . --start --run-id delivery-004 --plan run-plan.json --format toon
python3 skills/ai-sdlc-runtime/scripts/runtime.py . --next --run-id delivery-004 --format toon
python3 skills/ai-sdlc-runtime/scripts/runtime.py . --record --run-id delivery-004 --task T001 --outcome succeeded --result-fingerprint <sha256> --tokens 420 --commit <sha>
python3 skills/ai-sdlc-runtime/scripts/runtime.py . --resume --run-id delivery-004 --format toon
```

## Success criteria

The hash-chained JSONL journal stores contiguous sequence numbers and transition
payloads. Exact JSON state supports deterministic replay comparison. Complete
TOON state exposes the plan identity, task states and attempts, running and ready
tasks, budgets, stop reason, sequence, and fingerprint to agents. Replay must
reproduce both projections.

Quality gate:

- Pass when journal chain and replay are valid, dependencies are satisfied,
  budgets remain, outcome evidence is complete, and commit-boundary tasks carry
  commit identity.
- Fail when a transition duplicates work, skips dependencies, exceeds a hard
  boundary, omits evidence, or conflicts with journal history.

## Blockers and recovery

- Corrupt or missing summarized state is repaired from a valid journal.
- A journal sequence gap, hash mismatch, or invalid transition fails recovery.
- Retry exhaustion and each budget type have distinct stop reasons.
- A commit-boundary task cannot succeed with a missing or malformed commit SHA.

On a blocker, preserve failed/stale evidence, name the accountable owner and exact missing input, then resume this skill or the earliest reopened producer. Never manufacture completion by editing derived state.

## Handoff

- Report run status, sequence, current task, ready tasks, budgets, stop reason,
  recovery status, and next command.
- Return validation and handoff summaries directly in the Codex response.
- Emit `ai-sdlc-handoff/v1` with `result`, `blockers`, `next_required`, and
  `next_optional`; actions include `reason`, `command`, and `expected_artifact`.
- Do not create `summary.txt`, `*-summary.txt`, or another standalone summary file.

The downstream consumer rechecks artifacts and freshness; it does not trust a previous chat's completion claim.

## State, metadata, and indexes

??? info "Feature state"

    - Read the owning feature `_ai_sdlc/state.toon` before starting feature work.
    - Runtime task state does not replace feature `state.toon`; the owning workflow
      performs feature transitions only after runtime and validation evidence agree.

??? info "Artifact metadata"

    - Runtime-related Markdown uses canonical `artifact_metadata` and `metatags`.
    - Machine records use `ai-sdlc-run-plan/v1`, `ai-sdlc-run-event/v1`, and
      `ai-sdlc-run-state/v1` with deterministic fingerprints.

??? info "Specs index"

    - Read `_ai_sdlc/specs-index.toon` first and use `specs-index.md` for human
      feature discovery before constructing a plan.
    - Runtime state does not refresh either specs index.

## Example

A repeated `--next` after T001 was claimed returns T001 with `idempotent: true`
and does not increase attempts or journal sequence. A repeated identical success
record also returns the existing outcome without another event.

## Source contract

This page is generated from [`skills/ai-sdlc-runtime/SKILL.md`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-runtime/SKILL.md). Edit the source contract, rerun the catalog generator, and review both changes together; never hand-edit this page.

[Back to the skill catalog](../skills.md) · [Script reference](../scripts.md) · [Choose a workflow](../../flows/index.md)
