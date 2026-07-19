---
title: Release 1.1 audit
description: Exact task-to-commit mapping and release evidence for the executable delivery control plane.
---

# Release 1.1 audit

The program uses one focused commit for each T-ID. The compatibility gate reads
the contiguous history after `v1.0.0` and compares these subjects with the
versioned baseline. The earlier `cb35fcc` Material documentation migration is a
site prerequisite, not a control-plane task.

| Task | Commit | Subject |
| --- | --- | --- |
| T001 | `99003ae` | `docs(roadmap): define executable delivery control plane` |
| T002 | `654790c` | `feat(change-set): add isolated proposal workspaces` |
| T003 | `196c3d5` | `feat(change-set): validate semantic requirement deltas` |
| T004 | `883d65e` | `feat(change-set): preview canonical specification changes` |
| T005 | `b04a887` | `feat(change-set): apply and archive approved changes` |
| T006 | `8cb3b3b` | `feat(traceability): add repository delivery graph` |
| T007 | `e187d2b` | `feat(evidence): add freshness-aware evidence ledger` |
| T008 | `46f929e` | `feat(policy): add protected policy evaluation` |
| T009 | `b25d4b9` | `feat(context): add bounded task context packs` |
| T010 | `1439226` | `feat(runtime): add resumable TOON-first control plane` |
| T011 | `193277f` | `feat(workflow): add declarative gated wave planning` |
| T012 | `916c833` | `feat(adapter): add portable host capability negotiation` |
| T013 | `fc7251b` | `feat(doctor): add safe installation upgrade planning` |
| T014 | `3959d7c` | `feat(trust): add verified packages and private metrics` |
| T015 | release commit | `chore(release): validate control plane v1.1.0` |

T015 is referenced by its immutable expected subject because a commit cannot
embed its own final hash. After the commit exists, the compatibility gate
requires it at the exact final position and no pending-task exemption is used.

Release validation covers every skill test, schema and migration fixtures,
compatibility and commit history, generated documentation, strict Material
build, rendered-link checks, SDD gates, prohibited-name search, and Git
whitespace validation. See [Validate a release](../how-to/validate-release.md)
for the executable commands.
