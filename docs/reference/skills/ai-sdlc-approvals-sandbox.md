---
title: Approvals Sandbox
description: Human-facing operating guide for ai-sdlc-approvals-sandbox, including inputs, authority, artifacts, modes, helpers, gates, recovery, and handoff.
---

# `ai-sdlc-approvals-sandbox`

| Lifecycle position | Primary owner | Supporting roles | Module | Output |
| --- | --- | --- | --- | --- |
| Sandbox escalation decision | Dev | QA | `core` | Sandbox escalation decision record with prefix_rule guidance and residual risk |

## Why it exists

Decide, request, and report sandbox escalation for AI SDLC commands only when the sandbox blocks a required action or the task explicitly requires approved external access.

## Use it when

AI SDLC approvals, sandbox, and command rule workflow. Use when an AI assistant needs to decide whether to request escalated permissions, explain sandbox failures, propose prefix_rule approvals, avoid unsafe command patterns, or document why a command was or was not rerun outside the sandbox. Supports `--quick-flow` for fast assumption-driven execution and `--full-flow` for question-driven verified execution.

If the correct entry point is still unclear, ask the read-only navigator first instead of guessing.

## Do not use it when

- Do not use it to decide product, delivery, or security risk. Use the owning lifecycle skill and accountable human policy instead.


## Who is involved

The summary table above names the primary and supporting human roles for this capability.
- **Agent:** follows this contract, reports assumptions and blockers, and cannot accept protected decisions for the humans above.

## Before you start

- Exact command that failed or requires external access.
- Task reason for the command.
- Sandbox error, expected restriction, and risk profile.

## Tell your agent

```text
Use ai-sdlc-approvals-sandbox for <target>.
Choose --quick-flow for bounded assumption-driven progress or --full-flow
for strict verification only as described below.
Read the required evidence,
produce or report Sandbox escalation decision record with prefix_rule guidance and residual risk, preserve human approval boundaries,
and return blockers plus a complete ai-sdlc-handoff/v1.
```

This is an agent instruction, not a shell command. Terminal commands belong in the helper section.

## What the agent reads

- Collect the exact command that failed or must run outside the sandbox.
- Collect the task reason that makes the command necessary.
- Collect the sandbox error or expected restriction: filesystem, network, listener, GUI, external service, or destructive action.
- Collect whether the command is destructive, secret-bearing, shell-heavy, or reusable.
- Collect an intended narrow `prefix_rule` only when repeated approval is safe.

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
| [`approval_plan.py`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-approvals-sandbox/scripts/approval_plan.py) | Validate an AI SDLC sandbox approval request draft. | `python3 skills/ai-sdlc-approvals-sandbox/scripts/approval_plan.py --help` | Read-only/reporting by default; inspect `--help` and the owning skill before direct use. |

The owning agent normally runs these helpers. A human uses the direct starting point for diagnosis or reproduction after inspecting `--help` and repository policy.

### Contract-provided usage

- Validate approval requests before asking for escalation or recording an approval decision.
- Quick flow: `python3 skills/ai-sdlc-approvals-sandbox/scripts/approval_plan.py --quick-flow --command "<command>" --justification "<user-facing question?>"`
- Full flow: `python3 skills/ai-sdlc-approvals-sandbox/scripts/approval_plan.py --full-flow --command "<command>" --justification "<user-facing question?>" --prefix-rule "<safe reusable prefix>"`
- Use `--prefix-rule` only when proposing a reusable non-destructive approval prefix; omit it for destructive or one-off commands.

## Success criteria

Return this decision record when escalation is requested, denied, or skipped:

```text
Sandbox decision:
- Command: exact command
- Required for: task-specific reason
- Sandbox issue: filesystem | network | listener | GUI | external service | destructive | none
- Escalation: requested | not requested | denied | granted
- Prefix rule: proposed rule | none and why
- Result: passed | failed | skipped | blocked
- Residual risk: none | concrete limitation
```

Quality gate:

- Pass when escalation is narrow, justified by the task, and avoids broad reusable approval for dangerous commands.
- Fail when the request uses vague justification, proposes broad interpreter or shell prefixes, includes secrets, or escalates unrelated work.

## Blockers and recovery

- Skip reusable `prefix_rule` for destructive commands such as `rm`, `git reset`, force push, or data deletion.
- Skip reusable `prefix_rule` for heredocs, redirection, wildcards, command substitution, environment-heavy one-liners, or shell wrappers.
- Warn immediately and avoid reusing commands when a command contains credentials, bearer tokens, private keys, webhook secrets, or production-only values.
- Treat a missing dependency error as a setup issue first, not an escalation reason, unless the dependency download is required and network is blocked.
- Report partial approval when one command segment is approved but another remains blocked.

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

Valid request:

```json
{
  "sandbox_permissions": "require_escalated",
  "justification": "Allow running Go tests with a writable external cache for this package?",
  "prefix_rule": ["go", "test", "./internal/service/..."]
}
```

Invalid counter-example:

```json
{
  "sandbox_permissions": "require_escalated",
  "justification": "Need permissions.",
  "prefix_rule": ["python3"]
}
```

Reject this because the justification is vague and the prefix allows arbitrary scripts.

## Source contract

This page is generated from [`skills/ai-sdlc-approvals-sandbox/SKILL.md`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-approvals-sandbox/SKILL.md). Edit the source contract, rerun the catalog generator, and review both changes together; never hand-edit this page.

[Back to the skill catalog](../skills.md) · [Script reference](../scripts.md) · [Choose a workflow](../../flows/index.md)
