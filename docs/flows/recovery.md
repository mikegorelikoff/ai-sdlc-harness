---
title: Recovery and learning flow
description: Reopen stale work safely, recover interrupted execution, and turn observations into governed improvement proposals.
---

# Recovery and learning flow

AI-assisted delivery is not linear. Requirements change, evidence expires,
validation fails, writes are interrupted, agents lose sessions, and production
teaches the team something new. Recovery preserves authority instead of hiding
those events.

## Choose the recovery owner

| Signal | First capability | Accountable owner | Safe result |
| --- | --- | --- | --- |
| Requirement/decision changed | Change impact or isolated change set | Product/BA/Delivery | Affected artifacts and reopen sequence, then approved apply. |
| Artifact changed after evidence | Evidence ledger / delivery graph | QA/Delivery/Dev | Stale chain and fresh-only coverage; rerun producing work. |
| Runtime interrupted | Runtime resume | Dev/Delivery | Journal replay, repaired projection, same ready/running task. |
| State and artifact disagree | State/status diagnostics | Artifact owner | Validate authoritative artifact, then repair derived state/index. |
| Legacy and canonical paths diverge | Migration check | Maintainer/owner | Explicit comparison and decision; no automatic overwrite. |
| Validation or review fails | Validation/review owner | Dev/QA/Security | Failed claim remains open; smallest fix and exact rerun. |
| Process problem observed | Retrospective | Delivery/team owner | Observation separated from proposal and policy decision. |

## Recovery algorithm

1. Stop mutation and preserve current bytes, journal, status, and command output.
2. Identify the authoritative artifact or accepted decision.
3. Rebuild or validate derived graph, index, state, context, or preview.
4. Compare fingerprints and find the earliest stale or contradictory evidence.
5. Ask the accountable owner for any material decision.
6. Repair the smallest derived or implementation surface.
7. Rerun the exact gate that failed, then downstream dependent gates.
8. Record the result and handoff; do not erase the incident trail.

## What not to do

- Do not delete a failing test to make validation green.
- Do not edit generated state to contradict the journal or artifact.
- Do not overwrite divergent legacy/canonical files by timestamp.
- Do not create an unbounded waiver or weaken protected policy.
- Do not rerun an idempotent task as new work after a session interruption.
- Do not convert an observation directly into team policy without an owner and
  accepted decision.

## Learning loop

Retrospectives capture what happened, evidence, impact, and candidate
improvements. Proposals may change a skill, policy, workflow, test suite, or
ownership model only after review. Metrics help find patterns; qualitative
context explains them. Neither substitutes for accountable adoption decisions.

For symptom-level commands, use the operational troubleshooting runbook when it
is introduced in the adoption and operations section.
