---
name: ai-sdlc-branching
description: AI SDLC Git-flow branching workflow. Use when an AI assistant starts implementation work, needs to create or verify a task branch, checks branch/spec alignment, or prepares to hand off a completed user-visible task to validation and commit prep. Supports `--quick-flow` for fast assumption-driven execution and `--full-flow` for question-driven verified execution.
---

# ai-sdlc-branching: Branching

> Internal AI SDLC skill, not client-facing by default.
> Every rule below is important to follow. None of it can be skipped.
> Before producing the final artifact, confirm required inputs, target audience, missing facts, output format, and constraints when they are unclear.
> Do not invent missing information. Ask concise clarification questions when required inputs are absent.

## 0. Skill Card

- Skill name: `ai-sdlc-branching`
- Primary audience: Dev
- Supporting audience: PM, BA
- Audience tags: Dev, PM, BA
- SDLC stage: Git workflow setup
- Purpose: Create or verify the correct Git-flow task branch before repo-tracked file mutation, keep branch names aligned with active specs, and hand completed work to validation and commit prep without mixing unrelated changes.
- Output: Branching decision, branch name, base branch, dirty-tree assessment, and next handoff

### 0.1 Required Inputs

- User-visible task name and change type.
- Current branch and dirty tree state.
- Active spec folder for medium or large work.

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

- Use `scripts/branch_plan.py` when deterministic scaffolding, planning, or formatting is useful for this workflow; pass the same `--quick-flow` or `--full-flow` flag that was supplied to the skill.
- No external reference files are required for this skill.

## Script Usage

- Run `scripts/branch_plan.py` before drafting or updating this skill's artifact when inputs are longer than a few bullets, when traceability matters, or when a flow flag is supplied. For agent analysis, pass `--format toon`, read `anchors` first, and open only `next_reads`; without that flag the script keeps its human-readable Markdown output.
- Quick flow analysis: `python3 skills/ai-sdlc-branching/scripts/branch_plan.py --feature <feature-name> --quick-flow <input.md>...`
- Full flow analysis: `python3 skills/ai-sdlc-branching/scripts/branch_plan.py --feature <feature-name> --full-flow <input.md>...`
- To write content, pass one canonical heading with `--section "<section>"`; provide only that section body on stdin, without H1, H2, frontmatter, or a temporary content file.
- Repeat `--section` for each required section, then run the same script with `--finalize` to validate the artifact and refresh metadata and specs indexes.
- The AI must not write or directly edit the routed Markdown artifact; the script owns scaffold creation, section placement, and durable file writes.
- Use `--decision-row` with one nine-cell Markdown table row on stdin when a decision-log entry is required.
- Legacy `--emit-template`, `--emit-decision-log-entry`, and `--write` remain available for compatibility.
- Use `--quick-flow` for first-pass synthesis with assumptions; use `--full-flow` before readiness, handoff, signoff, or any decision-sensitive output.

## Purpose

Create or verify the correct Git-flow task branch before repo-tracked file
mutation, keep branch names aligned with active specs, and hand completed work
to validation and commit prep without mixing unrelated changes.

## Inputs

- Collect the user-visible task name and change classification.
- Collect the active spec folder for medium or large work.
- Collect the current branch and dirty tree from:

  ```bash
  git status --short --branch
  ```

- Collect the repository's declared base branch before creating any new task branch.
- Collect whether the intended change is feature, fix, docs-only, or
  repo-local maintenance/governance.
- Collect sandbox or approval constraints from `$ai-sdlc-approvals-sandbox` if
  Git branch commands fail because Git refs cannot be written.

## Steps

1. Run `git status --short --branch` before mutating repo-tracked files.
2. Allow read-only planning, repository inspection, and SDD drafting before a
   task branch exists when those actions do not mutate repo-tracked files.
3. Classify dirty files as related, unrelated, or unclear.
4. Stop before branch creation or branch switching when unrelated or unclear
   dirty files would be carried into the task without explicit user approval.
5. Choose the branch name:
   - Medium or large SDD work: `feature/NNN-short-feature-name`.
   - Small bug fix: `fix/<short-name>`.
   - Docs-only work: `docs/<short-name>`.
   - Repo-local governance or maintenance: `chore/<short-name>`.
6. For medium or large work, preserve the full active spec slug after the
   prefix, for example `feature/191-branching-workflow`.
