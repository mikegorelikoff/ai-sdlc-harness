---
title: Test Cases
description: Human-facing operating guide for ai-sdlc-test-cases, including inputs, authority, artifacts, modes, helpers, gates, recovery, and handoff.
---

# `ai-sdlc-test-cases`

AI SDLC test-case-driven testing workflow. Use when an AI assistant is asked to derive test cases, create a test plan, expand coverage, or write tests from explicit scenarios before implementing unit, service, transport, or integration tests. Supports `--quick-flow` for fast assumption-driven execution and `--full-flow` for question-driven verified execution. Explicit full or end-to-end spec refinement requests continue through the existing 18-stage refinement cascade.

| Lifecycle position | Primary owner | Supporting roles | Module | Output |
| --- | --- | --- | --- | --- |
| Implementation test design | QA | Dev, BA | `core` | Scenario matrix with requirement refs, verifiable outcomes, automation paths, and execution order |

## Why it exists

Derive executable AI SDLC test scenarios from requirements or delivery context and place QA refinement artifacts under `specs-refiniment/<feature-name>/<file.md>` when writing files.

## Use it when

AI SDLC test-case-driven testing workflow. Use when an AI assistant is asked to derive test cases, create a test plan, expand coverage, or write tests from explicit scenarios before implementing unit, service, transport, or integration tests. Supports `--quick-flow` for fast assumption-driven execution and `--full-flow` for question-driven verified execution. Explicit full or end-to-end spec refinement requests continue through the existing 18-stage refinement cascade.

If the correct entry point is still unclear, ask the read-only navigator first instead of guessing.

## Do not use it when

- Do not use it while requirements or test strategy still have blocking gaps. Use `ai-sdlc-qa-requirements-gap-review` or `ai-sdlc-test-scope-and-strategy-design` instead.


## Who is involved

- **Accountable/primary:** QA.
- **Supporting:** Dev, BA.
- **Agent:** follows this contract, reports assumptions and blockers, and cannot accept protected decisions for the humans above.

## Before you start

- Requirements, design, and behavior under test.
- Affected package, endpoint, provider, workflow, or contract.
- Known fixtures, mocks, and unavailable dependencies.

## Tell your agent

```text
Use ai-sdlc-test-cases for <target>.
Choose --quick-flow for bounded assumption-driven progress or --full-flow
for strict verification only as described below.
Read the required evidence,
produce or report Scenario matrix with requirement refs, verifiable outcomes, automation paths, and execution order, preserve human approval boundaries,
and return blockers plus a complete ai-sdlc-handoff/v1.
```

This is an agent instruction, not a shell command. Terminal commands belong in the helper section.

## What the agent reads

- Read the provided requirements, delivery spec, stories, workflows, risks, and existing test cases.
- Read existing QA notes from `specs-refiniment/<feature-name>/<file.md>` when acceptance or manual validation already exists.
- Collect the changed behavior, contract, bug, regression risk, endpoint, provider, asset, or workflow under test.
- Collect existing test files for the affected package when implementing tests.
- Read `references/test-case-template.md` when the scenario matrix needs reusable wording.
- Collect known fixtures, mocks, seeded data, and unavailable dependencies.

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

- When writing or updating files, place PM, BA, QA, Delivery, discovery, planning, refinement, and readiness artifacts at `specs-refiniment/<feature-name>/<file.md>`.
- Use the path pattern `specs-refiniment/<feature-name>/<file.md>`; choose a stable feature slug when known, otherwise use `tbd-<short-topic>` for `<feature-name>`.
- Do not write this skill's output into `specs/`; that folder is reserved for developer implementation SDD artifacts.
- If the user explicitly asks to convert a refined artifact into developer implementation work, hand off to `$ai-sdlc-sdd`.

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

| Helper | Purpose | Direct starting point | Repository effect |
| --- | --- | --- | --- |
| [`case_matrix.py`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-test-cases/scripts/case_matrix.py) | Compress requirements into executable test-case matrix signals. | `python3 skills/ai-sdlc-test-cases/scripts/case_matrix.py --feature <feature-name> --quick-flow <input.md>...` | Read-only/reporting by default; inspect `--help` and the owning skill before direct use. |

The owning agent normally runs these helpers. A human uses the direct starting point for diagnosis or reproduction after inspecting `--help` and repository policy.

### Contract-provided usage

- In default and full flow, always run this skill's primary analysis script with `--format toon --budget-tokens 24000` before drafting; explicit inputs are priority evidence but do not replace the rest of the feature package.
- Read this skill's reference file before writing sections. Use its detailed tables and quality bar, not only the compact scaffold headings.
- Run the primary script with `--emit-template` in the active flow mode to obtain the exact shared context headings and required stage table columns before section writes.
- Make every default/full artifact self-contained by completing all ten shared feature-context sections plus the stage-specific profile sections. Quick flow may use the compact stage-only draft.
- Follow every `next_reads` entry before finalization and list every consumed source in `Source Coverage`; do not claim whole-feature context from a partial source set.
- Keep the final artifact within `--max-artifact-tokens 24000`; condense repetition instead of dropping feature dimensions or source traceability.

