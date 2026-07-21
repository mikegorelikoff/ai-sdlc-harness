---
title: Test and validation report
description: Baseline, focused correction, installation, documentation, security, and regression evidence.
---

# Test and validation report

## Baseline

| Check | Result |
| --- | --- |
| Aggregate skill contract tests | PASS — 25 |
| Per-skill wrapper | PASS |
| Compatibility with Git audit skipped | PASS — 44 skills, 5 modules |
| Documentation unit tests | PASS — 17 |
| Health fixture | PASS — 2 |
| Catalog/source docs | PASS — 44 skills, 5 modules, 106 scripts; 131 public pages |
| Strict MkDocs build/render | PASS — baseline 132 HTML, 20,040 local targets |
| `test_modules.py` | **FAIL** — stale core 1.10.0 expectation |
| `test_compatibility.py` | **FAIL** — legitimate post-release maintenance rejected |
| Documented release audit | **FAIL** |
| Empty-cache `uv --offline` first build | Expected **FAIL**, previously undocumented |
| Fabricated `exit 99` described as PASS | Structural SDD gates incorrectly PASS |

The failing shared tests were absent from CI, proving the advertised aggregate
was incomplete.

## Installation and workflows

- Clean project-scoped real-CLI install: PASS after approved npm/GitHub network
  access; 44 skills; expected host-specific paths; navigator and SDD help PASS.
- Navigator quick-flow in disposable consumer: PASS, valid read-only TOON.
- Repeated install: PASS without duplicate skill inventory.
- Remove: CLI PASS but stale lock/empty directories observed and documented.
- Runnable health fixture baseline and final regression: two tests PASS. The
  clean install smoke separately covers installed SDD gates and commit
  readiness; it does not claim to automate every human/review step in the
  first-feature tutorial.

## Focused correction evidence

| Correction | Evidence |
| --- | --- |
| Context secret exclusion | 13 context-engine and 4 project-context tests PASS, including vendor key, bearer, authenticated URL, private-key fixtures |
| Instruction authority | Arbitrary `docs/*.instructions.md` remains `evidence_only` |
| Change approval limitation | Four change-apply tests PASS; result exposes unauthenticated identity status |
| Shared test discovery | CI now runs `unittest discover` over every shared `test*.py`; per-skill runner remains |
| Module expectation | Core version test updated to 1.11.0 |
| Release sequence | Unit cases allow later maintenance but reject interleaving/duplication |
| Dependency integrity | 29-package `requirements-docs.lock` generated with hashes after approved network resolution |
| CI supply chain | Every referenced Action pinned to a resolved full SHA; Dependabot added |
| Documentation accessibility | Render validator requires one H1 and image alt attributes |

## Final regression commands

These commands define the final local gate and must all pass on the final diff:

```bash
PYTHONPYCACHEPREFIX=/tmp/ai-sdlc-pyc python3 -m compileall -q skills docs/scripts
PYTHONPYCACHEPREFIX=/tmp/ai-sdlc-pyc python3 -m unittest discover -s skills/_shared -p 'test*.py' -v
PYTHONPYCACHEPREFIX=/tmp/ai-sdlc-pyc python3 skills/_shared/test_each_skill_tests.py
PYTHONPYCACHEPREFIX=/tmp/ai-sdlc-pyc python3 skills/_shared/ai_sdlc_compatibility.py --git-base v1.1.0 --format toon
PYTHONPYCACHEPREFIX=/tmp/ai-sdlc-pyc python3 docs/scripts/build_catalog.py --check
PYTHONPYCACHEPREFIX=/tmp/ai-sdlc-pyc python3 docs/scripts/validate_docs.py
PYTHONPYCACHEPREFIX=/tmp/ai-sdlc-pyc python3 -m unittest discover -s docs/tests -v
PYTHONPYCACHEPREFIX=/tmp/ai-sdlc-pyc python3 -m unittest discover -s examples/onboarding-health-service -v
UV_CACHE_DIR=/tmp/ai-sdlc-uv-cache uv run --offline --with-requirements requirements-docs.lock mkdocs build --strict
PYTHONPYCACHEPREFIX=/tmp/ai-sdlc-pyc python3 docs/scripts/validate_rendered.py site
git diff --check
```

Remote-only evidence remains required for Python 3.10/3.13 matrix status,
branch protection, and Pages deployment.

## Final local regression result

All commands in the final gate passed on the corrected tree on 2026-07-21:

- aggregate skill contract suite: 29 passed;
- complete shared discovery: 97 passed after its two detected compatibility and
  receipt-fixture regressions were corrected, then rerun successfully;
- every per-skill test file: passed, including 10 validation-runner, 7
  controlled-apply, 13 runtime, 6 policy, and 3 package-trust cases;
- documentation unit suite: 18 passed;
- generated catalog/source validation: 166 public pages, 44 skills, 5 modules,
  115 scripts;
- installed-runtime synchronization: 20 canonical helpers;
- strict MkDocs/rendered validation: 167 HTML pages and 31,172 local targets;
- emulated installed workflow: passed;
- clean synthetic candidate, real Skills CLI 1.5.19, `--agent codex`: passed the
  complete installed SDD and commit-readiness workflow;
- immutable `v1.2.0` commit `7f36bdbad73e1d73dd8ea2185f8b88c88c8f2dc2`:
  reproduced the exact expected `.agents/specs/001-runtime-smoke/requirements.md`
  defect;
- repository trash, broken-symlink, high-confidence secret, machine-local path,
  runtime-mirror, and `git diff --check` scans: passed.
- deliberate health failure/recovery: the enabled probe failed exactly `404 !=
  200`; removing only the disposable probe restored the trusted two-test suite
  to PASS.

The real CLI checks required approved npm/GitHub network access. The synthetic
candidate commit is local audit evidence, not a release or provenance claim.
Source and rendered validators intentionally do not crawl arbitrary HTTP(S)
targets. Critical primary-source URLs were reviewed during research, but
continuous external-link availability is an accepted documentation-owner
limitation because remote availability, authentication, and rate limits are not
deterministic repository properties.
