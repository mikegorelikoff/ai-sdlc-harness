---
title: Sdd
description: Human-facing operating guide for ai-sdlc-sdd, including inputs, authority, artifacts, modes, helpers, gates, recovery, and handoff.
---

# `ai-sdlc-sdd`

AI SDLC repository spec-driven development workflow. Use when an AI assistant receives a medium or large feature, refactor, API change, architecture change, provider integration change, or any request that must follow requirements, design, test cases, QA planning, tasks, implementation, and validation. Supports `--quick-flow` for fast assumption-driven execution and `--full-flow` for question-driven verified execution.

| Lifecycle position | Primary owner | Supporting roles | Module | Output |
| --- | --- | --- | --- | --- |
| Repository SDD workflow | Dev | BA, QA, PM | `core` | SDD package, Markdown execution plan, TOON machine plan, validation status, task alignment, and implementation handoff |

## Why it exists

Create, update, validate, and enforce the AI SDLC SDD package for medium and large changes before implementation expands.

## Use it when

AI SDLC repository spec-driven development workflow. Use when an AI assistant receives a medium or large feature, refactor, API change, architecture change, provider integration change, or any request that must follow requirements, design, test cases, QA planning, tasks, implementation, and validation. Supports `--quick-flow` for fast assumption-driven execution and `--full-flow` for question-driven verified execution.

If the correct entry point is still unclear, ask the read-only navigator first instead of guessing.

## Do not use it when

- Do not use it while the customer problem or required behavior is still unclear. Use the relevant refinement workflow instead.
- Do not use it for review-only work or a trivial non-behavioral edit. Use `ai-sdlc-code-review` or the focused task workflow instead.


## Who is involved

- **Accountable/primary:** Dev.
- **Supporting:** BA, QA, PM.
- **Agent:** follows this contract, reports assumptions and blockers, and cannot accept protected decisions for the humans above.

## Before you start

- Medium or large change request.
- Affected systems, APIs, packages, or artifacts.
- Existing spec folder or proposed feature name if available.

## Tell your agent

```text
Use ai-sdlc-sdd for <target>.
Choose --quick-flow for bounded assumption-driven progress or --full-flow
for strict verification only as described below.
Read the required evidence,
produce or report SDD package, Markdown execution plan, TOON machine plan, validation status, task alignment, and implementation handoff, preserve human approval boundaries,
and return blockers plus a complete ai-sdlc-handoff/v1.
```

This is an agent instruction, not a shell command. Terminal commands belong in the helper section.

## What the agent reads

- Read `AGENTS.md` for change classification and repository workflow rules.
- Collect the user request, affected systems, and likely spec name.
- Search existing `specs/` folders for a matching active or historical spec.
- Use `$ai-sdlc-ba`, `$ai-sdlc-test-cases`, and `$ai-sdlc-qa` when those phases are incomplete.
- In `--full-flow`, read `specs-refiniment/_ai_sdlc/specs-index.toon`, upstream `state.toon`, `delivery-spec.md`, `qa-readiness.md`, and `decision-log.md` before finalizing implementation SDD.
- Read existing code only after the spec intent and affected surface are clear enough to avoid scope drift.

## What it may write

- Maintain a feature decision log whenever this skill records, resolves, changes, or depends on a product, delivery, QA, security, validation, branching, implementation, or rollout decision.
- For PM, BA, QA, Delivery, discovery, planning, refinement, and readiness work, write decisions to `specs-refiniment/<feature-name>/decision-log.md`.
- For developer implementation SDD work, write decisions to `specs/<feature-name>/decision-log.md`.
- Each decision-log entry must include date, decision, context or evidence, options considered when relevant, owner, status, and links to affected artifacts, tasks, tests, or validation evidence.
- Use this exact decision-log structure:

  ```markdown
  # Decision Log

  | ID | Date | Status | Owner | Decision | Context/Evidence | Options Considered | Affected Artifacts | Validation/Trace Links |
  | --- | --- | --- | --- | --- | --- | --- | --- | --- |
  | DEC-001 | YYYY-MM-DD | proposed / accepted / superseded / rejected | role or name | concise decision | source facts, artifact links, or evidence | option A; option B; recommended default | affected docs, tasks, code, tests, or rollout notes | requirement IDs, test IDs, validation commands, PRs, commits, or tickets |
  ```

