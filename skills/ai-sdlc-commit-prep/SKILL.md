---
name: ai-sdlc-commit-prep
description: AI SDLC commit preparation workflow. Use when Codex is asked to commit repository changes, prepare an auditable commit message, stage files safely, include SDD and Asana traceability, verify branch/spec alignment, or verify the working tree before committing.
---

# AI SDLC Commit Prep

## Purpose

Prepare and create a safe AI SDLC commit by reviewing the branch and working tree, staging only related files, validating SDD evidence, using a valid Conventional Commit message, and reporting post-commit traceability.

## Inputs

- Collect the user’s explicit commit request or workflow state showing commit prep is justified.
- Collect the active spec folder for medium or large work.
- Collect validation commands and outcomes that are current for the active diff.
- Collect the related Asana task from the spec or commit body when one exists.
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
15. Use `$ai-sdlc-asana-commit-comment` for Asana-linked work after the commit succeeds.

## Output Spec

Return this final report:

```text
Commit:
- Hash: full_hash
- Subject: conventional subject
- Branch: branch-name
- Spec: specs/NNN-feature-name | none
- Asana: task_gid URL | none

Staging:
- Included: path groups and why they belong.
- Excluded: unrelated dirty paths or none.

Validation:
- command -> outcome

Post-commit:
- Working tree: clean | dirty with listed paths.
- Asana comment: posted comment_gid | skipped: reason.
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
- Do not move an Asana task that is already `Done` or `Released` unless the user explicitly requests it.

## Scope Boundary

- Do not draft commit message content without `$ai-sdlc-conventional-commit`.
- Do not decide test coverage; use `$ai-sdlc-test-cases`, `$ai-sdlc-qa`, and `$ai-sdlc-validation`.
- Do not create Asana task traceability; use `$ai-sdlc-asana-traceability`.
- Do not revert user changes to make staging easier.
