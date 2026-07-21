---
name: ai-sdlc-validation
description: AI SDLC backend validation workflow. Use when an AI assistant needs to validate Go, SQL, API, provider integration, SDD, or documentation changes in this repository and choose focused deterministic checks without running unrelated expensive tests by default. Supports `--quick-flow` for fast assumption-driven execution and `--full-flow` for question-driven verified execution.
---

# ai-sdlc-validation: Validation Command Selection

> Internal AI SDLC skill, not client-facing by default.
> Every rule below is important to follow. None of it can be skipped.
> Before producing the final artifact, confirm required inputs, target audience, missing facts, output format, and constraints when they are unclear.
> Do not invent missing information. Ask concise clarification questions when required inputs are absent.

## 0. Skill Card

- Skill name: `ai-sdlc-validation`
- Primary audience: Dev
- Supporting audience: QA, BA
- Audience tags: Dev, QA, BA
- SDLC stage: Implementation validation
- Purpose: Select, run, and report focused deterministic validation checks for AI SDLC code, SQL, API, provider, SDD, documentation, and tool-governance changes.
- Output: Focused validation commands, outcomes, coverage notes, and residual risk

### 0.1 Required Inputs

- Changed files, diff, or explicit validation target.
- Active spec and QA context when user-visible or release-sensitive.
- Sandbox constraints and previous validation output if relevant.

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
- Tie recommendations to evidence from the provided artifact, repository, `specs-refiniment/<feature-name>/<file.md>` workspace, or user context.
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

- Use `specs/` only for developer implementation SDD packages and repo-governance artifacts.
- Do not place PM, BA, QA, Delivery, discovery, planning, refinement, or readiness outputs in `specs/`; those belong at `specs-refiniment/<feature-name>/<file.md>`.
- When consuming `specs-refiniment/<feature-name>/<file.md>`, treat it as upstream refinement context and create or update `specs/` only when implementation work is explicitly in scope.

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

## References

- Use `scripts/run_validation.py` to execute a human-reviewed JSON argv plan
  without a shell and write `_ai_sdlc/validation-receipt.json` containing actual
  exit codes, revision/diff identity, environment, duration, and output digests.
  The runner rejects executable paths, Python `-c`, mutating Git, and unbounded
  downloader/build command families, but repository test/scripts still execute
  code and require the normal sandbox. Use `--verify` before full-flow commit
  readiness. The local self-hash is forgeable by a workspace writer and proves
  neither authenticated execution nor human approval; protected CI is the
  independent source when that assurance is required. A receipt also does not
  prove that the tests express the right requirement.
  Store the reviewed plan as `_ai_sdlc/validation-plan.json` beside the receipt;
  the receipt binds its path and digest. The runner requires a valid Git `HEAD`,
  streams bounded output (10 MB total by default), and terminates a noisy or
  timed-out process group rather than retaining unbounded output in memory.
- `run_validation.py --complete-state` is intentionally rejected. Write
  finalized `validation.md`, execute the final plan, rerun it with `--verify`,
  then complete the validation stage with `state_machine.py complete`; completion revalidates
  the current receipt and rejects failed, malformed, forged, or stale evidence.
  Canonical `state.toon`, specs indexes, and downstream review/commit artifacts
  are derived evidence excluded from the workspace fingerprint; changing
  validated source, specs, tests, `validation.md`, or the plan still makes the
  receipt stale.

- Use `scripts/validation_plan.py` when deterministic validation, planning, or formatting is required by the workflow; pass the same `--quick-flow` or `--full-flow` flag that was supplied to the skill when supported.

## Script Usage

- Run validation planning after identifying changed files and before choosing commands manually.
- Quick flow: `python3 skills/ai-sdlc-validation/scripts/validation_plan.py --quick-flow <changed-file>...`
- Full flow: `python3 skills/ai-sdlc-validation/scripts/validation_plan.py --full-flow <changed-file>...`
- If no files are supplied, the script inspects the current git worktree.
- Execute the suggested commands that match the requested risk level; document skipped broader commands as residual risk.

## Purpose

Select, run, and report focused deterministic validation checks for AI SDLC code, SQL, API, provider, SDD, documentation, and tool-governance changes.

## Inputs

- Collect changed files from `git status --short`, `git diff --name-only`, or explicit user-provided paths.
- Read the active spec and `qa.md` when the work is medium, large, release-sensitive, or user-visible.
- Collect previous validation output only when it is current for the same diff signature.
- Collect sandbox constraints that affect Go cache, network access, local listeners, or external services.
- Run the validation planner when changed files are not trivial:

  ```bash
  python3 skills/ai-sdlc-validation/scripts/validation_plan.py
  ```

## Steps

1. Classify changed files by surface: Go package, SQL/sqlc, API contract, provider integration, frontend/docs, SDD/spec, tool governance, or mixed.
2. Select the narrowest command set that proves the changed behavior.
3. Prefer focused tests before broad suites when the risk is localized.
4. Use `GOCACHE=/tmp/ai-sdlc-go-cache` for Go tests to avoid sandbox cache write failures.
5. Run spec and skill validators for SDD, skill, helper script, or spec changes.
6. For active feature specs, run structural SDD validation plus clarify,
   checklist, analyze, and workflow-status commands when the spec changed or is
   the main subject of the work.
7. Run `git diff --check` for every change before completion.
8. Rerun with escalation only when a required command fails due to sandbox restrictions and the command is still necessary.
9. Record each command exactly as run and its outcome: passed, failed, skipped, or blocked.
10. Fix failures caused by the current change before reporting success.
11. Report skipped or blocked checks with residual risk.

## Output Spec

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

## Examples

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

## Edge Cases

- Mark a check `blocked` when sandbox, missing dependency, missing credential, or unavailable service prevents execution.
- Request escalation only after a required command fails for a likely sandbox reason; do not escalate to bypass project policy.
- Run broader suites after focused checks when the changed surface spans handlers, services, providers, config, or generated contracts.
- Do not run production integrations unless the user explicitly requests them and required credentials are already available through approved mechanisms.
- Treat stale validation as absent when files changed after the command ran.

## Scope Boundary

- Do not design acceptance scenarios; use `$ai-sdlc-qa`.
- Do not derive scenario matrices; use `$ai-sdlc-test-cases`.
- Do not review code for findings; use `$ai-sdlc-code-review` or `$ai-sdlc-security-testing`.
- Do not mark work done when validation is failed, blocked without disclosure, or unrelated to the changed surface.
