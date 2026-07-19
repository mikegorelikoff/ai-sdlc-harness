---
title: Resume a delivery run
description: Start bounded task execution, record outcomes, and recover safely from an interrupted state projection.
---

# Resume a delivery run

Create an `ai-sdlc-run-plan/v1` file with unique tasks, dependencies, input
fingerprints, maximum attempts, commit-boundary flags, and positive step,
failure, and token budgets. Start a new run once:

```bash
python3 skills/ai-sdlc-runtime/scripts/runtime.py . \
  --start --run-id delivery-004 --plan run-plan.json --format toon
```

Claim the next dependency-ready task:

```bash
python3 skills/ai-sdlc-runtime/scripts/runtime.py . \
  --next --run-id delivery-004 --format toon
```

Calling `--next` again returns the same running task without another attempt.
Execute it through the owning workflow, then record exact evidence:

```bash
python3 skills/ai-sdlc-runtime/scripts/runtime.py . \
  --record --run-id delivery-004 \
  --task T001 --outcome succeeded \
  --result-fingerprint <sha256> \
  --tokens 420 --commit <commit-sha>
```

Failed tasks retry automatically while attempts and budgets remain. Blocked
tasks require an explicit retry reason after the cause is resolved.

## Recover after interruption

```bash
python3 skills/ai-sdlc-runtime/scripts/runtime.py . \
  --resume --run-id delivery-004 --format toon
```

Resume validates the complete event sequence and hash chain, replays every
transition, and repairs missing or stale `state.json` and `state.toon`
projections. Agents should read complete TOON state; integrations may use exact
JSON recovery state. Resume fails closed if journal history was edited,
reordered, truncated into an invalid transition, or given a conflicting
repeated outcome.
