---
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "009-operational-feedback-hardening"
  artifact: "test-cases.md"
  path: "specs/009-operational-feedback-hardening/test-cases.md"
  workspace: "implementation"
  skill: "ai-sdlc-sdd"
  flow_mode: "quick"
  state_file: "specs/009-operational-feedback-hardening/_ai_sdlc/state.toon"
  decision_log: "specs/009-operational-feedback-hardening/decision-log.md"
  status: "review"
  owner: "Repository-maintainers"
  created_at: "2026-07-21"
  updated_at: "2026-07-21"
  trace_ids: ["AC-001", "AC-002", "AC-003", "AC-004", "AC-005", "AC-006", "AC-007"]
  related_artifacts: ["specs/009-operational-feedback-hardening/requirements.md", "specs/009-operational-feedback-hardening/design.md"]
  validation: []
  metatags: ["ai-sdlc", "implementation", "ai-sdlc-sdd", "test-cases", "review", "operational-feedback"]
---

# Test Cases

## Scope
Navigator roots, external snapshot behavior and abuse cases, documentation contracts, generated references, and full regression.

## Scenario Matrix

## Functional Cases
- TC-001 (AC-001, AC-002): execute a copied navigator from a temporary packaged skill root against a separate repository; sibling skills are discovered and the packaged root is reported.
- TC-002 (AC-001): project and source roots still work and duplicate skill names are counted once.
- TC-003 (AC-005): snapshot two safe external Markdown files; verify deterministic destinations, portable manifest, hashes, and `--check` success.
- TC-004 (AC-005): change a source after snapshot; `--check` exits non-zero and identifies drift without modifying outputs.
- TC-005 (AC-005): reject source path escape, symlink, non-Markdown input, destination collision, oversized content, and credential-shaped content before any write.
- TC-006 (AC-003, AC-004, AC-006): documentation validator and link checks find every new canonical page and command contract.

## Regression Cases
- TC-007 (AC-007): all navigator and project-context tests pass.
- TC-008 (AC-007): all shared tests, every skill test suite, installed-runtime mirror check, compatibility, documentation validation, strict site build, and `git diff --check` pass.

## Manual Cases
- TC-009 (AC-003): compare documented local/global install tables with clean Skills CLI behavior and confirm that broad global target failures are explained as host-target failures, not broken skill packages.
- TC-010 (AC-006): trace each harness-relevant meeting note to a disposition and canonical control or explicit adopter-owned limitation.

## Layer Mapping
Unit: discovery, validation, hashes, drift. Integration: packaged navigator and checkout-to-consumer snapshot. Documentation: links, commands, and dispositions. Regression: shared, skill, compatibility, and site gates.

## Automation Plan
Automate TC-001 through TC-008. TC-009 and TC-010 remain evidence reviews because external hosts and meeting interpretation are not local unit-test contracts.

## Open Gaps
Live Cursor, Claude, Eve, PromptScript, Dexter, Elixir, organizational vault, and subscription behavior remain external conformance or governance decisions.
