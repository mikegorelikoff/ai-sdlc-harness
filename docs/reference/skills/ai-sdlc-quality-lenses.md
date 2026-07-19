---
title: Quality Lenses
description: Human-facing operating guide for ai-sdlc-quality-lenses, including inputs, authority, artifacts, modes, helpers, gates, recovery, and handoff.
---

# `ai-sdlc-quality-lenses`

AI SDLC reusable quality-lens workflow. Use when an AI assistant needs to challenge a requirement, design, plan, test strategy, change, or delivery artifact through pre-mortem, adversarial, edge-case, stakeholder-conflict, reversibility, abuse-case, operational-failure, or assumption lenses and finalize evidence-backed findings with ownership and traceability. Supports `--quick-flow` for selected high-value lenses and `--full-flow` for the complete applicable registry.

| Lifecycle position | Primary owner | Supporting roles | Module | Output |
| --- | --- | --- | --- | --- |
| Cross-lifecycle quality review | BA, QA, Dev, Delivery | PM, Architecture, Security | `core` | `quality-lens-report.md` and `_ai_sdlc/quality-lens-report.toon` |

## Why it exists

Apply reusable challenge lenses and finalize evidence-backed findings.

## Use it when

AI SDLC reusable quality-lens workflow. Use when an AI assistant needs to challenge a requirement, design, plan, test strategy, change, or delivery artifact through pre-mortem, adversarial, edge-case, stakeholder-conflict, reversibility, abuse-case, operational-failure, or assumption lenses and finalize evidence-backed findings with ownership and traceability. Supports `--quick-flow` for selected high-value lenses and `--full-flow` for the complete applicable registry.

If the correct entry point is still unclear, ask the read-only navigator first instead of guessing.

## Do not use it when

- Do not use a quality lens when the primary artifact is missing. Use its owning producer skill instead.
- Do not use a lens as formal approval. Use the accountable human review gate instead.


## Who is involved

- **Accountable/primary:** BA, QA, Dev, Delivery.
- **Supporting:** PM, Architecture, Security.
- **Agent:** follows this contract, reports assumptions and blockers, and cannot accept protected decisions for the humans above.

## Before you start

- One readable source artifact.
- One or more lens identifiers from `references/quality-lenses.json`.
- A feature or initiative identifier.
- An owner for every finding.

## Tell your agent

```text
Use ai-sdlc-quality-lenses for <target>.
Choose --quick-flow for bounded assumption-driven progress or --full-flow
for strict verification only as described below.
Read the required evidence,
produce or report `quality-lens-report.md` and `_ai_sdlc/quality-lens-report.toon`, preserve human approval boundaries,
and return blockers plus a complete ai-sdlc-handoff/v1.
```

This is an agent instruction, not a shell command. Terminal commands belong in the helper section.

## What the agent reads

- Read the source artifact and its direct trace sources.
- Select lenses by applicability and review risk.
- Create a JSON array conforming to `references/finding-contract.md`.
- Anchor evidence to an exact repository-relative path and positive line.

## What it may write

- Default human output: `<artifact-parent>/quality-lens-report.md`.
- Default machine output: `<artifact-parent>/_ai_sdlc/quality-lens-report.toon`.
- Use `--output-root` to route the pair to an owning feature directory.
- Keep the source artifact unchanged; reports are review evidence.

## Human checkpoints

- Ask only when the artifact, review objective, or accountable owner is ambiguous.
- Record uncertainty as a finding; do not invent evidence or trace targets.
- Treat a lens with no supported finding as a valid clean result.
- Do not silently convert a finding into a requirement, decision, or task.

Humans accept or reject material product, security, QA, policy, rollout, release, and destructive-action decisions; a complete agent handoff is evidence, not approval.

## Flow modes

- Support `--quick-flow` and `--full-flow`; full flow takes precedence.
- Quick flow uses the explicitly selected lenses, or the registry defaults.
- Full flow applies every lens whose `applies_to` includes the artifact kind.
- Both modes use the same finding schema and finalization gates.

## Deterministic helpers

| Helper | Purpose | Direct starting point | Repository effect |
| --- | --- | --- | --- |
| [`quality_lens_report.py`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-quality-lenses/scripts/quality_lens_report.py) | Validate and render reusable evidence-backed quality-lens reports. | `python3 skills/ai-sdlc-quality-lenses/scripts/quality_lens_report.py --help` | May write only through an explicit mutation mode; start with `--help`, check, preview, or emit. |

