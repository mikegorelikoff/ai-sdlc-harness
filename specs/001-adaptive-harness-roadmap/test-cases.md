---
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "001-adaptive-harness-roadmap"
  artifact: "test-cases.md"
  path: "specs/001-adaptive-harness-roadmap/test-cases.md"
  workspace: "implementation"
  skill: "ai-sdlc-sdd"
  flow_mode: "quick"
  state_file: "specs/001-adaptive-harness-roadmap/_ai_sdlc/state.toon"
  decision_log: "specs/001-adaptive-harness-roadmap/decision-log.md"
  status: "approved"
  owner: "QA"
  created_at: "2026-07-18"
  updated_at: "2026-07-18"
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
  related_artifacts:
    - "specs/001-adaptive-harness-roadmap/decision-log.md"
    - "specs/001-adaptive-harness-roadmap/design.md"
    - "specs/001-adaptive-harness-roadmap/requirements.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-sdd"
    - "test-cases"
    - "approved"
---

# Test Cases

## Scope
All roadmap acceptance criteria and cross-capability compatibility behavior.

## Scenario Matrix
| ID | Spec ref | Scenario | Setup | Trigger | Verifiable outcome | Layer | Automation |
| --- | --- | --- | --- | --- | --- | --- | --- |
| TC-001 | AC-001 | Navigator ranks next action | Empty and existing fixture repos | Run navigator in Markdown and TOON | Required and optional actions include reason, command, output, and blockers | integration | navigator tests |
| TC-002 | AC-002 | Workflow handoff contract | Completed, blocked, and optional-next fixtures | Emit handoff | Every required handoff field is present and normalized | unit | handoff contract tests |
| TC-003 | AC-003 | Deterministic risk classification | Fixed factor matrix | Classify twice | Same profile, scores, and reasons | unit | rigor policy tests |
| TC-004 | AC-004 | Minimum rigor protection | Low automatic score plus full override and organization minimum | Resolve effective profile | Result never drops below explicit or protected minimum | unit | rigor policy tests |
| TC-005 | AC-005 | Evidence-backed project context | Established repository fixture | Generate and recheck context | Markdown and TOON contain evidence, revision, commands, constraints, and drift | integration | project-context tests |
| TC-006 | AC-006 | Traceable quality findings | Artifact fixture and each registered lens | Generate report | Findings contain evidence, severity, traces, owner, state, and next action | unit | quality-lens tests |
| TC-007 | AC-007 | Change impact and reopen plan | Requirement and decision delta fixture | Analyze impact | Stale artifacts, stages, reasons, and evidence-backed reopen actions are returned | integration | change-impact tests |
| TC-008 | AC-008 | Retrospective proposal safety | Completed feature fixture | Run retrospective | Observations and proposals are separate and policy files remain unchanged | integration | retrospective tests |
| TC-009 | AC-009 | Layered customization | Base, team, user, and invalid weakening fixtures | Resolve config | Precedence and provenance are deterministic and weakening fails | unit | config resolver tests |
| TC-010 | AC-010 | Optional module discovery | Core and optional manifest fixtures | Discover modules | Compatible optional skills list without changing core requirements | unit | module registry tests |
| TC-011 | AC-011 | Domain capability routing | Architecture, UX, and Research requests | Invoke each skill helper | Routed artifacts contain metadata, traceability, and deterministic validation | integration | domain skill tests |
| TC-012 | AC-012 | Evidence council modes | Review topic and evidence fixture | Run simulated and independent plans | Structured report preserves authority and distinguishes review outcomes | integration | council tests |
| TC-013 | AC-013 | Compatibility contract | Baseline and intentionally breaking fixtures | Run compatibility validator | Existing names, flags, routes, config, and module contracts are checked | integration | compatibility tests |
| TC-014 | AC-014 | One task per commit | Program Git history | Audit task commits | Every completed task maps to exactly one focused commit | acceptance | commit audit |

## Layer Mapping
- Pure registry and policy behavior: unit tests.
- CLI formatting and filesystem fixtures: integration tests.
- Skill invocation and artifact routing: workflow integration tests.
- Commit boundaries and compatibility: acceptance checks over Git history and repository contracts.

## Automation Plan
- Use unittest and existing repository test conventions.
- Keep fixtures local and deterministic.
- Add focused tests with each task before implementation is marked complete.
- Run skills/_shared/test_all_skill_scripts.py after shared-contract changes.
- Run full compatibility and SDD suites in T015.

## Open Gaps
- True cross-host independent-agent execution depends on host capability; portable council output tests validate the orchestration contract.
- Remote marketplace publication and production integrations are out of scope.
