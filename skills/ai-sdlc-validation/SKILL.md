---
name: ai-sdlc-validation
description: AI SDLC backend validation workflow. Use when Codex needs to validate Go, SQL, API, provider integration, SDD, or documentation changes in this repository and choose focused deterministic checks without running unrelated expensive tests by default.
---

# AI SDLC Validation

## Purpose

Select, run, and report focused deterministic validation checks for AI SDLC code, SQL, API, provider, SDD, documentation, and Codex-governance changes.

## Inputs

- Collect changed files from `git status --short`, `git diff --name-only`, or explicit user-provided paths.
- Read the active spec and `qa.md` when the work is medium, large, release-sensitive, or user-visible.
- Collect previous validation output only when it is current for the same diff signature.
- Collect sandbox constraints that affect Go cache, network access, local listeners, or external services.
- Run the validation planner when changed files are not trivial:

  ```bash
  python3 .codex/skills/ai-sdlc-validation/scripts/validation_plan.py
  ```

## Steps

1. Classify changed files by surface: Go package, SQL/sqlc, API contract, provider integration, frontend/docs, SDD/spec, Codex governance, or mixed.
2. Select the narrowest command set that proves the changed behavior.
3. Prefer focused tests before broad suites when the risk is localized.
4. Use `GOCACHE=/tmp/ai-sdlc-go-cache` for Go tests to avoid sandbox cache write failures.
5. Run spec and skill validators for SDD, `.codex`, hook, or skill changes.
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

Codex setup change:

```text
Validation:
- command: python3 .codex/scripts/quick_validate_skill.py .codex/skills/ai-sdlc-workflow
  outcome: passed
  reason: validates changed skill metadata.
- command: python3 .codex/skills/ai-sdlc-sdd/scripts/sdd_status.py --spec specs/185-spec-kit-sdd-quality-gates
  outcome: passed
  reason: confirms the active governance spec is structurally valid and ready for implementation.
- command: python3 .codex/scripts/codex_governance_audit.py --limit 3
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
