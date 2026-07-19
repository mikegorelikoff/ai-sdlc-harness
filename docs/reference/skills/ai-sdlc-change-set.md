---
title: Change Set
description: Human-facing operating guide for ai-sdlc-change-set, including inputs, authority, artifacts, modes, helpers, gates, recovery, and handoff.
---

# `ai-sdlc-change-set`

AI SDLC controlled change-workspace and specification-delta workflow. Use when an AI assistant needs to create or validate an isolated proposal workspace, author and validate requirement deltas, preview canonical changes, or apply and archive an explicitly approved change with rollback evidence. Supports `--quick-flow` for assumption-driven drafts and `--full-flow` for strict owner, target, evidence, and authority checks.

| Lifecycle position | Primary owner | Supporting roles | Module | Output |
| --- | --- | --- | --- | --- |
| Controlled change intake | Delivery, Dev, BA | PM, QA, Architecture, Security | `core` | `changes/<change-id>/` with proposal, design, tasks, delta and evidence indexes, lifecycle records, preview, approval, and recovery evidence |

## Why it exists

Create and validate an isolated, reviewable workspace before any authoritative specification mutation.

## Use it when

AI SDLC controlled change-workspace and specification-delta workflow. Use when an AI assistant needs to create or validate an isolated proposal workspace, author and validate requirement deltas, preview canonical changes, or apply and archive an explicitly approved change with rollback evidence. Supports `--quick-flow` for assumption-driven drafts and `--full-flow` for strict owner, target, evidence, and authority checks.

If the correct entry point is still unclear, ask the read-only navigator first instead of guessing.

## Do not use it when

- Do not use it for an ordinary new feature with no accepted downstream baseline. Use `ai-sdlc-navigator` to select refinement or `ai-sdlc-sdd` instead.


## Who is involved

- **Accountable/primary:** Delivery, Dev, BA.
- **Supporting:** PM, QA, Architecture, Security.
- **Agent:** follows this contract, reports assumptions and blockers, and cannot accept protected decisions for the humans above.

## Before you start

- Repository root and a lowercase hyphenated change ID.
- Change title, summary, owner, and one or more repository-relative canonical
  target paths.
- Quick or full flow selection when organization policy requires it.

## Tell your agent

```text
Use ai-sdlc-change-set for <target>.
Choose --quick-flow for bounded assumption-driven progress or --full-flow
for strict verification only as described below.
Read the required evidence,
produce or report `changes/<change-id>/` with proposal, design, tasks, delta and evidence indexes, lifecycle records, preview, approval, and recovery evidence, preserve human approval boundaries,
and return blockers plus a complete ai-sdlc-handoff/v1.
```

This is an agent instruction, not a shell command. Terminal commands belong in the helper section.

## What the agent reads

- Use a stable change ID that describes one bounded outcome.
- Use repository-relative POSIX paths for canonical targets.
- Use an accountable role or person as owner.
- Keep summary factual and state uncertainty in the proposal after creation.

## What it may write

- Route every change to `<repository>/changes/<change-id>/`.
- Keep human intent in `proposal.md`, `design.md`, `tasks.md`,
  `deltas/index.md`, and `evidence/index.md`.
- Keep complete agent-facing TOON beside interoperable JSON for the change set,
  delta set, apply preview, approval, and recovery records.
- Never store a change workspace inside `specs/`, `specs-refiniment/`, or a
  canonical target directory.

## Human checkpoints

- Ask when the owner, target authority, or intended outcome is ambiguous.
- Reject absolute paths, parent traversal, targets inside `changes/`, and
  duplicate targets instead of normalizing them silently.
- Treat generated workspace content as a proposal until a later controlled
  apply workflow proves approval and conflict freedom.

Humans accept or reject material product, security, QA, policy, rollout, release, and destructive-action decisions; a complete agent handoff is evidence, not approval.

## Flow modes

- Support `--quick-flow` and `--full-flow`; full flow takes precedence.
- Quick flow may create a draft from confirmed repository context and visible
  assumptions.
- Full flow requires explicit owner, summary, and canonical targets.
- Neither flow reads, writes, renames, or deletes canonical targets.

## Deterministic helpers

Paths beginning with `skills/` below are canonical **source-checkout** forms for maintainers and CI. In a consumer repository, normally tell the installed skill to act; for human diagnosis, use the matching project-scoped `.agents/skills/<skill>/...` path reported by your host. Do not expect source-only `skills/_shared` to exist after installation.

| Helper | Purpose | Direct starting point | Repository effect |
| --- | --- | --- | --- |
| [`change_apply.py`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-change-set/scripts/change_apply.py) | Apply approved change previews with rollback, then archive evidence. | `python3 skills/ai-sdlc-change-set/scripts/change_apply.py --help` | May write only through an explicit mutation mode; start with `--help`, check, preview, or emit. |
| [`change_preview.py`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-change-set/scripts/change_preview.py) | Preview specification delta application, conflicts, impact, and gates. | `python3 skills/ai-sdlc-change-set/scripts/change_preview.py --help` | May write only through an explicit mutation mode; start with `--help`, check, preview, or emit. |
| [`change_set.py`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-change-set/scripts/change_set.py) | Create and validate isolated AI SDLC change workspaces. | `python3 skills/ai-sdlc-change-set/scripts/change_set.py --help` | May write only through an explicit mutation mode; start with `--help`, check, preview, or emit. |
| [`spec_delta.py`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-change-set/scripts/spec_delta.py) | Parse and validate semantic requirement deltas without canonical writes. | `python3 skills/ai-sdlc-change-set/scripts/spec_delta.py --help` | May write only through an explicit mutation mode; start with `--help`, check, preview, or emit. |

