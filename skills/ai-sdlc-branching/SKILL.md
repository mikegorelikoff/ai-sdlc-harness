---
name: ai-sdlc-branching
description: AI SDLC Git-flow branching workflow. Use when Codex starts implementation work, needs to create or verify a task branch, checks branch/spec alignment, or prepares to hand off a completed user-visible task to validation and commit prep.
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

### 0.3 Output Rules

- Keep output structured with headings and bullets.
- Make findings, gaps, risks, and blockers explicit.
- Tie recommendations to evidence from the provided artifact, repository, `specs-refiniment/<feature-name>/<file.md>` workspace, or user context.
- Include role ownership when the output creates follow-up work for BA, QA, Dev, PM, or Delivery.

### 0.4 Artifact Routing

- Use `specs/` only for developer implementation SDD packages and repo-governance artifacts.
- Do not place PM, BA, QA, Delivery, discovery, planning, refinement, or readiness outputs in `specs/`; those belong at `specs-refiniment/<feature-name>/<file.md>`.
- When consuming `specs-refiniment/<feature-name>/<file.md>`, treat it as upstream refinement context and create or update `specs/` only when implementation work is explicitly in scope.

## References

- No external reference files are required for this skill.

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

- Collect the current `dev` branch state before creating any new task branch.
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
   prefix, for example `feature/191-codex-branching-workflow`.
7. Use `dev` as the default base branch for every new task branch.
8. If already on a correctly named task branch for the current task, continue
   and report `already correct`; do not recreate the branch.
9. Before creating a new task branch, switch to `dev` and pull the latest
   remote state with fast-forward-only semantics:

   ```bash
   git checkout dev
   git pull --ff-only
   ```

10. If `dev` cannot be checked out or pulled cleanly, stop and report the
    blocker instead of branching from stale or divergent local state.
11. Create the new branch from the refreshed `dev` branch with a non-interactive
    command, for example:

   ```bash
   git checkout -b feature/191-codex-branching-workflow
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
- Base branch: dev | other with reason
- Base refresh: pulled latest dev | reused existing task branch | blocked
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
- Task: Codex Git-flow branching skill and workflow update
- Change size: medium
- Spec: specs/191-codex-branching-workflow
- Base branch: dev
- Base refresh: pulled latest dev
- Current branch: dev
- Expected branch: feature/191-codex-branching-workflow
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
- Base branch: dev
- Base refresh: pulled latest dev
- Current branch: dev
- Expected branch: fix/validation-warning-typo
- Action: created
- Dirty tree: clean
- Next phase: implementation
```

Invalid counter-example:

```text
Edited files directly on dev and will make a branch later.
```

Reject this because branch verification must happen before repo-tracked file
mutation for implementation work.

## Edge Cases

- If already on a correctly named task branch, continue and report `already
  correct`.
- If already on a non-default branch that clearly belongs to the same task,
  report `reused with reason`; do not create a second branch.
- For new task branches, do not skip `git checkout dev` and `git pull --ff-only`
  merely because local `dev` looks recent.
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
