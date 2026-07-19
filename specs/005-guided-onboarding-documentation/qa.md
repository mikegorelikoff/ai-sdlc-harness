---
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "005-guided-onboarding-documentation"
  artifact: "qa.md"
  path: "specs/005-guided-onboarding-documentation/qa.md"
  workspace: "implementation"
  skill: "ai-sdlc-sdd"
  flow_mode: "quick"
  state_file: "specs/005-guided-onboarding-documentation/_ai_sdlc/state.toon"
  decision_log: "specs/005-guided-onboarding-documentation/decision-log.md"
  status: "review"
  owner: "TBD"
  created_at: "2026-07-19"
  updated_at: "2026-07-19"
  trace_ids: []
  related_artifacts:
    - "specs/005-guided-onboarding-documentation/decision-log.md"
    - "specs/005-guided-onboarding-documentation/design.md"
    - "specs/005-guided-onboarding-documentation/requirements.md"
    - "specs/005-guided-onboarding-documentation/test-cases.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-sdd"
    - "qa"
    - "review"
---

# QA

## Change Summary
Replace the reference-first documentation experience with a canonical guided onboarding system for the AI SDLC Harness. The change adds first-principles foundations, persona paths, runnable tutorials, complete lifecycle flows, generated detail for every skill and script, organizational adoption/governance guidance, troubleshooting, maintainer guidance, semantic completeness checks, and independent persona gates.

## Acceptance Scenarios
QA follows four reader journeys:
1. Junior: Home → AI SDLC/SDD foundations → install → first 30 minutes → runnable small feature → choose another flow → locate any skill.
2. Lead: system model → exact lifecycle → role/authority → skill/script contracts → failure recovery → extension and validation.
3. VP: why/fit → risks/non-goals → pilot/adoption → metrics/thresholds → governance → scale/stop decision.
4. Maintainer/agent: capability selection → authoritative skill → deterministic helper → artifact and handoff → validation/recovery.

For each journey, verify terms precede use, actions identify the actor, links stay within two-click targets where required, expected results are concrete, and no hidden root guide is needed.

## Regression Targets
Material navigation and search; canonical release/install/update pages; every discovered skill package name; module ownership; all Python helpers; 18-stage refinement order; SDD artifacts and state paths; TOON-first contracts; quick/full/adaptive semantics; artifact authority; handoffs; policy, approvals, package trust, host capability, runtime, recovery, compatibility, and Pages deployment. Preserve old public URLs unless an explicit replacement is linked.

## Risk Notes
Highest risks are overwhelming beginners, generating misleading detail from prose contracts, duplicating canonical sources, publishing unsafe commands, hiding human approval boundaries, overstating ROI, and passing shallow word-count tests despite semantic gaps. Mitigations are progressive disclosure, stable guide templates, source links, deterministic inventory closure, local-command checks, actor labels, governance/RACI, explicit proof levels, runnable examples, and persona rereads.

## Validation Commands
- `python3 docs/scripts/build_catalog.py --check`
- `python3 docs/scripts/validate_docs.py`
- `python3 docs/tests/test_docs.py`
- `UV_CACHE_DIR=/tmp/ai-sdlc-uv-cache uv run --offline --with-requirements requirements-docs.txt mkdocs build --strict`
- `python3 docs/scripts/validate_rendered.py`
- `python3 skills/_shared/test_all_skill_scripts.py`
- `python3 skills/_shared/test_each_skill_tests.py`
- `python3 skills/_shared/ai_sdlc_compatibility.py --skip-git-audit --format toon`
- `python3 skills/ai-sdlc-sdd/scripts/plan_links.py specs/005-guided-onboarding-documentation --check --quick-flow`
- `python3 skills/ai-sdlc-sdd/scripts/analyze_spec.py specs/005-guided-onboarding-documentation --quick-flow`
- `python3 skills/ai-sdlc-sdd/scripts/validate_spec.py specs/005-guided-onboarding-documentation --quick-flow`
- `git diff --check`
- repository-wide prohibited-name search excluding generated site and Git internals

## Manual Checks
- Complete the copyable small-change tutorial without reading internal package files.
- Use the decision tree for new idea, bounded feature, bug, review-only, security-sensitive change, changed requirement, full refinement, and interrupted run.
- Verify any randomly selected skill and script exposes the required human-facing fields.
- Compare source checkout, installed agent environment, and consumer repository diagrams.
- Inspect light/dark responsive navigation and code/admonition labels.
- Verify every risky mutation has a visible human checkpoint or protected policy gate.
- Confirm pilot metrics state what they can and cannot prove.
- Ask independent junior, lead, and VP agents to reread from a clean perspective and return evidence-backed PASS/FAIL.

## Signoff
Documentation owner signs off on source and navigation completeness. Dev/maintainer signs off on generated inventory, commands, scripts, and build tests. Delivery/Security signs off on authority, governance, failure, and recovery descriptions. Final program signoff requires junior, lead, and VP persona PASS, no unresolved P0/P1, all automated gates green, clean task-to-commit mapping, and no hidden dependency on root concepts/guides for public onboarding.
