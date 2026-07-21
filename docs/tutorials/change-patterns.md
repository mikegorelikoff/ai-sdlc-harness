---
title: Common change patterns
description: Ten end-to-end patterns for features, defects, refactors, APIs, schemas, tests, ambiguity, review, recovery, and requirement change.
---

# Common change patterns

Terms used below are Specification-driven development (SDD), quality assurance
(QA), business analysis (BA), non-functional requirement (NFR), minimum viable
product (MVP), continuous integration (CI), artificial intelligence (AI), and
application programming interface (API). It also uses representational state
transfer (REST), not applicable (N/A), Press Release/Frequently Asked Questions
(PRFAQ), and business requirements document (BRD).

These compact tutorials adapt the complete [first feature](first-feature.md)
journey to common delivery work. They show the evidence contract; substitute
your repository's language, test runner, deployment controls, and accountable
owners. Commands are examples, not universal standards.

Every pattern preserves this sequence:

```text
request → discovery → specification → test cases → tasks → implementation
        → independent review → current validation → human acceptance
```

Before starting, install the harness, create or select a task branch, and read
the repository instructions. If `AGENTS.md` is absent, use the documented SDD
risk rubric and record that assumption rather than inventing local policy.

## 1. Implement a small feature

Initial request: “Add `GET /health` returning `200` and
`{"status":"ok"}`.”

- **Discovery questions:** Does health mean process liveness or dependency
  readiness? Is authentication required? Which existing routes must remain
  unchanged?
- **Resulting specification:** exact method, path, status, body, exclusions,
  and regression acceptance criteria.
- **Plan and tasks:** add the failing route test; implement the smallest route;
  run the full route suite; review and commit.
- **Skills:** navigator → branching → SDD → validation → code review → commit
  preparation.
- **Implementation sequence:** test first, implement, run focused and
  regression tests, inspect the diff.
- **Validation:** exact body/status assertion, unknown-route regression, test
  suite, and `git diff --check`.
- **Artifacts:** `requirements.md`, `test-cases.md`, `tasks.md`, code/test diff,
  validation record, reviewed commit.
- **Common failures:** silently adding dependency readiness, adding a framework,
  or claiming pass without executing tests.
- **Final acceptance evidence:** acceptance criteria map to passing current test
  output and product-owner confirmation.

The runnable version is [Ship a first feature](first-feature.md).

## 2. Fix a defect

Initial request: “A plus sign in an email address is rejected during signup.”

- **Discovery questions:** Which valid examples fail? Which invalid examples
  must remain rejected? Where is the rule defined? Is stored data affected?
- **Resulting specification:** reproduce the observed defect, define accepted
  and rejected boundaries, preserve unrelated validation, and exclude a broad
  identity-policy rewrite.
- **Plan and tasks:** capture a failing regression; locate the narrow decision
  point; repair it; run validation and signup regressions.
- **Skills:** project context → SDD quick flow → test cases → implementation →
  validation → code review.
- **Implementation sequence:** prove failure before editing, add regression,
  make the smallest correction, rerun negative cases.
- **Validation:** the original input passes, malformed addresses still fail,
  integration behavior is unchanged, and no existing test is weakened.
- **Artifacts:** defect evidence, root-cause note, AC/TC links, patch, test
  output, reviewer disposition.
- **Common failures:** coding from a vague report, expanding to an email parser
  rewrite, or deleting a failing negative test.
- **Final acceptance evidence:** original reproduction now passes on the
  reviewed commit and the reporter or owner confirms the intended rule.

## 3. Refactor legacy code

Initial request: “Split the 900-line billing function so it is maintainable.”

- **Discovery questions:** Which behavior is authoritative? What seams exist?
  What performance, ordering, and error behavior must remain? Which defects are
  explicitly out of scope?
- **Resulting specification:** behavior-preservation contract, measurable
  structural goal, performance tolerance, rollback boundary, and exclusions.
- **Plan and tasks:** characterize behavior; add missing characterization tests;
  extract one seam at a time; compare outputs; remove dead code only with proof.
