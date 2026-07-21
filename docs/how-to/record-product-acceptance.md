---
title: Record product acceptance
description: Preserve a revision-bound Product Owner accept, reject, or follow-up decision without inventing a new source of truth.
---

# Record product acceptance

Use this procedure after implementation validation and independent review. It
binds the Product Owner's outcome decision to one revision and its acceptance
evidence. It does not replace QA, code review, security acceptance, or release
approval.

## Canonical location and authority

Record product acceptance as one `DEC-###` row in
`specs/<feature>/decision-log.md`. The decision log is already the canonical
implementation decision record; do not create an untracked chat approval or a
second `acceptance.md` source of truth. The Product Owner may decide only within
documented delegation. Escalate strategy, budget, legal, security, and
cross-product decisions to the named owner.

## Required inputs

- exact reviewed Git commit hash or immutable revision;
- accepted acceptance-criterion identifiers;
- current test/validation receipt or exact command evidence;
- product demonstration or observation evidence;
- unresolved defects, exclusions, follow-ups, and residual risk;
- accountable Product Owner identity or governed role.

## Write the decision

Use the existing decision-log columns. A complete row has this form:

```markdown
| DEC-042 | 2026-07-21 | accepted / rejected | Product Owner: <name-or-governed-role> | Accept revision `<full-commit>` for AC-001 and AC-002; non-blocking follow-up `<ticket-or-none>` remains owned by `<owner>` | Demonstration `<link-or-local-evidence>`; validation receipt `specs/<feature>/_ai_sdlc/validation-receipt.json`; review `<reference>` | accept; reject; follow-up | requirements.md; test-cases.md; tasks.md; reviewed code | AC-001; AC-002; TC-001; TC-002; T001; `<full-commit>`; follow-up ticket or `none` |
```

Replace every placeholder. Use `rejected` when intended behavior is absent or
evidence is stale. Use canonical status `accepted` when any remaining item is
explicitly outside the accepted criteria and is an owned, non-blocking risk;
record that conditional disposition, owner, and tracking reference in the
Decision, Context/Evidence, and Trace fields. Never change an acceptance criterion
after observing the implementation merely to make the outcome pass.

## Verify and hand off

```bash
git rev-parse HEAD
git diff --check
git status --short
```

Expected: the recorded revision equals the reviewed revision; only the intended
decision-log change is present or staged; every cited local path exists; and
the decision row names a disposition, accountable owner, criteria, evidence,
and remaining work. A later code, requirement, or evidence change makes the
acceptance stale and requires a new decision row rather than silently editing
history.

The release owner consumes this decision but still checks all other release
gates. See [Open, review, and merge](review-and-merge.md), the
[Product Owner guide](../roles/product-owner.md), and the
[traceability model](../explanation/traceability.md).
