---
name: ai-sdlc-approvals-sandbox
description: AI SDLC approvals, sandbox, and command rule workflow. Use when Codex needs to decide whether to request escalated permissions, explain sandbox failures, propose prefix_rule approvals, avoid unsafe command patterns, or document why a command was or was not rerun outside the sandbox.
---

# AI SDLC Approvals Sandbox

## Purpose

Decide, request, and report sandbox escalation for AI SDLC commands only when the sandbox blocks a required action or the task explicitly requires approved external access.

## Inputs

- Collect the exact command that failed or must run outside the sandbox.
- Collect the task reason that makes the command necessary.
- Collect the sandbox error or expected restriction: filesystem, network, listener, GUI, external service, or destructive action.
- Collect whether the command is destructive, secret-bearing, shell-heavy, or reusable.
- Collect an intended narrow `prefix_rule` only when repeated approval is safe.

## Steps

1. Run normal reads, workspace writes, local tests, and formatting in the default sandbox first.
2. Classify the command into one segment per shell operator when the command contains pipes, separators, logical operators, or subshells.
3. Request escalation only when a required command is blocked by sandbox restrictions or explicitly needs approved external access.
4. Do not request escalation to bypass SDD, skip validation, avoid fixing a local setup issue, or run unrelated broad commands.
5. Validate the approval plan before asking when time permits:

   ```bash
   python3 .codex/skills/ai-sdlc-approvals-sandbox/scripts/approval_plan.py \
     --command 'go test ./internal/service/...' \
     --justification 'Allow running focused service tests with the required sandbox permissions?' \
     --prefix-rule 'go test ./internal/service/...'
   ```

6. Phrase `justification` as a short user-facing question.
7. Provide `prefix_rule` only for narrow, reusable, non-destructive command classes.
8. Rerun the command only after approval is granted.
9. Report denied or partial approval and continue with the best safe fallback.

## Output Spec

Return this decision record when escalation is requested, denied, or skipped:

```text
Sandbox decision:
- Command: exact command
- Required for: task-specific reason
- Sandbox issue: filesystem | network | listener | GUI | external service | destructive | none
- Escalation: requested | not requested | denied | granted
- Prefix rule: proposed rule | none and why
- Result: passed | failed | skipped | blocked
- Residual risk: none | concrete limitation
```

Quality gate:

- Pass when escalation is narrow, justified by the task, and avoids broad reusable approval for dangerous commands.
- Fail when the request uses vague justification, proposes broad interpreter or shell prefixes, includes secrets, or escalates unrelated work.

## Examples

Valid request:

```json
{
  "sandbox_permissions": "require_escalated",
  "justification": "Allow running Go tests with a writable external cache for this package?",
  "prefix_rule": ["go", "test", "./internal/service/..."]
}
```

Invalid counter-example:

```json
{
  "sandbox_permissions": "require_escalated",
  "justification": "Need permissions.",
  "prefix_rule": ["python3"]
}
```

Reject this because the justification is vague and the prefix allows arbitrary scripts.

## Edge Cases

- Skip reusable `prefix_rule` for destructive commands such as `rm`, `git reset`, force push, or data deletion.
- Skip reusable `prefix_rule` for heredocs, redirection, wildcards, command substitution, environment-heavy one-liners, or shell wrappers.
- Warn immediately and avoid reusing commands when a command contains credentials, bearer tokens, private keys, webhook secrets, or production-only values.
- Treat a missing dependency error as a setup issue first, not an escalation reason, unless the dependency download is required and network is blocked.
- Report partial approval when one command segment is approved but another remains blocked.

## Scope Boundary

- Do not decide which validation commands are required; use `$ai-sdlc-validation`.
- Do not approve destructive commands on the user's behalf.
- Do not weaken repository SDD, review, or validation requirements because sandbox permissions are inconvenient.
- Do not replace the active runtime’s higher-priority sandbox and approval policies.
