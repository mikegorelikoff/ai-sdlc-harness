---
title: Validate a release
description: Combine focused change checks with compatibility, documentation, and release-contract evidence.
---

## Start from changed risk

Use `ai-sdlc-validation` to select deterministic checks for the changed packages, contracts, schemas, workflows, and documentation. Run focused tests before broad suites so failures remain attributable.

## Protect public contracts

Run compatibility validation for stable skill names, flow flags, artifact routes, configuration schemas, module API ranges, and required commit audit rules. An additive release should not require undocumented migration.

```bash
python3 skills/_shared/ai_sdlc_compatibility.py --git-base v1.1.0 --format toon
python3 docs/scripts/build_catalog.py --check
python3 docs/scripts/validate_docs.py
python3 docs/tests/test_docs.py
UV_CACHE_DIR=/tmp/ai-sdlc-uv-cache uv run --offline --with-requirements requirements-docs.txt mkdocs build --strict
python3 docs/scripts/validate_rendered.py
```

Before the T007 release commit exists, add `--allow-pending-last` to the
compatibility command. Remove it after committing so the exact T001–T007
sequence occupies the complete `v1.1.0..HEAD` range; an extra, missing, or
duplicate task commit fails the audit. The baseline explicitly permits no
unreviewed prelude commits.

## Verify delivery evidence

Confirm acceptance criteria map to passing tests, known gaps have owners, security review matches the risk profile, and deployment or installation instructions match the actual release mechanics.

## Record the result

Keep exact commands, outcomes, revision, environment assumptions, skipped checks, and residual risk. “CI green” is a useful signal, but it is not a substitute for knowing which release contracts CI covered.