- **Skills:** project context → change impact → SDD → test cases → validation →
  code review.
- **Implementation sequence:** baseline tests and timing, small mechanical
  extraction, test after each step, no feature change in the same commit.
- **Validation:** characterization and integration suites, representative
  performance comparison, public API diff, and static checks.
- **Artifacts:** dependency map, preservation ACs, baseline evidence, task
  sequence, focused commits, before/after measures.
- **Common failures:** “cleaner” as an untestable goal, mixing behavior changes,
  deleting odd edge cases, or accepting generated abstractions without review.
- **Final acceptance evidence:** all preserved behaviors pass, the structural
  measure is met, and reviewers can revert each bounded step.

## 4. Introduce a new API

Initial request: “Expose customer preferences through a REST API.”

- **Discovery questions:** Who may read/write? What is the schema and versioning
  policy? What are error, idempotency, rate, audit, and privacy requirements?
- **Resulting specification:** endpoint contract, actors and authorization,
  validation, error model, compatibility, non-functional requirements, and
  observability.
- **Plan and tasks:** approve contract; implement authorization and validation;
  add service and transport tests; publish consumer guidance; stage rollout.
- **Skills:** business analysis → architecture → SDD → security testing → test
  synthesis → validation → code review.
- **Implementation sequence:** contract/tests first, service behavior,
  transport, authorization negatives, compatibility checks, documentation.
- **Validation:** unit, service, contract, integration, authorization, malformed
  input, rate-limit or N/A decision, and API documentation render.
- **Artifacts:** API schema, decisions, threat notes, tests, implementation,
  compatibility evidence, rollout/rollback plan.
- **Common failures:** happy-path-only tests, authorization after data access,
  undocumented errors, or a breaking schema under an unchanged version.
- **Final acceptance evidence:** contract tests and abuse cases pass, API owner
  accepts compatibility, and operations accepts rollout signals.

## 5. Change a database schema

Initial request: “Make `orders.external_id` unique and required.”

- **Discovery questions:** Are nulls or duplicates already present? Which
  writers/readers are deployed independently? What database and lock limits
  apply? How is rollback handled after backfill?
- **Resulting specification:** current-data preconditions, expand/migrate/
  contract phases, compatibility window, performance limits, backup and
  rollback decisions.
- **Plan and tasks:** inventory data; add compatible schema; dual-read/write if
  required; backfill idempotently; verify; enforce constraint later.
- **Skills:** business analysis → architecture → change impact → SDD → QA and
  security review → validation.
- **Implementation sequence:** dry-run query, reversible migration, application
  compatibility, bounded backfill, constraint validation, deferred cleanup.
- **Validation:** duplicate/null queries, migration up/down in disposable data,
  old/new application compatibility, lock duration, backup/restore evidence.
- **Artifacts:** data profile, migration design, scripts, test fixtures,
  execution runbook, decision log, monitored rollout record.
- **Common failures:** one-step destructive migration, unbounded table lock,
  non-idempotent backfill, secret-bearing production data in prompts, or
  pretending rollback is possible after destructive conversion.
- **Final acceptance evidence:** staged migration gates pass on representative
  data and the database/service owners approve the next irreversible gate.

## 6. Add automated tests

Initial request: “Increase checkout test coverage.”

- **Discovery questions:** Which risks or escaped defects motivate this? Which
  layer gives the best signal? What makes a test deterministic? Is a coverage
  number a requirement or only a diagnostic?
- **Resulting specification:** named behaviors and risks, suite location,
  fixtures, isolation, runtime budget, and explicit non-goals.
- **Plan and tasks:** map uncovered risk; write failing tests where a defect is
  known; add boundary/negative cases; remove nondeterminism; measure runtime.
- **Skills:** QA requirements gap review → test strategy → test synthesis →
  validation → code review.
- **Implementation sequence:** choose risk, create minimal fixture, assert
  observable behavior, prove the test can fail, run focused/full suites.
- **Validation:** deterministic repeat runs, mutation or controlled-failure
  probe, suite runtime, and traceability to the risk—not a vanity percentage.
