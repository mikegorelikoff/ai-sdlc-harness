---
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "004-executable-delivery-control-plane"
  artifact: "qa.md"
  path: "specs/004-executable-delivery-control-plane/qa.md"
  workspace: "implementation"
  skill: "ai-sdlc-sdd"
  flow_mode: "quick"
  state_file: "specs/004-executable-delivery-control-plane/_ai_sdlc/state.toon"
  decision_log: "specs/004-executable-delivery-control-plane/decision-log.md"
  status: "approved"
  owner: "QA"
  created_at: "2026-07-19"
  updated_at: "2026-07-19"
  trace_ids: []
  related_artifacts:
    - "specs/004-executable-delivery-control-plane/decision-log.md"
    - "specs/004-executable-delivery-control-plane/design.md"
    - "specs/004-executable-delivery-control-plane/requirements.md"
    - "specs/004-executable-delivery-control-plane/test-cases.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-sdd"
    - "qa"
    - "approved"
---

# QA

## Change Summary
Introduce an additive executable control plane across the existing harness: isolated specification changes, controlled application, lifecycle graph and evidence freshness, versioned policy evaluation, bounded context packs, resumable workflows, host adapters, operational diagnostics, trusted packages, local metrics, and versioned documentation.

## Acceptance Scenarios
QA will exercise a representative feature from proposal through delta preview, approval, canonical apply, archive, graph refresh, context-pack creation, task execution, validation, commit recording, metrics, and upgrade preview. Negative paths cover conflict, stale evidence, expired waiver, denied capability, interruption, cycle, unsafe package, incompatible migration, and partial filesystem failure.

## Regression Targets
Existing 35 skills and 5 module manifests; quick and full flow precedence; state.toon and plan.toon semantics; Markdown artifact authority; decision and evidence ownership; navigator and handoff routes; configuration protection; project context secret exclusions; compatibility checks; generated documentation catalogs; MkDocs build and public navigation.

## Risk Notes
Highest risks are accidental canonical mutation during preview, partial apply, policy weakening, runtime work duplication after resume, context leakage, untrusted workflow execution, graph drift, and oversized complexity. Gates require byte-identity preview tests, staged atomic writes, fail-closed evaluation, idempotency, secret fixtures, declared capabilities, fingerprints, modular packages, and focused per-task commits.

## Validation Commands
- python3 skills/ai-sdlc-sdd/scripts/check_clarify.py specs/004-executable-delivery-control-plane --quick-flow
- python3 skills/ai-sdlc-sdd/scripts/check_checklist.py specs/004-executable-delivery-control-plane --quick-flow
- python3 skills/ai-sdlc-sdd/scripts/plan_links.py specs/004-executable-delivery-control-plane --check --quick-flow
- python3 skills/ai-sdlc-sdd/scripts/analyze_spec.py specs/004-executable-delivery-control-plane --quick-flow
- python3 skills/ai-sdlc-sdd/scripts/validate_spec.py specs/004-executable-delivery-control-plane --quick-flow
- python3 skills/_shared/test_all_skill_scripts.py
- python3 skills/_shared/validate_compatibility.py
- python3 docs/scripts/build_catalog.py --check
- python3 docs/scripts/validate_docs.py
- python3 -m unittest discover -s docs/tests -v
- mkdocs build --strict
- git diff --check

## Manual Checks
Review preview and explain output for clarity, inspect archive recovery evidence, follow one end-to-end graph query, stop and resume a run, review a denied policy decision and valid waiver, inspect a context pack for relevance and exclusions, and verify doctor output gives safe next actions. Confirm each completed T-ID has one focused commit before integration.

## Signoff
Dev owns implementation and focused validation. QA signoff requires every task test to pass before its commit, all program-level suites to pass, no unresolved critical or high findings, deterministic recovery for mutation paths, and a clean one-task-one-commit audit. Security and Delivery own any accepted waiver or external capability exception.
