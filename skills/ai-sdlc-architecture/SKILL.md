---
name: ai-sdlc-architecture
description: Optional AI SDLC architecture workflow. Use when an AI assistant needs to define system boundaries, components, interfaces, architectural constraints, alternatives, decisions, tradeoffs, risks, or validation for a feature and produce routed human and machine artifacts linked to requirements and durable decisions. Supports `--quick-flow` for focused design and `--full-flow` for strict decision, risk, and validation coverage.
---

# ai-sdlc-architecture: Traceable System Design

> Optional domain skill, not required by the core module.
> Every rule below is important to follow. None of it can be skipped.
> Architecture artifacts support SDD; they do not replace requirements or ADR authority.

## 0. Skill Card

- Skill name: `ai-sdlc-architecture`
- Primary audience: Architecture, Dev
- Supporting audience: QA, Security, Delivery, BA
- Audience tags: Architecture, Dev, QA, Security
- SDLC stage: Design and implementation planning
- Purpose: Preserve traceable architecture boundaries, decisions, and risks.
- Output: `architecture.md` and `_ai_sdlc/architecture.toon`

### 0.1 Required Inputs

- Implementation feature root.
- Architecture input using `ai-sdlc-architecture-input/v1`.
- Requirement, acceptance, risk, or decision trace targets.

### 0.2 Clarification Rules

- Ask when system boundary, quality attribute, authority, or irreversible choice is ambiguous.
- Separate constraints from decisions and decisions from implementation tasks.
- Record alternatives and consequences for every material decision.
- Do not invent infrastructure, data classification, or production topology.

### 0.2.1 Flow Mode Flags

- Support `--quick-flow` and `--full-flow`; full flow takes precedence.
- Quick flow permits a bounded architecture slice with explicit gaps.
- Full flow requires at least one decision, risk, and validation check.
- Both modes require trace targets for constraints, interfaces, decisions, and risks.

### 0.3 Output Rules

- Return design scope, decision/risk counts, blockers, validation status, and
  output paths directly in the active agent response.
- Before the final response, emit `ai-sdlc-handoff/v1` with `result`,
  `blockers`, `next_required`, and `next_optional`; every action includes
  `reason`, `command`, and `expected_artifact`.
- Do not create `summary.txt`, `*-summary.txt`, or untraced diagrams.
- Keep Markdown authoritative for detail and TOON bounded for routing.

### 0.4 Artifact Routing

- Write `<feature-root>/architecture.md`.
- Write `<feature-root>/_ai_sdlc/architecture.toon`.
- Keep ADRs or decision-log entries separate when organizational authority
  requires them; link their IDs from architecture decisions.
- Do not write into refinement unless architecture work is explicitly upstream.

## 0.4.1 Runtime Path Resolution

- Treat `skills/` in commands as a logical skill root. In a harness source checkout, use `skills/`; in a project-scoped consumer installation, resolve it to `.agents/skills/`. Before running a helper, verify that the selected root contains both this skill and `ai-sdlc-shared-runtime`; block with the missing path if neither layout exists.

## 0.5 Feature State Machine

- Read `<feature-root>/_ai_sdlc/state.toon` before architecture work.
- Architecture is an optional design utility and does not add a core lifecycle stage.
- `--state-check` is read-only; `--begin-state` and `--complete-state` are rejected.
- Route accepted design changes back through SDD and change-impact recovery.

## 0.6 Artifact Metadata And Metatags

- Markdown starts with `artifact_metadata` using schema
  `ai-sdlc-architecture-metadata/v1`.
- Include `metatags` for `ai-sdlc`, `architecture`, `design`, and `traceable`.
- Record feature, workspace, flow mode, state file, trace IDs, and status.

## 0.7 Specs Index

- Read `specs/_ai_sdlc/specs-index.toon` and feature state before broad reads.
- Refresh `specs/specs-index.md` only after a durable architecture write.
- Do not alter `specs-refiniment/_ai_sdlc/specs-index.toon` or
  `specs-refiniment/specs-index.md` for implementation-owned architecture.

## References

- Read `references/architecture-contract.md` for the input schema and design gates.
- Use `scripts/architecture.py` to validate and route canonical outputs.

## Script Usage

```bash
python3 skills/ai-sdlc-architecture/scripts/architecture.py specs/payments --input /tmp/architecture.json --emit --quick-flow
python3 skills/ai-sdlc-architecture/scripts/architecture.py specs/payments --input /tmp/architecture.json --write --full-flow --format toon
```

## Purpose

Add architecture depth when a feature needs it without making architecture
ceremony or the optional module a dependency of every core workflow.

## Inputs

- Capture design context and constraints before components.
- Trace interfaces and decisions to durable requirement or decision IDs.
- Give risks an owner and mitigation.
- Provide executable or inspectable validation evidence.

## Steps

1. Read requirements, decisions, project context, state, and relevant quality findings.
2. Define boundaries, constraints, components, and interfaces.
3. Compare alternatives and record decisions plus consequences.
4. Identify architecture risks, owners, and mitigations.
5. Define validation checks for the design claims.
6. Finalize canonical outputs with the deterministic script.
7. Route implementation changes through SDD tasks and validation.

## Output Spec

`ai-sdlc-architecture/v1` contains context, constraints, components, interfaces,
decisions, risks, and validation checks with trace targets and owners.

Quality gate:

- Pass when boundaries are explicit and every material claim has traceability.
- Full flow fails without decisions, risks, validation, alternatives, consequences,
  risk ownership, or mitigation.

## Examples

A valid decision records `DEC-021`, its requirement traces, selected option,
rationale, alternatives, and operational consequences. “Use microservices
because they scale” is invalid without evidence, boundary, alternatives, or tradeoff.

## Edge Cases

- A local reversible patch may use quick flow and record no new decision.
- External systems remain components with explicit unverified interface assumptions.
- Existing ADRs are referenced, not duplicated.
- Diagram generation is optional; structured contracts remain authoritative.

## Scope Boundary

- Do not approve architecture on behalf of owners.
- Do not provision infrastructure or change production systems.
- Do not replace SDD requirements, tests, tasks, or decisions.
- Do not hide unresolved architecture risks.
- Use `$ai-sdlc-change-impact` when an accepted design changes downstream work.
