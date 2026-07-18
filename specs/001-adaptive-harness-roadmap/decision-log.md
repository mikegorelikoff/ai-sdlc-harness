---
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "001-adaptive-harness-roadmap"
  artifact: "decision-log.md"
  path: "specs/001-adaptive-harness-roadmap/decision-log.md"
  workspace: "implementation"
  skill: "ai-sdlc-sdd"
  flow_mode: "quick"
  state_file: "specs/001-adaptive-harness-roadmap/_ai_sdlc/state.toon"
  decision_log: "specs/001-adaptive-harness-roadmap/decision-log.md"
  status: "draft"
  owner: "TBD"
  created_at: "2026-07-18"
  updated_at: "2026-07-18"
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
| DEC-001 | 2026-07-18 | accepted | Product / Dev | Build a navigator-first guidance layer above the existing control plane. | Existing state, indexes, plans, and profiles already contain authoritative routing signals while discoverability is the primary product gap. | Add disconnected skills; copy persona menus; navigator-first guidance layer. | requirements.md; design.md; T002; T003 | AC-001; AC-002; TC-001; TC-002 |
| DEC-002 | 2026-07-18 | accepted | Product / Dev / QA | Base adaptive rigor on risk dimensions and protected minimums rather than story count. | Blast radius, reversibility, ambiguity, security, compliance, dependencies, and novelty better represent delivery risk than backlog size. | Binary quick/full only; story-count tracks; explainable risk profiles. | requirements.md; design.md; T004; T009 | AC-003; AC-004; TC-003; TC-004 |
| DEC-003 | 2026-07-18 | accepted | Dev | Use one program branch from main and one focused commit per task. | The repository has no dev branch and the user explicitly requires one task per commit until roadmap closure. | Create dev branch; branch per task; one program branch with focused commits. | tasks.md; plan.md; plan.toon | AC-014; TC-014 |
