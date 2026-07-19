---
title: Prepare and release
description: Build a release candidate, prove compatibility and portability, publish versioned evidence, and retain rollback and deprecation paths.
---

# Prepare and release

A release is an accountable publication decision backed by exact repository
evidence. Passing CI is necessary but not sufficient: the maintainer must know
which public contracts, installed paths, migrations, documentation, and
rollback procedures were tested.

## Release inputs

- accepted tasks and one-task/one-commit audit;
- clean target branch and reviewed diff from the previous release;
- version/harness API decision and compatibility baseline;
- migrations, deprecations, known limitations, and rollback;
- package inventory, origin/provenance evidence, and installed portability;
- updated README, public docs, versions, roadmap, and release notes;
- QA, security, compatibility, documentation, and persona review evidence.

## Candidate sequence

1. Freeze scope and record the intended tag/version.
2. Audit commits against completed tasks and affected public contracts.
3. Update source authority, module versions, compatibility baseline, and migration docs.
4. Synchronize installed runtime mirrors and regenerate catalogs.
5. Run focused tests, all shared/per-skill tests, compatibility, installation smoke, SDD gates, docs tests, strict build, and rendered validation.
6. Review package trust, permissions, data behavior, release workflow, and rollback.
7. Ask independent junior, lead, security/QA as appropriate, and adoption-owner readers to review the final surfaces.
8. Create the release commit, tag, and publication only through authorized repository operations.

## Required source-checkout checks

Use the exact commands maintained in [Validate a release](../how-to/validate-release.md).
At minimum, evidence covers:

- `python3 skills/_shared/test_all_skill_scripts.py`;
- `python3 skills/_shared/test_each_skill_tests.py`;
- compatibility against the intended baseline;
- emulated and real pinned installation smoke when network is available;
- generated catalog drift and documentation tests;
- strict MkDocs build and rendered target validation;
- SDD plan/analyze/validate for the release task;
- prohibited-name, secret, whitespace, and dirty-tree audits.

Record environment, revision, command, exit, skipped checks, and why any skip is
acceptable. A network-blocked real installation test remains a blocker or
explicit residual risk; it is not silently replaced by an emulated test.

## Version and API decision

The repository release version describes the delivered capability set. The
harness API protects stable names, flags, routes, schemas, module contracts,
handoffs, and authority. Additive behavior can use a release minor while
preserving the API range. Breaking public behavior needs a planned API-major
decision, migration, compatibility fixtures, support window, and rollback.

## Publication and rollback

Before publication verify the tag target, release notes, package source,
documentation URL, install command, compatibility baseline, and expected Pages
workflow. After publication verify the tag, installation into a fresh consumer
fixture, generated site, and release links.

Rollback options are versioned and non-destructive:

- stop publication before tag/push when candidate evidence fails;
- publish a corrected commit/release rather than rewriting consumed history;
- direct consumers to the last accepted tag and documented install rollback;
- preserve failed artifacts, checks, incidents, and revoked release decisions;
- deprecate or yank only through platform and organizational policy.

## Release handoff

The release owner records result, version/tag, revision, included tasks, checks,
package/install evidence, compatibility, docs URL, migrations, limitations,
deprecations, rollback, incidents, approvers, and next required action. The
agent may assemble it; the release owner accepts publication.
