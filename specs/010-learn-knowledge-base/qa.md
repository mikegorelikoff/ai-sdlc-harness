---
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "010-learn-knowledge-base"
  artifact: "qa.md"
  path: "specs/010-learn-knowledge-base/qa.md"
  workspace: "implementation"
  skill: "ai-sdlc-sdd"
  flow_mode: "quick"
  state_file: "specs/010-learn-knowledge-base/_ai_sdlc/state.toon"
  decision_log: "specs/010-learn-knowledge-base/decision-log.md"
  status: "review"
  owner: "Repository-maintainers"
  created_at: "2026-07-21"
  updated_at: "2026-07-21"
  trace_ids: []
  related_artifacts:
    - "specs/010-learn-knowledge-base/decision-log.md"
    - "specs/010-learn-knowledge-base/design.md"
    - "specs/010-learn-knowledge-base/requirements.md"
    - "specs/010-learn-knowledge-base/test-cases.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-sdd"
    - "qa"
    - "review"
    - "learn-curriculum"
---

# QA

## Change Summary
Add a curriculum layer, provenance governance, deterministic depth validation, and entry-point changes without changing runtime contracts.

## Acceptance Scenarios
A beginner selects a level, follows prerequisites, produces exercise evidence, and reaches a real-repository workflow. An experienced user takes a fast lane. A maintainer receives exact token, contract, source, link, and heading failures. A reviewer traces each material idea to a verified record and transformation note.

## Regression Targets
Existing paths, nav-listed pages, generated catalogs, install commands, role mappings, Evidence Council, Quality Lenses, foundation terms, tutorials, operational contracts, strict build, rendered links, compatibility, and smoke.

## Risk Notes
Highest risks are padding, contract duplication, close adaptation, inaccessible long pages, stale pins, brittle YAML parsing, and different reviewer diffs. Freeze the worktree during review and preserve disagreement.

## Validation Commands
python3 docs/scripts/build_catalog.py --check; python3 docs/scripts/validate_docs.py; python3 docs/scripts/learning_tokens.py --config mkdocs.yml --encoding o200k_base --minimum 6000 --maximum 8000; python3 -m unittest discover -s docs/tests -v; mkdocs build --strict; python3 docs/scripts/validate_rendered.py site; python3 skills/_shared/ai_sdlc_compatibility.py --skip-git-audit --format toon; supported documentation installation smoke.

## Manual Checks
Inspect every page for scannability, useful examples and exercises, correct answers, reciprocal links, non-duplicated contracts, international English, accessible tables, authority limits, and original synthesis. Verify same diff and read-only reviewers.

## Signoff
QA evidence recommends readiness but does not approve publication. All applicable commands must pass, blocker and high findings must be corrected, material medium findings resolved or owned, and the repository owner retains final approval.

