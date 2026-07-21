---
name: ai-sdlc-doctor
description: AI SDLC installation diagnostics and safe upgrade planning. Use when an AI assistant needs to inspect harness prerequisites, repository layout, module and skill registration, detect actionable installation problems, compare versioned file inventories, preview additions/modifications/removals/schema migrations, or produce backup and rollback plans without applying an upgrade. Supports `--quick-flow` and `--full-flow`.
---

# ai-sdlc-doctor: Diagnostics And Safe Upgrade Plans

> Internal AI SDLC skill, not client-facing by default.
> Doctor and upgrade planning are read-only with respect to installation files.

## 0. Skill Card

- Skill name: `ai-sdlc-doctor`
- Primary audience: Dev, Delivery
- Supporting audience: Release, Architecture
- Audience tags: Dev, Delivery, Release, Architecture
- SDLC stage: Installation and upgrade operations
- Purpose: Explain installation health and upgrade impact before mutation.
- Output: `_ai_sdlc/doctor/report.{toon,json,md}` or `_ai_sdlc/upgrades/<id>/plan.{toon,json,md}`

### 0.1 Required Inputs

- Repository root for doctor checks.
- Current and target versioned inventories plus active harness API for upgrade planning.

### 0.2 Clarification Rules

- Ask when the installation root or target inventory is ambiguous.
- Reject unsafe paths, invalid hashes, duplicate files, invalid versions, and incompatible API ranges.
- Never repair, install, delete, overwrite, migrate, or restore files automatically.

### 0.2.1 Flow Mode Flags

- Support `--quick-flow` and `--full-flow`; full flow takes precedence.
- Full flow requires review of every warning, migration, backup, rollback, and blocker.

### 0.3 Output Rules

- Default to complete TOON with checks, evidence, remediation, file changes,
  migrations, backups, rollback actions, blockers, and fingerprints.
- Return summaries directly in the active agent response.
- Emit `ai-sdlc-handoff/v1` with `result`, `blockers`, `next_required`, and
  `next_optional`; actions include `reason`, `command`, and `expected_artifact`.
- Do not create `summary.txt`, `*-summary.txt`, or another standalone summary file.

### 0.4 Artifact Routing

- Write generated reports only below repository `_ai_sdlc/`.
- Keep authored upgrade inventories visible and version controlled.
- Never treat a generated plan as authority to apply changes.

## 0.4.1 Runtime Path Resolution

- Treat `skills/` in commands as a logical skill root. In a harness source checkout, use `skills/`; in a project-scoped consumer installation, resolve it to `.agents/skills/`. Before running a helper, verify that the selected root contains both this skill and `ai-sdlc-shared-runtime`; block with the missing path if neither layout exists.

## 0.5 Feature State Machine

- Read owning feature `_ai_sdlc/state.toon` when diagnostics affect feature work.
- Diagnostics and upgrade plans do not mutate feature state.

## 0.6 Artifact Metadata And Metatags

- Related Markdown uses canonical `artifact_metadata` and `metatags`.
- Machine records use versioned doctor, inventory, and upgrade-plan schemas.

## 0.7 Specs Index

- Read `_ai_sdlc/specs-index.toon` first and use `specs-index.md` for human review.
- Operational reports do not refresh either index.

## References

- Read `references/doctor-contract.md` before interpreting health or upgrade safety.
- Use `references/diagnostics.json` as the deterministic check registry.
- Validate inventories with `references/upgrade-inventory.schema.json`.
- Use `scripts/doctor.py` for all reports and plans.

## Script Usage

```bash
python3 skills/ai-sdlc-doctor/scripts/doctor.py . --doctor --write
python3 skills/ai-sdlc-doctor/scripts/doctor.py . --upgrade --current current.json --target target.json --upgrade-id v2-preview --write
```

## Purpose

Make operational gaps and upgrade risk reviewable before any installation mutation.

## Steps

1. Run registered prerequisite, layout, module, skill, and docs checks.
2. Report evidence and exact remediation without executing it.
3. Validate current and target inventories and API compatibility.
4. Diff files into add, modify, remove, unchanged, and schema-migration actions.
5. Plan backups for every modified or removed file.
6. Plan reverse-order rollback for every proposed change.
7. Emit TOON-first records; require a later authorized workflow to apply them.

## Output Spec

Doctor checks have stable codes, statuses, evidence, and remediation. Upgrade
plans contain exact hashes, schema transitions, backup destinations, rollback
actions, compatibility blockers, and deterministic identity.

## Scope Boundary

- Do not install dependencies or modify the installation.
- Do not execute remediation, backup, migration, apply, or rollback actions.
- Do not hide incompatible or destructive changes behind an aggregate status.
