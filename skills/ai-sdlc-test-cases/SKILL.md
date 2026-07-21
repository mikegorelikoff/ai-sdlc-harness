---
name: ai-sdlc-test-cases
description: AI SDLC test-case-driven testing workflow. Use when an AI assistant is asked to derive test cases, create a test plan, expand coverage, or write tests from explicit scenarios before implementing unit, service, transport, or integration tests. Supports `--quick-flow` for fast assumption-driven execution and `--full-flow` for question-driven verified execution. Explicit full or end-to-end spec refinement requests continue through the existing 18-stage refinement cascade.
---

# ai-sdlc-test-cases: Test Cases For Implementation

> Internal AI SDLC skill, not client-facing by default.
> Every rule below is important to follow. None of it can be skipped.
> Before producing the final artifact, confirm required inputs, target audience, missing facts, output format, and constraints when they are unclear.
> Do not invent missing information. Ask concise clarification questions when required inputs are absent.

## 0. Skill Card

- Skill name: `ai-sdlc-test-cases`
- Primary audience: QA
- Supporting audience: Dev, BA
- Audience tags: QA, Dev, BA
- SDLC stage: Implementation test design
- Purpose: Derive executable AI SDLC test scenarios from requirements or delivery context and place QA refinement artifacts under `specs-refiniment/<feature-name>/<file.md>` when writing files.
- Output: Scenario matrix with requirement refs, verifiable outcomes, automation paths, and execution order

### 0.1 Required Inputs

- Requirements, design, and behavior under test.
- Affected package, endpoint, provider, workflow, or contract.
- Known fixtures, mocks, and unavailable dependencies.

### 0.2 Clarification Rules

- Ask concise questions before finalizing when role, artifact, requirements, scope, audience, or constraints are unclear.
- If optional information is missing, mark it as `TBD`, `Not provided`, or `Assumption` instead of inventing it.
- Separate confirmed facts from assumptions and open questions.
- Do not proceed to downstream synthesis when a required upstream artifact or decision is missing.

### 0.2.1 Flow Mode Flags

- Support two explicit execution flags: `--quick-flow` and `--full-flow`.
- If both flags are supplied, `--full-flow` takes precedence because it is the stricter mode.
- `--quick-flow`: move fast, make high-quality progress with available context, avoid clarification questions unless continuing would create material product, security, compliance, data-loss, or irreversible implementation risk.
- In `--quick-flow`, use documented assumptions, recommended defaults, existing repository patterns, and the nearest available artifact evidence; record important assumptions and decisions in `decision-log.md`.
- In `--quick-flow`, run only focused checks that are directly relevant, cheap, and likely to catch regressions for the requested work; report any skipped broader checks as residual risk.
- `--full-flow`: ask concise clarification questions when inputs, scope, ownership, acceptance criteria, or decisions are unclear; do not silently assume material requirements.
- In `--full-flow`, verify upstream and downstream artifacts, decision-log entries, traceability links, acceptance criteria, and validation evidence before finalizing.
- In `--full-flow`, run or recommend the skill-appropriate gates, reviews, scripts, and validation commands needed for end-to-end confidence; document any blocked verification explicitly.
- When neither flag is supplied, follow the skill default rules and choose the least risky behavior for the request size and domain.

### 0.3 Output Rules

- Keep output structured with headings and bullets.
- Make findings, gaps, risks, and blockers explicit.
- Tie recommendations to evidence from the provided artifact, `specs-refiniment/<feature-name>/<file.md>` workspace, stakeholder context, or user-provided source material.
- Include role ownership when the output creates follow-up work for BA, QA, Dev, PM, or Delivery.
- Return progress, completion, validation, and handoff summaries directly in the active agent response.
- Before the final response, emit the `ai-sdlc-handoff/v1` contract with `result`, `blockers`, `next_required`, and `next_optional`; every action includes `reason`, `command`, and `expected_artifact`.
- Do not create `summary.txt`, `*-summary.txt`, or another standalone summary file unless the user explicitly requests one.
- Keep durable writes limited to the canonical lifecycle artifacts, decision log, human-readable index, and `_ai_sdlc` machine files.
- Let shared helpers migrate legacy paths on the next write; never overwrite or manually merge divergent legacy and canonical files.

### 0.4 Artifact Routing

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

## 0.4.1 Runtime Path Resolution

- Treat `skills/` in commands as a logical skill root. In a harness source checkout, use `skills/`; in a project-scoped consumer installation, resolve it to `.agents/skills/`. Before running a helper, verify that the selected root contains both this skill and `ai-sdlc-shared-runtime`; block with the missing path if neither layout exists.

