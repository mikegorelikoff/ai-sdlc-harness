---
name: ai-sdlc-change-impact
description: AI SDLC change-impact and lifecycle recovery workflow. Use when a requirement, acceptance criterion, decision, API contract, risk assumption, or other traced source changed after downstream artifacts were created and an AI assistant must identify stale artifacts, affected lifecycle stages, and evidence-backed reopen or revalidation actions without silently rewriting authoritative state. Supports `--quick-flow` for focused trace scanning and `--full-flow` for strict state and source-evidence gates.
---

# ai-sdlc-change-impact: Evidence-Backed Lifecycle Recovery

> Internal AI SDLC skill, not client-facing by default.
> Every rule below is important to follow. None of it can be skipped.
> Analysis proposes recovery actions; the owning lifecycle skill applies them.

## 0. Skill Card

- Skill name: `ai-sdlc-change-impact`
- Primary audience: Delivery, Dev, BA, QA
- Supporting audience: PM, Architecture, Security
- Audience tags: Delivery, Dev, BA, QA
- SDLC stage: Cross-lifecycle change recovery
- Purpose: Trace changed sources to stale artifacts and safe reopen actions.
- Output: `change-impact.md` and `_ai_sdlc/change-impact.toon`

### 0.1 Required Inputs

- Feature root in `specs/` or `specs-refiniment/`.
- A JSON change set with stable changed references and exact source evidence.
- Readable feature artifacts and, in full flow, canonical lifecycle state.

### 0.2 Clarification Rules

- Ask only when the feature, changed reference, or source evidence is ambiguous.
- Do not infer that an artifact is stale without an exact trace occurrence.
- Report missing state or unowned artifacts as blockers, not guessed stages.
- Preserve multiple changes independently even when they affect one artifact.

### 0.2.1 Flow Mode Flags

- Support `--quick-flow` and `--full-flow`; full flow takes precedence.
- Quick flow scans feature Markdown and reports missing state as a blocker.
- Full flow requires canonical state plus valid changed-reference source lines.
- Neither mode changes state, artifacts, decisions, tasks, or indexes.

### 0.3 Output Rules

- Return changed refs, stale artifacts, affected stages, blockers, and ordered
  reopen actions directly in the active agent response.
- Before the final response, emit `ai-sdlc-handoff/v1` with `result`,
  `blockers`, `next_required`, and `next_optional`; every action includes
  `reason`, `command`, and `expected_artifact`.
- Do not create `summary.txt`, `*-summary.txt`, or ad hoc recovery files.
- Every affected artifact and reopen action must retain exact evidence.

### 0.4 Artifact Routing

- Write human analysis to `<feature-root>/change-impact.md`.
- Write machine analysis to `<feature-root>/_ai_sdlc/change-impact.toon`.
- Never overwrite the changed source, downstream artifacts, or state.
- Route approved actions through the owning lifecycle skill.

## 0.4.1 Runtime Path Resolution

- Treat `skills/` in commands as a logical skill root. In a harness source checkout, use `skills/`; in a project-scoped consumer installation, resolve it to `.agents/skills/`. Before running a helper, verify that the selected root contains both this skill and `ai-sdlc-shared-runtime`; block with the missing path if neither layout exists.

## 0.5 Feature State Machine

- Read `<feature-root>/_ai_sdlc/state.toon` before proposing stage actions.
- `--state-check` validates read-only state availability.
- `--begin-state` and `--complete-state` are rejected because analysis cannot
  authorize reopening.
- A `reopen` proposal applies only to a stage currently in a complete state;
  active and not-started stages receive revalidation or pre-start gates.
- The owning workflow records accepted recovery in state and decision log.

## 0.6 Artifact Metadata And Metatags

- Markdown starts with `artifact_metadata` using schema
  `ai-sdlc-change-impact-metadata/v1`.
- Include `metatags` for `ai-sdlc`, `change-impact`, `recovery`, and the affected
  stage identifiers.
- Record feature, workspace, changed refs, state file, and flow mode.

## 0.7 Specs Index

- Read `specs/_ai_sdlc/specs-index.toon` or
  `specs-refiniment/_ai_sdlc/specs-index.toon` before feature analysis.
- Do not refresh `specs/specs-index.md` or
  `specs-refiniment/specs-index.md` during read-only analysis.
- The owning workflow refreshes indexes only after an accepted state or
  authoritative artifact change.

## References

- Read `references/change-set-contract.md` before preparing change evidence.
- Use `scripts/change_impact.py` for deterministic trace scanning, stage
  mapping, validation, and canonical report generation.

## Script Usage

```bash
python3 skills/ai-sdlc-change-impact/scripts/change_impact.py specs/payments --changes /tmp/changes.json --emit --quick-flow
python3 skills/ai-sdlc-change-impact/scripts/change_impact.py specs/payments --changes /tmp/changes.json --write --full-flow --format toon
python3 skills/ai-sdlc-change-impact/scripts/change_impact.py specs/payments --changes /tmp/changes.json --state-check --format toon
```

The change set is read-only input. `--write` atomically creates both report
formats after all evidence gates pass.

## Purpose

Make late change recovery explicit and bounded so teams update the smallest
credible lifecycle surface instead of either ignoring drift or restarting all
delivery work.

## Inputs

- Use repository-relative source evidence with a positive line number.
- Use stable trace IDs already present in source and downstream artifacts.
- Read state status and artifact ownership from canonical repository records.
- Exclude generated change-impact reports from their own analysis.

## Steps

1. Record each changed reference and exact changed-source evidence.
2. Validate that the source path is inside the feature and the evidence line
   contains the changed reference.
3. Scan feature Markdown for exact downstream trace occurrences.
4. Map affected artifacts to lifecycle skills and stages using metadata.
5. Classify the safe action from current state: reopen complete work,
   revalidate active work, or add a pre-start validation gate.
6. Order actions by canonical lifecycle stage order and retain all evidence.
7. Emit or write the analysis, then hand approved actions to owning skills.

## Output Spec

The TOON schema `ai-sdlc-change-impact/v1` contains changes, affected artifacts,
stage status, blockers, and actions with `stage`, `skill`, `action`, `reason`,
`evidence_path`, `evidence_line`, `changed_ref`, and `expected_artifact`.

Quality gate:

- Pass when every change has valid source evidence and every impact/action is
  backed by an exact downstream trace occurrence.
- Full flow fails when state is absent, source evidence is invalid, or an
  affected artifact cannot be mapped to a lifecycle owner.

## Examples

Valid change:

```json
{"id":"CHG-001","changed_ref":"AC-004","source":{"path":"requirements.md","line":121,"detail":"Retry behavior changed from optional to required."}}
```

Invalid counter-example: `The requirements changed recently.` It cannot prove
which durable source changed or which downstream artifacts are stale.

## Edge Cases

- A valid change with no downstream occurrence reports no stale artifact and
  recommends targeted trace review rather than broad reopening.
- Multiple occurrences in one artifact are collapsed into one affected row per
  changed reference using the earliest exact line as evidence.
- Unknown artifact owners block full flow but remain visible in quick flow.
- Already active stages are revalidated, never reopened concurrently.

## Scope Boundary

- Do not mutate lifecycle state, indexes, source artifacts, or policy.
- Do not reopen a stage solely because it follows another stage chronologically.
- Do not treat filename similarity or model intuition as impact evidence.
- Do not approve recovery actions on behalf of artifact owners.
- Use `$ai-sdlc-navigator` when the owning workflow is unclear.
