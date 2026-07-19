---
name: ai-sdlc-change-set
description: AI SDLC controlled change-workspace workflow. Use when an AI assistant needs to create or validate an isolated proposal workspace before changing canonical requirements, designs, policies, APIs, or other authoritative artifacts. Supports `--quick-flow` for assumption-driven drafts and `--full-flow` for strict owner, target, and authority checks.
---

# ai-sdlc-change-set: Isolated Change Workspace

> Internal AI SDLC skill, not client-facing by default.
> Every rule below is important to follow. None of it can be skipped.
> A change workspace proposes intent; it never becomes canonical truth by itself.

## 0. Skill Card

- Skill name: `ai-sdlc-change-set`
- Primary audience: Delivery, Dev, BA
- Supporting audience: PM, QA, Architecture, Security
- Audience tags: Delivery, Dev, BA, PM, QA
- SDLC stage: Controlled change intake
- Purpose: Create and validate an isolated, reviewable workspace before any
  authoritative specification mutation.
- Output: `changes/<change-id>/` with proposal, design, tasks, delta and
  evidence indexes, plus `_ai_sdlc/change-set.json`

### 0.1 Required Inputs

- Repository root and a lowercase hyphenated change ID.
- Change title, summary, owner, and one or more repository-relative canonical
  target paths.
- Quick or full flow selection when organization policy requires it.

### 0.2 Clarification Rules

- Ask when the owner, target authority, or intended outcome is ambiguous.
- Reject absolute paths, parent traversal, targets inside `changes/`, and
  duplicate targets instead of normalizing them silently.
- Treat generated workspace content as a proposal until a later controlled
  apply workflow proves approval and conflict freedom.

### 0.2.1 Flow Mode Flags

- Support `--quick-flow` and `--full-flow`; full flow takes precedence.
- Quick flow may create a draft from confirmed repository context and visible
  assumptions.
- Full flow requires explicit owner, summary, and canonical targets.
- Neither flow reads, writes, renames, or deletes canonical targets.

### 0.3 Output Rules

- Report the change ID, workspace path, status, owner, targets, fingerprint,
  validation result, and next required action.
- Before the final response, emit an `ai-sdlc-handoff/v1` result that routes a
  structurally valid workspace to delta authoring and validation. Include
  `next_required` and `next_optional` actions with reasons, commands, and
  expected artifacts.
- Return progress, validation, and handoff summaries directly in the Codex response.
- Do not create `summary.txt`, `*-summary.txt`, or another standalone summary file.
- Do not create ad hoc summaries outside the canonical workspace files.

### 0.4 Artifact Routing

- Route every change to `<repository>/changes/<change-id>/`.
- Keep human intent in `proposal.md`, `design.md`, `tasks.md`,
  `deltas/index.md`, and `evidence/index.md`.
- Keep the bounded machine projection in `_ai_sdlc/change-set.json`.
- Never store a change workspace inside `specs/`, `specs-refiniment/`, or a
  canonical target directory.

## 0.5 Feature State Machine

- Change status begins as `draft` in the change-set record.
- T002 creates only the intake state; later delta, preview, apply, and archive
  tasks own their state transitions.
- Read the owning feature `_ai_sdlc/state.toon` when targets belong to an
  existing feature, but do not modify feature `state.toon` during intake.

## 0.6 Artifact Metadata And Metatags

- Generated Markdown starts with `artifact_metadata` frontmatter using
  `ai-sdlc-change-set-metadata/v1`.
- Include change ID, artifact, status, owner, created and updated dates,
  canonical targets, and `metatags` for `ai-sdlc`, `change-set`, `proposal`,
  and `draft`.
- The JSON record uses schema `ai-sdlc-change-set/v1` and a deterministic
  contract fingerprint.

## 0.7 Specs Index

- Read `_ai_sdlc/specs-index.toon` first and use `specs-index.md` for human
  feature discovery when canonical targets belong to existing specs.
- A draft change workspace is not a feature spec and does not refresh either
  specs index.
- The later apply workflow refreshes indexes only after an approved canonical
  artifact change.

## References

- Read `references/change-set-contract.md` before creating or reviewing a
  workspace.
- Use `references/change-set.schema.json` for the versioned machine contract.
- Use `scripts/change_set.py` for deterministic emit, create, and validation.

## Script Usage

```bash
python3 skills/ai-sdlc-change-set/scripts/change_set.py . --change-id add-session-timeout --title "Add session timeout" --summary "Expire inactive sessions." --owner Security --target specs/auth/requirements.md --emit --quick-flow
python3 skills/ai-sdlc-change-set/scripts/change_set.py . --change-id add-session-timeout --title "Add session timeout" --summary "Expire inactive sessions." --owner Security --target specs/auth/requirements.md --create --full-flow
python3 skills/ai-sdlc-change-set/scripts/change_set.py . --change-id add-session-timeout --validate --format json
```

`--emit` renders the planned record without writes. `--create` builds the
workspace atomically and fails if it already exists. `--validate` verifies the
existing workspace and fingerprint.

## Purpose

Separate proposed change intent from current system truth so humans and AI can
review scope, ownership, targets, tasks, deltas, and evidence before any
canonical mutation is possible.

## Inputs

- Use a stable change ID that describes one bounded outcome.
- Use repository-relative POSIX paths for canonical targets.
- Use an accountable role or person as owner.
- Keep summary factual and state uncertainty in the proposal after creation.

## Steps

1. Inspect canonical sources read-only and identify their authority owners.
2. Run `--emit` to review the planned workspace and fingerprint.
3. Resolve unsafe IDs, paths, duplicate targets, or missing ownership.
4. Run `--create`; confirm canonical target bytes did not change.
5. Edit proposal sections through normal reviewed repository changes.
6. Run `--validate` before authoring semantic deltas.
7. Hand the validated workspace to the delta workflow; do not apply it.

## Output Spec

The JSON schema `ai-sdlc-change-set/v1` contains `change_id`, `title`,
`summary`, `status`, `owner`, `flow_mode`, dates, canonical targets, workspace
artifact paths, authority rules, and `contract_fingerprint`.

Quality gate:

- Pass when the workspace has every required artifact, the JSON record matches
  the schema, paths are safe and unique, headings and metadata are complete,
  and the fingerprint recomputes exactly.
- Fail when creation would overwrite a workspace, a target crosses a safety
  boundary, metadata and machine state disagree, or any required artifact is
  missing.

## Examples

Valid target: `specs/identity/requirements.md`.

Invalid counter-example: `../../policy.md`. Reject it because a change target
must remain repository-relative and cannot traverse outside the repository.

## Edge Cases

- A target may not exist yet when the proposal adds a new canonical artifact;
  record it explicitly and let delta validation decide whether `ADDED` is valid.
- Multiple targets are sorted for deterministic identity.
- Re-running `--create` never merges or replaces an existing workspace.
- A hand-edited record with a stale fingerprint fails validation.
- Empty delta and evidence indexes are valid at intake and become stricter in
  later lifecycle stages.

## Scope Boundary

- Do not parse or approve requirement delta semantics; use the delta workflow.
- Do not compute downstream impact; use `$ai-sdlc-change-impact` and preview.
- Do not mutate canonical artifacts, policy, feature state, or specs indexes.
- Do not approve, apply, archive, merge, commit, or release a change.
