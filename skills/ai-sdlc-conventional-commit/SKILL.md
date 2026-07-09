---
name: ai-sdlc-conventional-commit
description: AI SDLC Conventional Commit workflow. Use when Codex drafts, validates, reviews, or fixes commit messages in this repository, especially when commits must include SDD spec references, validation summaries, or safe conventional commit subjects.
---

# ai-sdlc-conventional-commit: Conventional Commit Message

> Internal AI SDLC skill, not client-facing by default.
> Every rule below is important to follow. None of it can be skipped.
> Before producing the final artifact, confirm required inputs, target audience, missing facts, output format, and constraints when they are unclear.
> Do not invent missing information. Ask concise clarification questions when required inputs are absent.

## 0. Skill Card

- Skill name: `ai-sdlc-conventional-commit`
- Primary audience: Dev
- Supporting audience: PM, BA, QA
- Audience tags: Dev, PM, BA, QA
- SDLC stage: Commit message drafting
- Purpose: Draft, validate, or repair an AI SDLC commit message that uses Conventional Commit syntax and includes SDD, business, implementation, testing, and validation traceability when the change is medium or large.
- Output: Conventional Commit subject/body with traceability and validation summary

### 0.1 Required Inputs

- Change type, scope, and implementation summary.
- Spec, validation, and test evidence when applicable.
- Breaking-change or migration details if any.

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

- Use `scripts/validate_commit_msg.py` when deterministic validation, planning, or formatting is required by the workflow.

## Purpose

Draft, validate, or repair an AI SDLC commit message that uses Conventional Commit syntax and includes SDD, business, implementation, testing, and validation traceability when the change is medium or large.

## Inputs

- Collect the intended change type: `feat`, `fix`, `docs`, `test`, `refactor`, `chore`, `ci`, `build`, `perf`, or `revert`.
- Collect the optional scope when it adds useful precision, for example `api`, `bitgo`, `sdd`, `codex`, or `docs`.
- Collect the active spec folder for medium or large work, for example `specs/177-codex-skill-instruction-upgrade`.
- Collect the implementation summary, reviewer-visible test path, and exact validation commands with outcomes.
- Collect breaking-change details when behavior, schema, API contract, migration requirements, or compatibility changes are not backward compatible.

## Steps

1. Write the subject as `type(scope): imperative summary` or `type: imperative summary`.
2. Keep the subject under 72 characters unless a longer subject prevents ambiguity.
3. Use a lowercase type and lowercase kebab-case scope.
4. Use an imperative summary, for example `fix bitgo wallet routing`, not `fixed bitgo wallet routing`.
6. Add `Spec: specs/NNN-feature-name` for medium or large work.
6. Add `Business context`, `Implementation details`, `Mermaid diagram`, `How to test`, and `Validation` sections for medium or large work.
8. Add `BREAKING CHANGE:` when the change requires a migration, client update, data backfill, or operator action.
9. Validate the message before committing:

   ```bash
   python3 .codex/skills/ai-sdlc-conventional-commit/scripts/validate_commit_msg.py path/to/message.txt --require-traceability
   ```

10. Fix every validator error before using the message.

## Output Spec

Return a complete commit message, not a paragraph about the message:

````text
type(scope): imperative summary


Spec: specs/NNN-feature-name

Business context:
One or two sentences explaining why the change matters to product, operations, risk, clients, QA, or delivery governance.

Implementation details:
- Concrete code, contract, doc, workflow, provider, schema, or validation changes.
- Important compatibility, rollout, or failure-mode decisions.

Mermaid diagram:
```mermaid
flowchart LR
    Actor["Actor or trigger"] --> Change["Changed AI SDLC path"]
    Change --> Outcome["Business-visible outcome"]
```

How to test:
1. Reviewer-visible happy path or documentation path.
2. Important permission, failure, boundary, regression, or governance path.

Validation:
- command -> outcome
````

Quality gate:

- Pass when the subject is Conventional Commit compliant, traceability is present when required, validation commands are exact, and every required body section contains concrete project-specific content.
- Fail when the message uses placeholders, omits required traceability, hides failed validation, or describes implementation in vague terms such as "updated stuff" or "improved docs".

## Examples

Valid medium-change message:

````text
docs(codex): upgrade repo-local skill instructions


Spec: specs/177-codex-skill-instruction-upgrade

Business context:
This makes Codex skill usage deterministic for future AI SDLC work and reduces reviewer effort caused by vague skill outputs.

Implementation details:
- Rewrote every repo-local skill with Purpose, Inputs, Steps, Output spec, Examples, Edge cases, and Scope boundary.
- Added a skill index that maps each workflow phase to the correct skill.

Mermaid diagram:
```mermaid
flowchart LR
    Request["Skill audit"] --> Rewrite["Normalized SKILL.md files"]
    Rewrite --> Output["Consistent Codex behavior"]
```

How to test:
1. Read a cold skill and confirm it contains a complete execution contract.
2. Run skill and spec validators for the updated files.

Validation:
- python3 .codex/scripts/quick_validate_skill.py .codex/skills/ai-sdlc-workflow -> passed
- git diff --check -> passed
````

Invalid counter-example:

```text
updates

Made skills better.
```

Reject this because the subject is not Conventional Commit syntax, traceability is absent, and validation evidence is missing.

## Edge Cases

- Include `BREAKING CHANGE:` even for documentation-only commits when the documented workflow intentionally retires a previously required control.
- Use `revert: ...` only when the commit actually reverts a previous commit; include the reverted hash in the body.
- Stop and fix the message when the validator fails; do not commit with an invalid message.
- State failed or skipped validation honestly in the `Validation` section with the residual risk.

## Scope Boundary

- Do not stage files or create commits; use `$ai-sdlc-commit-prep` for staging and commit execution.
- Do not invent validation results; use `$ai-sdlc-validation` to choose and run checks.
- Do not use this skill to summarize a diff unless the output is a commit message.
