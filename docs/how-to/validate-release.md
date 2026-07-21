---
title: Validate a release
description: Combine focused change checks with compatibility, documentation, and release-contract evidence.
---

## Start from changed risk

This maintainer procedure requires a clone of the harness source repository;
the `skills/_shared` and `docs/scripts` paths do not exist in an installed-only
consumer project.

Use `ai-sdlc-validation` to select deterministic checks for the changed packages, contracts, schemas, workflows, and documentation. Run focused tests before broad suites so failures remain attributable.

## Protect public contracts

Run compatibility validation for stable skill names, flow flags, artifact routes, configuration schemas, module API ranges, and required commit audit rules. An additive release should not require undocumented migration.

First resolve and review the system Git path. It must be absolute and outside
the candidate repository. Then pass that exact path explicitly; do not let the
candidate choose an executable through `PATH`.

```bash
command -v git
python3 skills/_shared/ai_sdlc_compatibility.py \
  --git-executable /absolute/reviewed/path/to/git \
  --git-base v1.1.0 --format toon
python3 docs/scripts/build_catalog.py --check
python3 docs/scripts/validate_docs.py
python3 docs/tests/test_docs.py
UV_CACHE_DIR=/tmp/ai-sdlc-uv-cache uv run --with-requirements requirements-docs.lock mkdocs build --strict
python3 docs/scripts/validate_rendered.py site
```

Before the final roadmap commit exists, add `--allow-pending-last` to the
compatibility command. Remove it after committing. The exact ordered roadmap
sequence must begin at the configured base after any explicitly allowed
prelude; missing, duplicate, reordered, or interleaved task commits fail.
Later maintenance commits are allowed because the release sequence is a
bounded historical contract, not a claim that no work can follow the release.
Use a newer base/baseline for the next release rather than reinterpreting the
old sequence.

The first dependency resolution needs network access. After the uv cache is
populated, repeat with `--offline` to prove the cached build path.

## Verify delivery evidence

Confirm acceptance criteria map to passing tests, known gaps have owners, security review matches the risk profile, and deployment or installation instructions match the actual release mechanics.

## Record the result

Keep exact commands, outcomes, revision, environment assumptions, skipped checks, and residual risk. “CI green” is a useful signal, but it is not a substitute for knowing which release contracts CI covered.
