---
title: Project Context
description: Human-facing operating guide for ai-sdlc-project-context, including inputs, authority, artifacts, modes, helpers, gates, recovery, and handoff.
---

# `ai-sdlc-project-context`

AI SDLC evidence-backed project context and bounded task-pack workflow. Use when an AI assistant needs to onboard to a repository, detect stack and commands, map ownership and test topology, check context drift, conditionally select task sources, exclude secrets, or allocate a freshness-aware context pack within an explicit token budget. Supports `--quick-flow` for focused evidence and `--full-flow` for stricter repository coverage.

| Lifecycle position | Primary owner | Supporting roles | Module | Output |
| --- | --- | --- | --- | --- |
| Cross-feature repository context | Dev | QA, BA, Delivery, AI assistants | `core` | `project-context.md`, `_ai_sdlc/project-context.toon`, and optional topology and task-pack records below `_ai_sdlc/context/` |

## Why it exists

Generate durable repository memory and task-specific, bounded, freshness-aware context from explained safe sources.

## Use it when

AI SDLC evidence-backed project context and bounded task-pack workflow. Use when an AI assistant needs to onboard to a repository, detect stack and commands, map ownership and test topology, check context drift, conditionally select task sources, exclude secrets, or allocate a freshness-aware context pack within an explicit token budget. Supports `--quick-flow` for focused evidence and `--full-flow` for stricter repository coverage.

If the correct entry point is still unclear, ask the read-only navigator first instead of guessing.

## Do not use it when

- Do not use repository context as product authority or missing requirements. Use `ai-sdlc-ba` or `ai-sdlc-sdd` instead.


## Who is involved

- **Accountable/primary:** Dev.
- **Supporting:** QA, BA, Delivery, AI assistants.
- **Agent:** follows this contract, reports assumptions and blockers, and cannot accept protected decisions for the humans above.

## Before you start

- Repository root.
- Readable repository manifests, guidance, and validation configuration.
- Task ID, goal, relevant paths or tags, and explicit token budget for a pack.
- Write authorization when `--write` is requested.

## Tell your agent

```text
Use ai-sdlc-project-context for <target>.
Choose --quick-flow for bounded assumption-driven progress or --full-flow
for strict verification only as described below.
Read the required evidence,
produce or report `project-context.md`, `_ai_sdlc/project-context.toon`, and optional topology and task-pack records below `_ai_sdlc/context/`, preserve human approval boundaries,
and return blockers plus a complete ai-sdlc-handoff/v1.
```

This is an agent instruction, not a shell command. Terminal commands belong in the helper section.

## What the agent reads

- Collect `AGENTS.md`, README, language/package manifests, Makefile, and common
  CI workflow evidence when present.
- Collect the current Git commit and tracked high-signal file content.
- Exclude environment files, credentials, keys, tokens, and secret-named paths.
- Prefer explicit commands from manifests and repository guidance.

## What it may write

- Write the human artifact to `<root>/project-context.md`.
- Write the machine projection to `<root>/_ai_sdlc/project-context.toon`.
- Do not place project-wide context inside one feature folder.
- Do not overwrite either output when `--check` or `--emit` is used.
- Route topology to `_ai_sdlc/context/topology.{toon,json,md}` and task packs to
  `_ai_sdlc/context/task-packs/<task>.{toon,json,md}` only with `--write`.

## Human checkpoints

- Ask only when the target repository or output root is ambiguous.
- Mark missing stack, command, or architecture evidence as not detected.
- Separate detected evidence from inferred conventions.
- Never infer credentials, deployment authority, or production access.

Humans accept or reject material product, security, QA, policy, rollout, release, and destructive-action decisions; a complete agent handoff is evidence, not approval.

## Flow modes

- Support `--quick-flow` and `--full-flow`; full flow takes precedence.
- Quick flow scans the canonical high-signal repository files.
- Full flow also treats missing guidance, validation commands, or revision
  identity as blockers in the returned report.
- Both modes use the same deterministic fingerprint and secret exclusions.
- Full-flow task packs require ownership and test topology plus explicit review
  of every freshness warning and budget exclusion.

## Deterministic helpers

Paths beginning with `skills/` below are canonical **source-checkout** forms for maintainers and CI. In a consumer repository, normally tell the installed skill to act; for human diagnosis, use the matching project-scoped `.agents/skills/<skill>/...` path reported by your host. Do not expect source-only `skills/_shared` to exist after installation.

| Helper | Purpose | Direct starting point | Repository effect |
| --- | --- | --- | --- |
| [`context_engine.py`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-project-context/scripts/context_engine.py) | Build repository topology and bounded freshness-aware context packs. | `python3 skills/ai-sdlc-project-context/scripts/context_engine.py --help` | May write only through an explicit mutation mode; start with `--help`, check, preview, or emit. |
| [`project_context.py`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-project-context/scripts/project_context.py) | Generate and check evidence-backed AI SDLC project context. | `python3 skills/ai-sdlc-project-context/scripts/project_context.py --help` | May write only through an explicit mutation mode; start with `--help`, check, preview, or emit. |

