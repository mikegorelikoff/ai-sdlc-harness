---
name: ai-sdlc-quality-lenses
description: AI SDLC reusable quality-lens workflow. Use when an AI assistant needs to challenge a requirement, design, plan, test strategy, change, or delivery artifact through pre-mortem, adversarial, edge-case, stakeholder-conflict, reversibility, abuse-case, operational-failure, or assumption lenses and finalize evidence-backed findings with ownership and traceability. Supports `--quick-flow` for selected high-value lenses and `--full-flow` for the complete applicable registry.
---

# ai-sdlc-quality-lenses: Traceable Cross-Artifact Review

> Internal AI SDLC skill, not client-facing by default.
> Every rule below is important to follow. None of it can be skipped.
> Findings are proposals for review, not authority to change source artifacts.

## 0. Skill Card

- Skill name: `ai-sdlc-quality-lenses`
- Primary audience: BA, QA, Dev, Delivery
- Supporting audience: PM, Architecture, Security
- Audience tags: BA, QA, Dev, Delivery, PM
- SDLC stage: Cross-lifecycle quality review
- Purpose: Apply reusable challenge lenses and finalize evidence-backed findings.
- Output: `quality-lens-report.md` and `_ai_sdlc/quality-lens-report.toon`

### 0.1 Required Inputs

- One readable source artifact.
- One or more lens identifiers from `references/quality-lenses.json`.
- A feature or initiative identifier.
- An owner for every finding.

### 0.2 Clarification Rules

- Ask only when the artifact, review objective, or accountable owner is ambiguous.
- Record uncertainty as a finding; do not invent evidence or trace targets.
- Treat a lens with no supported finding as a valid clean result.
- Do not silently convert a finding into a requirement, decision, or task.

### 0.2.1 Flow Mode Flags

- Support `--quick-flow` and `--full-flow`; full flow takes precedence.
- Quick flow uses the explicitly selected lenses, or the registry defaults.
- Full flow applies every lens whose `applies_to` includes the artifact kind.
- Both modes use the same finding schema and finalization gates.

### 0.3 Output Rules

- Return selected lenses, finding counts by severity and status, blockers, and
  output paths directly in the active agent response.
- Before the final response, emit `ai-sdlc-handoff/v1` with `result`,
  `blockers`, `next_required`, and `next_optional`; every action includes
  `reason`, `command`, and `expected_artifact`.
- Do not create `summary.txt`, `*-summary.txt`, or unregistered review files.
- Never finalize a finding without evidence, severity, trace targets, owner,
  resolution status, and next action.

### 0.4 Artifact Routing

- Default human output: `<artifact-parent>/quality-lens-report.md`.
- Default machine output: `<artifact-parent>/_ai_sdlc/quality-lens-report.toon`.
- Use `--output-root` to route the pair to an owning feature directory.
- Keep the source artifact unchanged; reports are review evidence.

## 0.4.1 Runtime Path Resolution

- Treat `skills/` in commands as a logical skill root. In a harness source checkout, use `skills/`; in a project-scoped consumer installation, resolve it to `.agents/skills/`. Before running a helper, verify that the selected root contains both this skill and `ai-sdlc-shared-runtime`; block with the missing path if neither layout exists.

## 0.5 Feature State Machine

- Quality review does not advance lifecycle state by itself.
- Read `_ai_sdlc/state.toon` to understand the current stage and valid owner.
- `--state-check` is read-only; `--begin-state` and `--complete-state` are
  rejected by the report finalizer.
- Route accepted findings to the owning workflow for lifecycle changes.

## 0.6 Artifact Metadata And Metatags

- Markdown starts with `artifact_metadata` using schema
  `ai-sdlc-quality-report-metadata/v1`.
- Include `metatags` for `ai-sdlc`, `quality-lens`, selected lenses, and
  `evidence-backed`.
- Record the source artifact, registry version, feature, flow mode, and trace
  identifiers in metadata.

## 0.7 Specs Index

