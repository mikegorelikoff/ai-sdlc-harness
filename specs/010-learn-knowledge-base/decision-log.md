---
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "010-learn-knowledge-base"
  artifact: "decision-log.md"
  path: "specs/010-learn-knowledge-base/decision-log.md"
  workspace: "implementation"
  skill: "ai-sdlc-sdd"
  flow_mode: "quick"
  state_file: "specs/010-learn-knowledge-base/_ai_sdlc/state.toon"
  decision_log: "specs/010-learn-knowledge-base/decision-log.md"
  status: "draft"
  owner: "Repository-maintainers"
  created_at: "2026-07-21"
  updated_at: "2026-07-21"
  trace_ids: []
  related_artifacts: []
  validation: []
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-sdd"
    - "decision-log"
    - "draft"
    - "learn-curriculum"
---

# Decision Log

| ID | Date | Status | Owner | Decision | Context/Evidence | Options Considered | Affected Artifacts | Validation/Trace Links |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| DEC-001 | 2026-07-21 | accepted | Repository-maintainers | Keep ten substantial Learn pages at stable paths and preserve operational pages as canonical owners. | User architecture constraints and current six-section site. | Many narrow lessons; move public pages; duplicate contracts in Learn. | mkdocs.yml; docs/start.md; docs/learn; canonical pages | AC-001; AC-002; AC-004 |
| DEC-002 | 2026-07-21 | accepted | Repository-maintainers | Adopt ideas rather than wording, classify every source, pin Git sources, replace source examples with original harness exercises, and keep reference-only sources non-adapted. | User provenance rule and repository authority boundary. | Copy licensed text; generic bibliography; omit external research. | content_sources.yml; Learn pages; source governance | AC-003; AC-005 |
| DEC-003 | 2026-07-21 | accepted | Repository-maintainers | Make mkdocs Learn navigation the token inventory and integrate exact o200k_base, structure, source, link, and heading checks into existing validation. | Deterministic 6000 to 8000 requirement and current validator architecture. | Word-count approximation; manual-only checks; unrelated validation framework. | learning validators; tests; dependencies; CI | AC-002; AC-006; AC-009 |
