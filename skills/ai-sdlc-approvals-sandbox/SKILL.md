---
name: ai-sdlc-approvals-sandbox
description: AI SDLC approvals, sandbox, and command rule workflow. Use when Codex needs to decide whether to request escalated permissions, explain sandbox failures, propose prefix_rule approvals, avoid unsafe command patterns, or document why a command was or was not rerun outside the sandbox.
---

# ai-sdlc-approvals-sandbox: Approvals And Sandbox

> Internal AI SDLC skill, not client-facing by default.
> Every rule below is important to follow. None of it can be skipped.
> Before producing the final artifact, confirm required inputs, target audience, missing facts, output format, and constraints when they are unclear.
> Do not invent missing information. Ask concise clarification questions when required inputs are absent.

## 0. Skill Card

- Skill name: `ai-sdlc-approvals-sandbox`
- Primary audience: Dev
- Supporting audience: QA
- Audience tags: Dev, QA
- SDLC stage: Sandbox escalation decision
- Purpose: Decide, request, and report sandbox escalation for AI SDLC commands only when the sandbox blocks a required action or the task explicitly requires approved external access.
- Output: Sandbox escalation decision record with prefix_rule guidance and residual risk

### 0.1 Required Inputs

- Exact command that failed or requires external access.
- Task reason for the command.
- Sandbox error, expected restriction, and risk profile.

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

- Use `scripts/approval_plan.py` when deterministic validation, planning, or formatting is required by the workflow.

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
- Do not weaken developer SDD, review, or validation requirements because sandbox permissions are inconvenient.
- Do not replace the active runtime’s higher-priority sandbox and approval policies.