- Use `specs/` only for developer implementation SDD packages and repo-governance artifacts.
- Do not place PM, BA, QA, Delivery, discovery, planning, refinement, or readiness outputs in `specs/`; those belong at `specs-refiniment/<feature-name>/<file.md>`.
- When consuming `specs-refiniment/<feature-name>/<file.md>`, treat it as upstream refinement context and create or update `specs/` only when implementation work is explicitly in scope.

## Human checkpoints

- Ask concise questions before finalizing when role, artifact, requirements, scope, audience, or constraints are unclear.
- If optional information is missing, mark it as `TBD`, `Not provided`, or `Assumption` instead of inventing it.
- Separate confirmed facts from assumptions and open questions.
- Do not proceed to downstream synthesis when a required upstream artifact or decision is missing.

Humans accept or reject material product, security, QA, policy, rollout, release, and destructive-action decisions; a complete agent handoff is evidence, not approval.

## Flow modes

- Support two explicit execution flags: `--quick-flow` and `--full-flow`.
- If both flags are supplied, `--full-flow` takes precedence because it is the stricter mode.
- `--quick-flow`: move fast, make high-quality progress with available context, avoid clarification questions unless continuing would create material product, security, compliance, data-loss, or irreversible implementation risk.
- In `--quick-flow`, use documented assumptions, recommended defaults, existing repository patterns, and the nearest available artifact evidence; record important assumptions and decisions in `decision-log.md`.
- In `--quick-flow`, run only focused checks that are directly relevant, cheap, and likely to catch regressions for the requested work; report any skipped broader checks as residual risk.
- `--full-flow`: ask concise clarification questions when inputs, scope, ownership, acceptance criteria, or decisions are unclear; do not silently assume material requirements.
- In `--full-flow`, verify upstream and downstream artifacts, decision-log entries, traceability links, acceptance criteria, and validation evidence before finalizing.
- In `--full-flow`, SDD must consume upstream refinement context from `specs-refiniment/<feature-name>/`; missing or incomplete delivery-spec or QA-readiness context blocks implementation SDD handoff.
- In `--full-flow`, run or recommend the skill-appropriate gates, reviews, scripts, and validation commands needed for end-to-end confidence; document any blocked verification explicitly.
- When neither flag is supplied, follow the skill default rules and choose the least risky behavior for the request size and domain.

## Deterministic helpers

Paths beginning with `skills/` below are canonical **source-checkout** forms for maintainers and CI. In a consumer repository, normally tell the installed skill to act; for human diagnosis, use the matching project-scoped `.agents/skills/<skill>/...` path reported by your host. Do not expect source-only `skills/_shared` to exist after installation.