## 0.5 Feature State Machine

- Maintain feature lifecycle state in TOON at `specs-refiniment/<feature-name>/_ai_sdlc/state.toon` for refinement work and `specs/<feature-name>/_ai_sdlc/state.toon` for implementation work.
- Before executing this skill for a feature, check the state machine with `python3 skills/ai-sdlc-shared-runtime/scripts/state_machine.py check --feature <feature-name> --skill <this-skill-name> --workspace <refinement|implementation> --quick-flow|--full-flow`.
- When this skill starts durable work, mark it in progress with `begin`; when the skill's required artifact or review is complete, mark it done with `complete` and include `--artifacts <path>` plus `--decision-ref DEC-###` when a decision was involved.
- In `--full-flow`, do not proceed when predecessor stages are incomplete, another lifecycle skill is active, or the state file reports a blocker.
- In `--quick-flow`, a predecessor skip is allowed only when continuing is low risk and the command includes `--assumption "..."` or `--decision-ref DEC-###`; record the same assumption or decision in `decision-log.md`.
- Use `python3 skills/ai-sdlc-shared-runtime/scripts/state_machine.py status --feature <feature-name> --workspace <refinement|implementation> --format toon` to emit compact LLM-readable state before choosing the next skill.
- The state machine is feature-scoped: do not reuse a `state.toon` across unrelated feature folders.

## 0.6 Artifact Metadata And Metatags

- Every Markdown artifact generated or updated by this skill must start with an `artifact_metadata` YAML frontmatter block before the first visible heading.
- Use schema `ai-sdlc-artifact-metadata/v1` and keep these fields current: `feature`, `artifact`, `path`, `workspace`, `skill`, `flow_mode`, `state_file`, `decision_log`, `status`, `owner`, `created_at`, `updated_at`, `trace_ids`, `related_artifacts`, `validation`, and `metatags`.
- `metatags` must include at minimum `ai-sdlc`, the workspace (`refinement` or `implementation`), this skill name, the artifact type or filename stem, and a lifecycle/status tag such as `draft`, `review`, `approved`, or `validated`.
- When `--quick-flow` is active, set `flow_mode: quick`, keep assumptions visible in the body, and add tags for major defaults or unresolved risk only when they help retrieval.
- When `--full-flow` is active, set `flow_mode: full`, keep blockers and validation evidence reflected in `status`, `validation`, `trace_ids`, and `related_artifacts`.
- Update metadata whenever the artifact path, status, owner, trace links, validation evidence, related artifacts, or decision references change.
- Metadata is an index for routing, retrieval, and traceability; it does not replace the artifact body, `decision-log.md`, or `state.toon`.

## 0.7 Specs Index

- Before searching across feature folders, inspect the compact LLM index first: `specs-refiniment/_ai_sdlc/specs-index.toon` for refinement work or `specs/_ai_sdlc/specs-index.toon` for implementation work.
- Use the human-readable index at `specs-refiniment/specs-index.md` or `specs/specs-index.md` when reporting feature coverage, artifact inventory, or handoff status to people.
- After this skill creates or materially updates an artifact, refresh the matching workspace index with `python3 skills/ai-sdlc-shared-runtime/scripts/ai_sdlc_specs_index.py --workspace <refinement|implementation> --quick-flow|--full-flow`.
- In `--quick-flow`, rely on `specs-index.toon` to choose the smallest relevant artifact set before opening files.
- In `--full-flow`, verify the updated artifact appears in both `specs-index.toon` and `specs-index.md` before final handoff.
- The specs index summarizes artifact metadata and state; it does not replace reading the selected source artifacts when details, approvals, or validation evidence matter.

## 0.8 Complete Refinement Cascade

