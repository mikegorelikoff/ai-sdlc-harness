# Handoff Checklist

Review whether:

- actors are clear and consistently used;
- stories link to real outcomes and business value;
- acceptance criteria are testable;
- workflows cover the main happy path and material edge cases;
- business rules are explicit;
- spec sections agree with story intent;
- dependencies and owners are visible;
- assumptions and open questions are clearly separated;
- rollout or operational constraints that affect delivery are captured;
- contradictions remain between upstream package, stories, and spec.

## Readiness Scale

- 1-3: Not ready for delivery planning
- 4-6: Direction exists, but major blockers remain
- 7-8: Good enough for delivery alignment with some follow-up
- 9-10: Strong enough for engineering and cross-functional handoff

## Final Review Output

Explain:

- why the score was given;
- what is strong;
- what is weak;
- what is still blocking;
- what should happen before implementation starts.

## When To Load This Reference

Load this before handing refined work to implementation, QA, design, or delivery
coordination. It is a final consistency check across stories, spec, rules,
dependencies, assumptions, and decisions.

## Handoff Evidence Matrix

| Area | Evidence | Ready? | Gap | Action |
|---|---|---|---|---|
| Actors | roles and permissions |  |  |  |
| Stories | outcome-oriented stories |  |  |  |
| Acceptance | testable ACs |  |  |  |
| Workflows | happy/edge/failure paths |  |  |  |
| Rules | business/domain invariants |  |  |  |
| Dependencies | owners and blockers |  |  |  |
| Decisions | decision-log coverage |  |  |  |
| QA | test strategy or scenarios |  |  |  |

## Quick Flow Guidance

In `--quick-flow`, produce the readiness score and top blockers quickly. Do not
stall on minor polish; focus on whether delivery can move safely.

## Full Flow Guidance

In `--full-flow`, inspect upstream and downstream artifacts and verify
traceability. Do not mark ready if decisions, acceptance criteria, or blockers
are missing.

## Decision Log Guidance

Confirm that decision-log rows exist for material assumptions, scope cuts,
rule choices, and unresolved issues accepted into delivery.

## Readiness Verdicts

Use one of:

- Ready for implementation.
- Ready with explicit follow-ups.
- Needs delivery refinement.
- Needs product decision.
- Not ready.

Always include reason, evidence, and next action.
