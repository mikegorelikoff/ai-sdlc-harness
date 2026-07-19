---
title: Delivery Graph
description: Human-facing operating guide for ai-sdlc-delivery-graph, including inputs, authority, artifacts, modes, helpers, gates, recovery, and handoff.
---

# `ai-sdlc-delivery-graph`

AI SDLC repository delivery-graph and evidence-freshness workflow. Use when an AI assistant needs to index lifecycle traceability, resolve end-to-end paths, report gaps or orphans, register evidence identity, propagate stale dependencies, or calculate fresh evidence coverage. Supports `--quick-flow` for deterministic local analysis and `--full-flow` for strict trace and evidence review.

| Lifecycle position | Primary owner | Supporting roles | Module | Output |
| --- | --- | --- | --- | --- |
| Traceability and readiness | Delivery, Dev, QA, Architecture | PM, BA, Security, Release | `core` | complete `_ai_sdlc/delivery-graph.toon` for agents, plus `_ai_sdlc/delivery-graph.json` for schema/interoperability and `_ai_sdlc/delivery-graph.md` for human review when `--write` is requested |

## Why it exists

Build a deterministic repository-wide lifecycle graph and answer trace, gap, coverage, and orphan questions from stable evidence anchors.

## Use it when

AI SDLC repository delivery-graph and evidence-freshness workflow. Use when an AI assistant needs to index lifecycle traceability, resolve end-to-end paths, report gaps or orphans, register evidence identity, propagate stale dependencies, or calculate fresh evidence coverage. Supports `--quick-flow` for deterministic local analysis and `--full-flow` for strict trace and evidence review.

If the correct entry point is still unclear, ask the read-only navigator first instead of guessing.

## Do not use it when

- Do not use it to invent missing requirements or delivery artifacts. Use the owning producer skill instead, then rebuild the graph.


## Who is involved

- **Accountable/primary:** Delivery, Dev, QA, Architecture.
- **Supporting:** PM, BA, Security, Release.
- **Agent:** follows this contract, reports assumptions and blockers, and cannot accept protected decisions for the humans above.

## Before you start

- Repository root containing lifecycle Markdown and, optionally, Git history.
- A stable trace ID or graph node ID for path queries.
- Explicit structured trace lines when a relationship cannot be derived safely.

## Tell your agent

```text
Use ai-sdlc-delivery-graph for <target>.
Choose --quick-flow for bounded assumption-driven progress or --full-flow
for strict verification only as described below.
Read the required evidence,
produce or report complete `_ai_sdlc/delivery-graph.toon` for agents, plus `_ai_sdlc/delivery-graph.json` for schema/interoperability and `_ai_sdlc/delivery-graph.md` for human review when `--write` is requested, preserve human approval boundaries,
and return blockers plus a complete ai-sdlc-handoff/v1.
```

This is an agent instruction, not a shell command. Terminal commands belong in the helper section.

## What the agent reads

- Stable trace identifiers in lifecycle Markdown.
- `Refs:` lines or co-located declaration references.
- Optional explicit `Component: <path> -> <trace-id>` and
  `Evidence: <path> -> <trace-id>` links.
- Conventional commit bodies containing `Spec:` and `Task:` and annotated Git
  tags for release nodes.

## What it may write

- Write generated graph data only below repository `_ai_sdlc/`.
- Keep versioned schemas and interpretation rules in this skill package.
- Preserve repository-relative evidence paths and one-based source line numbers.

## Human checkpoints

- Report ambiguous short IDs with all matching scoped node IDs.
- Never invent an edge because two terms look semantically similar.
- Treat missing links as gaps or orphans instead of guessing intent.

Humans accept or reject material product, security, QA, policy, rollout, release, and destructive-action decisions; a complete agent handoff is evidence, not approval.

## Flow modes

- Support `--quick-flow` and `--full-flow`; full flow takes precedence.
- Both modes rebuild from current authoritative inputs before answering.
- Full flow requires reviewers to resolve every reported ambiguity and high-value
  requirement coverage gap before claiming readiness.

## Deterministic helpers

Paths beginning with `skills/` below are canonical **source-checkout** forms for maintainers and CI. In a consumer repository, normally tell the installed skill to act; for human diagnosis, use the matching project-scoped `.agents/skills/<skill>/...` path reported by your host. Do not expect source-only `skills/_shared` to exist after installation.

| Helper | Purpose | Direct starting point | Repository effect |
| --- | --- | --- | --- |
| [`delivery_graph.py`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-delivery-graph/scripts/delivery_graph.py) | Build and query a deterministic repository delivery graph. | `python3 skills/ai-sdlc-delivery-graph/scripts/delivery_graph.py --help` | May write only through an explicit mutation mode; start with `--help`, check, preview, or emit. |
| [`evidence_ledger.py`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-delivery-graph/scripts/evidence_ledger.py) | Build a deterministic dependency-aware evidence freshness ledger. | `python3 skills/ai-sdlc-delivery-graph/scripts/evidence_ledger.py --help` | May write only through an explicit mutation mode; start with `--help`, check, preview, or emit. |