The owning agent normally runs these helpers. A human uses the direct starting point for diagnosis or reproduction after inspecting `--help` and repository policy.

### Contract-provided usage

```bash
python3 skills/ai-sdlc-project-context/scripts/project_context.py --emit --format toon --quick-flow
python3 skills/ai-sdlc-project-context/scripts/project_context.py --write --full-flow
python3 skills/ai-sdlc-project-context/scripts/project_context.py --check --format toon
python3 skills/ai-sdlc-project-context/scripts/context_engine.py --topology --write --format toon
python3 skills/ai-sdlc-project-context/scripts/context_engine.py --build-pack --task T009 --goal "Build bounded context" --path specs/example/tasks.md --tag implementation --budget 2000 --write --format toon
```

`--check` exits non-zero when revision or evidence fingerprint drifted.

## Success criteria

The TOON schema `ai-sdlc-project-context/v1` includes repository, revision,
fingerprint, drift status, stack, commands, architecture paths, and evidence
rows with exact `path`, `line`, `kind`, and `detail` fields.

The complete TOON/JSON `ai-sdlc-context-pack/v2` record includes task identity, topology and
revision identity, deterministic budget use, selector outcomes, bounded source
ranges and content, exclusions, freshness warnings, and fingerprint.

Quality gate:

- Pass when both outputs share revision and fingerprint, every claim has a
  source anchor, secret paths are excluded, and `--check` reports current.
- Fail when context contains unsupported rules, leaks secret material, lacks
  drift identity, or presents stale evidence as current.

## Blockers and recovery

- A repository without Git uses revision `unversioned`; fingerprint drift still
  works.
- An empty repository produces explicit not-detected values.
- Untracked high-signal files participate in the fingerprint when readable.
- Symlinked or secret-named sources are skipped.
- Credential-like assignment content is excluded even when its filename looks safe.
- Custom selectors that do not match remain visible with the failed condition.
- Budget exhaustion records skipped candidates instead of silently truncating
  the candidate list.
- A Git revision change without evidence-content change still reports revision
  drift so consumers can consciously accept regeneration.

On a blocker, preserve failed/stale evidence, name the accountable owner and exact missing input, then resume this skill or the earliest reopened producer. Never manufacture completion by editing derived state.

## Handoff

- Return generation, drift, blockers, evidence coverage, and output paths
  directly in the Codex response.
- Before the final response, emit the `ai-sdlc-handoff/v1` contract with
  `result`, `blockers`, `next_required`, and `next_optional`; every action
  includes `reason`, `command`, and `expected_artifact`.
- Do not create `summary.txt`, `*-summary.txt`, or ad hoc context files.
- Keep Markdown readable and TOON bounded and machine-oriented.
- For task packs, report every selection reason, exclusion reason, token
  allocation, current hash, and freshness warning.

The downstream consumer rechecks artifacts and freshness; it does not trust a previous chat's completion claim.

## State, metadata, and indexes

??? info "Feature state"

    - Project context is cross-feature utility evidence and does not advance a
      feature lifecycle.
    - Read feature `_ai_sdlc/state.toon` only when a downstream workflow needs
      feature-specific routing.
    - `--state-check` is read-only; `--begin-state` and `--complete-state` are
      rejected by the generator.

??? info "Artifact metadata"

    - `project-context.md` starts with `artifact_metadata` using schema
      `ai-sdlc-project-context-metadata/v1`.
    - Include `metatags` for `ai-sdlc`, `project-context`, `project`, and
      `evidence-backed`.
    - Metadata records revision, fingerprint, generation date, and source paths.
    - Task packs use `ai-sdlc-context-pack/v2`; selectors use
      `ai-sdlc-context-selectors/v2`; topology uses
      `ai-sdlc-repository-topology/v2`.

??? info "Specs index"

    - Project context does not replace `specs/_ai_sdlc/specs-index.toon`,
      `specs-refiniment/_ai_sdlc/specs-index.toon`, `specs/specs-index.md`, or
      `specs-refiniment/specs-index.md`.
    - Do not refresh feature indexes for project-wide context writes.
    - Downstream skills read project context before broad code and then use feature
      indexes for feature-specific evidence.

## Example

Valid evidence:

```text
path=README.md line=37 kind=command detail=npx skills add ...
```

Invalid counter-example:

```text
The project probably uses Kubernetes in production.
```

Reject unsupported inference without repository evidence.

## Source contract

This page is generated from [`skills/ai-sdlc-project-context/SKILL.md`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-project-context/SKILL.md). Edit the source contract, rerun the catalog generator, and review both changes together; never hand-edit this page.

[Back to the skill catalog](../skills.md) · [Script reference](../scripts.md) · [Choose a workflow](../../flows/index.md)
