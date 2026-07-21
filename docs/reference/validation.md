---
title: Validation commands
description: Deterministic repository gates for skills, specifications, modules, configuration, compatibility, and documentation.
---

# Validation commands

Run repository commands from a source checkout. In an installed consumer,
resolve skill commands beneath `.agents/skills/`; source-only
`skills/_shared/` commands have no consumer equivalent unless the installed
shared-runtime skill documents one.

Documentation validation requires the exact versions in
`requirements-docs.lock`, including `tiktoken`. A clean host should run the
documentation commands through the pinned environment:

```bash
UV_CACHE_DIR=/tmp/ai-sdlc-uv-cache uv run \
  --with-requirements requirements-docs.lock \
  python3 docs/scripts/validate_docs.py
```

The first run requires package-index access; a populated cache can use
`--offline`. Running the plain `python3 docs/scripts/validate_docs.py` command
is supported only after that interpreter has the locked documentation
dependencies. If it reports `ModuleNotFoundError: No module named 'tiktoken'`,
do not skip the Learn check: use the pinned `uv run` command or install the
lockfile in an isolated environment. Never substitute a word-count estimate.

```bash
# Repository shared and skill-local tests
python3 -m unittest discover -s skills/_shared -p 'test*.py' -v
python3 skills/_shared/test_each_skill_tests.py

# Release compatibility
python3 skills/_shared/ai_sdlc_compatibility.py --skip-git-audit --format toon

# Active SDD structure and links
python3 skills/ai-sdlc-sdd/scripts/validate_spec.py specs/NNN-feature --quick-flow
python3 skills/ai-sdlc-sdd/scripts/plan_links.py specs/NNN-feature --check --quick-flow

# Documentation catalogs and source
python3 docs/scripts/build_catalog.py --check
python3 docs/scripts/validate_docs.py
```

Use `ai-sdlc-validation` to choose the smallest relevant set. Commands above are contracts, not a requirement to run every suite for every tiny change. Always record exact outcomes and skipped risk.

## Executed validation receipts

`qa.md` commands are planned checks until a process actually runs them. For
full-flow readiness, create and human-review an argv-only plan such as:

```json
{
  "schema": "ai-sdlc-validation-command-plan/v1",
  "commands": [
    {
      "id": "V001",
      "argv": ["python3", "-m", "unittest", "-v"],
      "trace_ids": ["AC-001", "TC-001"]
    }
  ]
}
```

Then execute it through the validation skill's runner:

```bash
python3 skills/ai-sdlc-validation/scripts/run_validation.py \
  --root . --plan specs/NNN-feature/_ai_sdlc/validation-plan.json \
  --output specs/NNN-feature/_ai_sdlc/validation-receipt.json \
  --full-flow

python3 skills/ai-sdlc-validation/scripts/run_validation.py \
  --root . --plan specs/NNN-feature/_ai_sdlc/validation-plan.json \
  --output specs/NNN-feature/_ai_sdlc/validation-receipt.json \
  --verify --full-flow
```

The runner does not use a shell. It rejects executable paths, Python `-c`,
unapproved Python modules, mutating Git subcommands, `npx`, `uv`, `make`, and
non-test Go/npm command families. Repository Python scripts, tests, npm scripts,
and test plugins can still execute repository-controlled code, so this runner
is **not a sandbox or permission boundary**. Review the complete argv and run it
under normal least-privilege host policy.

The canonical plan must be named `validation-plan.json` beside the receipt. The
receipt binds its repository-relative path and SHA-256 digest. The runner
streams process output into bounded digests (10 MB total by default), records
byte counts, and terminates the process group if the limit is exceeded.

The receipt stores actual exit codes and output digests rather than potentially
sensitive output. Its fingerprint detects accidental edits and staleness but is
forgeable by anyone who can rewrite the receipt; the record explicitly says
`local-structural-not-authenticated`. Any non-zero command, changed plan, or
later revision/diff change makes verification fail. A missing Git work tree or
valid `HEAD` fails closed. Require protected CI logs or
another authenticated external system for independent execution proof. A
current local receipt does not prove requirement correctness or human approval.

The runner rejects `--complete-state` because state completion before command
execution could reuse stale evidence. Finalize `validation.md` **before** the
final runner execution, execute and verify the receipt, then run the installed
shared runtime's `state_machine.py complete` with `--artifacts
specs/NNN-feature/validation.md`. That completion
gate independently revalidates command exits, trace IDs, trust disclosure,
receipt fingerprint, revision, and current workspace fingerprint.

The fingerprint excludes only the receipt itself, canonical `state.toon`,
workspace specs indexes, and downstream code-review, security-review, and
commit evidence that is derived after validation. This keeps the receipt
current across lifecycle recording. A change to product/documentation source,
requirements, tests, tasks, plans, `validation.md`, or the validation command
plan still makes the receipt stale and requires a new run.