- Trigger the complete cascade only when the user explicitly asks for a full, complete, or end-to-end spec refinement or asks for every refinement artifact. A normal `--full-flow` call for one skill remains single-stage.
- Before the first durable write, run `python3 skills/ai-sdlc-shared-runtime/scripts/refinement_status.py --feature <feature-name> --gate full --format toon` and start with the earliest reported `next_skill`, including stages earlier than this skill.
- Execute the existing refinement skills in lifecycle order with `--full-flow`: discovery, PRFAQ, delivery-package gap review, requirements readiness, goal/capability mapping, backlog gap review, backlog decomposition, story decomposition, release slicing, BA context, delivery spec, QA plan, QA gap review, test strategy, test cases, test suite, QA readiness, and delivery handoff.
- Produce all 18 canonical Markdown artifacts. `release-slicing.md` is mandatory for a complete cascade; when release slicing is not applicable, write an explicit evidence-backed N/A artifact and complete the stage instead of skipping it.
- After every stage, finalize its artifact, record required decisions, mark the stage `done`, and refresh the refinement indexes before selecting the next skill.
- Do not declare the cascade complete until `python3 skills/ai-sdlc-shared-runtime/scripts/refinement_status.py --feature <feature-name> --gate full --format markdown` exits successfully with `18/18`. If it fails, continue with the reported next skill or return the concrete blocker and remaining inventory in the active agent response.
- Surface checkpoint and final summaries in Codex only; never persist a cascade summary as a text file.

## References

- Use `scripts/case_matrix.py` when deterministic scaffolding, planning, or formatting is useful for this workflow; pass the same `--quick-flow` or `--full-flow` flag that was supplied to the skill.
- Read `references/test-case-template.md` when the task needs the detailed structure, checklist, or examples for this skill.

## Script Usage

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

## Purpose

Derive executable AI SDLC test scenarios from requirements or delivery context. Link each scenario to a requirement, story, workflow, risk, or acceptance criterion and define verifiable outcomes, automation commands, execution order, and human decisions without leaving open TODOs.

## Inputs

- Read the provided requirements, delivery spec, stories, workflows, risks, and existing test cases.
- Read existing QA notes from `specs-refiniment/<feature-name>/<file.md>` when acceptance or manual validation already exists.
- Collect the changed behavior, contract, bug, regression risk, endpoint, provider, asset, or workflow under test.
- Collect existing test files for the affected package when implementing tests.
- Read `references/test-case-template.md` when the scenario matrix needs reusable wording.
- Collect known fixtures, mocks, seeded data, and unavailable dependencies.

## Steps

1. Write `In scope` and `Out of scope` before generating scenarios.
2. Check every proposed test case against `Out of scope`; delete any test case that tests excluded behavior.
3. Define the behavior under test in one sentence.
4. Identify the requirement, story, workflow, risk, or acceptance criterion each scenario proves.
5. Create scenario IDs using `TC-001`, `TC-002`, and continuing sequence.
6. Include happy path, boundary values, null or missing inputs, negative validation, authorization, state-transition, retry, idempotency, concurrency, and provider-failure cases when relevant.
7. Map each scenario to exactly one primary layer: unit, service, transport, integration, QA/manual, or not automated.
8. Write a verifiable outcome for every scenario using one of these forms:
   - shell command whose exit code proves the outcome
   - numbered checklist of observable facts a human can tick without interpretation
   - before/after diff or data pair that proves the behavior changed correctly
9. Write an automation path for every scenario using one of these forms:
   - script path plus exact invocation
   - CI step name
   - `Manual — automate by YYYY-MM-DD — blocker: concrete blocker`
10. Replace open TODOs with `Decisions required`; each decision must include Question, Options A/B/C, Recommended default, Owner, and Blocking yes/no.
11. Replace decorative layer descriptions with `Execution order`; each layer must include run condition, what it blocks, and failure action.
12. Write or update the scenario matrix under `specs-refiniment/<feature-name>/<file.md>` when file output is requested.
13. Implement tests only after the scenario matrix contains requirement refs, verifiable outcomes, automation paths, execution order, and structured decisions.
14. Name tests so a reviewer can trace each test back to a scenario ID or spec reference.

## Output Spec

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

## Examples

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

## Edge Cases

- Mark expected behavior as a structured decision when the spec is silent and code behavior is inconsistent.
- Prefer lower-layer tests when they prove the behavior without full integration setup.
- Use integration tests only when provider adapters, HTTP contracts, migrations, or cross-package behavior must be exercised together.
- Mark flaky or external-service-dependent scenarios as manual only with `Manual — automate by YYYY-MM-DD — blocker: reason`.
- Do not invent provider responses; use documented fixtures, existing mocks, or a structured decision with a recommended default.
- Do not output `TODO`, `TBD`, `manual review`, or `needs confirmation` as a final gap.

## Scope Boundary

- Do not claim QA signoff; use `$ai-sdlc-qa`.
- Do not choose final validation command execution; use `$ai-sdlc-validation`.
- Do not implement production behavior from this skill alone; use `$ai-sdlc-sdd` and approved `tasks.md`.
- Do not add broad snapshot tests when focused assertions can prove the behavior.
