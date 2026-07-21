---
name: ai-sdlc-security-testing
description: AI SDLC security testing workflow. Use when an AI assistant is asked for OWASP review, security testing, abuse-case analysis, authz/authn review, input validation review, secret exposure review, or security-focused validation of a diff, endpoint, workflow, or subsystem. Supports `--quick-flow` for fast assumption-driven execution and `--full-flow` for question-driven verified execution.
---

# ai-sdlc-security-testing: Security Testing

> Internal AI SDLC skill, not client-facing by default.
> Every rule below is important to follow. None of it can be skipped.
> Before producing the final artifact, confirm required inputs, target audience, missing facts, output format, and constraints when they are unclear.
> Do not invent missing information. Ask concise clarification questions when required inputs are absent.

## 0. Skill Card

- Skill name: `ai-sdlc-security-testing`
- Primary audience: Dev
- Supporting audience: QA, Security, BA
- Audience tags: Dev, QA, BA
- SDLC stage: Security review / abuse-case validation
- Purpose: Review AI SDLC diffs, endpoints, workflows, provider integrations, and configs for concrete security findings, abuse paths, trust-boundary failures, and missing security validation. When the output makes OWASP- or standards-based claims, verify them against current primary sources before presenting them as authoritative guidance.
- Output: Security findings, trust-boundary analysis, standards-backed notes, validation gaps, and fixes

### 0.1 Required Inputs

- Security review target: diff, endpoint, workflow, commit, branch, or subsystem.
- Identity, trust-boundary, data, provider, and state context.
- Relevant specs and validation evidence when available.

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

- Use `scripts/security_review_matrix.py` when deterministic scaffolding, planning, or formatting is useful for this workflow; pass the same `--quick-flow` or `--full-flow` flag that was supplied to the skill.
- Read `references/owasp-backend-checklist.md` when the task needs the detailed structure, checklist, or examples for this skill.

## Script Usage

- Run `scripts/security_review_matrix.py` before drafting or updating this skill's artifact when inputs are longer than a few bullets, when traceability matters, or when a flow flag is supplied. For agent analysis, pass `--format toon`, read `anchors` first, and open only `next_reads`; without that flag the script keeps its human-readable Markdown output.
- Quick flow analysis: `python3 skills/ai-sdlc-security-testing/scripts/security_review_matrix.py --feature <feature-name> --quick-flow <input.md>...`
- Full flow analysis: `python3 skills/ai-sdlc-security-testing/scripts/security_review_matrix.py --feature <feature-name> --full-flow <input.md>...`
- To write content, pass one canonical heading with `--section "<section>"`; provide only that section body on stdin, without H1, H2, frontmatter, or a temporary content file.
- Repeat `--section` for each required section, then run the same script with `--finalize` to validate the artifact and refresh metadata and specs indexes.
- The AI must not write or directly edit the routed Markdown artifact; the script owns scaffold creation, section placement, and durable file writes.
- Use `--decision-row` with one nine-cell Markdown table row on stdin when a decision-log entry is required.
- Legacy `--emit-template`, `--emit-decision-log-entry`, and `--write` remain available for compatibility.
- Use `--quick-flow` for first-pass synthesis with assumptions; use `--full-flow` before readiness, handoff, signoff, or any decision-sensitive output.

## Purpose

Review AI SDLC diffs, endpoints, workflows, provider integrations, and configs for concrete security findings, abuse paths, trust-boundary failures, and missing security validation. When the output makes OWASP- or standards-based claims, verify them against current primary sources before presenting them as authoritative guidance.

## Inputs

- Collect the exact review target: diff, commit, branch, endpoint, workflow, subsystem, or file set.
- Run or read `git status --short` and `git diff --stat` for diff-based reviews.
- Read relevant spec files for medium or large work.
- Identify entry points, identity sources, roles, organizations, accounts, providers, assets, secrets, and state transitions.
- Read `references/owasp-backend-checklist.md` when the surface is broad or the user asks for OWASP-style coverage.
- When the request mentions OWASP, ASVS, API Top 10, or other standards-driven guidance, browse current primary sources before citing categories, versions, or remediation guidance.

