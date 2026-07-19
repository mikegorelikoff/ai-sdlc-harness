# Resumable Runtime Contract

## Plans and readiness

A plan is immutable after start. Task IDs are unique, dependencies exist, and
the graph is acyclic. A task is ready only when it is pending, has attempts
remaining, and every dependency succeeded. Ready tasks sort by plan order then
ID. Only one task may be running; repeated selection returns that task without
another attempt or event.

## Journal and recovery

Every transition appends one canonical JSON event with a contiguous sequence,
previous-event fingerprint, and its own fingerprint. The journal is written and
fsynced before exact JSON state and complete agent-facing TOON state are
atomically replaced. Replay validates the hash chain and all transitions.
Missing, corrupt, or stale projections are recoverable from a valid journal;
invalid journal history fails closed.

## Budgets, retries, and stops

Task start consumes one step. Failed outcome consumes one failure; all outcomes
add reported tokens. Retryable failures return to pending. Maximum attempts,
steps, failures, and tokens produce exact stop reasons. Blocked tasks pause with
their recorded reason. A deliberate stop is terminal and preserves its reason.

## Completion and commits

Success requires a 64-character result fingerprint. Tasks marked
`commit_boundary` also require a 7-to-40-character hexadecimal commit identity.
The run completes only when every task succeeded. Repeating an identical success
record is idempotent; conflicting repeated evidence fails.