| Helper | Purpose | Direct starting point | Repository effect |
| --- | --- | --- | --- |
| [`analyze_spec.py`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-sdd/scripts/analyze_spec.py) | Validate cross-artifact consistency for an AI SDLC SDD spec. | `python3 skills/ai-sdlc-sdd/scripts/analyze_spec.py --help` | Read-only/reporting by default; inspect `--help` and the owning skill before direct use. |
| [`check_checklist.py`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-sdd/scripts/check_checklist.py) | Validate requirement-quality checklist rules for an AI SDLC SDD spec. | `python3 skills/ai-sdlc-sdd/scripts/check_checklist.py --help` | Read-only/reporting by default; inspect `--help` and the owning skill before direct use. |
| [`check_clarify.py`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-sdd/scripts/check_clarify.py) | Validate clarify-gate requirements for an AI SDLC SDD spec. | `python3 skills/ai-sdlc-sdd/scripts/check_clarify.py --help` | Read-only/reporting by default; inspect `--help` and the owning skill before direct use. |
| [`check_refinement_context.py`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-sdd/scripts/check_refinement_context.py) | Check upstream refinement context for SDD full-flow work. | `python3 skills/ai-sdlc-sdd/scripts/check_refinement_context.py --help` | Read-only/reporting by default; inspect `--help` and the owning skill before direct use. |
| [`plan_links.py`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-sdd/scripts/plan_links.py) | Create and validate SDD `plan.md` and `_ai_sdlc/plan.toon` execution links. | `python3 skills/ai-sdlc-sdd/scripts/plan_links.py --help` | May write only through an explicit mutation mode; start with `--help`, check, preview, or emit. |
| [`resolve_active_spec.py`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-sdd/scripts/resolve_active_spec.py) | Resolve the active AI SDLC feature spec from explicit, changed, or branch context. | `python3 skills/ai-sdlc-sdd/scripts/resolve_active_spec.py --help` | Read-only/reporting by default; inspect `--help` and the owning skill before direct use. |
| [`sdd_artifact_scaffold.py`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-sdd/scripts/sdd_artifact_scaffold.py) | Write SDD artifact sections from stdin and finalize deterministic Markdown. | `python3 skills/ai-sdlc-sdd/scripts/sdd_artifact_scaffold.py --help` | May write only through an explicit mutation mode; start with `--help`, check, preview, or emit. |
| [`sdd_context.py`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-sdd/scripts/sdd_context.py) | Emit a bounded TOON context pack for one implementation SDD package. | `python3 skills/ai-sdlc-sdd/scripts/sdd_context.py --help` | Read-only/reporting by default; inspect `--help` and the owning skill before direct use. |
| [`sdd_status.py`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-sdd/scripts/sdd_status.py) | Report AI SDLC SDD workflow status for the active feature spec. | `python3 skills/ai-sdlc-sdd/scripts/sdd_status.py --help` | Read-only/reporting by default; inspect `--help` and the owning skill before direct use. |
| [`spec_helpers.py`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-sdd/scripts/spec_helpers.py) | Shared helpers for AI SDLC SDD spec parsing and active-spec resolution. | `Imported helper; use the owning skill rather than invoking it directly.` | Read-only/reporting by default; inspect `--help` and the owning skill before direct use. |
| [`validate_spec.py`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-sdd/scripts/validate_spec.py) | Validate an AI SDLC SDD spec folder. | `python3 skills/ai-sdlc-sdd/scripts/validate_spec.py --help` | Read-only/reporting by default; inspect `--help` and the owning skill before direct use. |

The owning agent normally runs these helpers. A human uses the direct starting point for diagnosis or reproduction after inspecting `--help` and repository policy.

### Contract-provided usage

- Use SDD scripts as ordered gates for implementation work; pass the same flow flag supplied to the skill.
- Resolve active spec when the target is unclear: `python3 skills/ai-sdlc-sdd/scripts/resolve_active_spec.py --quick-flow --files <changed-file>...` or `python3 skills/ai-sdlc-sdd/scripts/resolve_active_spec.py --full-flow <spec-or-folder>`.
- Check workflow state for people with `python3 skills/ai-sdlc-sdd/scripts/sdd_status.py --spec specs/<feature-name> --quick-flow`; agents add `--format toon`, and full-flow remains required before handoff.
- Build bounded implementation context: `python3 skills/ai-sdlc-sdd/scripts/sdd_context.py specs/<feature-name> --quick-flow`; use `--cache-context` only when cross-session reuse is useful.
- Write one artifact section: `python3 skills/ai-sdlc-sdd/scripts/sdd_artifact_scaffold.py specs/<feature-name> --artifact <requirements|design|test-cases|qa|tasks> --section "<section>" --quick-flow`; provide only the section body on stdin.
- Repeat section writes and then replace `--section ...` with `--finalize`; the AI must not create a temporary content file or directly edit the generated Markdown artifact.
- Add a decision with `--decision-row` and one nine-cell Markdown table row on stdin; `--artifact` is not required for this action.
- Validate structure: `python3 skills/ai-sdlc-sdd/scripts/validate_spec.py specs/<feature-name> --quick-flow`.
- Create or refresh the execution plan pair: `python3 skills/ai-sdlc-sdd/scripts/plan_links.py specs/<feature-name> --write --quick-flow|--full-flow`.
- Emit compact machine plan only: `python3 skills/ai-sdlc-sdd/scripts/plan_links.py specs/<feature-name> --emit-toon --quick-flow|--full-flow`.
- Validate the execution plan links: `python3 skills/ai-sdlc-sdd/scripts/plan_links.py specs/<feature-name> --check --quick-flow|--full-flow`.
- Full-flow upstream gate: `python3 skills/ai-sdlc-sdd/scripts/check_refinement_context.py specs/<feature-name> --full-flow`.
- Full-flow pre-implementation gates, in order: `check_refinement_context.py`, `check_clarify.py`, `check_checklist.py`, `plan_links.py --check`, `analyze_spec.py`, then `validate_spec.py`, each with `specs/<feature-name> --full-flow`.
- Use quick flow for fast structural confidence; use full flow before expanding implementation tasks, handoff, review, or commit prep.

