---
title: TOON-first agent artifacts
description: Why agents read complete TOON projections while JSON remains at interoperability boundaries.
---

# TOON-first agent artifacts

The harness uses TOON as the default representation for records consumed by AI
agents. Every new durable control-plane record has a complete `.toon`
projection: no fields are replaced with counts, flattened summaries, or
prose-only explanations.

This follows the [TOON specification 3.3](https://toonformat.dev/reference/spec)
for nested objects, primitive arrays, tabular uniform-object arrays, expanded
non-uniform arrays, scalar values, and quoting. One shared deterministic encoder
keeps output consistent across capabilities.

## Where JSON remains

JSON is retained where its ecosystem support is the actual requirement:

- JSON Schema defines strict validation and compatibility contracts.
- JSON input remains available for external tools and authored policy records.
- JSONL provides the append-only, hash-chained runtime journal.
- Exact JSON recovery projections make deterministic replay comparisons simple.

These are interoperability and audit boundaries, not the default agent read
path. CLI commands default or opt into `--format toon`, and generated records
write `.toon` beside JSON whenever both audiences need the same data.

## Projection invariants

A JSON/TOON pair represents the same complete logical record. Fingerprints are
calculated from the normalized logical data, so changing presentation does not
change identity. Generated TOON is deterministic, newline-terminated, and
preserves nested evidence, gates, reasons, source anchors, budgets, and task
state.

Human review remains Markdown-first. Agents read TOON first. Integrations may
read JSON, and validators use the JSON schemas.

## Durable TOON paths

The TOON-first control plane includes:

- change set, delta set, apply preview, approval, and recovery records;
- delivery graph and evidence ledger;
- policy resolution and fingerprint-addressed decisions;
- repository topology and task context packs;
- resumable runtime state and full TOON CLI results.

The runtime journal intentionally stays `journal.jsonl`; its replayed current
state is available as complete `state.toon`.
