---
name: ai-sdlc-runtime
description: AI SDLC resumable task-runtime workflow. Use when an AI assistant needs to start or resume a versioned delivery run, select dependency-ready work, enforce step, failure, and token budgets, retry safely, persist exact stop reasons, recover state from an append-only journal, or require commit evidence at task boundaries. Supports `--quick-flow` for deterministic local runs and `--full-flow` for strict transition review.
---

# ai-sdlc-runtime: Resumable Delivery Runs

> Internal AI SDLC skill, not client-facing by default.
> Every rule below is important to follow. None of it can be skipped.
> The journal is the local structural source for recovery; it is not authenticated evidence. A user with workspace write access can rewrite entries and recompute the SHA-256 chain. Independent assurance requires protected Git history, trusted continuous-integration records, or an external audit log.

## 0. Skill Card

- Skill name: `ai-sdlc-runtime`
- Primary audience: Dev, Delivery
- Supporting audience: QA, Release, Architecture
- Audience tags: Dev, Delivery, QA, Release
- SDLC stage: Controlled execution
- Purpose: Persist task selection and outcomes so interrupted delivery can
  resume without duplicate work or unsupported completion claims.
- Output: `_ai_sdlc/runs/<run-id>/journal.jsonl`, exact `state.json`, and
  complete token-efficient `state.toon`

### 0.1 Required Inputs

- Versioned run plan, safe run ID, dependency graph, task input fingerprints,
  retry limits, budgets, and commit-boundary flags.
- Exact result fingerprint, token use, commit evidence, and reason when recording.

### 0.2 Clarification Rules

- Ask when task outcome, result identity, commit evidence, or stop reason is missing.
- Reject unknown tasks, invalid transitions, dependency cycles, and journal gaps.
- Never mark an unrecorded task complete from conversational confidence.

### 0.2.1 Flow Mode Flags

- Support `--quick-flow` and `--full-flow`; full flow takes precedence.
- Both modes use the same journal, idempotency, dependency, budget, and commit rules.
- Full flow reviews every event, retry, stop reason, and commit boundary.

### 0.3 Output Rules

- Report run status, sequence, current task, ready tasks, budgets, stop reason,
  recovery status, and next command.
- Return validation and handoff summaries directly in the active agent response.
- Emit `ai-sdlc-handoff/v1` with `result`, `blockers`, `next_required`, and
  `next_optional`; actions include `reason`, `command`, and `expected_artifact`.
- Do not create `summary.txt`, `*-summary.txt`, or another standalone summary file.

### 0.4 Artifact Routing

- Route each run only to `_ai_sdlc/runs/<run-id>/`.
- Keep journal append-only, JSON recovery state atomically replaceable, and
  TOON state as the complete agent-facing projection.
- Never store runtime records inside a feature spec folder.

## 0.4.1 Runtime Path Resolution

- Treat `skills/` in commands as a logical skill root. In a harness source checkout, use `skills/`; in a project-scoped consumer installation, resolve it to `.agents/skills/`. Before running a helper, verify that the selected root contains both this skill and `ai-sdlc-shared-runtime`; block with the missing path if neither layout exists.

## 0.5 Feature State Machine

- Read the owning feature `_ai_sdlc/state.toon` before starting feature work.
- Runtime task state does not replace feature `state.toon`; the owning workflow
  performs feature transitions only after runtime and validation evidence agree.

## 0.6 Artifact Metadata And Metatags

- Runtime-related Markdown uses canonical `artifact_metadata` and `metatags`.
- Machine records use `ai-sdlc-run-plan/v1`, `ai-sdlc-run-event/v1`, and
  `ai-sdlc-run-state/v1` with deterministic fingerprints.

## 0.7 Specs Index

- Read `_ai_sdlc/specs-index.toon` first and use `specs-index.md` for human
  feature discovery before constructing a plan.
- Runtime state does not refresh either specs index.

## References

- Read `references/runtime-contract.md` before starting, resuming, retrying, or
  recording a run.
- Validate plans with `references/run-plan.schema.json`, events with
  `references/run-event.schema.json`, and state with
  `references/run-state.schema.json`.
- Use `scripts/runtime.py` for every state mutation and recovery operation.

## Script Usage

```bash
python3 skills/ai-sdlc-runtime/scripts/runtime.py . --start --run-id delivery-004 --plan run-plan.json --format toon
python3 skills/ai-sdlc-runtime/scripts/runtime.py . --next --run-id delivery-004 --format toon
python3 skills/ai-sdlc-runtime/scripts/runtime.py . --record --run-id delivery-004 --task T001 --outcome succeeded --result-fingerprint <sha256> --tokens 420 --commit <sha>
python3 skills/ai-sdlc-runtime/scripts/runtime.py . --resume --run-id delivery-004 --format toon
```

## Purpose

Make long-running delivery resumable, bounded, and auditable without coupling
the durable task state to one agent host or chat session.

## Inputs

- Immutable plan identity and ordered task IDs with dependencies.
- Per-task maximum attempts and commit-boundary requirement.
- Run-level maximum task starts, failures, and recorded tokens.
- Exact outcome evidence for each started task.

## Steps

1. Validate plan identity, unique tasks, dependency existence, and acyclicity.
2. Start one atomically created run workspace.
3. Call `--next`; repeated calls return the same running task without another event.
4. Execute the task through the owning host and workflow.
5. Record succeeded, failed, or blocked with exact evidence and resource use.
6. Let retryable failures return to pending; inspect terminal retry or budget stops.
7. Use `--retry` only for an eligible blocked or failed task after its cause is resolved.
8. Use `--resume` to replay and hash-check the journal and repair stale state.

## Output Spec

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

## Examples

A repeated `--next` after T001 was claimed returns T001 with `idempotent: true`
and does not increase attempts or journal sequence. A repeated identical success
record also returns the existing outcome without another event.

## Edge Cases

- Corrupt or missing summarized state is repaired from a valid journal.
- A journal sequence gap, hash mismatch, or invalid transition fails recovery.
- Retry exhaustion and each budget type have distinct stop reasons.
- A commit-boundary task cannot succeed with a missing or malformed commit SHA.

## Scope Boundary

- Do not execute task commands, create commits, satisfy gates, or approve work.
- Do not edit journal lines, plan identity, attempts, budgets, or fingerprints manually.
- Do not run two mutating runtime commands concurrently for one run.
- Declarative workflow steps and host execution belong to later workflow and adapter layers.
