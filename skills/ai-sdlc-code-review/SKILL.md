---
name: ai-sdlc-code-review
description: AI SDLC code review workflow. Use when an AI assistant is asked to review a diff, PR, branch, commit, staged changes, or completed implementation against SDD requirements, tests, API contracts, security, and scope discipline. Supports `--quick-flow` for fast assumption-driven execution and `--full-flow` for question-driven verified execution.
---

# ai-sdlc-code-review: Code Review

> Internal AI SDLC skill, not client-facing by default.
> Every rule below is important to follow. None of it can be skipped.
> Before producing the final artifact, confirm required inputs, target audience, missing facts, output format, and constraints when they are unclear.
> Do not invent missing information. Ask concise clarification questions when required inputs are absent.

## 0. Skill Card

- Skill name: `ai-sdlc-code-review`
- Primary audience: Dev
- Supporting audience: QA, BA, Security
- Audience tags: Dev, QA, BA
- SDLC stage: Code review quality gate
- Purpose: Review AI SDLC code, diffs, branches, commits, or completed implementations for correctness, regressions, contract drift, missing tests, SDD drift, and material maintainability risks.
- Output: Findings-first review with severity, path, impact, fix, validation gaps, and residual risk

### 0.1 Required Inputs

- Review target: diff, commit, branch, PR, staged changes, or subsystem.
- Relevant spec files for medium or large work.
- Validation evidence or explicit note that it is absent.

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

- Read `references/review-checklist.md` when the task needs the detailed structure, checklist, or examples for this skill.
- Use `scripts/review_readiness.py` when deterministic validation, planning, or formatting is required by the workflow; pass the same `--quick-flow` or `--full-flow` flag that was supplied to the skill when supported.

## Script Usage

- Run review readiness before producing findings when reviewing diffs, branches, staged changes, or full-repo surfaces.
- Quick flow: `python3 skills/ai-sdlc-code-review/scripts/review_readiness.py --quick-flow`
- Full flow with spec: `python3 skills/ai-sdlc-code-review/scripts/review_readiness.py --full-flow --spec specs/<feature-name>`
- Branch review: add `--base <branch-or-commit>`; broad audit: use `--full-repo` instead of `--base`.
- Treat errors as blockers; treat warnings as review focus areas unless the user explicitly narrowed scope.

## Purpose

Review AI SDLC code, diffs, branches, commits, or completed implementations for correctness, regressions, contract drift, missing tests, SDD drift, and material maintainability risks.

## Inputs

- Collect the review target: staged diff, unstaged diff, branch, commit, PR, package, or subsystem.
- Run `git status --short` and `git diff --stat` for local diffs.
- Read the relevant diff:
  - staged: `git diff --cached`
  - unstaged: `git diff`
  - branch: `git diff <base>...HEAD`
- Read relevant `requirements.md`, `design.md`, `test-cases.md`, `qa.md`, `tasks.md`, `_ai_sdlc/plan.toon`, and `plan.md` for medium or large work.
- Read validation output or record that it is absent.
- Read `references/review-checklist.md` for deep-audit mode or complex surfaces.

## Steps

1. Identify review mode: normal review or deep-audit review.
2. Define the exact review boundary before judging code.
3. Use the `review` subagent only when the user requested review work and the active runtime policy permits delegation; otherwise perform the review locally.
4. Inspect high-risk files first: handlers, services, workflows, providers, config, schema, migrations, generated contracts, tests, and repo-local automation runtime files.
5. Compare implementation against spec requirements, design contracts, task scope, and validation evidence.
6. Check authorization, data integrity, state transitions, decimal math, asset identifiers, provider routing, errors, observability, and exported Go doc comments when touched.
7. Escalate to `$ai-sdlc-security-testing` when exploitability, auth boundaries, secrets, or abuse paths are the primary concern.
8. Report findings first, ordered by severity.
9. Report no findings explicitly when none are found.
10. Report validation gaps and residual risks after findings.

## Output Spec

Use this format:

```text
Findings:
- [CRITICAL|HIGH|MEDIUM|LOW] path:line - concise issue statement.
  Why it matters: concrete failure, regression, or maintenance risk.
  What should change: specific fix or test.

Open questions:
- Only blockers or assumptions that affect correctness, scope, or severity.

Validation gaps:
- Missing, failed, skipped, or stale checks.

Secondary observations:
- Deep-audit mode only; material non-blocking observations.

Summary:
- Brief change summary after findings.
```

Quality gate:

- Pass when every finding has a path, severity, impact, and fix; no-finding reports still include validation gaps.
- Fail when the review starts with a summary, lists style nits as findings, omits spec comparison for medium/large work, or hides missing validation.

## Examples

Finding example:

```text
Findings:
- [HIGH] internal/service/orders.go:218 - Accepted orders can be repriced after execution because the status guard excludes only cancelled orders.
  Why it matters: A borrower could see a different rate after the lender accepted the order, violating the order contract.
  What should change: Reject repricing unless the order is still in draft or requested state, and add a service test for accepted orders.
```

No-finding example:

```text
Findings:
- None found.

Validation gaps:
- `go test ./internal/service` was not run, so service-level regressions remain unverified.

Summary:
- Reviewed the staged service diff against `specs/NNN-feature-name`; no material defects found.
```

Invalid counter-example:

```text
Looks good. Nice cleanup.
```

Reject this because it is not findings-first and does not mention validation.

## Edge Cases

- State `target unclear` and ask for the review boundary when no diff, commit, branch, or subsystem is available.
- Keep docs-only review lightweight unless docs change SDD policy, API contracts, setup, security, or validation behavior.
- Use deep-audit mode only when the user asks for a broad pass or the surface spans multiple high-risk areas.
- Do not spawn subagents when the active runtime requires explicit permission and the user did not request delegation.
- Report stale validation when files changed after tests ran.
- Treat hook-driven review as advisory-first; warnings do not replace human-readable findings.

## Scope Boundary

- Do not edit code during review unless the user explicitly asks for fixes.
- Do not perform security-focused exploitability review as a side effect; use `$ai-sdlc-security-testing`.
- Do not choose final validation commands except to identify gaps; use `$ai-sdlc-validation`.
- Do not approve scope changes that are missing from `tasks.md`; require a spec update first.

## Hook Policy

- Skip automatic review for docs-only or metadata-only changes with no code, config, hook, spec-runtime, or test behavior impact.
- Require review for non-trivial production code, repo-local automation logic, config, hook, workflow, provider, transport, schema, or test changes.
- Recommend deep audit for high-churn surfaces, multiple risk categories, or changes spanning handlers, services, providers, and config.
- Keep hook enforcement advisory-first; emit warnings before hard blocks.
