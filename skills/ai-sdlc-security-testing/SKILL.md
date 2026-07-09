---
name: ai-sdlc-security-testing
description: AI SDLC security testing workflow. Use when Codex is asked for OWASP review, security testing, abuse-case analysis, authz/authn review, input validation review, secret exposure review, or security-focused validation of a diff, endpoint, workflow, or subsystem.
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

- Read `references/owasp-backend-checklist.md` when the task needs the detailed structure, checklist, or examples for this skill.

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