- Review the relevant `specs/_ai_sdlc/specs-index.toon` or
  `specs-refiniment/_ai_sdlc/specs-index.toon` before broad reads.
- Refresh `specs/specs-index.md` or `specs-refiniment/specs-index.md` only when
  the report is routed into that workspace and the owning workflow requires it.
- Do not use a quality report as a replacement for source requirements,
  decisions, tests, tasks, or state.

## References

- Read `references/quality-lenses.json` to select applicable lenses.
- Read `references/finding-contract.md` before creating or changing findings.
- Use `scripts/quality_lens_report.py` to list lenses, validate findings, and
  emit or atomically write the canonical report pair.

## Script Usage

```bash
python3 skills/ai-sdlc-quality-lenses/scripts/quality_lens_report.py --list-lenses --format markdown
python3 skills/ai-sdlc-quality-lenses/scripts/quality_lens_report.py --artifact specs/example/requirements.md --artifact-kind requirements --feature example --findings /tmp/findings.json --lens edge-case-hunt --emit --quick-flow
python3 skills/ai-sdlc-quality-lenses/scripts/quality_lens_report.py --artifact specs/example/design.md --artifact-kind design --feature example --findings /tmp/findings.json --write --full-flow
```

`--emit` prints one format without writes. `--write` creates both canonical
formats. Invalid or incomplete findings exit non-zero and produce no files.

## Purpose

Turn reusable critical-thinking modes into consistent, portable review
evidence instead of one-off prose that loses ownership and traceability.

## Inputs

- Read the source artifact and its direct trace sources.
- Select lenses by applicability and review risk.
- Create a JSON array conforming to `references/finding-contract.md`.
- Anchor evidence to an exact repository-relative path and positive line.

## Steps

1. Inspect the registry and select applicable lenses.
2. Read the source artifact plus targeted requirement, decision, test, or task
   evidence needed by those lenses.
3. Apply each lens independently; distinguish observed evidence from impact.
4. Create findings with stable IDs and all required contract fields.
5. Run the finalizer with `--emit` and correct every validation error.
6. Run `--write` only after owners and trace targets are credible.
7. Route open findings to the owning skill; preserve accepted, mitigated,
   rejected, and deferred resolution states in later reviews.

## Output Spec

The TOON schema `ai-sdlc-quality-report/v1` contains registry version, artifact,
artifact kind, feature, flow mode, selected lenses, summary counts, and findings
with `id`, `lens`, `evidence_path`, `evidence_line`, `evidence_detail`,
`severity`, `trace_targets`, `owner`, `resolution_status`, and `next_action`.

Quality gate:

- Pass when every finding uses a registered selected lens and contains all
  required evidence, traceability, ownership, state, and action fields.
- Fail when evidence is vague, a trace target is empty, a status is unknown,
  a severity is invalid, or a selected lens is not registered/applicable.

## Examples

Valid finding:

```json
{"id":"QL-001","lens":"edge-case-hunt","evidence":{"path":"specs/payments/requirements.md","line":88,"detail":"Timeout behavior is unspecified"},"severity":"high","trace_targets":["AC-004","TC-012"],"owner":"BA","resolution_status":"open","next_action":"Define timeout and retry acceptance behavior."}
```

Invalid counter-example: `The design feels risky.` It has no exact evidence,
trace target, owner, status, or executable next action.

## Edge Cases

- An empty findings array is valid and explicitly reports zero findings.
- Full flow selects only lenses applicable to the declared artifact kind.
- A finding may trace to multiple requirement, test, task, risk, or decision
  identifiers; preserve them as slash-separated values in TOON.
- Rejected and deferred findings still retain evidence and next action so the
  decision remains auditable.

## Scope Boundary

- Do not edit the reviewed artifact as part of report finalization.
- Do not accept, reject, or defer findings without the accountable owner.
- Do not use generic model opinion as evidence.
- Do not advance lifecycle state or weaken protected rigor gates.
- Use `$ai-sdlc-navigator` when the owning remediation workflow is unclear.
