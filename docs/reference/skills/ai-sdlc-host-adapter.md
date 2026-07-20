---
title: Host Adapter
description: Human-facing operating guide for ai-sdlc-host-adapter, including inputs, authority, artifacts, modes, helpers, gates, recovery, and handoff.
---

# `ai-sdlc-host-adapter`

| Lifecycle position | Primary owner | Supporting roles | Module | Output |
| --- | --- | --- | --- | --- |
| Portable execution handoff | Dev, Delivery, Architecture | Security, QA | `core` | `_ai_sdlc/adapters/<adapter-id>/negotiation.{toon,json,md}` |

## Why it exists

Preserve workflow semantics across hosts with explicit mappings and safe fallbacks.

## Use it when

AI SDLC host adapter and capability negotiation workflow. Use when an AI assistant needs to validate a host adapter manifest, map portable workflow operations to host-native operations, negotiate capabilities and limits, select deterministic semantic-preserving fallbacks, or explain why a host cannot run a plan. Supports `--quick-flow` and `--full-flow`.

If the correct entry point is still unclear, ask the read-only navigator first instead of guessing.

## Do not use it when

- Do not use it before a validated workflow declares the host capability it needs. Use `ai-sdlc-workflow` to define that contract instead.


## Who is involved

The summary table above names the primary and supporting human roles for this capability.
- **Agent:** follows this contract, reports assumptions and blockers, and cannot accept protected decisions for the humans above.

## Before you start

- Versioned adapter manifest and capability request.
- Exact portable operations, required capabilities, isolation need, and desired concurrency.

## Tell your agent

```text
Use ai-sdlc-host-adapter for <target>.
Choose --quick-flow for bounded assumption-driven progress or --full-flow
for strict verification only as described below.
Read the required evidence,
produce or report `_ai_sdlc/adapters/<adapter-id>/negotiation.{toon,json,md}`, preserve human approval boundaries,
and return blockers plus a complete ai-sdlc-handoff/v1.
```

This is an agent instruction, not a shell command. Terminal commands belong in the helper section.

## What the agent reads

- Versioned adapter manifest and capability request.
- Exact portable operations, required capabilities, isolation need, and desired concurrency.

## What it may write

- Write negotiations only below `_ai_sdlc/adapters/<adapter-id>/`.
- Keep manifests in repository-owned visible paths or skill conformance fixtures.
- Never mutate a manifest during negotiation.

## Human checkpoints

- Ask when required semantics or host operation identity is ambiguous.
- Reject unknown fields, duplicate operations, invalid API ranges, undeclared
  capabilities, or non-equivalent native mappings.
- Never infer shell, filesystem, network, isolation, concurrency, or approval support.

Humans accept or reject material product, security, QA, policy, rollout, release, and destructive-action decisions; a complete agent handoff is evidence, not approval.

## Flow modes

- Support `--quick-flow` and `--full-flow`; full flow takes precedence.
- Both modes use identical compatibility and fallback rules.
- Full flow reviews every mapping, limit, fallback, and unsupported requirement.

## Deterministic helpers

Paths beginning with `skills/` below are canonical **source-checkout** forms for maintainers and CI. In a consumer repository, normally tell the installed skill to act; for human diagnosis, use the matching project-scoped `.agents/skills/<skill>/...` path reported by your host. Do not expect source-only `skills/_shared` to exist after installation.

| Helper | Purpose | Direct starting point | Repository effect |
| --- | --- | --- | --- |
| [`adapter.py`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-host-adapter/scripts/adapter.py) | Validate host adapters and negotiate portable operations safely. | `python3 skills/ai-sdlc-host-adapter/scripts/adapter.py --help` | May write only through an explicit mutation mode; start with `--help`, check, preview, or emit. |

The owning agent normally runs these helpers. A human uses the direct starting point for diagnosis or reproduction after inspecting `--help` and repository policy.

### Contract-provided usage

```bash
python3 skills/ai-sdlc-host-adapter/scripts/adapter.py . --adapter adapter.json --validate
python3 skills/ai-sdlc-host-adapter/scripts/adapter.py . --adapter adapter.json --negotiate --request request.json --write
```

## Success criteria

The negotiation records native and fallback mappings, unsupported operations,
missing capabilities, requested and effective limits, compatibility, reasons,
and deterministic fingerprints.

Quality gate:

- Pass only when every required operation and capability has an equivalent
  mapping or registered semantic-preserving fallback.
- Fail closed when host behavior would change workflow semantics.

## Blockers and recovery

- Ask when required semantics or host operation identity is ambiguous.
- Reject unknown fields, duplicate operations, invalid API ranges, undeclared
  capabilities, or non-equivalent native mappings.
- Never infer shell, filesystem, network, isolation, concurrency, or approval support.

On a blocker, preserve failed/stale evidence, name the accountable owner and exact missing input, then resume this skill or the earliest reopened producer. Never manufacture completion by editing derived state.

## Handoff

- Default to complete TOON with mappings, missing requirements, fallbacks,
  effective limits, compatibility, source fingerprint, and result fingerprint.
- Return summaries directly in the Codex response.
- Emit `ai-sdlc-handoff/v1` with `result`, `blockers`, `next_required`, and
  `next_optional`; actions include `reason`, `command`, and `expected_artifact`.
- Do not create `summary.txt`, `*-summary.txt`, or another standalone summary file.

The downstream consumer rechecks artifacts and freshness; it does not trust a previous chat's completion claim.

## State, metadata, and indexes

??? info "Feature state"

    - Read owning feature `_ai_sdlc/state.toon` before execution handoff.
    - Negotiation does not advance feature or runtime state.

??? info "Artifact metadata"

    - Related Markdown uses canonical `artifact_metadata` and `metatags`.
    - Machine records use versioned adapter, request, and negotiation schemas.

??? info "Specs index"

    - Read `_ai_sdlc/specs-index.toon` first and use `specs-index.md` for human review.
    - Negotiation does not refresh either index.

## Example

```bash
python3 skills/ai-sdlc-host-adapter/scripts/adapter.py . --adapter adapter.json --validate
python3 skills/ai-sdlc-host-adapter/scripts/adapter.py . --adapter adapter.json --negotiate --request request.json --write
```

## Source contract

This page is generated from [`skills/ai-sdlc-host-adapter/SKILL.md`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-host-adapter/SKILL.md). Edit the source contract, rerun the catalog generator, and review both changes together; never hand-edit this page.

[Back to the skill catalog](../skills.md) · [Script reference](../scripts.md) · [Choose a workflow](../../flows/index.md)
