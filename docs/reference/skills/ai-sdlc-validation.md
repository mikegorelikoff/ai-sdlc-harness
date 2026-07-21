---
title: Validation
description: Human-facing operating guide for ai-sdlc-validation, including inputs, authority, artifacts, modes, helpers, gates, recovery, and handoff.
---

# `ai-sdlc-validation`

| Lifecycle position | Primary owner | Supporting roles | Module | Output |
| --- | --- | --- | --- | --- |
| Implementation validation | Dev | QA, BA | `core` | Focused validation commands, outcomes, coverage notes, and residual risk |

## Why it exists

Select, run, and report focused deterministic validation checks for AI SDLC code, SQL, API, provider, SDD, documentation, and tool-governance changes.

## Use it when

AI SDLC backend validation workflow. Use when an AI assistant needs to validate Go, SQL, API, provider integration, SDD, or documentation changes in this repository and choose focused deterministic checks without running unrelated expensive tests by default. Supports `--quick-flow` for fast assumption-driven execution and `--full-flow` for question-driven verified execution.

If the correct entry point is still unclear, ask the read-only navigator first instead of guessing.

## Do not use it when

- Do not use it when expected behavior is undefined. Use `ai-sdlc-sdd` or the QA requirements workflow instead.
- Do not use it to produce review findings. Use `ai-sdlc-code-review` or `ai-sdlc-security-testing` instead.


## Who is involved

The summary table above names the primary and supporting human roles for this capability.
- **Agent:** follows this contract, reports assumptions and blockers, and cannot accept protected decisions for the humans above.

## Before you start

- Changed files, diff, or explicit validation target.
- Active spec and QA context when user-visible or release-sensitive.
- Sandbox constraints and previous validation output if relevant.

## Tell your agent

```text
Use ai-sdlc-validation for <target>.
Choose --quick-flow for bounded assumption-driven progress or --full-flow
for strict verification only as described below.
Read the required evidence,
produce or report Focused validation commands, outcomes, coverage notes, and residual risk, preserve human approval boundaries,
and return blockers plus a complete ai-sdlc-handoff/v1.
```

This is an agent instruction, not a shell command. Terminal commands belong in the helper section.

## What the agent reads

- Collect changed files from `git status --short`, `git diff --name-only`, or explicit user-provided paths.
- Read the active spec and `qa.md` when the work is medium, large, release-sensitive, or user-visible.
- Collect previous validation output only when it is current for the same diff signature.
- Collect sandbox constraints that affect Go cache, network access, local listeners, or external services.
- Run the validation planner when changed files are not trivial:

  ```bash
  python3 skills/ai-sdlc-validation/scripts/validation_plan.py
  ```

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
- In `--full-flow`, run or recommend the skill-appropriate gates, reviews, scripts, and validation commands needed for end-to-end confidence; document any blocked verification explicitly.
- When neither flag is supplied, follow the skill default rules and choose the least risky behavior for the request size and domain.

## Deterministic helpers

Paths beginning with `skills/` below are canonical **source-checkout** forms for maintainers and CI. In a consumer repository, normally tell the installed skill to act; for human diagnosis, use the matching project-scoped `.agents/skills/<skill>/...` path reported by your host. Do not expect source-only `skills/_shared` to exist after installation.

| Helper | Purpose | Direct starting point | Repository effect |
| --- | --- | --- | --- |
| [`run_validation.py`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-validation/scripts/run_validation.py) | Execute a reviewed argv-only validation plan and write current evidence. | `python3 skills/ai-sdlc-validation/scripts/run_validation.py --help` | May write only through an explicit mutation mode; start with `--help`, check, preview, or emit. |
| [`validation_plan.py`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-validation/scripts/validation_plan.py) | Suggest focused AI SDLC validation commands from changed files. | `python3 skills/ai-sdlc-validation/scripts/validation_plan.py --help` | Read-only/reporting by default; inspect `--help` and the owning skill before direct use. |

The owning agent normally runs these helpers. A human uses the direct starting point for diagnosis or reproduction after inspecting `--help` and repository policy.

### Contract-provided usage

- Run validation planning after identifying changed files and before choosing commands manually.
- Quick flow: `python3 skills/ai-sdlc-validation/scripts/validation_plan.py --quick-flow <changed-file>...`
- Full flow: `python3 skills/ai-sdlc-validation/scripts/validation_plan.py --full-flow <changed-file>...`
- If no files are supplied, the script inspects the current git worktree.
- Execute the suggested commands that match the requested risk level; document skipped broader commands as residual risk.

## Success criteria

Use this format:

```text
Validation:
- command: exact command
  outcome: passed | failed | skipped | blocked
  reason: why this command was selected or skipped

Coverage:
- Changed surface: files or package group.
- Behavior covered: requirement, scenario, or risk covered by the command.

Residual risk:
- none | explicit unvalidated behavior and why it remains.
```

Quality gate:

- Pass when validation commands match the changed surfaces, required checks are current for the active diff, and skipped checks include residual risk.
- Fail when validation is broad but irrelevant, narrow but misses a changed contract, or reports success while a command failed.

