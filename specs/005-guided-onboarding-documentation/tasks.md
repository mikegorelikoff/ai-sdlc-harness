---
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "005-guided-onboarding-documentation"
  artifact: "tasks.md"
  path: "specs/005-guided-onboarding-documentation/tasks.md"
  workspace: "implementation"
  skill: "ai-sdlc-sdd"
  flow_mode: "quick"
  state_file: "specs/005-guided-onboarding-documentation/_ai_sdlc/state.toon"
  decision_log: "specs/005-guided-onboarding-documentation/decision-log.md"
  status: "review"
  owner: "TBD"
  created_at: "2026-07-19"
  updated_at: "2026-07-19"
  trace_ids:
    - "AC-001"
    - "AC-002"
    - "AC-003"
    - "AC-004"
    - "AC-005"
    - "AC-006"
    - "AC-007"
    - "AC-008"
    - "AC-009"
    - "AC-010"
    - "AC-011"
    - "AC-012"
    - "AC-013"
    - "AC-014"
    - "AC-015"
    - "AC-016"
    - "AC-017"
    - "AC-018"
  related_artifacts:
    - "specs/005-guided-onboarding-documentation/decision-log.md"
    - "specs/005-guided-onboarding-documentation/design.md"
    - "specs/005-guided-onboarding-documentation/plan.md"
    - "specs/005-guided-onboarding-documentation/qa.md"
    - "specs/005-guided-onboarding-documentation/requirements.md"
    - "specs/005-guided-onboarding-documentation/test-cases.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-sdd"
    - "tasks"
    - "review"
---

# Tasks

## Implementation
- [x] T001. Define the guided onboarding documentation program and persona acceptance gates.
  Output: Complete SDD package, accepted information architecture, persona findings, generated plan/indexes, focused validation, and one planning commit.
  Refs: AC-001, AC-002, AC-014, AC-016, AC-018
- [x] T002. Build the beginner-first foundations and first-use path.
  Output: Canonical product story and naming, AI SDLC/SDD foundations, fit/non-fit, mental model, responsibilities, glossary, canonical install/verification, first 30 minutes, action labels, Home/README/Start integration, navigation, tests, and one focused commit.
  Refs: AC-001, AC-002, AC-003, AC-009, AC-013, AC-017, AC-018
  Depends on: T001
- [x] T003. Make project-scoped skill installation portable and executable.
  Output: Installable shared runtime capability, source-to-runtime synchronization, portable fallback in every dependent helper, module and compatibility registration, fresh skill-only install scaffold smoke test, generated inventory refresh, and one focused commit.
  Refs: AC-003, AC-007, AC-014, AC-015, AC-018
  Depends on: T002
- [x] T004. Publish runnable tutorials and the complete lifecycle flow library.
  Output: Copyable small-change and full-feature walkthroughs, explicit prompts/terminal actions/expected artifacts/checkpoints/recovery, all 18 refinement stages, implementation/control-plane journeys, entry/exit/reopen matrices, decision tree, navigation, tests, and one focused commit.
  Refs: AC-004, AC-005, AC-006, AC-009, AC-012, AC-018
  Depends on: T003
- [x] T005. Generate complete human-facing skill and script documentation.
  Output: Enhanced deterministic catalog generator, inventory-complete per-skill guides, complete in-scope script inventory, coverage manifest, required detail fields, navigation/discovery surfaces, parser/render/coverage tests, and one focused commit.
  Refs: AC-007, AC-008, AC-014, AC-015, AC-018
  Depends on: T004
- [ ] T006. Publish adoption, governance, operations, and maintainer guidance.
  Output: Persona/role paths, pilot playbook, metrics interpretation, operating model, human/agent RACI, trust/governance, maturity/limitations, troubleshooting runbook, contributor/extension path, canonical-source reconciliation, full navigation/index consistency, tests, and one focused commit.
  Refs: AC-002, AC-009, AC-010, AC-011, AC-012, AC-013, AC-014, AC-017, AC-018
  Depends on: T005
- [ ] T007. Close independent persona review and release-quality validation.
  Output: Junior, lead, and VP reread findings, revisions until all return PASS with no P0/P1, complete regression/build/render/compatibility/SDD evidence, exact task-to-commit audit, clean tree, and one focused completion commit.
  Refs: AC-014, AC-015, AC-016, AC-018
  Depends on: T006

## Testing
Each task includes focused source, link, navigation, and content checks for its pages. T003 adds source-to-installed-runtime drift, import, and disposable scaffold smoke tests. T005 adds inventory closure and generator unit tests. T007 runs every documentation, strict build, rendered target, shared skill, compatibility, SDD, prohibited-name, and Git audit gate. Any persona P0/P1 finding reopens the owning task content and must be corrected before T007 completes.

## Documentation
T002 establishes the learning vocabulary and first-use contract. T003 makes the installed helper runtime portable. T004 teaches journeys and exact lifecycle behavior. T005 makes every executable capability discoverable and complete. T006 supports team adoption, governance, recovery, and contribution. T007 reconciles all indexes, cross-links, claims, and reviewer feedback. Public `docs/` is canonical; root guides/concepts must not remain a contradictory onboarding dependency.