- **Artifacts:** strategy, test cases, fixtures, test diff, run evidence,
  residual coverage gaps.
- **Common failures:** tests that restate implementation, snapshots with no
  review, flaky clocks/networks, and fabricated coverage claims.
- **Final acceptance evidence:** tests fail for the intended regression, pass
  for the correction, and the QA owner accepts residual risk.

## 7. Clarify an ambiguous business request

Initial request: “Let premium customers skip approval.”

- **Discovery questions:** What qualifies as premium, which approval, for which
  amount/region/product, who may override, and what audit or regulatory rules
  apply? Which stakeholders disagree?
- **Resulting specification:** actors, decision table, exceptions, assumptions,
  measurable outcomes, exclusions, non-functional/audit requirements, and
  unresolved decisions with owners.
- **Plan and tasks:** working-backwards discovery; requirements readiness;
  goal/backlog/story decomposition and release slicing; then the BA
  workflow/rule model. Stories must exist before the canonical BA stage.
- **Skills:** working-backwards discovery → PRFAQ/BRD synthesis → delivery gap
  review → requirements readiness → goal/epic mapping → backlog gap and
  decomposition → story decomposition → release slicing → business analysis →
  delivery specification.
- **Implementation sequence:** none until conflicting definitions and approval
  authority are resolved; then hand the accepted package to story/spec work.
- **Validation:** stakeholder scenario walkthrough, rule-table coverage,
  contradiction scan, and signed/delegated decision references.
- **Artifacts:** question log, stakeholder positions, assumption register,
  decision table, requirements, risks, acceptance scenarios, and the canonical
  `business-context.md` after accepted stories and release boundaries exist.

Representative `business-context.md` evidence—not generic filler—looks like:

| Rule / exception | Actor and trigger | Expected outcome | Source / decision | Acceptance link |
| --- | --- | --- | --- | --- |
| BR-001: only accounts with accepted premium classification may request the bypass | Account owner submits an approval-bound action | Policy evaluates the classification and either follows normal approval or enters the explicitly authorized exception | Pricing policy section 4; DEC-014 owned by Product | AC-021 / TC-033 |
| EX-001: regulated regions never use the bypass | Same actor; account region is regulated | Normal approval remains mandatory and an audit reason is recorded | Compliance owner decision DEC-015 | AC-022 / TC-034 |
| CONFLICT-001: Sales asks for automatic bypass while Compliance prohibits it | Product manager and compliance owner review the same scenario | Work remains blocked until one accountable decision supersedes the conflict | Stakeholder notes plus DEC-015 | AC-022 |

The complete artifact also includes user and system workflows, permissions,
failure paths, non-functional needs, dependencies, assumptions, open questions,
source coverage, and owner review. The table demonstrates evidence shape; it is
not a reusable business rule.
- **Common failures:** treating one stakeholder's wording as policy, letting the
  agent choose a monetary threshold, or creating backlog volume before value
  and authority are clear.
- **Final acceptance evidence:** accountable product/business owners approve
  one interpretation and every material exception has a testable outcome.

## 8. Review AI-generated code

Initial request: “Review the agent's payment retry implementation.”

- **Discovery questions:** What specification and revision does it claim to
  implement? Which commands actually ran? What money, privacy, concurrency,
  and idempotency risks exist? Was any dependency added?
- **Resulting specification:** unchanged; if the diff reveals a new decision,
  return to requirements instead of normalizing it in review.
- **Plan and tasks:** inspect diff and provenance; map code/tests to AC/TC IDs;
  run independent checks; threat-model abuse and failure paths; disposition
  every finding.
- **Skills:** code review → security testing → validation → evidence council for
  high-risk disagreement.
- **Implementation sequence:** reviewers do not trust comments or PASS labels;
  inspect behavior, run commands on the exact revision, then request bounded
  corrections.
- **Validation:** retry/idempotency integration tests, forced timeouts,
  duplicate-delivery tests, secret scan, dependency review, and current CI.
