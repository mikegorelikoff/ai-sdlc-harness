---
title: Shared Runtime
description: Human-facing operating guide for ai-sdlc-shared-runtime, including inputs, authority, artifacts, modes, helpers, gates, recovery, and handoff.
---

# `ai-sdlc-shared-runtime`

Portable AI SDLC shared-helper runtime. Use when an AI assistant installs, verifies, diagnoses, or repairs project-scoped AI SDLC skills whose deterministic scripts depend on shared state, artifact, context, path, TOON, migration, or index modules. This is an installation dependency, not a lifecycle entry point.

| Lifecycle position | Primary owner | Supporting roles | Module | Output |
| --- | --- | --- | --- | --- |
| Installation and cross-lifecycle runtime support | agent runners, platform engineers, harness maintainers | AI assistants and repository owners diagnosing install failures | `core` | Read-only runtime verification or an explicit installation blocker |

## Why it exists

Make the deterministic shared Python runtime portable when Skills CLI installs individual skill directories without the source-only `skills/_shared/` directory.

## Use it when

Portable AI SDLC shared-helper runtime. Use when an AI assistant installs, verifies, diagnoses, or repairs project-scoped AI SDLC skills whose deterministic scripts depend on shared state, artifact, context, path, TOON, migration, or index modules. This is an installation dependency, not a lifecycle entry point.

If the correct entry point is still unclear, ask the read-only navigator first instead of guessing.

## Do not use it when

- Do not use shared helpers as a lifecycle entry point. Use `ai-sdlc-navigator` or the owning skill instead.
- Do not edit installed mirrors to repair packaging. Use the authorized install or update workflow and canonical `_shared` sources instead.


## Who is involved

- **Accountable/primary:** agent runners, platform engineers, harness maintainers.
- **Supporting:** AI assistants and repository owners diagnosing install failures.
- **Agent:** follows this contract, reports assumptions and blockers, and cannot accept protected decisions for the humans above.

## Before you start

- The installed skills root, normally `.agents/skills/` for a project-scoped
  universal installation.
- The consumer repository root.
- The downstream skill script that failed or must be verified.
- The installed package revision or trusted source identity when known.

## Tell your agent

```text
Use ai-sdlc-shared-runtime for <target>.
Do not select a flow flag independently; preserve the mode of the owning downstream skill as described below.
Read the required evidence,
produce or report Read-only runtime verification or an explicit installation blocker, preserve human approval boundaries,
and return blockers plus a complete ai-sdlc-handoff/v1.
```

This is an agent instruction, not a shell command. Terminal commands belong in the helper section.

## What the agent reads

- Resolve the current skill file and its sibling skills root.
- Locate `ai-sdlc-shared-runtime/scripts/` under that root.
- Select the smallest downstream helper that exercises the reported dependency.
- Preserve the consumer repository as the helper's working directory.

## What it may write

- This skill creates no refinement or implementation artifact.
- Read installed files from the agent-owned skills root and consumer evidence
  from the current repository.
- Do not write `specs-refiniment/`, `specs/`, `_ai_sdlc/state.toon`, or an
  `_ai_sdlc/specs-index.toon` during runtime verification.
- Route repair to the canonical install/update workflow and lifecycle work to
  the owning skill.

## Human checkpoints

- Ask only when the installed skills root or failing downstream script cannot
  be located safely.
- Distinguish a missing runtime package from a corrupt runtime copy, missing
  Python, an unsupported package revision, and an application-level failure.
- Never infer that an import failure is permission to download or execute an
  unreviewed replacement.

Humans accept or reject material product, security, QA, policy, rollout, release, and destructive-action decisions; a complete agent handoff is evidence, not approval.

## Flow modes

- This package has no independent quick/full lifecycle flow.
- Preserve `--quick-flow` and `--full-flow` flags for the downstream owning
  skill; this runtime must not reinterpret them.
- Verification is read-only. Reinstallation or repair requires the same human
  authority and trusted source used for installation.

## Deterministic helpers

Paths beginning with `skills/` below are canonical **source-checkout** forms for maintainers and CI. In a consumer repository, normally tell the installed skill to act; for human diagnosis, use the matching project-scoped `.agents/skills/<skill>/...` path reported by your host. Do not expect source-only `skills/_shared` to exist after installation.

