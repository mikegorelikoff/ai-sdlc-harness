---
name: ai-sdlc-approvals-sandbox
description: AI SDLC approvals, sandbox, and command rule workflow. Use when an AI assistant needs to decide whether to request escalated permissions, explain sandbox failures, propose prefix_rule approvals, avoid unsafe command patterns, or document why a command was or was not rerun outside the sandbox. Supports `--quick-flow` for fast assumption-driven execution and `--full-flow` for question-driven verified execution.
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

- Exact command structure that failed or requires external access, with every
  credential and secret-bearing value replaced by `<redacted>` before capture.
- Task reason for the command.
- Sandbox error, expected restriction, and risk profile.

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

### 0.3.1 Credential Boundary

- Preserve enough command structure to assess scope, shell operators, and the
  proposed prefix, but redact secret-bearing values before the command reaches
  any prompt, approval request, tool argument, log, decision record, or output.
- Never place a raw credential, bearer token, private key, password, webhook
  secret, signed URL, session identifier, or production-only value in an
  escalation record. Use `<redacted>` and describe the value's role separately.
- If safe redaction would make the command impossible to review, stop and ask
  the user for a sanitized command. Do not echo the unsafe input back.

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

- Use `scripts/approval_plan.py` when deterministic validation, planning, or formatting is required by the workflow; pass the same `--quick-flow` or `--full-flow` flag that was supplied to the skill when supported.

## Script Usage

- Validate approval requests before asking for escalation or recording an approval decision.
- Quick flow: `python3 skills/ai-sdlc-approvals-sandbox/scripts/approval_plan.py --quick-flow --command "<command>" --justification "<user-facing question?>"`
- Full flow: `python3 skills/ai-sdlc-approvals-sandbox/scripts/approval_plan.py --full-flow --command "<command>" --justification "<user-facing question?>" --prefix-rule "<safe reusable prefix>"`
- Use `--prefix-rule` only when proposing a reusable non-destructive approval prefix; omit it for destructive or one-off commands.

## Purpose

Decide, request, and report sandbox escalation for AI SDLC commands only when the sandbox blocks a required action or the task explicitly requires approved external access.

## Inputs

- Collect the command structure that failed or must run outside the sandbox;
  redact secret-bearing values before collecting or returning it.
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
   python3 skills/ai-sdlc-approvals-sandbox/scripts/approval_plan.py \
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
- Command: sanitized command with every secret-bearing value shown as <redacted>
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
- Never repeat the raw secret-bearing command while warning; refer only to the
  sanitized structure and the credential category.
- Treat a missing dependency error as a setup issue first, not an escalation reason, unless the dependency download is required and network is blocked.
- Report partial approval when one command segment is approved but another remains blocked.

## Scope Boundary

- Do not decide which validation commands are required; use `$ai-sdlc-validation`.
- Do not approve destructive commands on the user's behalf.
- Do not weaken developer SDD, review, or validation requirements because sandbox permissions are inconvenient.
- Do not replace the active runtime’s higher-priority sandbox and approval policies.
