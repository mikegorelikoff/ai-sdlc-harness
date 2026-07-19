---
title: Doctor
description: Human-facing operating guide for ai-sdlc-doctor, including inputs, authority, artifacts, modes, helpers, gates, recovery, and handoff.
---

# `ai-sdlc-doctor`

AI SDLC installation diagnostics and safe upgrade planning. Use when an AI assistant needs to inspect harness prerequisites, repository layout, module and skill registration, detect actionable installation problems, compare versioned file inventories, preview additions/modifications/removals/schema migrations, or produce backup and rollback plans without applying an upgrade. Supports `--quick-flow` and `--full-flow`.

| Lifecycle position | Primary owner | Supporting roles | Module | Output |
| --- | --- | --- | --- | --- |
| Installation and upgrade operations | Dev, Delivery | Release, Architecture | `core` | `_ai_sdlc/doctor/report.{toon,json,md}` or `_ai_sdlc/upgrades/<id>/plan.{toon,json,md}` |

## Why it exists

Explain installation health and upgrade impact before mutation.

## Use it when

AI SDLC installation diagnostics and safe upgrade planning. Use when an AI assistant needs to inspect harness prerequisites, repository layout, module and skill registration, detect actionable installation problems, compare versioned file inventories, preview additions/modifications/removals/schema migrations, or produce backup and rollback plans without applying an upgrade. Supports `--quick-flow` and `--full-flow`.

If the correct entry point is still unclear, ask the read-only navigator first instead of guessing.

## Do not use it when

- Do not use it to diagnose application feature behavior. Use `ai-sdlc-validation` instead.
- Do not use it to apply installation or upgrade changes. Use the authorized install or update workflow instead.


## Who is involved

- **Accountable/primary:** Dev, Delivery.
- **Supporting:** Release, Architecture.
- **Agent:** follows this contract, reports assumptions and blockers, and cannot accept protected decisions for the humans above.

## Before you start

- Repository root for doctor checks.
- Current and target versioned inventories plus active harness API for upgrade planning.

## Tell your agent

```text
Use ai-sdlc-doctor for <target>.
Choose --quick-flow for bounded assumption-driven progress or --full-flow
for strict verification only as described below.
Read the required evidence,
produce or report `_ai_sdlc/doctor/report.{toon,json,md}` or `_ai_sdlc/upgrades/<id>/plan.{toon,json,md}`, preserve human approval boundaries,
and return blockers plus a complete ai-sdlc-handoff/v1.
```

This is an agent instruction, not a shell command. Terminal commands belong in the helper section.

## What the agent reads

- Repository root for doctor checks.
- Current and target versioned inventories plus active harness API for upgrade planning.

## What it may write

- Write generated reports only below repository `_ai_sdlc/`.
- Keep authored upgrade inventories visible and version controlled.
- Never treat a generated plan as authority to apply changes.

## Human checkpoints

- Ask when the installation root or target inventory is ambiguous.
- Reject unsafe paths, invalid hashes, duplicate files, invalid versions, and incompatible API ranges.
- Never repair, install, delete, overwrite, migrate, or restore files automatically.

Humans accept or reject material product, security, QA, policy, rollout, release, and destructive-action decisions; a complete agent handoff is evidence, not approval.

## Flow modes

- Support `--quick-flow` and `--full-flow`; full flow takes precedence.
- Full flow requires review of every warning, migration, backup, rollback, and blocker.

## Deterministic helpers

| Helper | Purpose | Direct starting point | Repository effect |
| --- | --- | --- | --- |
| [`doctor.py`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-doctor/scripts/doctor.py) | Diagnose harness installations and preview safe upgrade plans. | `python3 skills/ai-sdlc-doctor/scripts/doctor.py --help` | May write only through an explicit mutation mode; start with `--help`, check, preview, or emit. |

The owning agent normally runs these helpers. A human uses the direct starting point for diagnosis or reproduction after inspecting `--help` and repository policy.

### Contract-provided usage

```bash
python3 skills/ai-sdlc-doctor/scripts/doctor.py . --doctor --write
python3 skills/ai-sdlc-doctor/scripts/doctor.py . --upgrade --current current.json --target target.json --upgrade-id v2-preview --write
```

## Success criteria

Doctor checks have stable codes, statuses, evidence, and remediation. Upgrade
plans contain exact hashes, schema transitions, backup destinations, rollback
actions, compatibility blockers, and deterministic identity.

## Blockers and recovery

- Ask when the installation root or target inventory is ambiguous.
- Reject unsafe paths, invalid hashes, duplicate files, invalid versions, and incompatible API ranges.
- Never repair, install, delete, overwrite, migrate, or restore files automatically.

On a blocker, preserve failed/stale evidence, name the accountable owner and exact missing input, then resume this skill or the earliest reopened producer. Never manufacture completion by editing derived state.

## Handoff

- Default to complete TOON with checks, evidence, remediation, file changes,
  migrations, backups, rollback actions, blockers, and fingerprints.
- Return summaries directly in the Codex response.
- Emit `ai-sdlc-handoff/v1` with `result`, `blockers`, `next_required`, and
  `next_optional`; actions include `reason`, `command`, and `expected_artifact`.
- Do not create `summary.txt`, `*-summary.txt`, or another standalone summary file.

The downstream consumer rechecks artifacts and freshness; it does not trust a previous chat's completion claim.

## State, metadata, and indexes

??? info "Feature state"

    - Read owning feature `_ai_sdlc/state.toon` when diagnostics affect feature work.
    - Diagnostics and upgrade plans do not mutate feature state.

??? info "Artifact metadata"

    - Related Markdown uses canonical `artifact_metadata` and `metatags`.
    - Machine records use versioned doctor, inventory, and upgrade-plan schemas.

??? info "Specs index"

    - Read `_ai_sdlc/specs-index.toon` first and use `specs-index.md` for human review.
    - Operational reports do not refresh either index.

## Example

```bash
python3 skills/ai-sdlc-doctor/scripts/doctor.py . --doctor --write
python3 skills/ai-sdlc-doctor/scripts/doctor.py . --upgrade --current current.json --target target.json --upgrade-id v2-preview --write
```

## Source contract

This page is generated from [`skills/ai-sdlc-doctor/SKILL.md`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-doctor/SKILL.md). Edit the source contract, rerun the catalog generator, and review both changes together; never hand-edit this page.

[Back to the skill catalog](../skills.md) · [Script reference](../scripts.md) · [Choose a workflow](../../flows/index.md)
