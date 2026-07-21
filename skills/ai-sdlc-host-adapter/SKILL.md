---
name: ai-sdlc-host-adapter
description: AI SDLC host adapter and capability negotiation workflow. Use when an AI assistant needs to validate a host adapter manifest, map portable workflow operations to host-native operations, negotiate capabilities and limits, select deterministic semantic-preserving fallbacks, or explain why a host cannot run a plan. Supports `--quick-flow` and `--full-flow`.
---

# ai-sdlc-host-adapter: Portable Host Negotiation

> Internal AI SDLC skill, not client-facing by default.
> Negotiation describes host behavior; it never invokes the host.

## 0. Skill Card

- Skill name: `ai-sdlc-host-adapter`
- Primary audience: Dev, Delivery, Architecture
- Supporting audience: Security, QA
- Audience tags: Dev, Delivery, Architecture, Security
- SDLC stage: Portable execution handoff
- Purpose: Preserve workflow semantics across hosts with explicit mappings and safe fallbacks.
- Output: `_ai_sdlc/adapters/<adapter-id>/negotiation.{toon,json,md}`

### 0.1 Required Inputs

- Versioned adapter manifest and capability request.
- Exact portable operations, required capabilities, isolation need, and desired concurrency.

### 0.2 Clarification Rules

- Ask when required semantics or host operation identity is ambiguous.
- Reject unknown fields, duplicate operations, invalid API ranges, undeclared
  capabilities, or non-equivalent native mappings.
- Never infer shell, filesystem, network, isolation, concurrency, or approval support.

### 0.2.1 Flow Mode Flags

- Support `--quick-flow` and `--full-flow`; full flow takes precedence.
- Both modes use identical compatibility and fallback rules.
- Full flow reviews every mapping, limit, fallback, and unsupported requirement.

### 0.3 Output Rules

- Default to complete TOON with mappings, missing requirements, fallbacks,
  effective limits, compatibility, source fingerprint, and result fingerprint.
- Return summaries directly in the active agent response.
- Emit `ai-sdlc-handoff/v1` with `result`, `blockers`, `next_required`, and
  `next_optional`; actions include `reason`, `command`, and `expected_artifact`.
- Do not create `summary.txt`, `*-summary.txt`, or another standalone summary file.

### 0.4 Artifact Routing

- Write negotiations only below `_ai_sdlc/adapters/<adapter-id>/`.
- Keep manifests in repository-owned visible paths or skill conformance fixtures.
- Never mutate a manifest during negotiation.

## 0.4.1 Runtime Path Resolution

- Treat `skills/` in commands as a logical skill root. In a harness source checkout, use `skills/`; in a project-scoped consumer installation, resolve it to `.agents/skills/`. Before running a helper, verify that the selected root contains both this skill and `ai-sdlc-shared-runtime`; block with the missing path if neither layout exists.

## 0.5 Feature State Machine

- Read owning feature `_ai_sdlc/state.toon` before execution handoff.
- Negotiation does not advance feature or runtime state.

## 0.6 Artifact Metadata And Metatags

- Related Markdown uses canonical `artifact_metadata` and `metatags`.
- Machine records use versioned adapter, request, and negotiation schemas.

## 0.7 Specs Index

- Read `_ai_sdlc/specs-index.toon` first and use `specs-index.md` for human review.
- Negotiation does not refresh either index.

## References

- Read `references/adapter-contract.md` before adding a mapping or fallback.
- Validate manifests and requests with the JSON schemas in `references/`.
- Use `scripts/adapter.py` for validation and negotiation.
- Use `references/fixtures/` only as contract conformance hosts, not claims about products.

## Script Usage

```bash
python3 skills/ai-sdlc-host-adapter/scripts/adapter.py . --adapter adapter.json --validate
python3 skills/ai-sdlc-host-adapter/scripts/adapter.py . --adapter adapter.json --negotiate --request request.json --write
```

## Purpose

Keep workflow meaning portable while making host limitations and fallbacks explicit.

## Steps

1. Validate manifest identity, API range, unique capabilities, mappings, and limits.
2. Validate the exact capability request.
3. Prefer equivalent native mappings.
4. Use only registered deterministic fallbacks whose prerequisites are supported.
5. Reduce concurrency or isolation to sequential execution with exact reasons.
6. Fail incompatible when a required operation or capability has no safe mapping.
7. Emit a complete TOON-first negotiation without invoking host operations.

## Output Spec

The negotiation records native and fallback mappings, unsupported operations,
missing capabilities, requested and effective limits, compatibility, reasons,
and deterministic fingerprints.

Quality gate:

- Pass only when every required operation and capability has an equivalent
  mapping or registered semantic-preserving fallback.
- Fail closed when host behavior would change workflow semantics.

## Scope Boundary

- Do not execute host operations, commands, hooks, or approvals.
- Do not claim capabilities not declared by the adapter.
- Do not silently drop workflow steps or required gates.