The owning agent normally runs these helpers. A human uses the direct starting point for diagnosis or reproduction after inspecting `--help` and repository policy.

### Contract-provided usage

```bash
python3 skills/ai-sdlc-change-set/scripts/change_set.py . --change-id add-session-timeout --title "Add session timeout" --summary "Expire inactive sessions." --owner Security --target specs/auth/requirements.md --emit --quick-flow
python3 skills/ai-sdlc-change-set/scripts/change_set.py . --change-id add-session-timeout --title "Add session timeout" --summary "Expire inactive sessions." --owner Security --target specs/auth/requirements.md --create --full-flow
python3 skills/ai-sdlc-change-set/scripts/change_set.py . --change-id add-session-timeout --validate --format toon
python3 skills/ai-sdlc-change-set/scripts/spec_delta.py . --change-id add-session-timeout --validate --write --format toon
python3 skills/ai-sdlc-change-set/scripts/change_preview.py . --change-id add-session-timeout --preview --write --format toon
python3 skills/ai-sdlc-change-set/scripts/change_apply.py . --change-id add-session-timeout --apply --approval changes/add-session-timeout/evidence/owner-approval.json --format toon
python3 skills/ai-sdlc-change-set/scripts/change_apply.py . --change-id add-session-timeout --archive --format toon
```

`--emit` renders the planned record without writes. `--create` builds the
workspace atomically and fails if it already exists. `--validate` verifies the
existing workspace and fingerprint.

## Success criteria

The `ai-sdlc-change-set/v1` record is written as complete TOON plus JSON and contains `change_id`, `title`,
`summary`, `status`, `owner`, `flow_mode`, dates, canonical targets, workspace
artifact paths, authority rules, and `contract_fingerprint`.

The `ai-sdlc-spec-delta/v1` TOON/JSON pair contains normalized operations, target
and source evidence, exact source hashes, and a deterministic fingerprint.

The `ai-sdlc-change-preview/v1` TOON/JSON pair contains virtual target hashes and
diffs, conservative conflicts, stale references, reopen actions, gates, and a
fingerprint that becomes invalid when any input drifts.

The JSON schemas `ai-sdlc-change-approval/v1` and
`ai-sdlc-change-recovery/v1` bind accountable approval to the current preview
and preserve transaction, backup, apply, and rollback evidence.

Quality gate:

- Pass when the workspace has every required artifact, the JSON record matches
  the schema, paths are safe and unique, headings and metadata are complete,
  and the fingerprint recomputes exactly.
- Fail when creation would overwrite a workspace, a target crosses a safety
  boundary, metadata and machine state disagree, or any required artifact is
  missing.

## Blockers and recovery

- A target may not exist yet when the proposal adds a new canonical artifact;
  record it explicitly and let delta validation decide whether `ADDED` is valid.
- Multiple targets are sorted for deterministic identity.
- Re-running `--create` never merges or replaces an existing workspace.
- A hand-edited record with a stale fingerprint fails validation.
- Empty delta and evidence indexes are valid at intake and become stricter in
  later lifecycle stages.
- Preview returns status `blocked` and exit code 2 for semantic conflicts while
  still emitting complete review evidence.
- Interrupted or failed multi-target apply uses the persisted recovery manifest
  to restore every already-replaced target before another attempt is accepted.

On a blocker, preserve failed/stale evidence, name the accountable owner and exact missing input, then resume this skill or the earliest reopened producer. Never manufacture completion by editing derived state.

## Handoff

- Report the change ID, workspace path, status, owner, targets, fingerprint,
  validation result, and next required action.
- Before the final response, emit an `ai-sdlc-handoff/v1` result that routes a
  structurally valid workspace to delta authoring and validation. Include
  `next_required` and `next_optional` actions with reasons, commands, and
  expected artifacts.
- Return progress, validation, and handoff summaries directly in the Codex response.
- Do not create `summary.txt`, `*-summary.txt`, or another standalone summary file.
- Do not create ad hoc summaries outside the canonical workspace files.

The downstream consumer rechecks artifacts and freshness; it does not trust a previous chat's completion claim.

## State, metadata, and indexes

??? info "Feature state"

    - Change status begins as `draft` in the change-set record.
    - T002 creates only the intake state; later delta, preview, apply, and archive
      tasks own their state transitions.
    - Read the owning feature `_ai_sdlc/state.toon` when targets belong to an
      existing feature, but do not modify feature `state.toon` during intake.

??? info "Artifact metadata"

    - Generated Markdown starts with `artifact_metadata` frontmatter using
      `ai-sdlc-change-set-metadata/v1`.
    - Include change ID, artifact, status, owner, created and updated dates,
      canonical targets, and `metatags` for `ai-sdlc`, `change-set`, `proposal`,
      and `draft`.
    - The JSON record uses schema `ai-sdlc-change-set/v1` and a deterministic
      contract fingerprint.

??? info "Specs index"

    - Read `_ai_sdlc/specs-index.toon` first and use `specs-index.md` for human
      feature discovery when canonical targets belong to existing specs.
    - A draft change workspace is not a feature spec and does not refresh either
      specs index.
    - The later apply workflow refreshes indexes only after an approved canonical
      artifact change.

## Example

Valid target: `specs/identity/requirements.md`.

Invalid counter-example: `../../policy.md`. Reject it because a change target
must remain repository-relative and cannot traverse outside the repository.

## Source contract

This page is generated from [`skills/ai-sdlc-change-set/SKILL.md`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-change-set/SKILL.md). Edit the source contract, rerun the catalog generator, and review both changes together; never hand-edit this page.

[Back to the skill catalog](../skills.md) · [Script reference](../scripts.md) · [Choose a workflow](../../flows/index.md)