## Success criteria

Use this completion report:

```text
SDD compliance:
- Spec: specs/NNN-feature-name
- Change size: small | medium | large
- Requirements: updated | unchanged with reason
- Design: updated | unchanged with reason
- Test cases: updated | unchanged with reason
- QA: updated | unchanged with reason
- Tasks: completed task numbers and remaining task numbers
- Plan: `_ai_sdlc/plan.toon` and `plan.md` updated | unchanged with reason
- Validation: command -> outcome
- Scope control: no drift | drift and spec update
- Residual risk: none | concrete issue
```

Quality gate:

- Pass when the SDD package exists, required sections are populated, `_ai_sdlc/plan.toon` links AC/TC/TASK/DEC status and dependencies, `plan.md` reflects those links for humans, tasks match implementation, and the validator passes.
- Fail when code starts before missing spec artifacts are created, when implementation exceeds `tasks.md`, when the clarify/checklist/analyze gates fail, or when task checkboxes are marked complete without evidence.

## Blockers and recovery

- Reuse an existing active spec when its requirements clearly match the user request.
- Create a new spec when an existing completed or archived spec is only historically related.
- Add `TODO(dm): exact question` when a required decision cannot be discovered and guessing would affect scope, contract, security, or rollout.
- Use `Assumptions`, `Open Questions`, and `Decision Status` sections in `requirements.md` for clarify-gate evidence.
- Update the spec first when code and spec conflict during an active change.
- Treat unlisted historical numbered specs as `unclassified` until `specs/spec-registry.md` says otherwise.
- Do not treat scaffolded historical `qa.md` or `test-cases.md` files with unresolved TODOs as validated evidence.
- Treat missing `_ai_sdlc/plan.toon` or `plan.md` as a structural SDD failure, even in quick flow.
- When `_ai_sdlc/plan.toon` and `plan.md` disagree, trust `_ai_sdlc/plan.toon` for machine task status and regenerate `plan.md` with `plan_links.py --write`.
- In full flow, treat missing upstream refinement delivery or QA readiness as a blocker unless the predecessor is explicitly skipped with a decision reference.

On a blocker, preserve failed/stale evidence, name the accountable owner and exact missing input, then resume this skill or the earliest reopened producer. Never manufacture completion by editing derived state.

## Handoff

- Keep output structured with headings and bullets.
- Make findings, gaps, risks, and blockers explicit.
- Tie recommendations to evidence from the provided artifact, repository, `specs-refiniment/<feature-name>/<file.md>` workspace, or user context.
- Include role ownership when the output creates follow-up work for BA, QA, Dev, PM, or Delivery.
- Return progress, completion, validation, and handoff summaries directly in the Codex response.
- Before the final response, emit the `ai-sdlc-handoff/v1` contract with `result`, `blockers`, `next_required`, and `next_optional`; every action includes `reason`, `command`, and `expected_artifact`.
- Do not create `summary.txt`, `*-summary.txt`, or another standalone summary file unless the user explicitly requests one.
- Keep durable writes limited to the canonical lifecycle artifacts, decision log, human-readable index, and `_ai_sdlc` machine files.
- Let shared helpers migrate legacy paths on the next write; never overwrite or manually merge divergent legacy and canonical files.

The downstream consumer rechecks artifacts and freshness; it does not trust a previous chat's completion claim.

## State, metadata, and indexes

