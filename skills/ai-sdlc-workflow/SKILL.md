---
name: ai-sdlc-workflow
description: AI SDLC declarative workflow planning. Use when an AI assistant needs to validate a versioned workflow, plan typed dependency steps, evaluate bounded conditions, enforce approval gates, attach deterministic hooks, detect cycles, or create safe dependency waves with sequential fallback when host concurrency or isolation is unavailable. Supports `--quick-flow` and `--full-flow`.
---

# ai-sdlc-workflow: Declarative Workflow Planning

> Internal AI SDLC skill, not client-facing by default.
> Planning never executes actions, hooks, approvals, or shell commands.

## 0. Skill Card

- Skill name: `ai-sdlc-workflow`
- Primary audience: Delivery, Dev
- Supporting audience: QA, Security, Architecture
- Audience tags: Delivery, Dev, QA, Security
- SDLC stage: Controlled execution planning
- Purpose: Compile portable workflow intent into deterministic, gated, host-safe waves.
- Output: `_ai_sdlc/workflows/<workflow-id>/plan.{toon,json,md}`

### 0.1 Required Inputs

- Versioned workflow JSON, declared capabilities, typed steps, dependencies,
  bounded conditions, approval gates, and deterministic hook declarations.
- Optional JSON context and explicit host concurrency/isolation capabilities.

### 0.2 Clarification Rules

- Ask when an action, approval owner, or required capability is missing.
- Reject unknown fields, undeclared capabilities, cycles, unsafe identifiers,
  invalid conditions, and hooks without exact targets.
- Never infer approval, shell authority, network authority, or safe isolation.

### 0.2.1 Flow Mode Flags

- Support `--quick-flow` and `--full-flow`; full flow takes precedence.
- Both modes use identical validation, cycle, capability, and fallback rules.
- Full flow requires review of every skipped/deferred condition, gate, hook, and fallback.

### 0.3 Output Rules

- Default to complete TOON with workflow fingerprint, step decisions, waves,
  gates, hooks, fallbacks, host capabilities, and plan fingerprint.
- Return validation and handoff summaries directly in the active agent response.
- Emit `ai-sdlc-handoff/v1` with `result`, `blockers`, `next_required`, and
  `next_optional`; actions include `reason`, `command`, and `expected_artifact`.
- Do not create `summary.txt`, `*-summary.txt`, or another standalone summary file.

### 0.4 Artifact Routing

- Write generated plans only below `_ai_sdlc/workflows/<workflow-id>/`.
- Keep authored workflow definitions in visible repository-owned paths.
- Never execute or rewrite the authored workflow during planning.

## 0.4.1 Runtime Path Resolution

- Treat `skills/` in commands as a logical skill root. In a harness source checkout, use `skills/`; in a project-scoped consumer installation, resolve it to `.agents/skills/`. Before running a helper, verify that the selected root contains both this skill and `ai-sdlc-shared-runtime`; block with the missing path if neither layout exists.

## 0.5 Feature State Machine

- Read the owning feature `_ai_sdlc/state.toon` before planning feature work.
- Workflow plans do not advance feature state or runtime task state.

## 0.6 Artifact Metadata And Metatags

- Machine records use `ai-sdlc-workflow/v1` and `ai-sdlc-workflow-plan/v1`.
- Workflow-related Markdown uses canonical `artifact_metadata` and `metatags`
  when authored.

## 0.7 Specs Index

- Read `_ai_sdlc/specs-index.toon` before resolving feature-local actions and
  use `specs-index.md` for human review.
- Planning does not refresh either specs index.

## References

- Read `references/workflow-contract.md` before authoring or reviewing workflows.
- Validate definitions with `references/workflow.schema.json` and generated
  plans with `references/workflow-plan.schema.json`.
- Use `scripts/workflow.py` for validation and planning.

## Script Usage

```bash
python3 skills/ai-sdlc-workflow/scripts/workflow.py . --workflow workflow.json --validate --format toon
python3 skills/ai-sdlc-workflow/scripts/workflow.py . --workflow workflow.json --plan --context context.json --concurrency 4 --isolation-supported --write
```

## Purpose

Separate portable workflow semantics from host execution while preserving gates,
capability boundaries, deterministic hooks, and safe parallelism.

## Inputs

- Exact workflow identity and version.
- Declared capability set and typed steps.
- Optional bounded condition context.
- Explicit host concurrency and isolation support.

## Steps

1. Validate schema shape, IDs, actions, declared capabilities, and hook targets.
2. Detect dependency cycles before evaluating conditions.
3. Evaluate only `eq`, `in`, and `exists` conditions against explicit context.
4. Preserve approval steps as exclusive gates; never auto-satisfy them.
5. Build topological dependency waves from eligible steps.
6. Keep a parallel wave only for isolated task/validation steps when the host supports it.
7. Otherwise split deterministically into sequential waves and report exact fallbacks.
8. Emit complete TOON and optional JSON/Markdown projections without executing actions.

## Output Spec

The plan records every step as eligible, skipped, or deferred; selected waves;
approval gates; hooks; fallback reason codes; source and plan fingerprints; and
explicit host capabilities.

Quality gate:

- Pass when the workflow is acyclic, capabilities are declared, conditions are
  bounded, hook targets resolve, and every planned parallel step is isolated.
- Fail closed on invalid workflow structure or ambiguous authority.

## Scope Boundary

- Do not execute workflow actions or hooks.
- Do not grant capabilities, approvals, isolation, or concurrency implicitly.
- Do not mutate policy, feature state, runtime state, or canonical artifacts.