| Helper | Purpose | Direct starting point | Repository effect |
| --- | --- | --- | --- |
| [`ai_sdlc_artifact_helper.py`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-shared-runtime/scripts/ai_sdlc_artifact_helper.py) | Shared artifact compression helpers for AI SDLC skill scripts. | `python3 skills/ai-sdlc-shared-runtime/scripts/ai_sdlc_artifact_helper.py --help` | Generated copy; repository behavior is defined by its canonical shared source. |
| [`ai_sdlc_artifact_profiles.py`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-shared-runtime/scripts/ai_sdlc_artifact_profiles.py) | Canonical refinement artifact profiles and self-contained context schema. | `Imported helper; use the owning skill rather than invoking it directly.` | Generated copy; repository behavior is defined by its canonical shared source. |
| [`ai_sdlc_compatibility.py`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-shared-runtime/scripts/ai_sdlc_compatibility.py) | Validate an AI SDLC release against its compatibility baseline. | `python3 skills/ai-sdlc-shared-runtime/scripts/ai_sdlc_compatibility.py --help` | Generated copy; repository behavior is defined by its canonical shared source. |
| [`ai_sdlc_config.py`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-shared-runtime/scripts/ai_sdlc_config.py) | Resolve versioned base, team, and user AI SDLC configuration safely. | `python3 skills/ai-sdlc-shared-runtime/scripts/ai_sdlc_config.py --help` | Generated copy; repository behavior is defined by its canonical shared source. |
| [`ai_sdlc_context.py`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-shared-runtime/scripts/ai_sdlc_context.py) | Build compact, evidence-backed TOON context packs for AI SDLC skills. | `Imported helper; use the owning skill rather than invoking it directly.` | Generated copy; repository behavior is defined by its canonical shared source. |
| [`ai_sdlc_context_benchmark.py`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-shared-runtime/scripts/ai_sdlc_context_benchmark.py) | Measure raw, compact, and targeted-reread context payloads. | `python3 skills/ai-sdlc-shared-runtime/scripts/ai_sdlc_context_benchmark.py --help` | Generated copy; repository behavior is defined by its canonical shared source. |
| [`ai_sdlc_handoff.py`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-shared-runtime/scripts/ai_sdlc_handoff.py) | Render a normalized AI SDLC post-workflow handoff report. | `python3 skills/ai-sdlc-shared-runtime/scripts/ai_sdlc_handoff.py --help` | Generated copy; repository behavior is defined by its canonical shared source. |
| [`ai_sdlc_migrate.py`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-shared-runtime/scripts/ai_sdlc_migrate.py) | Check or apply safe migrations from legacy AI SDLC paths to canonical paths. | `python3 skills/ai-sdlc-shared-runtime/scripts/ai_sdlc_migrate.py --help` | Generated copy; repository behavior is defined by its canonical shared source. |
| [`ai_sdlc_modules.py`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-shared-runtime/scripts/ai_sdlc_modules.py) | Discover and validate compatible AI SDLC module manifests. | `python3 skills/ai-sdlc-shared-runtime/scripts/ai_sdlc_modules.py --help` | Generated copy; repository behavior is defined by its canonical shared source. |
| [`ai_sdlc_paths.py`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-shared-runtime/scripts/ai_sdlc_paths.py) | Canonical and legacy paths for AI SDLC machine-readable artifacts. | `Imported helper; use the owning skill rather than invoking it directly.` | Generated copy; repository behavior is defined by its canonical shared source. |
| [`ai_sdlc_rigor.py`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-shared-runtime/scripts/ai_sdlc_rigor.py) | Select an explainable risk-adaptive AI SDLC rigor profile. | `python3 skills/ai-sdlc-shared-runtime/scripts/ai_sdlc_rigor.py --help` | Generated copy; repository behavior is defined by its canonical shared source. |
| [`ai_sdlc_specs_index.py`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-shared-runtime/scripts/ai_sdlc_specs_index.py) | Build compact TOON and human Markdown indexes for spec workspaces. | `python3 skills/ai-sdlc-shared-runtime/scripts/ai_sdlc_specs_index.py --help` | Generated copy; repository behavior is defined by its canonical shared source. |
| [`ai_sdlc_state_machine.py`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-shared-runtime/scripts/ai_sdlc_state_machine.py) | Feature-level state machine for AI SDLC skill chains. | `python3 skills/ai-sdlc-shared-runtime/scripts/ai_sdlc_state_machine.py --help` | Generated copy; repository behavior is defined by its canonical shared source. |
| [`ai_sdlc_toon.py`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-shared-runtime/scripts/ai_sdlc_toon.py) | Deterministic TOON 3.3 encoding for the JSON data model. | `Imported helper; use the owning skill rather than invoking it directly.` | Generated copy; repository behavior is defined by its canonical shared source. |
| [`refinement_status.py`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-shared-runtime/scripts/refinement_status.py) | Report whether an end-to-end refinement package is complete. | `python3 skills/ai-sdlc-shared-runtime/scripts/refinement_status.py --help` | Generated copy; repository behavior is defined by its canonical shared source. |
| [`skill_script_contract.py`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-shared-runtime/scripts/skill_script_contract.py) | Reusable per-skill test contract for AI SDLC helper scripts. | `Imported helper; use the owning skill rather than invoking it directly.` | Generated copy; repository behavior is defined by its canonical shared source. |
| [`state_machine.py`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-shared-runtime/scripts/state_machine.py) | CLI for AI SDLC feature state.toon files. | `python3 skills/ai-sdlc-shared-runtime/scripts/state_machine.py --help` | Generated copy; repository behavior is defined by its canonical shared source. |

