---
name: ai-sdlc-code-review
description: AI SDLC code review workflow. Use when Codex is asked to review a diff, PR, branch, commit, staged changes, or completed implementation against SDD requirements, tests, API contracts, security, and scope discipline.
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

- Read `references/review-checklist.md` when the task needs the detailed structure, checklist, or examples for this skill.
- Use `scripts/review_readiness.py` when deterministic validation, planning, or formatting is required by the workflow.

## Purpose

Review AI SDLC code, diffs, branches, commits, or completed implementations for correctness, regressions, contract drift, missing tests, SDD drift, and material maintainability risks.

## Inputs

- Collect the review target: staged diff, unstaged diff, branch, commit, PR, package, or subsystem.
- Run `git status --short` and `git diff --stat` for local diffs.
- Read the relevant diff:
  - staged: `git diff --cached`
  - unstaged: `git diff`
  - branch: `git diff <base>...HEAD`
- Read relevant `requirements.md`, `design.md`, `test-cases.md`, `qa.md`, and `tasks.md` for medium or large work.
- Read validation output or record that it is absent.
- Read `references/review-checklist.md` for deep-audit mode or complex surfaces.

## Steps

1. Identify review mode: normal review or deep-audit review.
2. Define the exact review boundary before judging code.
3. Use the `review` subagent only when the user requested review work and the active runtime policy permits delegation; otherwise perform the review locally.
4. Inspect high-risk files first: handlers, services, workflows, providers, config, schema, migrations, generated contracts, tests, and repo-local Codex runtime files.
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
- Require review for non-trivial production code, repo-local Codex logic, config, hook, workflow, provider, transport, schema, or test changes.
- Recommend deep audit for high-churn surfaces, multiple risk categories, or changes spanning handlers, services, providers, and config.
- Keep hook enforcement advisory-first; emit warnings before hard blocks.