- Run `scripts/case_matrix.py` before drafting or updating this skill's artifact when inputs are longer than a few bullets, when traceability matters, or when a flow flag is supplied. For agent analysis, pass `--format toon`, read `anchors` first, and open only `next_reads`; without that flag the script keeps its human-readable Markdown output.
- Quick flow analysis: `python3 skills/ai-sdlc-test-cases/scripts/case_matrix.py --feature <feature-name> --quick-flow <input.md>...`
- Full flow analysis: `python3 skills/ai-sdlc-test-cases/scripts/case_matrix.py --feature <feature-name> --full-flow <input.md>...`
- To write content, pass one canonical heading with `--section "<section>"`; provide only that section body on stdin, without H1, H2, frontmatter, or a temporary content file.
- Repeat `--section` for each required section, then run the same script with `--finalize` to validate the artifact and refresh metadata and specs indexes.
- The AI must not write or directly edit the routed Markdown artifact; the script owns scaffold creation, section placement, and durable file writes.
- Use `--decision-row` with one nine-cell Markdown table row on stdin when a decision-log entry is required.
- Legacy `--emit-template`, `--emit-decision-log-entry`, and `--write` remain available for compatibility.
- Use `--quick-flow` for first-pass synthesis with assumptions; use `--full-flow` before readiness, handoff, signoff, or any decision-sensitive output.

## Success criteria

Use this format:

```text
Scope:
- In scope:
  - Behavior, contract, endpoint, workflow, or artifact covered.
- Out of scope:
  - Behavior, contract, endpoint, workflow, or artifact deliberately excluded.

Scenario matrix:
| ID | Requirement ref | Scenario | Setup | Trigger | Verifiable outcome | Layer | Automation |
| --- | --- | --- | --- | --- | --- | --- | --- |
| TC-001 | AC-001, story ID, workflow, risk, or artifact section | Scenario name | Fixture/state | Action | Command, checklist, or before/after pair | unit/service/transport/integration/QA/manual | script path + invocation, CI step, or manual blocker |

Automation plan:
- TC-001: exact command or CI step, target file if new, expected pass condition.

Execution order:
1. Layer: run condition; blocks: later layer or release gate; failure action: stop, fix, rerun, or escalate.

Decisions required:
- Question: decision needed.
  Options:
  A. Option A
  B. Option B
  C. Option C
  Recommended default: option and reason.
  Owner: role or person.
  Blocking: yes | no.
```

Quality gate:

- Pass when every scenario has scope fit, requirement ref, setup, trigger, verifiable outcome, layer, concrete automation path, and execution-order placement.
- Pass when every manual scenario uses `Manual — automate by YYYY-MM-DD — blocker: reason`.
- Pass when every unresolved item is a structured decision with options and recommended default.
- Fail when any scenario lacks a spec ref, uses prose-only expected outcomes, says only `Manual review`, contains `TODO`, or leaves layer mapping as descriptive text instead of execution order.

## Blockers and recovery

- Mark expected behavior as a structured decision when the spec is silent and code behavior is inconsistent.
- Prefer lower-layer tests when they prove the behavior without full integration setup.
- Use integration tests only when provider adapters, HTTP contracts, migrations, or cross-package behavior must be exercised together.
- Mark flaky or external-service-dependent scenarios as manual only with `Manual — automate by YYYY-MM-DD — blocker: reason`.
- Do not invent provider responses; use documented fixtures, existing mocks, or a structured decision with a recommended default.
- Do not output `TODO`, `TBD`, `manual review`, or `needs confirmation` as a final gap.

On a blocker, preserve failed/stale evidence, name the accountable owner and exact missing input, then resume this skill or the earliest reopened producer. Never manufacture completion by editing derived state.

## Handoff

- Keep output structured with headings and bullets.
- Make findings, gaps, risks, and blockers explicit.
- Tie recommendations to evidence from the provided artifact, `specs-refiniment/<feature-name>/<file.md>` workspace, stakeholder context, or user-provided source material.
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

Valid executable scenario:

```text
Scenario matrix:
| ID | Requirement ref | Scenario | Setup | Trigger | Verifiable outcome | Layer | Automation |
| --- | --- | --- | --- | --- | --- | --- | --- |
| TC-003 | AC-003 | Reject unsupported provider asset | BitGo wallet fixture contains BTC only | Submit a USDC transfer request | `GOCACHE=/tmp/ai-sdlc-go-cache go test ./internal/service -run TestRejectUnsupportedProviderAsset -count=1` exits 0 and asserts no transfer row is created | service | `skills/ai-sdlc-validation/scripts/validation_plan.py internal/service/transfer_service.go`; implement `TestRejectUnsupportedProviderAsset` |

Execution order:
1. Service tests: run after scenario matrix is approved; blocks transport tests; failure action: fix service validation and rerun focused service test.

Decisions required:
- Question: Should unsupported provider assets return 400 validation error or 409 conflict?
  Options:
  A. 400 validation error
  B. 409 conflict
  C. Provider-specific 502
  Recommended default: A, because the request is invalid before provider submission.
  Owner: Delivery Manager
  Blocking: yes
```

Invalid counter-example:

```text
| TC-003 |  | Test bad inputs | Existing tests | Run tests | Service rejects bad data | service | Manual review |
```

Reject this because it has no spec ref, the outcome is prose-only, and `Manual review` has no blocker or automation date.

## Source contract

This page is generated from [`skills/ai-sdlc-test-cases/SKILL.md`](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/skills/ai-sdlc-test-cases/SKILL.md). Edit the source contract, rerun the catalog generator, and review both changes together; never hand-edit this page.

[Back to the skill catalog](../skills.md) · [Script reference](../scripts.md) · [Choose a workflow](../../flows/index.md)