The owning agent normally runs these helpers. A human uses the direct starting point for diagnosis or reproduction after inspecting `--help` and repository policy.

### Contract-provided usage

```bash
python3 skills/ai-sdlc-quality-lenses/scripts/quality_lens_report.py --list-lenses --format markdown
python3 skills/ai-sdlc-quality-lenses/scripts/quality_lens_report.py --artifact specs/example/requirements.md --artifact-kind requirements --feature example --findings /tmp/findings.json --lens edge-case-hunt --emit --quick-flow
python3 skills/ai-sdlc-quality-lenses/scripts/quality_lens_report.py --artifact specs/example/design.md --artifact-kind design --feature example --findings /tmp/findings.json --write --full-flow
```

`--emit` prints one format without writes. `--write` creates both canonical
formats. Invalid or incomplete findings exit non-zero and produce no files.

## Success criteria

The TOON schema `ai-sdlc-quality-report/v1` contains registry version, artifact,
artifact kind, feature, flow mode, selected lenses, summary counts, and findings
with `id`, `lens`, `evidence_path`, `evidence_line`, `evidence_detail`,
`severity`, `trace_targets`, `owner`, `resolution_status`, and `next_action`.

Quality gate:

- Pass when every finding uses a registered selected lens and contains all
  required evidence, traceability, ownership, state, and action fields.
- Fail when evidence is vague, a trace target is empty, a status is unknown,
  a severity is invalid, or a selected lens is not registered/applicable.

## Blockers and recovery

- An empty findings array is valid and explicitly reports zero findings.
- Full flow selects only lenses applicable to the declared artifact kind.
- A finding may trace to multiple requirement, test, task, risk, or decision
  identifiers; preserve them as slash-separated values in TOON.
- Rejected and deferred findings still retain evidence and next action so the
  decision remains auditable.

On a blocker, preserve failed/stale evidence, name the accountable owner and exact missing input, then resume this skill or the earliest reopened producer. Never manufacture completion by editing derived state.

## Handoff

- Return selected lenses, finding counts by severity and status, blockers, and
  output paths directly in the Codex response.
- Before the final response, emit `ai-sdlc-handoff/v1` with `result`,
  `blockers`, `next_required`, and `next_optional`; every action includes
  `reason`, `command`, and `expected_artifact`.
- Do not create `summary.txt`, `*-summary.txt`, or unregistered review files.
- Never finalize a finding without evidence, severity, trace targets, owner,
  resolution status, and next action.

The downstream consumer rechecks artifacts and freshness; it does not trust a previous chat's completion claim.

## State, metadata, and indexes

??? info "Feature state"

    - Quality review does not advance lifecycle state by itself.
    - Read `_ai_sdlc/state.toon` to understand the current stage and valid owner.
    - `--state-check` is read-only; `--begin-state` and `--complete-state` are
      rejected by the report finalizer.
    - Route accepted findings to the owning workflow for lifecycle changes.

??? info "Artifact metadata"

    - Markdown starts with `artifact_metadata` using schema
      `ai-sdlc-quality-report-metadata/v1`.
    - Include `metatags` for `ai-sdlc`, `quality-lens`, selected lenses, and
      `evidence-backed`.
    - Record the source artifact, registry version, feature, flow mode, and trace
      identifiers in metadata.

??? info "Specs index"

    - Review the relevant `specs/_ai_sdlc/specs-index.toon` or
      `specs-refiniment/_ai_sdlc/specs-index.toon` before broad reads.
    - Refresh `specs/specs-index.md` or `specs-refiniment/specs-index.md` only when
      the report is routed into that workspace and the owning workflow requires it.
    - Do not use a quality report as a replacement for source requirements,
      decisions, tests, tasks, or state.

## Example

Valid finding:

```json
{"id":"QL-001","lens":"edge-case-hunt","evidence":{"path":"specs/payments/requirements.md","line":88,"detail":"Timeout behavior is unspecified"},"severity":"high","trace_targets":["AC-004","TC-012"],"owner":"BA","resolution_status":"open","next_action":"Define timeout and retry acceptance behavior."}
```

Invalid counter-example: `The design feels risky.` It has no exact evidence,
trace target, owner, status, or executable next action.

## Source contract

This page is generated from [`skills/ai-sdlc-quality-lenses/SKILL.md`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-quality-lenses/SKILL.md). Edit the source contract, rerun the catalog generator, and review both changes together; never hand-edit this page.

[Back to the skill catalog](../skills.md) · [Script reference](../scripts.md) · [Choose a workflow](../../flows/index.md)
