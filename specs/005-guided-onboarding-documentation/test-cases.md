---
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "005-guided-onboarding-documentation"
  artifact: "test-cases.md"
  path: "specs/005-guided-onboarding-documentation/test-cases.md"
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
  related_artifacts:
    - "specs/005-guided-onboarding-documentation/decision-log.md"
    - "specs/005-guided-onboarding-documentation/design.md"
    - "specs/005-guided-onboarding-documentation/requirements.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-sdd"
    - "test-cases"
    - "review"
---

# Test Cases

## Scope
Validate that the public site teaches the product from first principles, provides executable onboarding, exposes complete lifecycle/skill/script coverage, supports organizational adoption decisions, preserves safety and compatibility, and passes independent persona review. Tests cover source generation, navigation, link integrity, semantic completeness, command/path existence, strict rendering, and human usability.

## Scenario Matrix
| ID | Acceptance | Scenario | Expected result |
| --- | --- | --- | --- |
| TC-001 | AC-001 | Read Foundations in order without prior repository knowledge. | Core terms are defined before operational use; reader can explain the control loop and non-goals. |
| TC-002 | AC-002 | Enter from Home as executive and as practitioner. | Each path reaches fit/pilot or first-use content within two links. |
| TC-003 | AC-003 | Follow installation from a clean consumer repository. | Canonical Skills CLI commands are consistent; prerequisites, verification, pinning, update, and rollback are explicit; local paths exist. |
| TC-004 | AC-004 | Complete the small-change tutorial using only public docs. | Every terminal action, agent prompt, expected file/result, checkpoint, recovery, validation, and commit result is available. |
| TC-005 | AC-005 | Trace the full-feature tutorial across roles. | Discovery through learning has explicit evidence, owners, approvals, SDD, QA, release, and handoffs. |
| TC-006 | AC-006 | Compare lifecycle inventory with the canonical profile registry and control-plane packages. | All 18 refinement stages and implementation/control branches have complete entry/exit/reopen fields. |
| TC-007 | AC-007 | Add a fixture skill or remove a required detail field. | Generation or validation fails; current repository reports 43/43 complete guides. |
| TC-008 | AC-008 | Add a fixture script or omit its generated coverage. | Validation fails; every in-scope helper appears with the required operational fields. |
| TC-009 | AC-009 | Inspect lifecycle gates and authority matrix. | Accountable human, allowed agent work, prohibited action, evidence, and escalation are explicit. |
| TC-010 | AC-010 | Evaluate and design a pilot as VP Engineering. | Fit, baseline, metrics, thresholds, checkpoints, stop/rollback, and scale decision are actionable without invented ROI. |
| TC-011 | AC-011 | Review trust/governance as security or delivery owner. | Boundaries, data, packages, policy, incidents, retention, exceptions, and limitations link to enforcement. |
| TC-012 | AC-012 | Select each documented failure symptom. | Safe diagnosis, repair, validation, escalation, and do-not-do guidance exist. |
| TC-013 | AC-013 | Scan beginner pages and glossary. | Core acronyms are expanded or linked before reliance; glossary contains the complete required set. |
| TC-014 | AC-014 | Break a command path, persona route, lifecycle stage, generated guide, or nav entry in fixtures. | Deterministic documentation checks fail with source-specific diagnostics. |
| TC-015 | AC-015 | Run complete source, build, rendered, compatibility, skill, and SDD gates. | All commands exit zero; prohibited-name search is empty. |
| TC-016 | AC-016 | Ask junior, lead, and VP agents for independent rereads. | All return explicit PASS with no unresolved P0/P1; failures trigger revision and another review. |
| TC-017 | AC-017 | Search claims and evaluation pages. | Maturity, proof level, hypotheses, limitations, support, and non-goals are visible and consistent. |
| TC-018 | AC-018 | Compare completed T-IDs to Git history. | Each task maps to one focused commit in order. |

## Layer Mapping
- Unit: catalog parser, section extraction, inventory discovery, renderer, validation predicates, local-command parsing.
- Integration: source inventories → generated pages/manifest → navigation → strict MkDocs output.
- Contract: 43/43 skill closure, complete script closure, 18-stage lifecycle closure, canonical install path, public page metadata, stable URLs.
- Smoke: canonical install/version commands that are safe in CI, documentation validation, Material build, rendered target verification.
- Human acceptance: junior, lead, and VP read-only persona gates.
- Regression: shared skill tests, compatibility validator, SDD gates, Git whitespace, prohibited-name scan.

## Automation Plan
Extend `docs/tests/test_docs.py` with inventory and semantic completeness fixtures. Extend `docs/scripts/build_catalog.py` to generate per-skill pages, script catalog, and a deterministic coverage manifest. Extend `docs/scripts/validate_docs.py` to enforce generated closure, required persona/foundation/lifecycle routes, valid local executable paths, consistent canonical installation, and required guide sections. Run generation in check mode, strict MkDocs, rendered validation, affected shared/skill tests, compatibility, and SDD validators in CI-compatible commands.

## Open Gaps
Actual business outcome/ROI evidence is not available; documentation must present pilot metrics as hypotheses and decision inputs, not established impact. Persona agents provide structured heuristic review rather than representative user research. Network-dependent Skills CLI installation may require a bounded smoke check or command-existence/package-resolution check when CI has no network; document the distinction.
