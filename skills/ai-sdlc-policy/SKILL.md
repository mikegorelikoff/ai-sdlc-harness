---
name: ai-sdlc-policy
description: AI SDLC versioned policy-as-code workflow. Use when an AI assistant needs to resolve layered delivery policy, evaluate an action with explainable rules and gates, protect organization minimums from weaker overrides, apply or reject an expiring waiver, or select a reusable assurance profile. Supports `--quick-flow` for deterministic evaluation and `--full-flow` for strict owner and exception review.
---

# ai-sdlc-policy: Explainable Delivery Controls

> Internal AI SDLC skill, not client-facing by default.
> Every rule below is important to follow. None of it can be skipped.
> Unknown or invalid policy inputs fail closed when they could weaken protection.

## 0. Skill Card

- Skill name: `ai-sdlc-policy`
- Primary audience: Delivery, Security, Architecture, Release
- Supporting audience: Dev, QA, PM, BA
- Audience tags: Delivery, Security, Architecture, Release, Dev
- SDLC stage: Governance and control evaluation
- Purpose: Resolve policy layers with provenance and evaluate actions against
  protected, versioned, waiver-aware rules.
- Output: `_ai_sdlc/policy-resolution.{toon,json}` or fingerprint-addressed TOON/JSON records
  below `_ai_sdlc/policy-decisions/` when `--write` is requested

### 0.1 Required Inputs

- Action name and JSON context for evaluation.
- Base policy plus optional organization profile, project, and user layers.
- Explicit owner-approved waiver record when an allowed exception is requested.

### 0.2 Clarification Rules

- Ask when action identity, subject, accountable waiver owner, or decision
  reference is missing.
- Reject unknown fields, operators, layer scopes, and ambiguous rule identity.
- Never infer approval or create a waiver on the requester's behalf.

### 0.2.1 Flow Mode Flags

- Support `--quick-flow` and `--full-flow`; full flow takes precedence.
- Both modes use the same fail-closed evaluator and protected-rule semantics.
- Full flow requires explicit review of every matched rule, rejected override,
  required gate, and waiver result.

### 0.3 Output Rules

- Report resolved policy fingerprint, layer provenance, action decision, matched
  rules, required gates, reason codes, and applied or rejected waivers.
- Return validation and handoff summaries directly in the active agent response.
- Emit `ai-sdlc-handoff/v1` with `result`, `blockers`, `next_required`, and
  `next_optional`; actions include `reason`, `command`, and `expected_artifact`.
- Do not create `summary.txt`, `*-summary.txt`, or another standalone summary file.

### 0.4 Artifact Routing

- Keep approved policy layers in visible repository-owned paths.
- Write generated resolution and decision records only below `_ai_sdlc/`.
- Never overwrite a source policy or waiver during evaluation.

## 0.4.1 Runtime Path Resolution

- Treat `skills/` in commands as a logical skill root. In a harness source checkout, use `skills/`; in a project-scoped consumer installation, resolve it to `.agents/skills/`. Before running a helper, verify that the selected root contains both this skill and `ai-sdlc-shared-runtime`; block with the missing path if neither layout exists.

## 0.5 Feature State Machine

- Read canonical `_ai_sdlc/state.toon` before applying a decision to feature
  work. Policy evaluation does not create or advance feature `state.toon`.
- A deny or unsatisfied required gate blocks the owning workflow transition.

## 0.6 Artifact Metadata And Metatags

- Policy-related Markdown uses canonical `artifact_metadata` and `metatags`.
- Machine records use `ai-sdlc-policy-layer/v1`, `ai-sdlc-policy-waiver/v1`,
  `ai-sdlc-policy-resolution/v1`, and `ai-sdlc-policy-decision/v1`.

## 0.7 Specs Index

- Read `_ai_sdlc/specs-index.toon` first and use `specs-index.md` for human
  discovery when evaluation context refers to feature artifacts.
- Policy evaluation does not refresh either specs index.

## References

- Read `references/policy-contract.md` before resolving or evaluating policy.
- Validate source layers with `references/policy-layer.schema.json`, waivers
  with `references/policy-waiver.schema.json`, and decisions with
  `references/policy-decision.schema.json`.
- Reuse organization profiles from `references/profiles/`.
- Use `scripts/policy.py` for resolution, evaluation, and explain output.

## Script Usage

```bash
python3 skills/ai-sdlc-policy/scripts/policy.py . --resolve --profile high-assurance --format toon
python3 skills/ai-sdlc-policy/scripts/policy.py . --evaluate change.apply --context policy-context.json --profile regulated --format toon
python3 skills/ai-sdlc-policy/scripts/policy.py . --explain release.publish --context release-context.json --waiver waiver.json --format markdown
```

## Purpose

Make delivery governance reproducible and inspectable while allowing bounded,
accountable, expiring exceptions without silently weakening organization rules.

## Inputs

- Versioned base, organization, project, and user policy layers.
- A stable action such as `change.apply`, `release.publish`, or
  `command.destructive` and a JSON context object.
- Optional waiver files tied to exact rule IDs, actions, subjects, constraints,
  owners, approvers, decisions, issue times, and expiry times.

## Steps

1. Load the built-in base and optional organization assurance profile.
2. Validate custom layers and merge them in base, organization, project, user order.
3. Reject any lower-layer change that weakens a protected effect, gate set,
   protected flag, or non-waivable boundary.
4. Match rules using only declared fields and deterministic operators.
5. Validate waivers against rule eligibility, action, subject, constraints,
   decision evidence, and the explicit evaluation time.
6. Combine unwaived rules with deny-first, require-second, allow-third precedence.
7. Inspect explain output and satisfy every required gate before acting.

## Output Spec

Complete TOON/JSON resolution records contain normalized rules, provenance, source hashes,
protected rule IDs, and a deterministic fingerprint. Decision records contain
the exact action and context fingerprint, matched and waived rules, gates,
reasons, result, evaluation time, and policy fingerprint.

Quality gate:

- Pass when all layers are valid, protected rules remain at least as strict,
  each waiver is current and authorized, and the action result plus gates are
  understood.
- Fail closed on invalid policy, unknown action, protected weakening, malformed
  or expired waiver, and missing context required by a predicate.

## Examples

A high-assurance profile may add `security-review` and `fresh-evidence` gates to
`change.apply`. A project layer can add more gates. A user layer cannot remove
those gates or turn a protected `require` into `allow`.

## Edge Cases

- Non-matching rules remain visible in explain output only when requested.
- Multiple matching deny rules remain deny even if another rule allows.
- A valid waiver suppresses only its named waivable rule, never an entire action.
- Expiry is evaluated at explicit `--as-of` time for reproducible decisions.

## Scope Boundary

- Do not edit source policy, issue waivers, record approvals, or satisfy gates.
- Do not treat `allow` as authorization outside the evaluated action and context.
- Do not let user or project layers weaken protected organization minimums.
- Do not execute the evaluated action; return the decision to its owning workflow.
