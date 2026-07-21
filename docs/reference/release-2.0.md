---
title: Release 2.0 candidate
description: Scope, evidence, migration, limitations, and rollback for v2.0.0-rc.1.
---

# Release `v2.0.0-rc.1`

`v2.0.0-rc.1` packages the context-contract major change, the production
readiness hardening program, marketplace security corrections, and operational
feedback fixes accumulated after `v1.2.0`.

## Delivered scope

- Context snapshots and task packs use v3 goal-relevant ranges, authority
  labels, sufficiency states, and targeted reads.
- Harness API and bundled module compatibility move to `2.0.0`.
- All 44 skills include portable runtime support, safer state and filesystem
  boundaries, and security-audited untrusted-evidence handling.
- The installed consumer-root defect from `v1.2.0` is corrected.
- Navigator discovery covers project, source, and packaged/global skill roots.
- Codex global installation avoids the 88 unsupported Eve/PromptScript target
  failures by keeping both skill and agent selection explicit.
- Documentation now includes progressive foundations, role guides, tutorials,
  governance, release operations, external specifications, and field feedback.

## Validation evidence

The candidate passed focused tests, the repository-wide shared and per-skill
suites, compatibility checks, catalog drift checks, documentation tests, strict
MkDocs build, rendered-link validation, source-checkout install smoke, isolated
Codex project/global installation, and a complete installed SDD/commit workflow.
The detailed evidence is recorded in the
[production readiness audit](../audits/2026-07-21-production-readiness/validation-report.md)
and [operational hardening validation](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/v2.0.0-rc.1/specs/009-operational-feedback-hardening/validation.md).

The release tag must resolve to the release commit, the `v1.2.0..HEAD` commit
audit must pass without its pending-last allowance, and remote CI must be
checked after publication.

## Known limitations

- No owner-selected `LICENSE` exists. The tag does not grant use,
  modification, or redistribution rights that are otherwise absent.
- Protected GitHub CI, branch protection, and private security settings are
  external evidence and are not proven by a local run.
- Codex on macOS is the manually validated host. Installer recognition is not
  behavioral certification for other hosts.
- Release evidence is locally generated and not cryptographically authenticated;
  organizations still need protected CI and accountable human approval.

These limitations require prerelease status. They must be resolved or
explicitly accepted by the accountable owner before stable `v2.0.0`.

## Migration and rollback

Read [Migrate to 2.0](../how-to/migrate-2.0.md) before upgrading a v2-only
context consumer. Roll back by reinstalling the last accepted exact revision;
restore harness-owned files only and preserve product artifacts and evidence.