## Blockers and recovery

- Mark a check `blocked` when sandbox, missing dependency, missing credential, or unavailable service prevents execution.
- Request escalation only after a required command fails for a likely sandbox reason; do not escalate to bypass project policy.
- Run broader suites after focused checks when the changed surface spans handlers, services, providers, config, or generated contracts.
- Do not run production integrations unless the user explicitly requests them and required credentials are already available through approved mechanisms.
- Treat stale validation as absent when files changed after the command ran.

On a blocker, preserve failed/stale evidence, name the accountable owner and exact missing input, then resume this skill or the earliest reopened producer. Never manufacture completion by editing derived state.

## Handoff

- Keep output structured with headings and bullets.
- Make findings, gaps, risks, and blockers explicit.
- Tie recommendations to evidence from the provided artifact, repository, `specs-refiniment/<feature-name>/<file.md>` workspace, or user context.
- Include role ownership when the output creates follow-up work for BA, QA, Dev, PM, or Delivery.
- Return progress, completion, validation, and handoff summaries directly in the active agent response.
- Before the final response, emit the `ai-sdlc-handoff/v1` contract with `result`, `blockers`, `next_required`, and `next_optional`; every action includes `reason`, `command`, and `expected_artifact`.
- Do not create `summary.txt`, `*-summary.txt`, or another standalone summary file unless the user explicitly requests one.
- Keep durable writes limited to the canonical lifecycle artifacts, decision log, human-readable index, and `_ai_sdlc` machine files.
- Let shared helpers migrate legacy paths on the next write; never overwrite or manually merge divergent legacy and canonical files.

The downstream consumer rechecks artifacts and freshness; it does not trust a previous chat's completion claim.

## State, metadata, and indexes

??? info "Feature state"

    - Maintain feature lifecycle state in TOON at `specs-refiniment/<feature-name>/_ai_sdlc/state.toon` for refinement work and `specs/<feature-name>/_ai_sdlc/state.toon` for implementation work.
    - Before executing this skill for a feature, check the state machine with `python3 skills/ai-sdlc-shared-runtime/scripts/state_machine.py check --feature <feature-name> --skill <this-skill-name> --workspace <refinement|implementation> --quick-flow|--full-flow`.
    - When this skill starts durable work, mark it in progress with `begin`; when the skill's required artifact or review is complete, mark it done with `complete` and include `--artifacts <path>` plus `--decision-ref DEC-###` when a decision was involved.
    - In `--full-flow`, do not proceed when predecessor stages are incomplete, another lifecycle skill is active, or the state file reports a blocker.
    - In `--quick-flow`, a predecessor skip is allowed only when continuing is low risk and the command includes `--assumption "..."` or `--decision-ref DEC-###`; record the same assumption or decision in `decision-log.md`.
    - Use `python3 skills/ai-sdlc-shared-runtime/scripts/state_machine.py status --feature <feature-name> --workspace <refinement|implementation> --format toon` to emit compact LLM-readable state before choosing the next skill.
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
    - After this skill creates or materially updates an artifact, refresh the matching workspace index with `python3 skills/ai-sdlc-shared-runtime/scripts/ai_sdlc_specs_index.py --workspace <refinement|implementation> --quick-flow|--full-flow`.
    - In `--quick-flow`, rely on `specs-index.toon` to choose the smallest relevant artifact set before opening files.
    - In `--full-flow`, verify the updated artifact appears in both `specs-index.toon` and `specs-index.md` before final handoff.
    - The specs index summarizes artifact metadata and state; it does not replace reading the selected source artifacts when details, approvals, or validation evidence matter.

## Example

Focused Go package change:

```text
Validation:
- command: GOCACHE=/tmp/ai-sdlc-go-cache go test ./internal/service -run 'TestLoanTransfer|TestReturnPreflight' -count=1
  outcome: passed
  reason: covers changed service behavior and preflight failure paths.
- command: git diff --check
  outcome: passed
  reason: required whitespace validation for all changes.

Residual risk:
- none
```

Tool setup change:

```text
Validation:
- command: PYTHONPYCACHEPREFIX=/tmp/ai-sdlc-harness-pycache python3 -m py_compile skills/ai-sdlc-validation/scripts/validation_plan.py
  outcome: passed
  reason: validates changed skill metadata.
- command: python3 skills/ai-sdlc-sdd/scripts/sdd_status.py --spec specs/185-spec-kit-sdd-quality-gates
  outcome: passed
  reason: confirms the active governance spec is structurally valid and ready for implementation.
- command: find skills -name SKILL.md -maxdepth 2
  outcome: passed
  reason: validates SDD governance shape.
```

Invalid counter-example:

```text
Validation passed.
```

Reject this because it omits exact commands, changed surface coverage, and residual risk.

## Source contract

This page is generated from [`skills/ai-sdlc-validation/SKILL.md`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-validation/SKILL.md). Edit the source contract, rerun the catalog generator, and review both changes together; never hand-edit this page.

[Back to the skill catalog](../skills.md) · [Script reference](../scripts.md) · [Choose a workflow](../../flows/index.md)
