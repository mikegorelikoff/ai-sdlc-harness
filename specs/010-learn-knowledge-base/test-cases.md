---
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "010-learn-knowledge-base"
  artifact: "test-cases.md"
  path: "specs/010-learn-knowledge-base/test-cases.md"
  workspace: "implementation"
  skill: "ai-sdlc-sdd"
  flow_mode: "quick"
  state_file: "specs/010-learn-knowledge-base/_ai_sdlc/state.toon"
  decision_log: "specs/010-learn-knowledge-base/decision-log.md"
  status: "review"
  owner: "Repository-maintainers"
  created_at: "2026-07-21"
  updated_at: "2026-07-21"
  trace_ids:
    - "TC-001"
    - "TC-002"
    - "TC-003"
    - "TC-004"
    - "TC-005"
    - "TC-006"
    - "TC-007"
    - "TC-008"
    - "TC-009"
    - "TC-010"
    - "TC-011"
    - "TC-012"
    - "TC-013"
    - "TC-014"
    - "TC-015"
    - "TC-016"
    - "TC-017"
    - "TC-018"
    - "TC-019"
    - "TC-020"
    - "TC-021"
    - "TC-022"
    - "TC-023"
    - "TC-024"
    - "TC-025"
    - "TC-026"
    - "TC-027"
    - "TC-028"
    - "TC-029"
    - "TC-030"
    - "TC-031"
  related_artifacts:
    - "specs/010-learn-knowledge-base/decision-log.md"
    - "specs/010-learn-knowledge-base/design.md"
    - "specs/010-learn-knowledge-base/requirements.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-sdd"
    - "test-cases"
    - "review"
    - "learn-curriculum"
---

# Test Cases

## Scope
Validate Learn navigation, normalized token measurement, page contract, curriculum order, source provenance, canonical links, accessibility structure, build output, existing behavior, installation compatibility, and review closure.

## Scenario Matrix
TC-001 [AC-002, AC-006] reject 5999 tokens.
TC-002 [AC-002, AC-006] accept 6000 tokens.
TC-003 [AC-002, AC-006] accept a middle token count.
TC-004 [AC-002, AC-006] accept 8000 tokens.
TC-005 [AC-002, AC-006] reject 8001 tokens.
TC-006 [AC-002, AC-006] exclude YAML front matter.
TC-007 [AC-002, AC-006] exclude non-rendered maintainer comments.
TC-008 [AC-002, AC-006] include code blocks.
TC-009 [AC-002, AC-006] tokenize Unicode.
TC-010 [AC-002, AC-006] reject malformed UTF-8.
TC-011 [AC-005, AC-006] reject unknown sources.
TC-012 [AC-005, AC-006] reject missing Git pins.
TC-013 [AC-005, AC-006] reject missing review dates.
TC-014 [AC-005, AC-006] reject reference-only sources declared adapted.
TC-015 [AC-005, AC-006] reject missing or unstructured visible source notes.
TC-016 [AC-001, AC-002, AC-006] reject a missing Learn page.
TC-017 [AC-001, AC-006] reject duplicate navigation entries.
TC-018 [AC-001, AC-002, AC-006] reject incorrect level order.
TC-019 [AC-002, AC-003, AC-006] reject a missing role path.
TC-020 [AC-001, AC-002, AC-006, AC-007] reject unresolved links or anchors.
TC-021 [AC-002, AC-006] reject heading-level skips.
TC-022 [AC-001, AC-002, AC-003, AC-004, AC-007] accept all ten pages and six-section navigation.
TC-023 [AC-002, AC-006] retain visible HTML-comment syntax inside fenced code.
TC-024 [AC-005, AC-006] reject source-ID-only visible notes.
TC-025 [AC-005, AC-006] reject visible metadata that differs from the registry.
TC-026 [AC-005, AC-006] reject directory shorthand in source destinations.
TC-027 [AC-005, AC-006] reject reverse registry/page destination drift.
TC-028 [AC-003, AC-006] reject a missing tracked Learn exercise fixture.
TC-029 [AC-008] verify nine read-only initial reports, parent corrections, and four required rechecks in the durable review record.
TC-030 [AC-009] require every prescribed validation command to finish successfully or retain its exact blocker.
TC-031 [AC-010] verify the final diff preserves unrelated work, excludes generated `site/`, and contains no task-created commit.

## Layer Mapping
Unit tests cover parsing, normalization, bounds, source schema and modes, headings, sections, and nav order. validate_docs covers repository constraints. MkDocs and rendered validation cover configuration and targets. Compatibility and smoke cover packaging. Human review covers usefulness, depth, pedagogy, provenance, security, and accessibility.

## Automation Plan
Use unittest under docs/tests. Keep learning_tokens.py reusable and runnable. Make structure and source validation callable from validate_docs.py. Pin dependencies with hashes. Add a standalone token step to CI.

## Open Gaps
Automation cannot prove originality, lack of close paraphrase, pedagogical usefulness, or organizational approval. Provenance and anti-padding reviewers add evidence; authority remains human.
