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
