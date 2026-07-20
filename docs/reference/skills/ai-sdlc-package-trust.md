---
title: Package Trust
description: Human-facing operating guide for ai-sdlc-package-trust, including inputs, authority, artifacts, modes, helpers, gates, recovery, and handoff.
---

# `ai-sdlc-package-trust`

| Lifecycle position | Primary owner | Supporting roles | Module | Output |
| --- | --- | --- | --- | --- |
| Package trust and local observability | Security, Delivery, Release | Dev, Architecture | `core` | `_ai_sdlc/trust/<package-id>/decision.{toon,json,md}` or `_ai_sdlc/metrics/local.{toon,json,md}` |

## Why it exists

Fail closed on untrusted packages and measure delivery without content collection.

## Use it when

AI SDLC package trust and privacy-preserving local metrics workflow. Use when an AI assistant needs to verify package origin, file integrity, harness compatibility, declared capabilities, provenance evidence, or generate reproducible aggregate run, retry, budget, coverage, and freshness metrics without collecting source, prompts, commands, or diffs. Supports `--quick-flow` and `--full-flow`.

If the correct entry point is still unclear, ask the read-only navigator first instead of guessing.

## Do not use it when

- Do not use package verification to install, execute, publish, sign, approve, or delete a package. Use the separately authorized package lifecycle workflow instead.
- Do not use local metrics for content analytics or telemetry upload. Use an approved observability and privacy workflow instead.

## Choose one package-trust branch

These are independent operations. Pick exactly one branch for the current request; neither grants install, execution, upload, or approval authority.

| Branch | Choose it when | Do not choose it when | Helper | Durable output |
| --- | --- | --- | --- | --- |
| **A — Verify a package** | A package must be evaluated against origin, API, capability, integrity, and provenance policy. | You need to install, execute, publish, sign, approve, or delete it; use the separately authorized package lifecycle workflow instead. | `package_trust.py` | `_ai_sdlc/trust/<package-id>/decision.{toon,json,md}` |
| **B — Generate local metrics** | You need reproducible content-free counts, budgets, statuses, coverage, freshness, and fingerprints from local run evidence. | You need content analytics, event telemetry, or upload; use an approved observability/privacy workflow instead. | `metrics.py` | `_ai_sdlc/metrics/local.{toon,json,md}` |

### Branch A — Verify a package

**Inputs and reads.** Read the package root, versioned manifest, allowed origins, allowed capabilities, active harness API, provenance policy, and every declared regular file. Reject unsafe paths, symlinks, hash drift, incompatibility, disallowed capabilities, or missing required provenance.

**Tell your agent.**

```text
Use ai-sdlc-package-trust branch A to verify <package-root> against <manifest>,
allowed origins/capabilities, harness API <version>, and provenance policy.
Start in report mode, explain every control, and do not install or execute anything.
```

**Terminal starting point.**

```bash
python3 skills/ai-sdlc-package-trust/scripts/package_trust.py . --package-root package --manifest package.json --allowed-origin repository --allowed-capability filesystem.read --require-provenance
```

**Human checkpoint.** A security or release owner supplies the policy and reviews allow/deny evidence. An `allow` result is evidence only, never installation or execution approval.

**Modes.** Quick flow checks every required control for the declared package. Full flow additionally reviews every file, capability, origin, provenance claim, and privacy field; full flow wins when both flags appear.

**Success example.** A deny is a valid successful evaluation when a required control fails:

```toon
schema: ai-sdlc-package-trust-decision/v1
decision: deny
controls[2]{code,status,evidence}:
  integrity,pass,all declared hashes match
  provenance,fail,required evidence missing
```

**Blockers and output.** Missing package root, manifest, allowed origin, valid harness API, or readable declared files blocks evaluation. Preserve the reason and write only `_ai_sdlc/trust/<package-id>/decision.{toon,json,md}` when explicit write mode is authorized.

### Branch B — Generate local metrics

**Inputs and reads.** Read only repository-local `_ai_sdlc/runs/*/state.json` records with schema `ai-sdlc-run-state/v1` and optional `_ai_sdlc/evidence-ledger.json` with schema `ai-sdlc-evidence-ledger/v1`. Aggregate schemas, fingerprints, statuses, booleans, and numeric counts or budgets only.

**Tell your agent.**

```text
Use ai-sdlc-package-trust branch B to generate local content-free metrics for <repository>.
Do not use the network, upload data, or include content, prompts, commands, diffs,
source text, artifact paths, messages, reasons, or file bodies.
```

**Terminal starting point.**

```bash
python3 skills/ai-sdlc-package-trust/scripts/metrics.py . --generate
```

**Human checkpoint.** A delivery or privacy owner reviews the permitted field set and confirms that any later sharing or upload is outside this skill and requires separate authority.

**Modes.** Quick flow produces the same deterministic privacy-safe aggregate over available local records. Full flow additionally reviews every privacy field; neither mode changes feature state or uses the network.

