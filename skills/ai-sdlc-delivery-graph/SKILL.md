---
name: ai-sdlc-delivery-graph
description: AI SDLC repository delivery-graph and evidence-freshness workflow. Use when an AI assistant needs to index lifecycle traceability, resolve end-to-end paths, report gaps or orphans, register evidence identity, propagate stale dependencies, or calculate fresh evidence coverage. Supports `--quick-flow` for deterministic local analysis and `--full-flow` for strict trace and evidence review.
---

# ai-sdlc-delivery-graph: Repository Traceability

> Internal AI SDLC skill, not client-facing by default.
> Every rule below is important to follow. None of it can be skipped.
> The graph is a generated projection; repository artifacts and Git remain authoritative.

## 0. Skill Card

- Skill name: `ai-sdlc-delivery-graph`
- Primary audience: Delivery, Dev, QA, Architecture
- Supporting audience: PM, BA, Security, Release
- Audience tags: Delivery, Dev, QA, Architecture, BA
- SDLC stage: Traceability and readiness
- Purpose: Build a deterministic repository-wide lifecycle graph and answer
  trace, gap, coverage, and orphan questions from stable evidence anchors.
- Output: `_ai_sdlc/delivery-graph.toon`, `_ai_sdlc/delivery-graph.json`, and
  `_ai_sdlc/delivery-graph.md` when `--write` is requested

### 0.1 Required Inputs

- Repository root containing lifecycle Markdown and, optionally, Git history.
- A stable trace ID or graph node ID for path queries.
- Explicit structured trace lines when a relationship cannot be derived safely.

### 0.2 Clarification Rules

- Report ambiguous short IDs with all matching scoped node IDs.
- Never invent an edge because two terms look semantically similar.
- Treat missing links as gaps or orphans instead of guessing intent.

### 0.2.1 Flow Mode Flags

- Support `--quick-flow` and `--full-flow`; full flow takes precedence.
- Both modes rebuild from current authoritative inputs before answering.
- Full flow requires reviewers to resolve every reported ambiguity and high-value
  requirement coverage gap before claiming readiness.

### 0.3 Output Rules

- Report the graph fingerprint, node and edge counts, source fingerprint,
  coverage, gaps, and orphans.
- Return query paths as ordered node and edge evidence, not prose-only claims.
- Return the validation and handoff summary directly in the Codex response.
- Do not create `summary.txt`, `*-summary.txt`, or another standalone summary file.
- Do not create ad hoc summaries outside the canonical graph outputs.

### 0.4 Artifact Routing

- Write generated graph data only below repository `_ai_sdlc/`.
- Keep versioned schemas and interpretation rules in this skill package.
- Preserve repository-relative evidence paths and one-based source line numbers.

## 0.5 Feature State Machine

- Graph indexing is read-only with respect to feature lifecycle state.
- Read canonical `_ai_sdlc/state.toon` before interpreting feature status; do
  not create a feature-local `state.toon` or change its sequencing.
- A graph gap may block a later gate but cannot advance or reopen state itself.

## 0.6 Artifact Metadata And Metatags

- Node and edge records use `ai-sdlc-delivery-node/v1` and
  `ai-sdlc-delivery-edge/v1`.
- The aggregate uses `ai-sdlc-delivery-graph/v1` and deterministic SHA-256
  fingerprints derived from normalized content.
- Evidence producers use `ai-sdlc-evidence-source/v1`; generated freshness
  records and ledgers use `ai-sdlc-evidence-record/v1` and
  `ai-sdlc-evidence-ledger/v1`.
- Source Markdown participates through canonical `artifact_metadata` and
  `metatags`; graph output does not replace or rewrite that metadata.

## 0.7 Specs Index

- Read canonical `_ai_sdlc/specs-index.toon` first and use `specs-index.md` for
  human discovery across implementation and refinement workspaces.
- Scope short trace IDs by feature directory to prevent cross-feature identity
  collisions.