The owning agent normally runs these helpers. A human uses the direct starting point for diagnosis or reproduction after inspecting `--help` and repository policy.

### Contract-provided usage

```bash
python3 skills/ai-sdlc-delivery-graph/scripts/delivery_graph.py . --index --write --format toon --quick-flow
python3 skills/ai-sdlc-delivery-graph/scripts/delivery_graph.py . --trace AC-004 --to T006 --format toon
python3 skills/ai-sdlc-delivery-graph/scripts/delivery_graph.py . --gaps --format markdown
python3 skills/ai-sdlc-delivery-graph/scripts/delivery_graph.py . --orphans --format toon
python3 skills/ai-sdlc-delivery-graph/scripts/evidence_ledger.py . --index --as-of 2026-07-19 --write --format toon
python3 skills/ai-sdlc-delivery-graph/scripts/evidence_ledger.py . --coverage --as-of 2026-07-19 --format toon
python3 skills/ai-sdlc-delivery-graph/scripts/evidence_ledger.py . --stale --as-of 2026-07-19 --format markdown
```

## Success criteria

The graph contains sorted nodes, edges, gaps, orphans, coverage counters, source
hashes, and fingerprints. Rebuilding identical inputs produces byte-identical
TOON, JSON, and Markdown.

The TOON/JSON evidence ledger contains recalculated file identities, resolved subjects,
freshness states, reason codes, upstream state, stale paths, and fresh-only
requirement coverage.

Quality gate:

- Pass when all node and edge evidence resolves, identities are unambiguous,
  fingerprints recompute, and required coverage gaps are understood.
- Fail when an explicit query is absent or ambiguous, an edge endpoint is
  missing, or generated output drifts from current authoritative inputs.

## Blockers and recovery

- The same `AC-001` in two features is two nodes and requires a scoped query.
- A reference without a local declaration still becomes a placeholder node and
  is reported as an orphan or coverage gap.
- Git-less fixture directories still produce valid lifecycle graphs.
- Generated graph files never become their own inputs.
- Evidence dependency cycles, duplicate IDs, ambiguous subjects, and unknown
  upstream evidence fail closed.

On a blocker, preserve failed/stale evidence, name the accountable owner and exact missing input, then resume this skill or the earliest reopened producer. Never manufacture completion by editing derived state.

## Handoff

- Report the graph fingerprint, node and edge counts, source fingerprint,
  coverage, gaps, and orphans.
- Return query paths as ordered node and edge evidence, not prose-only claims.
- Return the validation and handoff summary directly in the Codex response.
- Emit `ai-sdlc-handoff/v1` with `result`, `blockers`, `next_required`, and
  `next_optional`; actions include `reason`, `command`, and `expected_artifact`.
- Do not create `summary.txt`, `*-summary.txt`, or another standalone summary file.
- Do not create ad hoc summaries outside the canonical graph outputs.

The downstream consumer rechecks artifacts and freshness; it does not trust a previous chat's completion claim.

## State, metadata, and indexes

??? info "Feature state"

    - Graph indexing is read-only with respect to feature lifecycle state.
    - Read canonical `_ai_sdlc/state.toon` before interpreting feature status; do
      not create a feature-local `state.toon` or change its sequencing.
    - A graph gap may block a later gate but cannot advance or reopen state itself.

??? info "Artifact metadata"

    - Node and edge records use `ai-sdlc-delivery-node/v1` and
      `ai-sdlc-delivery-edge/v1`.
    - The aggregate uses `ai-sdlc-delivery-graph/v1` and deterministic SHA-256
      fingerprints derived from normalized content.
    - Evidence producers use `ai-sdlc-evidence-source/v1`; generated freshness
      records and ledgers use `ai-sdlc-evidence-record/v1` and
      `ai-sdlc-evidence-ledger/v1`.
    - Source Markdown participates through canonical `artifact_metadata` and
      `metatags`; graph output does not replace or rewrite that metadata.

??? info "Specs index"

    - Read canonical `_ai_sdlc/specs-index.toon` first and use `specs-index.md` for
      human discovery across implementation and refinement workspaces.
    - Scope short trace IDs by feature directory to prevent cross-feature identity
      collisions.
    - Do not mutate either specs index during graph generation.

## Example

`TC-004 / AC-004` declares a test and creates a `verifies` edge to the
acceptance criterion. A following `Refs: AC-004` under `T006` creates a task
`traces-to` edge. A commit with `Task: T006` creates an `implements` edge.

## Source contract

This page is generated from [`skills/ai-sdlc-delivery-graph/SKILL.md`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-delivery-graph/SKILL.md). Edit the source contract, rerun the catalog generator, and review both changes together; never hand-edit this page.

[Back to the skill catalog](../skills.md) · [Script reference](../scripts.md) · [Choose a workflow](../../flows/index.md)
