---
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "001-adaptive-harness-roadmap"
  artifact: "qa.md"
  path: "specs/001-adaptive-harness-roadmap/qa.md"
  workspace: "implementation"
  skill: "ai-sdlc-sdd"
  flow_mode: "quick"
  state_file: "specs/001-adaptive-harness-roadmap/_ai_sdlc/state.toon"
  decision_log: "specs/001-adaptive-harness-roadmap/decision-log.md"
  status: "validated"
  owner: "QA"
  created_at: "2026-07-18"
  updated_at: "2026-07-19"
  trace_ids: []
  related_artifacts:
    - "specs/001-adaptive-harness-roadmap/decision-log.md"
    - "specs/001-adaptive-harness-roadmap/design.md"
    - "specs/001-adaptive-harness-roadmap/plan.md"
    - "specs/001-adaptive-harness-roadmap/requirements.md"
    - "specs/001-adaptive-harness-roadmap/tasks.md"
    - "specs/001-adaptive-harness-roadmap/test-cases.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-sdd"
    - "qa"
    - "validated"
---

# QA

## Change Summary
A fifteen-capability program adds guidance, adaptive policy, repository memory, reusable review and recovery, customization, modular domain extensions, evidence council, and compatibility enforcement above the existing control plane.

## Acceptance Scenarios
- Navigator recommendations for empty, partial, blocked, and completed features.
- Handoff normalization for success, blocker, and optional continuation.
- Rigor factor boundaries, overrides, and protected minimums.
- Context generation and drift handling.
- Traceable findings, change reopen plans, and non-mutating retrospectives.
- Configuration precedence and protected gates.
- Module compatibility and optional domain skill routing.
- Council authority protection and fallback modes.
- Backward compatibility across all existing public contracts.

## Regression Targets
- Existing 26 skill tests and shared helper tests.
- Artifact scaffold, state, index, migration, context, plan, and commit validators.
- README installation and invocation examples.
- Existing quick-flow and full-flow CLI behavior.
- Legacy path read and migration safety.

## Risk Notes
- Shared helper changes can affect all installed skills.
- Mechanical handoff adoption can create inconsistent output if not contract-tested.
- Adaptive policy and customization must fail closed for protected requirements.
- Optional module loading must not make core dependent on optional files.
- Program spec status must stay aligned with one-task-one-commit history.

## Validation Commands
- PYTHONPYCACHEPREFIX=/tmp/ai-sdlc-harness-pycache python3 -m compileall -q skills
- python3 skills/_shared/test_state_machine.py
- python3 skills/_shared/test_artifact_scaffold.py
- python3 skills/_shared/test_migration.py
- python3 skills/_shared/test_all_skill_scripts.py
- python3 skills/_shared/test_config.py
- python3 skills/_shared/test_modules.py
- python3 skills/_shared/test_each_skill_tests.py
- python3 skills/_shared/test_compatibility.py
- python3 skills/_shared/ai_sdlc_compatibility.py --allow-pending-last --format toon
- python3 skills/ai-sdlc-sdd/scripts/check_clarify.py specs/001-adaptive-harness-roadmap --quick-flow
- python3 skills/ai-sdlc-sdd/scripts/check_checklist.py specs/001-adaptive-harness-roadmap --quick-flow
- python3 skills/ai-sdlc-sdd/scripts/plan_links.py specs/001-adaptive-harness-roadmap --check --quick-flow
- python3 skills/ai-sdlc-sdd/scripts/analyze_spec.py specs/001-adaptive-harness-roadmap --quick-flow
- python3 skills/ai-sdlc-sdd/scripts/validate_spec.py specs/001-adaptive-harness-roadmap --quick-flow
- git diff --check

## Manual Checks
- Confirm ai-sdlc-help presents a comprehensible next step without requiring knowledge of skill names.
- Confirm every adaptive decision explains why it selected its profile.
- Confirm team customization can be committed while user customization remains local.
- Confirm optional modules can be absent without breaking core discovery.
- Confirm council proposals do not modify authoritative artifacts.

## Signoff
Passed for release 1.0.0. T001 through T014 have one ordered focused commit each; T015 is the pending release-validation commit. Compile, state, scaffold, migration, repository contracts, layered config, module discovery, every per-skill test, compatibility baseline, and pre-commit history audit passed. Compatibility validator result: compatible; 35 skills; 5 modules; harness API 1.0.0.
