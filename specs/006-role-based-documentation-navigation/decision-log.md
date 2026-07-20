---
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "006-role-based-documentation-navigation"
  artifact: "decision-log.md"
  path: "specs/006-role-based-documentation-navigation/decision-log.md"
  workspace: "implementation"
  skill: "ai-sdlc-sdd"
  flow_mode: "quick"
  state_file: "specs/006-role-based-documentation-navigation/_ai_sdlc/state.toon"
  decision_log: "specs/006-role-based-documentation-navigation/decision-log.md"
  status: "draft"
  owner: "docs-maintainers"
  created_at: "2026-07-20"
  updated_at: "2026-07-20"
  trace_ids: []
  related_artifacts: []
  validation: []
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-sdd"
    - "decision-log"
    - "draft"
---

# Decision Log

| ID | Date | Status | Owner | Decision | Context/Evidence | Options Considered | Affected Artifacts | Validation/Trace Links |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| DEC-001 | 2026-07-20 | accepted | Documentation maintainers | Consolidate global navigation to six entries, promote Reference to third, and add a generated many-to-many role skill finder with seniority guidance. | Stakeholder feedback plus QA/BA, PM/PO, Dev, VP, and Head of AI Practice persona audits found 13 tabs, Reference at position 12, a 44-card flat catalog, and missing seniority routes. | Keep current IA; exclusive role folders; compact nav plus shared canonical guides (selected). | `mkdocs.yml`; `docs/onboarding/role-paths.md`; `docs/reference/skills-by-role.md`; `docs/scripts/build_catalog.py`; `docs/scripts/validate_docs.py` | AC-001 through AC-010; TC-001 through TC-010 |
| DEC-002 | 2026-07-20 | accepted | Documentation maintainers | Keep seniority and persona combinations as internal review evidence only; remove the public onboarding role-path page and expose only the task-oriented Skills by role reference. | User clarified that roles and seniorities were requested as validation perspectives, not documentation content. | Publish role/seniority paths; publish role skills only (selected). | `docs/reference/skills-by-role.md`; removed `docs/onboarding/role-paths.md`; `mkdocs.yml`; validation tests; SDD artifacts | AC-003 through AC-009; TC-003 through TC-009 |
