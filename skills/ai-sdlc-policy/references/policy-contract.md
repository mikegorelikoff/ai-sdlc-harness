# Policy Resolution, Evaluation, And Waiver Contract

## Layers and protected rules

Layers resolve in fixed `base`, `organization`, `project`, `user` order. Rule
IDs are stable. A later layer may replace an unprotected rule or strengthen a
protected rule. It may not lower effect strictness (`deny > require > allow`),
remove required gates, clear `protected`, or change `waivable` from false to
true. Sparse layers inherit rules; absence never deletes an earlier rule.

Rules declare action patterns, effect, predicates, gates, protection, waiver
eligibility, and human description. Predicates support only `eq`, `in`,
`exists`, `gte`, and `lte` against dot-addressed context fields. Missing or
incomparable values do not match.

## Decisions

Applicable unwaived rules combine with deny-first, require-second, allow-third
precedence. Required gates are the sorted union of matching rules. No matching
rule is `deny` with reason `unknown-action`, so policy cannot open by omission.
Every result includes rule provenance, policy and context fingerprints, reason
codes, and waiver results.

## Waivers

A waiver suppresses exactly one named rule only when that rule is waivable, the
action pattern and subject match, every constraint equals current context, an
owner, approver, decision reference, and reason exist, and `issued_at <= as_of <=
expires_at`. Expired, premature, mismatched, malformed, unknown-rule, and
non-waivable exceptions are rejected and do not weaken the decision.
