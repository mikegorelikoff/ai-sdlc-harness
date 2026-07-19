---
title: Evidence Council
description: Human-facing operating guide for ai-sdlc-evidence-council, including inputs, authority, artifacts, modes, helpers, gates, recovery, and handoff.
---

# `ai-sdlc-evidence-council`

Optional AI SDLC evidence-council workflow. Use when an AI assistant needs to review a high-impact topic through several explicit perspectives, orchestrate simulated lenses or truly independent reviewer executions, and synthesize evidence-backed agreements, conflicts, proposals, owners, and unresolved questions without allowing panel members to rewrite authoritative artifacts. Supports `--quick-flow` for labeled simulated review and `--full-flow` for stricter panel and evidence coverage.

| Lifecycle position | Primary owner | Supporting roles | Module | Output |
| --- | --- | --- | --- | --- |
| Cross-lifecycle high-impact review | Delivery, Architecture, QA, Dev, BA | PM, UX, Research, Security | `evidence-council` | `evidence-council.md` and `_ai_sdlc/evidence-council.toon` |

## Why it exists

Combine multiple evidence perspectives while preserving authority.

## Use it when

Optional AI SDLC evidence-council workflow. Use when an AI assistant needs to review a high-impact topic through several explicit perspectives, orchestrate simulated lenses or truly independent reviewer executions, and synthesize evidence-backed agreements, conflicts, proposals, owners, and unresolved questions without allowing panel members to rewrite authoritative artifacts. Supports `--quick-flow` for labeled simulated review and `--full-flow` for stricter panel and evidence coverage.

If the correct entry point is still unclear, ask the read-only navigator first instead of guessing.

## Do not use it when

- Do not use it as authoritative approval or sign-off. Use the accountable human gate instead.
- Do not use it to gather missing sources. Use `ai-sdlc-research` instead.


## Who is involved

- **Accountable/primary:** Delivery, Architecture, QA, Dev, BA.
- **Supporting:** PM, UX, Research, Security.
- **Agent:** follows this contract, reports assumptions and blockers, and cannot accept protected decisions for the humans above.

## Before you start

- Owning feature root and review topic.
- Council input using `ai-sdlc-evidence-council-input/v1`.
- Named authoritative artifact owner and exact evidence anchors.
- Host support for isolated reviewer executions when mode is `independent`.

## Tell your agent

```text
Use ai-sdlc-evidence-council for <target>.
Choose --quick-flow for bounded assumption-driven progress or --full-flow
for strict verification only as described below.
Read the required evidence,
produce or report `evidence-council.md` and `_ai_sdlc/evidence-council.toon`, preserve human approval boundaries,
and return blockers plus a complete ai-sdlc-handoff/v1.
```

This is an agent instruction, not a shell command. Terminal commands belong in the helper section.

## What the agent reads

- Name the authority owner and authoritative artifacts before reviewer work.
- Give reviewers bounded roles and isolated execution IDs in independent mode.
- Anchor evidence to feature-relative paths and positive lines.
- Synthesize agreements, conflicts, proposals, and unresolved questions separately.

## What it may write

- Write `<feature-root>/evidence-council.md`.
- Write `<feature-root>/_ai_sdlc/evidence-council.toon`.
- Treat all paths in `authority.authoritative_artifacts` as read-only.
- Route accepted proposals later through the artifact-owning workflow.

## Human checkpoints

- Ask when review question, authority owner, panel scope, or decision boundary is unclear.
- Label simulated and independent modes exactly; never imply independence.
- Preserve reviewer conflict and uncertainty instead of forcing consensus.
- Do not infer acceptance from reviewer count or apparent agreement.

Humans accept or reject material product, security, QA, policy, rollout, release, and destructive-action decisions; a complete agent handoff is evidence, not approval.

## Flow modes

- Support `--quick-flow` and `--full-flow`; full flow takes precedence.
- Quick flow may use labeled simulated reviewers and focused evidence.
- Full flow requires at least three reviewers, two roles, and populated evidence.
- Independent mode requires unique independent execution IDs for every reviewer.

