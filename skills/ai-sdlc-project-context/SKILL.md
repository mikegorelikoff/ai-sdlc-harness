---
name: ai-sdlc-project-context
description: AI SDLC evidence-backed project context workflow. Use when an AI assistant needs to onboard to an established repository, capture implementation conventions, detect stack and validation commands, preserve architecture constraints, generate human and machine project memory, or check whether saved project context drifted from the current codebase. Supports `--quick-flow` for focused evidence and `--full-flow` for stricter repository coverage.
---

# ai-sdlc-project-context: Evidence-Backed Repository Memory

> Internal AI SDLC skill, not client-facing by default.
> Every rule below is important to follow. None of it can be skipped.
> Confirm the repository root and output location before durable writes.
> Do not read, reproduce, or summarize secrets.

## 0. Skill Card

- Skill name: `ai-sdlc-project-context`
- Primary audience: Dev
- Supporting audience: QA, BA, Delivery, AI assistants
- Audience tags: Dev, QA, BA, Delivery
- SDLC stage: Cross-feature repository context
- Purpose: Generate durable, evidence-backed project rules and detect when they become stale.
- Output: `project-context.md` and `_ai_sdlc/project-context.toon`

### 0.1 Required Inputs

- Repository root.
- Readable repository manifests, guidance, and validation configuration.
- Write authorization when `--write` is requested.

### 0.2 Clarification Rules

- Ask only when the target repository or output root is ambiguous.
- Mark missing stack, command, or architecture evidence as not detected.
- Separate detected evidence from inferred conventions.
- Never infer credentials, deployment authority, or production access.

### 0.2.1 Flow Mode Flags

- Support `--quick-flow` and `--full-flow`; full flow takes precedence.
- Quick flow scans the canonical high-signal repository files.
- Full flow also treats missing guidance, validation commands, or revision
  identity as blockers in the returned report.
- Both modes use the same deterministic fingerprint and secret exclusions.

### 0.3 Output Rules

- Return generation, drift, blockers, evidence coverage, and output paths
  directly in the Codex response.
- Before the final response, emit the `ai-sdlc-handoff/v1` contract with
  `result`, `blockers`, `next_required`, and `next_optional`; every action
  includes `reason`, `command`, and `expected_artifact`.
- Do not create `summary.txt`, `*-summary.txt`, or ad hoc context files.
- Keep Markdown readable and TOON bounded and machine-oriented.

### 0.4 Artifact Routing

- Write the human artifact to `<root>/project-context.md`.
- Write the machine projection to `<root>/_ai_sdlc/project-context.toon`.
- Do not place project-wide context inside one feature folder.
- Do not overwrite either output when `--check` or `--emit` is used.

## 0.5 Feature State Machine

- Project context is cross-feature utility evidence and does not advance a
  feature lifecycle.
- Read feature `_ai_sdlc/state.toon` only when a downstream workflow needs
  feature-specific routing.
- `--state-check` is read-only; `--begin-state` and `--complete-state` are
  rejected by the generator.

## 0.6 Artifact Metadata And Metatags

- `project-context.md` starts with `artifact_metadata` using schema
  `ai-sdlc-project-context-metadata/v1`.
- Include `metatags` for `ai-sdlc`, `project-context`, `project`, and
  `evidence-backed`.
- Metadata records revision, fingerprint, generation date, and source paths.

## 0.7 Specs Index

- Project context does not replace `specs/_ai_sdlc/specs-index.toon`,
  `specs-refiniment/_ai_sdlc/specs-index.toon`, `specs/specs-index.md`, or
  `specs-refiniment/specs-index.md`.
- Do not refresh feature indexes for project-wide context writes.
- Downstream skills read project context before broad code and then use feature
  indexes for feature-specific evidence.

## References

- Use `scripts/project_context.py` to emit, write, or check context.
- Read `references/context-contract.md` when changing source precedence,
  exclusions, or the drift schema.

## Script Usage

```bash
python3 skills/ai-sdlc-project-context/scripts/project_context.py --emit --format toon --quick-flow
python3 skills/ai-sdlc-project-context/scripts/project_context.py --write --full-flow
python3 skills/ai-sdlc-project-context/scripts/project_context.py --check --format toon
```

`--check` exits non-zero when revision or evidence fingerprint drifted.

## Purpose

Give every new session a compact, verifiable repository constitution without
depending on chat history or unsupported generic claims.

## Inputs

- Collect `AGENTS.md`, README, language/package manifests, Makefile, and common
  CI workflow evidence when present.
- Collect the current Git commit and tracked high-signal file content.
- Exclude environment files, credentials, keys, tokens, and secret-named paths.
- Prefer explicit commands from manifests and repository guidance.

## Steps

1. Run `--emit --format toon` before broad repository reading.
2. Inspect detected stack, commands, guidance, architecture paths, revision, and
   evidence anchors.
3. Resolve missing or unsafe evidence before `--full-flow --write` when it
   would mislead implementation.
4. Run `--write` to create both canonical outputs atomically.
5. Run `--check` before reusing saved context after repository changes.
6. Regenerate when drift is reported; never patch the fingerprint manually.
7. Route feature-specific work through Navigator and the owning skill.

## Output Spec

The TOON schema `ai-sdlc-project-context/v1` includes repository, revision,
fingerprint, drift status, stack, commands, architecture paths, and evidence
rows with exact `path`, `line`, `kind`, and `detail` fields.

Quality gate:

- Pass when both outputs share revision and fingerprint, every claim has a
  source anchor, secret paths are excluded, and `--check` reports current.
- Fail when context contains unsupported rules, leaks secret material, lacks
  drift identity, or presents stale evidence as current.

## Examples

Valid evidence:

```text
path=README.md line=37 kind=command detail=npx skills add ...
```

Invalid counter-example:

```text
The project probably uses Kubernetes in production.
```

Reject unsupported inference without repository evidence.

## Edge Cases

- A repository without Git uses revision `unversioned`; fingerprint drift still
  works.
- An empty repository produces explicit not-detected values.
- Untracked high-signal files participate in the fingerprint when readable.
- Symlinked or secret-named sources are skipped.
- A Git revision change without evidence-content change still reports revision
  drift so consumers can consciously accept regeneration.

## Scope Boundary

- Do not create feature requirements, architecture, tests, or tasks.
- Do not modify repository source or configuration.
- Do not read secret values or production credentials.
- Do not replace state, indexes, decisions, or validation evidence.
- Use `$ai-sdlc-navigator` for downstream workflow selection.