## Steps

1. Define the protected asset and trust boundary.
2. Map externally controlled inputs, identity sources, and privileged operations.
3. Check authentication before business side effects.
4. Check authorization across organization, account, role, provider, and workflow boundaries.
5. Check input validation, normalization, decimal handling, output encoding, query construction, and command construction.
6. Check secret handling, logs, errors, test fixtures, docs, config defaults, and webhook material for leakage.
7. Check replay, idempotency, race windows, retry behavior, broken state transitions, and failure isolation.
8. If the output will map issues to OWASP or another security standard, verify the current standard text from primary sources first. Prefer official OWASP pages, ASVS, API Security Top 10, or equivalent authoritative documentation.
9. Separate local exploitability evidence from standards-backed interpretation. Do not present remembered OWASP categories or stale version assumptions as verified guidance.
10. Check whether `test-cases.md`, `qa.md`, automated tests, or validation commands cover the risky paths.
11. Report concrete findings first, ordered by severity.
12. Report no findings explicitly when none are found, then list validation gaps, blocked verification, or residual risk.

## Output Spec

Use this findings-first format:

```text
Findings:
- [CRITICAL|HIGH|MEDIUM|LOW] path:line - concise issue statement.
  Impact: exploitable outcome.
  Evidence: code path, input, state, or missing check.
  Fix: concrete remediation.

Verified sources:
- Required when the output uses OWASP or standards-based claims.
- Include the current primary source link and the specific claim it supports.

Open questions:
- Trust-boundary or exploitability question that blocks severity or fix selection.

Validation gaps:
- Missing security test, QA check, or command and why it matters.

Summary:
- Brief security posture summary after findings.
```

Quality gate:

- Pass when every finding is tied to a concrete path, exploit condition, impact, and fix.
- Fail when the output recites generic OWASP categories, cites standards from memory without verification, inflates speculative issues, omits severity, or hides missing validation.

## Examples

Finding example:

```text
Findings:
- [HIGH] internal/transport/http/v1/handlers/transfers.go:142 - Transfer lookup does not verify organization ownership before returning wallet metadata.
  Impact: A user with access to one organization could enumerate another organization's provider wallet labels.
  Evidence: Handler uses transfer ID from the route and returns provider details before checking org ownership.
  Fix: Load the transfer through an organization-scoped query or compare `transfer.OrganizationID` before building the response.
```

No-finding example:

```text
Findings:
- None found.

Validation gaps:
- No automated test covers replay of duplicate webhook IDs; add a service-level idempotency test before release.
```

Invalid counter-example:

```text
Security looks fine.
```

Reject this because it omits reviewed boundaries, findings status, and validation gaps.

## Edge Cases

- Stop and warn immediately if real secrets, bearer tokens, private keys, or production-only values appear in the diff; do not paste them back.
- State `target unclear` when no diff, endpoint, workflow, or subsystem is provided and local context cannot infer one safely.
- Use `$ai-sdlc-code-review` when the main ask is correctness, regression, or maintainability rather than exploitability.
- If browsing or primary-source verification is unavailable, report `standards verification blocked` and limit the output to locally supported exploitability findings instead of presenting unverified OWASP guidance.
- Mark validation as blocked when required credentials, fixtures, or environment are unavailable.
- Do not lower severity because a path is "internal" unless the trust boundary proves only trusted callers can reach it.

## Scope Boundary

- Do not perform general code review unless security is the primary question.
- Do not run production attacks, live exploitation, or credentialed provider actions.
- Do not expose sensitive values in findings, tests, comments.
- Do not decide business acceptance; use `$ai-sdlc-ba` and `$ai-sdlc-qa`.
- Do not cite OWASP categories, ASVS controls, or standards versions from memory when current-source verification is required.
