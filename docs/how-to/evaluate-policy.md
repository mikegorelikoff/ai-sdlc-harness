---
title: Evaluate delivery policy
description: Resolve protected policy layers, inspect action gates, and apply bounded expiring waivers.
---

# Evaluate delivery policy

Resolve the built-in base with an organization assurance profile:

```bash
python3 skills/ai-sdlc-policy/scripts/policy.py . \
  --resolve --profile high-assurance --format markdown
```

Add sparse project or user layers with `--project` and `--user`. A later layer
may replace an unprotected rule or strengthen a protected rule. Attempts to
remove protected effects or gates fail with the exact rule and source.

## Evaluate an action

Create a JSON context with the fields referenced by rule predicates, including
a stable `subject` when waivers may apply. Then run:

```bash
python3 skills/ai-sdlc-policy/scripts/policy.py . \
  --explain change.apply \
  --context policy-context.json \
  --profile regulated \
  --as-of 2026-07-19T12:00:00Z \
  --format markdown
```

`deny` blocks the action. `require` means every returned gate must be satisfied
by the owning workflow. `allow` applies only to the exact action and context
fingerprint. Unknown actions deny by default.

## Use a waiver

A waiver names one waivable rule, action pattern, subject, exact context
constraints, owner, approver, accepted decision, reason, issue time, and expiry.

```bash
python3 skills/ai-sdlc-policy/scripts/policy.py . \
  --explain change.apply \
  --context policy-context.json \
  --profile high-assurance \
  --waiver waivers/change-review.json \
  --as-of 2026-07-19T12:00:00Z
```

Inspect the waiver row in the decision. `expired`, `subject-mismatch`,
`constraint-mismatch`, and `rule-not-waivable` records are rejected and leave
the original rule effective.
