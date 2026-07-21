---
name: ai-sdlc-commit-prep
description: AI SDLC commit preparation workflow. Use when an AI assistant is asked to commit repository changes, prepare an auditable commit message, stage files safely, include SDD traceability, verify branch/spec alignment, or verify the working tree before committing. Supports `--quick-flow` for fast assumption-driven execution and `--full-flow` for question-driven verified execution.
---

# ai-sdlc-commit-prep: Commit Preparation

> Internal AI SDLC skill, not client-facing by default.
> Every rule below is important to follow. None of it can be skipped.
> Before producing the final artifact, confirm required inputs, target audience, missing facts, output format, and constraints when they are unclear.
> Do not invent missing information. Ask concise clarification questions when required inputs are absent.

## 0. Skill Card

- Skill name: `ai-sdlc-commit-prep`
- Primary audience: Dev
- Supporting audience: QA, BA, PM
- Audience tags: Dev, QA, BA, PM
- SDLC stage: Commit readiness / traceability
- Purpose: Prepare and create a safe AI SDLC commit by reviewing the branch and working tree, staging only related files, validating SDD evidence, using a valid Conventional Commit message, and reporting post-commit traceability.
- Output: Safe staged set, validated commit readiness, conventional commit message, and post-commit traceability

### 0.1 Required Inputs

- Explicit commit request or completed workflow state.
- Current branch, dirty tree, staged files, and diff.
- Validation results plus spec traceability when applicable.

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

- Use `scripts/check_commit_ready.py` when deterministic validation, planning, or formatting is required by the workflow; pass the same `--quick-flow` or `--full-flow` flag that was supplied to the skill when supported.

## Script Usage

- Run commit readiness before staging final commit content or writing the final commit summary.
- Quick flow: `python3 skills/ai-sdlc-commit-prep/scripts/check_commit_ready.py --quick-flow --spec specs/<feature-name> --allow-unstaged --no-require-staged`
- Full flow: `python3 skills/ai-sdlc-commit-prep/scripts/check_commit_ready.py --full-flow --spec specs/<feature-name>`
- For an explicitly task-scoped commit in a larger active SDD plan, add
  `--task TNNN`. The selected task must be present and complete; later pending
  tasks remain allowed. Without `--task`, every spec task must be complete.
- Every medium or large traced SDD commit message must include the completed
  task identity as `Task: TNNN` (or a comma-separated list). `--task` narrows
  the readiness check; it does not replace the commit-message trailer.
- Use `--allow-unstaged` only when intentionally checking readiness before final staging.
- Use `--no-require-staged` only for preflight checks; omit it immediately before commit creation.

## Purpose

Prepare and create a safe AI SDLC commit by reviewing the branch and working tree, staging only related files, validating SDD evidence, using a valid Conventional Commit message, and reporting post-commit traceability.

## Inputs

- Collect the user’s explicit commit request or workflow state showing commit prep is justified.
- Collect the active spec folder for medium or large work.
- Collect validation commands and outcomes that are current for the active diff.
- Collect the current branch and dirty tree from `git status --short --branch`.

## Steps

1. Run `git status --short --branch`.
2. Run `git diff --stat` and `git diff --cached --stat` when staged changes already exist.
3. Inspect relevant diffs for scope, accidental edits, generated files, secrets, and unrelated user changes.
4. Confirm medium or large work has current `requirements.md`, `design.md`, `test-cases.md`, `qa.md`, `tasks.md`, `_ai_sdlc/plan.toon`, and `plan.md`.
5. For medium or large work, confirm the current branch includes the active spec slug after a typed Git-flow prefix, for example `feature/NNN-short-feature-name`; otherwise report the branch/spec mismatch before committing.
6. Confirm completed tasks in `tasks.md` match the diff.
7. Run or confirm current validation before staging.
8. Ensure the active spec passes structural validation plus clarify,
   checklist, and analyze before final commit.
9. Run the readiness checker before final commit:

   ```bash
   python3 skills/ai-sdlc-commit-prep/scripts/check_commit_ready.py --spec specs/NNN-feature-name --no-require-staged
   ```

   When the user explicitly requested one commit per SDD task, add
   `--task TNNN` and verify that the staged diff belongs only to that task.

10. Stage only files belonging to the current change.
11. Leave unrelated dirty files unstaged and report them.
12. Use `$ai-sdlc-conventional-commit` to draft and validate the message.
    Include `Spec:`, `Task:`, and exact `Validation:` evidence for medium or
    large SDD work.
13. Commit with a non-interactive command, for example `git commit -F /tmp/message.txt`.
14. Run `git status --short --branch` after committing.

## Output Spec

Return this final report:

```text
Commit:
- Hash: full_hash
- Subject: conventional subject
- Branch: branch-name
- Spec: specs/NNN-feature-name | none
- Task: TNNN[, TNNN] | none

Staging:
- Included: path groups and why they belong.
- Excluded: unrelated dirty paths or none.

Validation:
- command -> outcome

Post-commit:
- Working tree: clean | dirty with listed paths.
- Residual risk: none | concrete issue.
```

Quality gate:

- Pass when the branch/spec relationship is explicit, the commit contains only related files, validation is current, message validation passes, and post-commit status is reported.
- Fail when branch/spec mismatch is hidden, unrelated files are staged, validation is stale, the message validator fails, or the final report hides a dirty tree.

## Examples

Valid staging rationale:

```text
Staging:
- Included: `skills/*/SKILL.md` because every file is part of the skill instruction upgrade.
- Included: `specs/177-skill-instruction-upgrade/*` because the SDD package documents this change.
- Excluded: `apps/web/.env.local` because it is unrelated and sensitive.
```

Invalid counter-example:

```text
Ran git add -A and committed everything.
```

Reject this when the working tree contains files not inspected for scope.

## Edge Cases

- Stop and ask before staging when unrelated changes are mixed inside a file required for the current change.
- Stop and resolve branch state with `$ai-sdlc-branching` when medium or large work is still on `dev`, `main`, `master`, or a branch that does not include the active spec slug.
- Use `--allow-unstaged` on the readiness checker only when unrelated unstaged files are intentionally left out and reported.
- Do not amend an existing commit unless the user explicitly requests amend.
- Do not run destructive cleanup commands unless the user requested or approved them.
- Report failed commit hooks with the hook output and do not claim a commit exists.

## Scope Boundary

- Do not draft commit message content without `$ai-sdlc-conventional-commit`.
- Do not decide test coverage; use `$ai-sdlc-test-cases`, `$ai-sdlc-qa`, and `$ai-sdlc-validation`.
- Do not revert user changes to make staging easier.