- **Artifacts:** findings-first report, command evidence, revision identity,
  dispositions, residual risk and named approval.
- **Common failures:** stylistic review only, approving because tests exist,
  executing a generated destructive command, or letting the authoring agent
  self-approve.
- **Final acceptance evidence:** independent reviewers verify the exact commit;
  no unresolved Critical/High finding remains.

## 9. Respond to a failed implementation

Initial request: “The new import job fails after ten minutes and leaves partial
records.”

- **Discovery questions:** Can the failure be reproduced safely? What state was
  committed? Can retry duplicate work? Is production containment required?
  Which evidence is trustworthy?
- **Resulting specification:** preserve the original acceptance contract; add
  explicit atomicity, retry, cleanup, and observability criteria if they were
  missing, with owner approval.
- **Plan and tasks:** stop unsafe automation; capture evidence; contain impact;
  reproduce in disposable data; diagnose cause; update spec/tests; repair or
  revert; revalidate.
- **Skills:** validation diagnosis → change impact → SDD change control → test
  cases → implementation → retrospective.
- **Implementation sequence:** do not repeatedly rerun against production;
  isolate, prove the failure, add a controlled negative test, repair the narrow
  cause, verify cleanup/retry.
- **Validation:** failure injection, transaction/compensation assertions,
  idempotent retry, telemetry, full regression, and post-recovery data check.
- **Artifacts:** failure log with redaction, incident/decision record, changed
  AC/TC links, repair or revert, validation and follow-up actions.
- **Common failures:** deleting failed evidence, changing code before diagnosis,
  treating a timeout as a test flake, or exposing production data to a model.
- **Final acceptance evidence:** the reproduced failure is blocked or safely
  recovered, partial state is accounted for, and operations/product accept the
  outcome.

## 10. Change requirements after work starts

Initial request: “The health endpoint must now include dependency readiness.”

- **Discovery questions:** Is this a replacement or an additional endpoint?
  What dependencies and timeouts count? Who consumes it? Could orchestration
  restart healthy processes during a dependency incident?
- **Resulting specification:** a versioned decision and changed ACs/NFRs;
  preserved old behavior or explicit breaking change; rollout and monitoring
  implications.
- **Plan and tasks:** pause implementation; create an isolated change-set intake
  and semantic delta; preview without applying; run change impact against those
  stable changed references; obtain the accountable owner's decision; then
  apply/reopen and update requirements, design, tests, QA, and tasks in
  authority order. Invalidate stale evidence and obtain new acceptance.
- **Skills:** change set intake/delta/preview → change impact → owner-approved
  apply/reopen → SDD analysis → QA gap review → validation.
- **Implementation sequence:** do not patch only the code. Preserve the proposed
  change as a valid change-set input before impact analysis; after approval,
  revise authoritative artifacts, regenerate derived plans, implement changed
  tasks, and rerun affected and regression suites.
- **Validation:** old/new contract tests, timeout/failure paths, orchestration
  behavior, stale-evidence detection, and rollout/rollback exercise.
- **Artifacts:** change request, impact map, decision, updated specification,
  obsolete evidence marker, revised tasks, new validation and acceptance.
- **Common failures:** silently changing acceptance, leaving old tests as if
  current, preserving an impossible schedule, or merging before operational
  ownership agrees.
- **Final acceptance evidence:** every changed requirement traces to a current
  task/test/result and the accountable owner explicitly accepts the new scope.

## Pattern completion checklist

- [ ] The initial request and discovery decisions are retained.
- [ ] Requirements distinguish assumptions, constraints, exclusions, and risks.
- [ ] Plans and tasks point to acceptance criteria and test cases.
- [ ] Validation was executed on the reviewed revision and records failures.
- [ ] Human product, technical, quality, security, and operations decisions are
  present where the risk requires them.
- [ ] The final evidence is understandable without access to the original
  prompt or chat.

For the broader organizational path, continue with [Run a bounded
pilot](../adoption/pilot.md) and [Stage a rollout](../adoption/rollout.md).
