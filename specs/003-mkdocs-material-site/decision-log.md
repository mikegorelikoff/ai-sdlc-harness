---
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "003-mkdocs-material-site"
  artifact: "decision-log.md"
  path: "specs/003-mkdocs-material-site/decision-log.md"
  workspace: "implementation"
  skill: "ai-sdlc-sdd"
  flow_mode: "quick"
  state_file: "specs/003-mkdocs-material-site/_ai_sdlc/state.toon"
  decision_log: "specs/003-mkdocs-material-site/decision-log.md"
  status: "draft"
  owner: "TBD"
  created_at: "2026-07-19"
  updated_at: "2026-07-19"
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
| DEC-001 | 2026-07-19 | accepted | Dev | Replace the custom Jekyll shell with MkDocs Material 9.7.7 and generated Markdown catalogs | User rejected the current visual quality; official Material guidance provides maintained responsive navigation, client-side search, palette controls, and GitHub Pages publishing | Keep custom Jekyll; adopt another theme; migrate to Material; selected Material | mkdocs.yml; requirements-docs.txt; docs/; .github/workflows/pages.yml; validators | AC-001 through AC-008; TC-001 through TC-008; T001 |
| DEC-002 | 2026-07-19 | accepted | Dev | Reuse clean main as the branch base and record branching as a quick-flow predecessor skip | The repository has no dev branch; feature/003-mkdocs-material-site was created from synchronized main before implementation | Block for dev creation; branch from main; selected main | feature/003-mkdocs-material-site; state.toon | T001; validation handoff |
| DEC-003 | 2026-07-19 | accepted | Dev | Use focused diff review plus complete docs and compatibility gates before commit | Review found and fixed missing workflow triggers for mkdocs.yml and requirements-docs.txt; no unrelated files or remaining high-severity findings were found | Add separate review stage; focused review; selected focused review | workflow; config; docs scripts; validation.md | T001; AC-007; AC-008; commit readiness passed |
