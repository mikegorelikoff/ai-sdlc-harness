---
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "009-operational-feedback-hardening"
  artifact: "decision-log.md"
  path: "specs/009-operational-feedback-hardening/decision-log.md"
  workspace: "implementation"
  skill: "ai-sdlc-sdd"
  flow_mode: "quick"
  state_file: "specs/009-operational-feedback-hardening/_ai_sdlc/state.toon"
  decision_log: "specs/009-operational-feedback-hardening/decision-log.md"
  status: "review"
  owner: "Repository-maintainers"
  created_at: "2026-07-21"
  updated_at: "2026-07-21"
  trace_ids: ["DEC-001", "DEC-002", "DEC-003"]
  related_artifacts: ["specs/009-operational-feedback-hardening/requirements.md", "specs/009-operational-feedback-hardening/design.md"]
  validation: []
  metatags: ["ai-sdlc", "implementation", "ai-sdlc-sdd", "decision-log", "review", "operational-feedback"]
---

# Decision Log

| ID | Date | Status | Owner | Decision | Evidence | Alternatives | Affected artifacts | Trace |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| DEC-001 | 2026-07-21 | accepted | Repository-maintainers | Discover skills from the executing packaged root plus repository-local roots, without scanning arbitrary home directories. | Navigator baseline implementation and global-install field report. | Home-directory scan; local-only discovery. | navigate.py; navigator tests and docs | AC-001; AC-002 |
| DEC-002 | 2026-07-21 | accepted | Repository-maintainers | Integrate external specification repositories through explicit reviewed snapshots with portable provenance. | Repository-bounded context model and field report that external Markdown was invisible. | Transparent absolute-path indexing; symlink; mandatory submodule. | project-context helper; operations guide | AC-005; AC-006 |
| DEC-003 | 2026-07-21 | accepted | Repository-maintainers | Keep cleanup review-driven and distinguish optional direct invocation from mandatory lifecycle dependencies. | Ownership ambiguity and destructive shared-directory incident in field notes. | Automatic removal by name; mandatory navigator for every action; arbitrary skill order. | install/update/workflow/security guidance | AC-003; AC-004; AC-006 |
