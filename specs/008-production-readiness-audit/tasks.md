---
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "008-production-readiness-audit"
  artifact: "tasks.md"
  path: "specs/008-production-readiness-audit/tasks.md"
  workspace: "implementation"
  skill: "ai-sdlc-sdd"
  flow_mode: "quick"
  state_file: "specs/008-production-readiness-audit/_ai_sdlc/state.toon"
  decision_log: "specs/008-production-readiness-audit/decision-log.md"
  status: "validated"
  owner: "Repository-maintainers"
  created_at: "2026-07-21"
  updated_at: "2026-07-21"
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
  related_artifacts:
    - "specs/008-production-readiness-audit/decision-log.md"
    - "specs/008-production-readiness-audit/design.md"
    - "specs/008-production-readiness-audit/plan.md"
    - "specs/008-production-readiness-audit/qa.md"
    - "specs/008-production-readiness-audit/requirements.md"
    - "specs/008-production-readiness-audit/test-cases.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-sdd"
    - "tasks"
    - "validated"
    - "production-readiness-audit"
---

# Tasks

## Implementation
- [x] T001. Complete repository inventory, baseline execution, clean installation, and initial independent reviews.
  Output: Baseline evidence and initial consolidated registers.
  Refs: AC-001, AC-002, AC-003, AC-004, AC-010
- [x] T002. Correct consumer command paths, prerequisite gates, AGENTS.md fallback, installation scope, troubleshooting, and safe PR or merge handoff.
  Output: Executable consumer guidance and installed-layout tests.
  Refs: AC-002, AC-003, AC-005, AC-011
  Depends on: T001
- [x] T003. Add foundational software delivery, AI, agent, sub-agent, skill, SDD, validation, and governance learning chapters.
  Output: Progressive beginner-to-advanced foundations and glossary.
  Refs: AC-006, AC-012
  Depends on: T001
- [x] T004. Add all required role guides and tutorial patterns with complete evidence sequences.
  Output: Thirteen role guides and ten tutorial journeys or chapter-complete equivalents.
  Refs: AC-007, AC-008
  Depends on: T003
- [x] T005. Strengthen security, support, host, release-label, CI, supply-chain, upgrade, rollback, and ownership documentation within authorized scope.
  Output: Root policies, support matrix, CI examples, and release distinction.
  Refs: AC-005, AC-011, AC-012, AC-013, AC-014
  Depends on: T001

## Testing
- [x] T006. Extend validators and tests for root terminology, installed-only commands, generated caches, role/tutorial coverage, release labeling, and clean-tree behavior.
  Output: Focused regression tests that fail on baseline defects.
  Refs: AC-005, AC-009, AC-011, AC-013
  Depends on: T002, T003, T004, T005
- [x] T007. Run focused checks after each correction group and the complete final regression suite.
  Output: Command-by-command validation report with clean-tree result.
  Refs: AC-003, AC-009, AC-011, AC-012, AC-015
  Depends on: T006

## Documentation
- [x] T008. Publish the inventory, issue, contradiction, assumption, installation, skills, coverage, research, validation, reviewer, limitation, and readiness reports.
  Output: docs/audits/2026-07-21-production-readiness package and navigation links.
  Refs: AC-001, AC-004, AC-005, AC-010, AC-014
  Depends on: T001
- [x] T009. Run every reviewer again, perform adversarial review, close new material findings, and finalize readiness.
  Output: Rereview evidence, adversarial findings, final signoff, and accurate readiness state.
  Refs: AC-004, AC-005, AC-015
  Depends on: T007, T008
- [x] T010. Reconcile every live Skills.sh security audit with the current source revision and publish the 44-skill provider matrix.
  Output: Marketplace audit report with finding classification, source links, affected paths, and disposition.
  Refs: AC-009, AC-012, AC-016
  Depends on: T009
- [x] T011. Add credential-redaction and indirect prompt-injection boundaries to affected skills and normalize reviewer evidence handling.
  Output: Independently usable skill instructions that treat external content as data and never record raw secrets.
  Refs: AC-012, AC-016
  Depends on: T010
- [x] T012. Replace target-root Python execution in compatibility validation with static inspection and trusted executable resolution.
  Output: Read-only compatibility validator that cannot execute a discovered repository script.
  Refs: AC-011, AC-012, AC-016
  Depends on: T010
- [x] T013. Run focused security contracts, all shared and per-skill tests, compatibility, documentation, mirror, and diff checks; record residual external rescan lag.
  Output: Regression evidence and current marketplace-security disposition.
  Refs: AC-005, AC-011, AC-015, AC-016
  Depends on: T011, T012
