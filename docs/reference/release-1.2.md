---
title: Release 1.2
description: Release evidence and migration notes for the guided onboarding and portable-runtime release.
---

# Release 1.2

`v1.2.0` is the tagged release for the guided onboarding program. It includes
the installable shared runtime, canonical Material onboarding, complete skill
and script guides, adoption/governance operations, and the final independent
persona/release audit.

## Release contract

| Item | Evidence |
| --- | --- |
| API compatibility | `1.0.0`; stable skill names, flags, routes, and module IDs remain additive. |
| Installer source | `https://github.com/mikegorelikoff/ai-sdlc-harness/tree/v1.2.0` with `DISABLE_TELEMETRY=1`. |
| Inventory | 44 skills, 5 modules, 106 scripts, 17 installed-runtime mirrors. |
| Documentation | Strict Material build, rendered target validation, canonical `docs/` navigation, and role/adoption/operations paths. |
| Runtime | Pinned CLI smoke verifies shared-runtime imports and a disposable SDD scaffold from the exact tagged source. |
| Governance | Human authority, data/telemetry, package trust, permissions, retention, incident, rollout, and limitations are documented. |

## One-task/one-commit audit

| Task | Commit | Subject |
| --- | --- | --- |
| T001 | `d51b165` | `docs(roadmap): define guided onboarding program` |
| T002 | `402cf15` | `docs(onboarding): add beginner foundations and install path` |
| T003 | `8fbd1b1` | `fix(install): package portable shared runtime` |
| T004 | `2687ebf` | `docs(workflows): add runnable lifecycle journeys` |
| T005 | `305d609` | `docs(reference): document every skill and script` |
| T006 | `9d0ec87` | `docs(operations): add adoption and governance guides` |
| T007 | pending release commit | `docs(release): close guided onboarding validation` |

T007 is represented by its immutable subject before the self-referential
commit exists. The post-commit compatibility check runs without a pending-last
allowance and verifies the exact `v1.1.0..HEAD` sequence; the `v1.2.0` tag must
resolve to that release commit.

## Upgrade guidance

1. Record the current installed inventory and accepted Git baseline.
2. Review the [tagged installation contract](../how-to/install.md), including
   Node.js `>=22.20.0`, the installer telemetry opt-out, and project scope.
3. Update in a disposable branch; run `list --json`, navigator `--help`, SDD
   helper `--help`, compatibility, and the first-use smoke.
4. Preserve consumer-owned specs, decisions, state, policies, and evidence.
5. Roll back through reviewed Git changes if the accepted baseline or helper
   imports cannot be restored; keep the incident and validation evidence.

The release proves repository and package contracts. It does not prove a
universal productivity, quality, security, compliance, or ROI outcome.
