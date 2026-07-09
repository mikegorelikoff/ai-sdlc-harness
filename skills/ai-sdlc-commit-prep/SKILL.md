---
name: ai-sdlc-commit-prep
description: AI SDLC commit preparation workflow. Use when Codex is asked to commit repository changes, prepare an auditable commit message, stage files safely, include SDD traceability, verify branch/spec alignment, or verify the working tree before committing.
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

- Use `scripts/check_commit_ready.py` when deterministic validation, planning, or formatting is required by the workflow.
- Use `scripts/test_check_commit_ready.py` only for validating helper behavior; do not load it for ordinary task execution.

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
4. Confirm medium or large work has current `requirements.md`, `design.md`, `test-cases.md`, `qa.md`, and `tasks.md`.
5. For medium or large work, confirm the current branch includes the active spec slug after a typed Git-flow prefix, for example `feature/NNN-short-feature-name`; otherwise report the branch/spec mismatch before committing.
6. Confirm completed tasks in `tasks.md` match the diff.
7. Run or confirm current validation before staging.
8. Ensure the active spec passes structural validation plus clarify,
   checklist, and analyze before final commit.
9. Run the readiness checker before final commit:

   ```bash
   python3 .codex/skills/ai-sdlc-commit-prep/scripts/check_commit_ready.py --spec specs/NNN-feature-name --no-require-staged
   ```

10. Stage only files belonging to the current change.
11. Leave unrelated dirty files unstaged and report them.
12. Use `$ai-sdlc-conventional-commit` to draft and validate the message.
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
- Included: `.codex/skills/*/SKILL.md` because every file is part of the skill instruction upgrade.
- Included: `specs/177-codex-skill-instruction-upgrade/*` because the SDD package documents this change.
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
