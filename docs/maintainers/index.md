---
title: Maintain and contribute
description: Enter the source-checkout workflow for changing skills, shared helpers, modules, contracts, documentation, compatibility, and releases.
---

# Maintain and contribute

Maintainer work happens in a source checkout of this repository. Consumer
repositories contain installed skills and portable runtime mirrors; they are
not the canonical source for harness changes.

## Source-checkout boundary

!!! terminal "Run in terminal — source checkout"

    ```bash
    git clone https://github.com/mikegorelikoff/ai-sdlc-harness.git
    cd ai-sdlc-harness
    git status --short
    python3 skills/_shared/ai_sdlc_compatibility.py --skip-git-audit --format toon
    ```

Do not copy an installed `.agents/skills` mirror back into this repository.
Edit canonical `skills/_shared` helpers and resynchronize installed runtime
copies through the packaging helper.

## Choose the maintainer path

- [Extend a skill or module](extend.md) for capability, helper, reference, schema, test, catalog, or compatibility work.
- [Prepare a release](release.md) for versioning, migration, package trust, documentation, deprecation, rollback, and release evidence.
- [Validate a release](../how-to/validate-release.md) for the command-level gate set.
- [Script catalog](../reference/scripts.md) for every canonical helper, validation runner, packaging helper, and mirror.

## Change discipline

1. Start from a concrete user or maintainer problem.
2. Use SDD for medium/large behavior, schema, API, architecture, or integration changes.
3. Create or verify a task branch before implementation.
4. Preserve backward compatibility or provide an explicit migration and version decision.
5. Update authority first: skill/reference/schema/source helper, then derived runtime/catalog/docs.
6. Add focused positive and negative tests.
7. Validate the changed surface, compatibility, docs, and installed portability.
8. Keep one bounded task in one auditable commit.

## Review expectations

A reviewer checks user value, source authority, data representation, permissions,
failure behavior, portability, compatibility, tests, documentation, deprecation,
and rollback. Generated files must be reviewed with their canonical source.

No maintainer tool grants release, tag, push, merge, or publication authority.
Those actions follow repository ownership and release policy.