- Do not mutate either specs index during graph generation.

## References

- Read `references/delivery-graph-contract.md` before interpreting nodes,
  edges, gaps, or query paths.
- Use `references/delivery-node.schema.json`,
  `references/delivery-edge.schema.json`, and
  `references/delivery-graph.schema.json` for machine contracts.
- Use `scripts/delivery_graph.py` for deterministic indexing and queries.
- Read `references/evidence-ledger-contract.md` before registering or judging
  evidence freshness. Validate inputs and outputs with
  `references/evidence-source.schema.json` and
  `references/evidence-ledger.schema.json`.
- Use `scripts/evidence_ledger.py` to recalculate current file identities,
  propagate stale state, and query fresh coverage.

## Script Usage

```bash
python3 skills/ai-sdlc-delivery-graph/scripts/delivery_graph.py . --index --write --format toon --quick-flow
python3 skills/ai-sdlc-delivery-graph/scripts/delivery_graph.py . --trace AC-004 --to T006 --format json
python3 skills/ai-sdlc-delivery-graph/scripts/delivery_graph.py . --gaps --format markdown
python3 skills/ai-sdlc-delivery-graph/scripts/delivery_graph.py . --orphans --format toon
python3 skills/ai-sdlc-delivery-graph/scripts/evidence_ledger.py . --index --as-of 2026-07-19 --write --format toon
python3 skills/ai-sdlc-delivery-graph/scripts/evidence_ledger.py . --coverage --as-of 2026-07-19 --format json
python3 skills/ai-sdlc-delivery-graph/scripts/evidence_ledger.py . --stale --as-of 2026-07-19 --format markdown
```

## Purpose

Make lifecycle traceability executable so reviewers can prove why work exists,
what verifies it, what shipped it, and where delivery evidence is missing.

## Inputs

- Stable trace identifiers in lifecycle Markdown.
- `Refs:` lines or co-located declaration references.
- Optional explicit `Component: <path> -> <trace-id>` and
  `Evidence: <path> -> <trace-id>` links.
- Conventional commit bodies containing `Spec:` and `Task:` and annotated Git
  tags for release nodes.

## Steps

1. Scan canonical lifecycle Markdown and hash every input file.
2. Scope declared and referenced trace IDs to their feature.
3. Add only evidence-backed semantic edges and Git task/release edges.
4. Normalize and fingerprint nodes, edges, sources, gaps, and coverage.
5. Inspect orphan and missing-coverage results.
6. Run trace queries using a scoped node ID when a short ID is ambiguous.
7. Write generated projections only when explicitly requested.
8. Register evidence with captured artifact and dependency hashes, expiry, and
   upstream evidence identities.
9. Rebuild the ledger for an explicit `as_of` date; resolve missing, changed,
   expired, unknown, ambiguous, or cyclic evidence before claiming coverage.

## Output Spec

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

## Examples

`TC-004 / AC-004` declares a test and creates a `verifies` edge to the
acceptance criterion. A following `Refs: AC-004` under `T006` creates a task
`traces-to` edge. A commit with `Task: T006` creates an `implements` edge.

## Edge Cases

- The same `AC-001` in two features is two nodes and requires a scoped query.
- A reference without a local declaration still becomes a placeholder node and
  is reported as an orphan or coverage gap.
- Git-less fixture directories still produce valid lifecycle graphs.
- Generated graph files never become their own inputs.
- Evidence dependency cycles, duplicate IDs, ambiguous subjects, and unknown
  upstream evidence fail closed.

## Scope Boundary

- Do not infer semantic similarity, ownership, or policy decisions.
- Do not mark evidence fresh without matching current hashes, expiry, and all
  upstream evidence states.
- Do not edit lifecycle artifacts to make a graph appear complete.
- Do not treat graph generation as approval, validation evidence, or release.
- Do not overwrite producer manifests or evidence artifacts during indexing.
