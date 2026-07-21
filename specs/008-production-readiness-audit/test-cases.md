---
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "008-production-readiness-audit"
  artifact: "test-cases.md"
  path: "specs/008-production-readiness-audit/test-cases.md"
  workspace: "implementation"
  skill: "ai-sdlc-sdd"
  flow_mode: "quick"
  state_file: "specs/008-production-readiness-audit/_ai_sdlc/state.toon"
  decision_log: "specs/008-production-readiness-audit/decision-log.md"
  status: "review"
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
  related_artifacts:
    - "specs/008-production-readiness-audit/decision-log.md"
    - "specs/008-production-readiness-audit/design.md"
    - "specs/008-production-readiness-audit/qa.md"
    - "specs/008-production-readiness-audit/requirements.md"
    - "specs/008-production-readiness-audit/tasks.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-sdd"
    - "test-cases"
    - "review"
    - "production-readiness-audit"
---

# Test Cases

## Scope
Cover repository inventory, clean installation, consumer command execution, workflow recovery, documentation learning progression, role and tutorial coverage, skills integrity, security boundaries, release labeling, audit traceability, regression, and remaining external blockers.

## Scenario Matrix
| ID | Acceptance | Actor / setup | Action | Expected / evidence | Risk and owner |
| --- | --- | --- | --- | --- | --- |
| TC-001 | AC-001 | Maintainer, full candidate tree and Git metadata. | Enumerate tracked, ignored, generated, empty, duplicate, suspicious, and misplaced content. | Every suspicious item has a disposition and no unexplained tracked trash remains; inventory and scan logs are recorded. | Accidental or encoded content; Maintainer accountable, Security consulted. |
| TC-002 | AC-002 | DevOps reviewer, disposable consumer with pinned prerequisites. | Install stable and candidate revisions and run inventory/helper checks. | Candidate succeeds; stable outcome is the exact locked regression; command, environment, revision, target, and count evidence is recorded. | Network/OS variance; DevOps owns, platform matrix remains external. |
| TC-003 | AC-003 | Lead Developer, clean tutorial fixture. | Run the sample workflow and deliberate regression. | Baseline passes, regression fails for the expected reason, recovery restores pass and clean state; console evidence retained. | False-positive tests; Lead owns with QA review. |
| TC-004 | AC-004 | Orchestrator, eleven isolated reviewer briefs. | Collect baseline and corrected-tree rereviews from all perspectives. | Every required question, material finding, evidence, and decision is present in reviewer reports. | Review correlation; Orchestrator owns and preserves independent first passes. |
| TC-005 | AC-005 | Orchestrator and issue owners, unified issue register. | Reconcile Critical, High, and Medium findings. | Local material issues close with acceptance tests; accepted items identify rationale and owner. | False closure; reporting reviewer rechecks. |
| TC-006 | AC-006 | Trainee with Git/terminal prerequisites only. | Follow the beginner path without assumed AI or SDLC knowledge. | Concepts precede use and glossary/links resolve terms; trainee walkthrough evidence recorded. | Reader diversity; Technical Writer owns, pilot feedback remains. |
| TC-007 | AC-007 | Each named role reviewer at its role route. | Inspect every required role guide and checklist. | Thirteen guides include care, participation, inputs, outputs, decisions, mistakes, workflow, and checklist evidence. | Role variation; role owner accountable. |
| TC-008 | AC-008 | Developer/QA pair with tutorial index. | Inspect every requested tutorial pattern. | Ten patterns contain request, discovery, spec, plan, tasks, skills, sequence, validation, artifacts, failures, and evidence. | Patterns are illustrative; Lead and QA own applicability review. |
| TC-009 | AC-009 | Maintainer with source and installed layouts. | Enumerate and test every skill. | Catalog closes over 44 skills/116 scripts, 20 mirrors sync, and deterministic suites pass. | Dynamic host behavior; Maintainer owns, installed smoke supplements unit tests. |
| TC-010 | AC-010 | Product Owner with all registers and graph. | Trace issues, assumptions, requirements, tasks, tests, reviews, and commits. | Registers agree; 100 declared AC have task/test coverage; historical gaps remain explicitly bounded. | Historical commit gaps; Product Owner accepts limitation, future Task trailer enforced. |
| TC-011 | AC-011 | QA in exact candidate snapshot. | Run the full deterministic regression suite and receipt verifier. | All planned commands exit zero and receipt revision/workspace/trace checks pass; validation report records digests/outcomes. | Local receipt unauthenticated; QA owns local proof, CI owner owns protected proof. |
| TC-012 | AC-012 | Security reviewer with exact diff and security guide. | Review privacy, permissions, prompt injection, secrets, dependency, and supply-chain boundaries. | Threat boundaries, human controls, findings, and residual risks are explicit in security review/audit. | Novel leakage/injection; Security owns adversarial review. |
| TC-013 | AC-013 | CTO/release owner with remote tag/release evidence. | Compare public main documentation with pinned v1.2.0. | Main is labeled preview; stable defect is reproduced; readiness remains blocked until corrected immutable publication. | Version drift; release owner accountable. |
| TC-014 | AC-014 | Repository owner/legal authority, repository root. | Check legal reuse grant. | Authorized license exists or final readiness stays blocked with the absence recorded. | Legal authority unavailable; repository owner accountable. |
| TC-015 | AC-015 | All eleven reviewers after correction sign-off. | Run separate adversarial review prompts against the final candidate. | No new local material issue remains; likely failures/confusion/claim/beginner/enterprise/scenario answers are recorded. | Sampling cannot prove absence; Orchestrator owns disposition and rerun. |
| TC-016 | AC-016 | Security reviewer with all 44 live Skills.sh audit records and the current source tree. | Reconcile provider findings, test secret-bearing approval input, inspect untrusted-content skill boundaries, and run compatibility against a target containing an executable trap script. | Every marketplace record has a disposition; secret values are forbidden from records; affected skills reject embedded authority; the trap script is never executed; security-contract and compatibility suites pass. | External provider rescans can lag the repository revision; Maintainer owns rescan after publication. |

## Layer Mapping
Unit and contract tests cover helpers and skill metadata. Integration tests cover installed-only consumer paths and generated mirrors. Documentation tests cover navigation, glossary, coverage, commands, links, release labels, and stale root surfaces. Manual persona reviews cover comprehension and governance. External checks cover registry, GitHub tag, and authoritative sources.

## Automation Plan
Extend existing Python standard-library validators and tests. Add installed-consumer smoke fixtures where a source root is absent. Run docs validation and strict build on pull requests. Keep network-dependent install checks isolated and record external failures separately.

## Open Gaps
A full virtual-machine matrix and non-Codex agent conformance require external
environments (DevOps owner). Protected continuous-integration receipt
attestation requires repository-platform access (CI owner). Accessibility
assistive-technology testing and broad novice comprehension require human test
participants (Technical Writer/Accessibility owner). Performance is limited to
documentation-build and helper-runtime sanity because this repository ships no
production service (Maintainer); a future consumer must add workload-specific
performance tests. License selection and release publication require repository
owner authority. Organizational outcome claims require a future measured pilot
owned by engineering leadership.