## Deterministic helpers

| Helper | Purpose | Direct starting point | Repository effect |
| --- | --- | --- | --- |
| [`evidence_council.py`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-evidence-council/scripts/evidence_council.py) | Validate and route authority-safe evidence council reports. | `python3 skills/ai-sdlc-evidence-council/scripts/evidence_council.py --help` | May write only through an explicit mutation mode; start with `--help`, check, preview, or emit. |

The owning agent normally runs these helpers. A human uses the direct starting point for diagnosis or reproduction after inspecting `--help` and repository policy.

### Contract-provided usage

```bash
python3 skills/ai-sdlc-evidence-council/scripts/evidence_council.py specs/payments --input /tmp/council.json --emit --quick-flow
python3 skills/ai-sdlc-evidence-council/scripts/evidence_council.py specs/payments --input /tmp/council.json --write --full-flow --format toon
```

## Success criteria

`ai-sdlc-evidence-council/v1` contains topic, mode, authority, panel, evidence,
agreements, conflicts with positions, proposals, and unresolved questions.

Quality gate:

- Pass when mode is honest, every synthesis row cites registered evidence and
  reviewers, conflicts preserve positions, and actionable rows name owner/next action.
- Full flow fails below three reviewers, two roles, or one evidence anchor.

## Blockers and recovery

- No consensus is a valid result; preserve owned unresolved questions.
- A reviewer may support one agreement and one side of a conflict.
- A proposal may be deferred or rejected but cannot be marked accepted by council.
- If independent execution fails midway, report partial/blocked rather than simulating missing votes.

On a blocker, preserve failed/stale evidence, name the accountable owner and exact missing input, then resume this skill or the earliest reopened producer. Never manufacture completion by editing derived state.

## Handoff

- Return mode, panel identity, agreements, conflicts, proposals, unresolved
  questions, blockers, and output paths directly in the Codex response.
- Before the final response, emit `ai-sdlc-handoff/v1` with `result`,
  `blockers`, `next_required`, and `next_optional`; every action includes
  `reason`, `command`, and `expected_artifact`.
- Do not create `summary.txt`, `*-summary.txt`, or panel-authored source patches.
- Every synthesis row requires evidence and named contributing reviewers.

The downstream consumer rechecks artifacts and freshness; it does not trust a previous chat's completion claim.

## State, metadata, and indexes

??? info "Feature state"

    - Read `<feature-root>/_ai_sdlc/state.toon` before council orchestration.
    - Council is optional review evidence and does not add a core lifecycle stage.
    - `--state-check` is read-only; `--begin-state` and `--complete-state` are rejected.
    - Only owning lifecycle skills can change state or authoritative artifacts.

??? info "Artifact metadata"

    - Markdown starts with `artifact_metadata` using schema
      `ai-sdlc-evidence-council-metadata/v1`.
    - Include `metatags` for `ai-sdlc`, `evidence-council`, the execution mode, and `review`.
    - Record feature, workspace, flow mode, authority owner, evidence traces, and status.

??? info "Specs index"

    - Read the relevant `specs/_ai_sdlc/specs-index.toon` or
      `specs-refiniment/_ai_sdlc/specs-index.toon` before targeted evidence reads.
    - Refresh matching `specs/specs-index.md` or
      `specs-refiniment/specs-index.md` only after the final report write.
    - Never update indexes for panel scratch outputs.

## Example

Valid independent panel rows use three different `execution_id` values produced
by actual isolated runs. Three role labels generated in one response are valid
only as `simulated`, never `independent`.

## Source contract

This page is generated from [`skills/ai-sdlc-evidence-council/SKILL.md`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-evidence-council/SKILL.md). Edit the source contract, rerun the catalog generator, and review both changes together; never hand-edit this page.

[Back to the skill catalog](../skills.md) · [Script reference](../scripts.md) · [Choose a workflow](../../flows/index.md)