The owning agent normally runs these helpers. A human uses the direct starting point for diagnosis or reproduction after inspecting `--help` and repository policy.

### Contract-provided usage

- Verify the generated mirror in a harness source checkout:

  ```bash
  python3 skills/_shared/sync_installed_runtime.py --check
  ```

- Verify an installed downstream helper from a consumer repository:

  ```bash
  python3 .agents/skills/ai-sdlc-sdd/scripts/sdd_artifact_scaffold.py --help
  ```

- A missing `ai-sdlc-shared-runtime/scripts/` directory, stale mirror, import
  traceback, or non-zero helper smoke result is a blocker.

## Success criteria

A passing verification reports:

```text
runtime: present
downstream helper: executable
consumer root: preserved
mutation: none, or disposable fixture only
next: owning lifecycle skill
```

Quality gate:

- Pass when the generated runtime mirror matches its canonical source and an
  installed downstream helper imports and executes successfully.
- Fail when inventory exists but imports fail, the runtime is installed under a
  different root, generated bytes drift, or verification mutates real delivery
  artifacts.

## Blockers and recovery

- A source checkout legitimately uses `skills/_shared/`; this is not drift.
- A project may expose host-specific symlinks, but all selected skill folders
  and the runtime must resolve to compatible bytes.
- Installing only one downstream skill without this dependency is incomplete.
- `--help` proves importability, not correctness of a consumer feature; run the
  downstream workflow's own validation for that claim.

On a blocker, preserve failed/stale evidence, name the accountable owner and exact missing input, then resume this skill or the earliest reopened producer. Never manufacture completion by editing derived state.

## Handoff

- Report the installed skills root, runtime path, checked downstream script,
  exact command, exit status, and any missing module.
- Return progress, blockers, and recommendations directly in the Codex response.
- Before the final response, emit the `ai-sdlc-handoff/v1` contract with
  `result`, `blockers`, `next_required`, and `next_optional`; every action
  includes `reason`, `command`, and `expected_artifact`.
- Do not create `summary.txt`, `*-summary.txt`, or a runtime status artifact.
- Do not claim an installation is healthy from inventory alone; execute a
  representative downstream helper.

The downstream consumer rechecks artifacts and freshness; it does not trust a previous chat's completion claim.

## State, metadata, and indexes

??? info "Feature state"

    - This runtime is a utility and never begins or completes a feature stage.
    - It may load `ai_sdlc_state_machine` for another skill, but it must not mutate
      lifecycle state on its own.
    - Use `state.toon` only through the downstream owning workflow.

??? info "Artifact metadata"

    - Runtime verification is ephemeral and carries no `artifact_metadata` or
      `metatags`.
    - The packaged helpers preserve the downstream skill's existing metadata and
      authority contracts; they do not create a second source of truth.

??? info "Specs index"

    - The runtime exposes index helpers but does not rebuild `specs-index.md` or a
      machine index by itself.
    - Index reads and writes remain owned by the selected lifecycle workflow.

## Example

Valid diagnosis:

```text
The SDD helper cannot import ai_sdlc_artifact_helper because the shared runtime
package is absent. Reinstall the complete pinned package, then rerun --help.
```

Invalid diagnosis:

```text
Copy one module from an arbitrary checkout into the installed package and keep
working.
```

Reject the invalid path because it bypasses package provenance and can mix
incompatible runtime bytes.

## Source contract

This page is generated from [`skills/ai-sdlc-shared-runtime/SKILL.md`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-shared-runtime/SKILL.md). Edit the source contract, rerun the catalog generator, and review both changes together; never hand-edit this page.

[Back to the skill catalog](../skills.md) · [Script reference](../scripts.md) · [Choose a workflow](../../flows/index.md)