7. Resolve the base branch in this order: explicit repository policy
   (`ai-sdlc.baseBranch`), `origin/HEAD`, then an existing local `dev`, `main`,
   or `master`. Use `dev` only when it is declared or actually present.
8. If already on a correctly named task branch for the current task, continue
   and report `already correct`; do not recreate the branch.
9. Before creating a new task branch, switch to the resolved base and pull the
   latest remote state with fast-forward-only semantics:

   ```bash
   git checkout <base-branch>
   git pull --ff-only origin <base-branch>
   ```

10. If the resolved base cannot be checked out or pulled cleanly, stop and report the
    blocker instead of branching from stale or divergent local state.
11. Create the new branch from the refreshed resolved base with a non-interactive
    command, for example:

   ```bash
   git checkout -b feature/191-branching-workflow
   ```

12. If checkout, pull, or branch creation fails because sandboxing blocks Git
    refs or network access, use `$ai-sdlc-approvals-sandbox` and request narrow
    approval for the specific Git command.
13. Perform implementation only after the branch is verified or created from
    refreshed `dev`.
14. When the user-visible task is complete, run `$ai-sdlc-validation`, then
    `$ai-sdlc-commit-prep`.
15. Use one branch and one commit per user-visible task by default. Do not treat
    individual `tasks.md` checkboxes as automatic branch or commit boundaries.

## Output Spec

Use this branch handoff report when branch state matters:

```text
Branching:
- Task: user-visible task name
- Change size: small | medium | large
- Spec: specs/NNN-short-feature-name | none
- Base branch: resolved branch | blocked with reason
- Base refresh: pulled latest resolved base | reused existing task branch | blocked
- Current branch: branch-name
- Expected branch: branch-name
- Action: already correct | created | reused with reason | blocked
- Dirty tree: clean | related files listed | unrelated/unclear blocker
- Next phase: implementation | validation | commit-prep
```

Quality gate:

- Pass when implementation starts on a branch that matches the task type and,
  for medium or large work, includes the active spec slug.
- Fail when repo-tracked files are mutated on a shared/default branch, unrelated
  dirty files are carried silently, branch/spec mismatch is hidden, or Git
  command failures are ignored.

## Examples

Valid medium-work start:

```text
Branching:
- Task: AI SDLC Git-flow branching skill and workflow update
- Change size: medium
- Spec: specs/191-branching-workflow
- Base branch: main (origin/HEAD)
- Base refresh: pulled latest resolved base
- Current branch: main
- Expected branch: feature/191-branching-workflow
- Action: created
- Dirty tree: clean
- Next phase: implementation
```

Valid small fix:

```text
Branching:
- Task: fix typo in validation warning
- Change size: small
- Spec: none
- Base branch: main (repository default)
- Base refresh: pulled latest resolved base
- Current branch: main
- Expected branch: fix/validation-warning-typo
- Action: created
- Dirty tree: clean
- Next phase: implementation
```

Invalid counter-example:

```text
Edited files directly on the shared base and will make a branch later.
```

Reject this because branch verification must happen before repo-tracked file
mutation for implementation work.

## Edge Cases

- If the repository has no declared/present base branch, stop and ask the owner
  to declare one; do not invent `dev`.
- If already on a correctly named task branch, continue and report `already
  correct`.
- If already on a non-default branch that clearly belongs to the same task,
  report `reused with reason`; do not create a second branch.
- For new task branches, do not skip checkout/pull of the resolved base merely
  because it looks recent.
- If `git pull --ff-only` reports divergence, stop and ask for repository
  maintenance instead of merge-committing during task setup.
- If the branch name matches multiple specs or no spec for medium or large work,
  resolve the active spec with `$ai-sdlc-sdd` before implementation.
- If unrelated dirty files exist, do not run destructive cleanup. Ask the user
  whether to keep, commit, stash, or otherwise handle them.
- If branch creation fails from sandboxing, request escalation rather than
  inventing an alternate branch state.
- Do not push branches unless the user explicitly asks or the commit workflow
  requires it.

## Scope Boundary

- Do not create or update SDD artifacts; use `$ai-sdlc-sdd`.
- Do not decide validation commands; use `$ai-sdlc-validation`.
- Do not stage files or create commits; use `$ai-sdlc-commit-prep`.
- Do not draft commit messages; use `$ai-sdlc-conventional-commit`.