**Success example.** No eligible evidence is not fabricated into activity; it produces an explicit insufficient-data result:

```toon
schema: ai-sdlc-local-metrics/v1
status: insufficient-data
runs:
  total: 0
tasks:
  total: 0
```

**Blockers and output.** A missing repository or any forbidden content-bearing field blocks the operation. Otherwise write only `_ai_sdlc/metrics/local.{toon,json,md}` in explicit write mode; the helper has no network operation and never uploads metrics.

## Who is involved

The summary table above names the primary and supporting human roles for this capability.
- **Agent:** follows this contract, reports assumptions and blockers, and cannot accept protected decisions for the humans above.

## Before you start

Choose exactly one branch above. Complete only that branch's inputs and reads; the other branch is not a prerequisite.

## Tell your agent

```text
Choose Branch A or Branch B above and copy its branch-specific prompt.
Do not send a combined package-verification and metrics request.
Apply --quick-flow or --full-flow only to the selected branch,
preserve human approval boundaries, and return ai-sdlc-handoff/v1.
```

This is an agent instruction, not a shell command. Terminal commands belong in the helper section.

## What the agent reads

Read only the inputs named by the selected branch above. Branch A does not read runtime metrics; Branch B does not read package files, manifests, origin policy, or provenance evidence.

## What it may write

- Write generated decisions and metrics only below `_ai_sdlc/`.
- Never rewrite package files, manifests, runtime records, or evidence ledgers.

## Human checkpoints

Use only the selected branch's human checkpoint above. The trust reviewer and metrics/privacy reviewer are not interchangeable approvals.

Humans accept or reject material product, security, QA, policy, rollout, release, and destructive-action decisions; a complete agent handoff is evidence, not approval.

## Flow modes

Apply quick/full behavior only within the selected branch as defined above. Do not use a flow flag to combine the branches.

## Deterministic helpers

Paths beginning with `skills/` below are canonical **source-checkout** forms for maintainers and CI. In a consumer repository, normally tell the installed skill to act; for human diagnosis, use the matching project-scoped `.agents/skills/<skill>/...` path reported by your host. Do not expect source-only `skills/_shared` to exist after installation.

| Helper | Purpose | Direct starting point | Repository effect |
| --- | --- | --- | --- |
| [`metrics.py`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-package-trust/scripts/metrics.py) | Generate deterministic, content-free local delivery metrics. | `python3 skills/ai-sdlc-package-trust/scripts/metrics.py --help` | May write only through an explicit mutation mode; start with `--help`, check, preview, or emit. |
| [`package_trust.py`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-package-trust/scripts/package_trust.py) | Verify package origin, integrity, compatibility, capabilities, and provenance. | `python3 skills/ai-sdlc-package-trust/scripts/package_trust.py --help` | May write only through an explicit mutation mode; start with `--help`, check, preview, or emit. |

The owning agent normally runs these helpers. A human uses the direct starting point for diagnosis or reproduction after inspecting `--help` and repository policy.

### Contract-provided usage

There is no combined command. Select one branch and use only its Terminal starting point above; add `--write` only after its output boundary is understood and authorized.

## Success criteria

Use the selected branch's success example and schema above. A trust decision and a local-metrics record are separate results.

## Blockers and recovery

Use only the selected branch's blocker and output rule above. If branch selection is ambiguous, stop and ask instead of reading both input sets.

On a blocker, preserve failed/stale evidence, name the accountable owner and exact missing input, then resume this skill or the earliest reopened producer. Never manufacture completion by editing derived state.

## Handoff

- Default to complete TOON trust decisions or content-free aggregate metrics.
- Return summaries directly in the Codex response.
- Emit `ai-sdlc-handoff/v1` with `result`, `blockers`, `next_required`, and
  `next_optional`; actions include `reason`, `command`, and `expected_artifact`.
- Do not create `summary.txt`, `*-summary.txt`, or another standalone summary file.

The downstream consumer rechecks artifacts and freshness; it does not trust a previous chat's completion claim.

## State, metadata, and indexes

??? info "Feature state"

    - Read owning feature `_ai_sdlc/state.toon` before using a trust decision.
    - Trust and metrics do not advance feature state.

??? info "Artifact metadata"

    - Related Markdown uses canonical `artifact_metadata` and `metatags`.
    - Machine records use versioned package, trust-decision, and local-metrics schemas.

??? info "Specs index"

    - Read `_ai_sdlc/specs-index.toon` first and use `specs-index.md` for human review.
    - Trust and metrics outputs do not refresh either index.

## Example

Choose one of the two success examples above. Do not run both helpers merely because both capabilities share this skill package.

## Source contract

This page is generated from [`skills/ai-sdlc-package-trust/SKILL.md`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-package-trust/SKILL.md). Edit the source contract, rerun the catalog generator, and review both changes together; never hand-edit this page.

[Back to the skill catalog](../skills.md) · [Script reference](../scripts.md) · [Choose a workflow](../../flows/index.md)