??? info "Feature state"

    - Maintain feature lifecycle state in TOON at `specs-refiniment/<feature-name>/_ai_sdlc/state.toon` for refinement work and `specs/<feature-name>/_ai_sdlc/state.toon` for implementation work.
    - Before executing this skill for a feature, check the state machine with `python3 skills/_shared/state_machine.py check --feature <feature-name> --skill <this-skill-name> --workspace <refinement|implementation> --quick-flow|--full-flow`.
    - When this skill starts durable work, mark it in progress with `begin`; when the skill's required artifact or review is complete, mark it done with `complete` and include `--artifacts <path>` plus `--decision-ref DEC-###` when a decision was involved.
    - In `--full-flow`, do not proceed when predecessor stages are incomplete, another lifecycle skill is active, or the state file reports a blocker.
    - In `--quick-flow`, a predecessor skip is allowed only when continuing is low risk and the command includes `--assumption "..."` or `--decision-ref DEC-###`; record the same assumption or decision in `decision-log.md`.
    - Use `python3 skills/_shared/state_machine.py status --feature <feature-name> --workspace <refinement|implementation> --format toon` to emit compact LLM-readable state before choosing the next skill.
    - The state machine is feature-scoped: do not reuse a `state.toon` across unrelated feature folders.

??? info "Artifact metadata"

    - Every Markdown artifact generated or updated by this skill must start with an `artifact_metadata` YAML frontmatter block before the first visible heading.
    - Use schema `ai-sdlc-artifact-metadata/v1` and keep these fields current: `feature`, `artifact`, `path`, `workspace`, `skill`, `flow_mode`, `state_file`, `decision_log`, `status`, `owner`, `created_at`, `updated_at`, `trace_ids`, `related_artifacts`, `validation`, and `metatags`.
    - `metatags` must include at minimum `ai-sdlc`, the workspace (`refinement` or `implementation`), this skill name, the artifact type or filename stem, and a lifecycle/status tag such as `draft`, `review`, `approved`, or `validated`.
    - When `--quick-flow` is active, set `flow_mode: quick`, keep assumptions visible in the body, and add tags for major defaults or unresolved risk only when they help retrieval.
    - When `--full-flow` is active, set `flow_mode: full`, keep blockers and validation evidence reflected in `status`, `validation`, `trace_ids`, and `related_artifacts`.
    - Update metadata whenever the artifact path, status, owner, trace links, validation evidence, related artifacts, or decision references change.
    - Metadata is an index for routing, retrieval, and traceability; it does not replace the artifact body, `decision-log.md`, or `state.toon`.

??? info "Specs index"

    - Before searching across feature folders, inspect the compact LLM index first: `specs-refiniment/_ai_sdlc/specs-index.toon` for refinement work or `specs/_ai_sdlc/specs-index.toon` for implementation work.
    - Use the human-readable index at `specs-refiniment/specs-index.md` or `specs/specs-index.md` when reporting feature coverage, artifact inventory, or handoff status to people.
    - After this skill creates or materially updates an artifact, refresh the matching workspace index with `python3 skills/_shared/ai_sdlc_specs_index.py --workspace <refinement|implementation> --quick-flow|--full-flow`.
    - In `--quick-flow`, rely on `specs-index.toon` to choose the smallest relevant artifact set before opening files.
    - In `--full-flow`, verify the updated artifact appears in both `specs-index.toon` and `specs-index.md` before final handoff.
    - The specs index summarizes artifact metadata and state; it does not replace reading the selected source artifacts when details, approvals, or validation evidence matter.

## Example

Spec folder shape:

```text
specs/177-skill-instruction-upgrade/
  requirements.md
  design.md
  test-cases.md
  qa.md
  tasks.md
  _ai_sdlc/plan.toon
  plan.md
```

Completion report sample:

```text
SDD compliance:
- Spec: specs/177-skill-instruction-upgrade
- Change size: medium
- Requirements: updated
- Design: updated
- Test cases: updated
- QA: updated
- Tasks: 1-10 completed
- Plan: _ai_sdlc/plan.toon and plan.md updated
- Validation: python3 skills/ai-sdlc-sdd/scripts/validate_spec.py specs/177-skill-instruction-upgrade -> passed
- Scope control: no drift
- Residual risk: none
```

Invalid counter-example:

```text
Implemented feature; will write spec later.
```

Reject this for medium and large work because the spec is the source of truth.

## Source contract

This page is generated from [`skills/ai-sdlc-sdd/SKILL.md`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-sdd/SKILL.md). Edit the source contract, rerun the catalog generator, and review both changes together; never hand-edit this page.

[Back to the skill catalog](../skills.md) · [Script reference](../scripts.md) · [Choose a workflow](../../flows/index.md)
