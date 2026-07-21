---
name: ai-sdlc-package-trust
description: AI SDLC package trust and privacy-preserving local metrics workflow. Use when an AI assistant needs to verify package origin, file integrity, harness compatibility, declared capabilities, provenance evidence, or generate reproducible aggregate run, retry, budget, coverage, and freshness metrics without collecting source, prompts, commands, or diffs. Supports `--quick-flow` and `--full-flow`.
---

# ai-sdlc-package-trust: Trusted Packages And Private Metrics

> Internal AI SDLC skill, not client-facing by default.
> Integrity and provenance evidence do not grant install or execution authority.

## 0. Skill Card

- Skill name: `ai-sdlc-package-trust`
- Primary audience: Security, Delivery, Release
- Supporting audience: Dev, Architecture
- Audience tags: Security, Delivery, Release, Dev
- SDLC stage: Package trust and local observability
- Purpose: Fail closed on untrusted packages and measure delivery without content collection.
- Output: `_ai_sdlc/trust/<package-id>/decision.{toon,json,md}` or `_ai_sdlc/metrics/local.{toon,json,md}`

### 0.1 Required Inputs

- Package root, versioned manifest, allowed origins/capabilities, active harness API, and provenance policy.
- Repository-local runtime and evidence records for metrics.

### 0.2 Clarification Rules

- Ask when trust policy or package root is ambiguous.
- Reject unsafe paths, symlinks, hash drift, incompatible APIs, undeclared or
  disallowed capabilities, and missing required provenance.
- Never equate a digest with author identity or approval.

### 0.2.1 Flow Mode Flags

- Support `--quick-flow` and `--full-flow`; full flow takes precedence.
- Full flow reviews every file, capability, origin, provenance claim, and privacy field.

### 0.3 Output Rules

- Default to complete TOON trust decisions or content-free aggregate metrics.
- Return summaries directly in the active agent response.
- Emit `ai-sdlc-handoff/v1` with `result`, `blockers`, `next_required`, and
  `next_optional`; actions include `reason`, `command`, and `expected_artifact`.
- Do not create `summary.txt`, `*-summary.txt`, or another standalone summary file.

### 0.4 Artifact Routing

- Write generated decisions and metrics only below `_ai_sdlc/`.
- Never rewrite package files, manifests, runtime records, or evidence ledgers.

## 0.4.1 Runtime Path Resolution

- Treat `skills/` in commands as a logical skill root. In a harness source checkout, use `skills/`; in a project-scoped consumer installation, resolve it to `.agents/skills/`. Before running a helper, verify that the selected root contains both this skill and `ai-sdlc-shared-runtime`; block with the missing path if neither layout exists.

## 0.5 Feature State Machine

- Read owning feature `_ai_sdlc/state.toon` before using a trust decision.
- Trust and metrics do not advance feature state.

## 0.6 Artifact Metadata And Metatags

- Related Markdown uses canonical `artifact_metadata` and `metatags`.
- Machine records use versioned package, trust-decision, and local-metrics schemas.

## 0.7 Specs Index

- Read `_ai_sdlc/specs-index.toon` first and use `specs-index.md` for human review.
- Trust and metrics outputs do not refresh either index.

## References

- Read `references/trust-metrics-contract.md` before interpreting results.
- Validate manifests with `references/package.schema.json`.
- Use `scripts/package_trust.py` for trust and `scripts/metrics.py` for aggregation.

## Script Usage

```bash
python3 skills/ai-sdlc-package-trust/scripts/package_trust.py . --package-root package --manifest package.json --allowed-origin repository --allowed-capability filesystem.read --require-provenance --write
python3 skills/ai-sdlc-package-trust/scripts/metrics.py . --generate --write
```

## Steps

1. Validate manifest structure, safe inventory, origin, API range, and capabilities.
2. Rehash every declared regular file and the normalized inventory.
3. Validate required provenance fields without claiming cryptographic identity.
4. Emit an explainable allow or deny decision; never install the package.
5. Aggregate local run states and evidence coverage using counts and numeric budgets only.
6. Reject any metrics structure containing content-bearing field names.
7. Emit deterministic TOON-first local metrics with explicit insufficient-data state.

## Output Spec

Trust decisions report each control, evidence, reason, and fingerprint. Metrics
report only aggregate counts, statuses, retries, tokens, coverage, freshness,
and input fingerprints; they never include paths, source, prompts, commands, or diffs.

## Scope Boundary

- Do not install, execute, publish, sign, approve, or delete packages.
- Do not upload metrics or collect content-bearing fields.
- Do not weaken allowed origins, capabilities, or provenance policy.
