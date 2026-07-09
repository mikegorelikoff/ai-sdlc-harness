# Review Checklist

Use this checklist when the review needs more depth than the short `SKILL.md`
workflow.

## Review Boundary

- What is being reviewed: diff, feature, package, subsystem, or broad audit?
- Which specs, contracts, migrations, configs, or generated artifacts define
  the expected behavior?
- Do `test-cases.md` and `qa.md` exist for medium/large work, and do they still
  describe the real risky scenarios?
- Which files are highest risk rather than merely highest churn?

## Contracts And APIs

- Are request and response contracts aligned across schemas, handlers, services,
  and docs?
- Do identifiers, enums, nullable fields, and defaults stay consistent?
- If transport files changed, are error mappings and status codes still stable?

## State And Workflow

- Are state transitions valid and idempotent where needed?
- Can retries, duplicate events, or concurrent requests violate invariants?
- Are outbox, saga, queue, or background-consumer interactions safe?

## Data Integrity

- Are decimal math, signs, rounding, units, and asset identifiers explicit?
- Are DB writes, transaction boundaries, and rollback behavior coherent?
- Are provider-side effects gated behind the correct checks?

## Authorization And Boundaries

- Are org/account/role boundaries enforced before side effects?
- Can one tenant influence another tenant's data or workflow?
- Is disabled/deleted/inactive actor handling explicit?

## Tests And Validation

- Which tests cover the changed or audited behavior today?
- Which risky paths are untested?
- What focused tests should exist at unit, service, transport, or integration
  level?
- Does `test-cases.md` still map the risky behavior to the intended test layer?
- Does `qa.md` still describe the acceptance and regression checks that matter?
- If the user wants broad coverage, which wider package or repo suites are the
  next justified step?

## Review Output Discipline

- Primary findings: correctness, regression, contract, authorization, or data
  risks.
- Validation gaps: missing checks or missing evidence.
- Secondary observations: only after primary findings, and only when the user
  explicitly wants a broader audit.

## When To Load This Reference

Load when the diff is medium/large, contract-sensitive, security-sensitive,
stateful, or when the user explicitly asks for a deeper review.

## Review Method

1. Identify the review boundary.
2. Identify the highest-risk changed surfaces.
3. Read the spec/test/QA artifacts if present.
4. Inspect contracts before implementation details.
5. Inspect state transitions and side effects.
6. Inspect authorization and data boundaries.
7. Inspect tests and validation evidence.
8. Report findings before summary.

## Finding Template

Use this shape for real issues:

```text
<severity>: <short issue>
File: <path:line>
Why it matters: <behavioral risk>
Evidence: <code/spec/test evidence>
Suggested fix direction: <concrete direction>
Validation: <test/check that would catch it>
```

Severity guidance:

- Critical: data loss, security bypass, financial/irreversible impact.
- High: user-visible regression, broken contract, incorrect state transition.
- Medium: important edge case, missing validation, likely operational issue.
- Low: maintainability issue only when user asked for broad review.

## Quick Flow Guidance

In `--quick-flow`, focus only on likely correctness/security/regression issues
and the highest-value missing validation.

## Full Flow Guidance

In `--full-flow`, verify spec alignment, decision-log assumptions, test
coverage, contract compatibility, migrations/config, rollout, and validation
evidence.

## Anti-Patterns

- Listing style nits before behavioral bugs.
- Reporting speculation without evidence.
- Treating missing tests as a bug without explaining risk.
- Ignoring changed generated/schema/config files.
- Reviewing every file equally instead of prioritizing risk.
