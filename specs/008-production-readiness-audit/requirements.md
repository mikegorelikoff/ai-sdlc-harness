---
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "008-production-readiness-audit"
  artifact: "requirements.md"
  path: "specs/008-production-readiness-audit/requirements.md"
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
    - "AC-016"
    - "DEC-001"
    - "DEC-003"
    - "DEC-004"
    - "NFR-001"
    - "NFR-002"
    - "NFR-003"
    - "NFR-004"
    - "NFR-005"
    - "NFR-006"
    - "NFR-007"
  related_artifacts:
    - "specs/008-production-readiness-audit/decision-log.md"
    - "specs/008-production-readiness-audit/design.md"
    - "specs/008-production-readiness-audit/plan.md"
    - "specs/008-production-readiness-audit/qa.md"
    - "specs/008-production-readiness-audit/tasks.md"
    - "specs/008-production-readiness-audit/test-cases.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-sdd"
    - "requirements"
    - "review"
    - "production-readiness-audit"
---

# Requirements

## Goal
Make the AI SDLC Harness production-quality, internally consistent, beginner-friendly, secure by explicit boundaries, installable from documented prerequisites, and evidence-backed across roles, tutorials, skills, validation, and enterprise adoption.

## Problem Statement
The current repository has strong deterministic mechanisms and a clear evidence model, but independent baseline reviews found material adoption blockers: no license grant, public documentation ahead of the pinned release, source-only commands in consumer guidance, undocumented host and AGENTS.md assumptions, incomplete beginner foundations, missing role and tutorial coverage, and weak pre-merge documentation and provenance controls.

## Scope
Inventory every tracked and accessible generated surface; test source validation and a clean consumer install; run eleven independent role reviews; create durable issue, contradiction, assumption, installation, skills, coverage, research, validation, and reviewer registers; correct repository-fixable Critical, High, and Medium defects; add progressive foundations, role guides, tutorial patterns, security/support guidance, and consumer CI examples; run full regression and adversarial rereview.

## Actors
Trainee and experienced developers; lead developers; quality assurance engineers; business analysts; product owners and managers; delivery and engineering managers; vice presidents of engineering; chief technology officers; DevOps and platform engineers; security reviewers; maintainers; AI agents and independent sub-agents.

## Inputs
The complete user audit brief; the clean main branch at commit 38da30737c15fcbe53c8e4854cea09eae0446fd0; repository history and release tags; current documentation, skills, scripts, tests, examples, configuration, CI, and generated artifacts; clean-install command evidence; independent reviewer evidence; authoritative primary sources.

## Outputs
A corrected repository; complete audit deliverables under docs/audits/2026-07-21-production-readiness; an SDD package with traceability; updated public documentation and navigation; safer installation and validation guidance; regression evidence; explicit unresolved owner and release blockers; a final readiness decision.

## Functional Requirements
FR-001: Build a tracked repository inventory and suspicious-file disposition. FR-002: Execute documented source checks, clean installation, helper verification, and one representative workflow. FR-003: Run the eleven required independent reviewers before consolidation and rerun them after corrections. FR-004: Maintain issue, contradiction, assumption, source, coverage, skills, installation, validation, and review registers. FR-005: Correct consumer path, prerequisite, generated-cache, AGENTS.md fallback, command-output, troubleshooting, and pull-request handoff defects. FR-006: Add foundational AI and software-delivery chapters, distinct role guides, and the requested tutorial scenarios. FR-007: Audit all skills for metadata, dependencies, references, conflicts, precedence, lifecycle, testing, and deprecation guidance. FR-008: Add or improve security, privacy, support, host, CI, supply-chain, and enterprise-adoption guidance without inventing legal or support promises. FR-009: Validate all internal links, advertised commands, generated catalogs, rendered pages, compatibility contracts, and relevant tests. FR-010: Preserve evidence for remaining external constraints and assign only an acceptance state allowed by the exit criteria. FR-011: Review the live Skills.sh provider audits for every published skill, remediate confirmed secret-handling, indirect prompt-injection, dynamic-loading, and target-root execution risks, and retain a provider-by-provider disposition.

## Non-Functional Requirements
NFR-001 Evidence: every material finding cites repository paths, line references, commands, or authoritative sources. NFR-002 Safety: no license, release, public support commitment, credential, external publication, or destructive project change is invented. NFR-003 Usability: acronyms are expanded and concepts appear before use. NFR-004 Portability: source and installed layouts are distinguished; platform and host claims match exercised evidence. NFR-005 Reproducibility: clean setup distinguishes online bootstrap from offline reuse and records versions and expected output. NFR-006 Maintainability: canonical pages own definitions and generated or historical surfaces cannot silently contradict them. NFR-007 Scope: objective defects take priority over stylistic preferences.

## Constraints
Do not choose a license, create or publish a release, change external repository settings, assert untested host support, promise a service level, or use inaccessible credentials. Preserve user-owned work. Use primary sources for unstable or standards-based claims. Keep the current historical specs-refiniment route compatible unless a separately approved migration is designed.

## Acceptance Criteria
Given the repository at the start of the audit, when the relevant test or review is executed, then each criterion below must produce observable pass or fail evidence. AC-001: A complete tracked inventory and suspicious-file disposition exists. AC-002: Clean consumer installation and documented helper checks succeed with recorded environment, commands, actual output, and recovery. AC-003: At least one representative workflow and deliberate failure recovery succeed. AC-004: All eleven independent reviewers submit evidence-based baseline and rereview decisions. AC-005: No repository-fixable Critical or High issue remains and Medium issues are resolved or explicitly accepted with rationale. AC-006: Foundations explain software delivery, SDLC, AI, ML, LLMs, generative AI, prompts, context, tokens, hallucinations, validation, agents, sub-agents, skills, SDD, traceability, and governance before advanced use. AC-007: Thirteen distinct role guides provide purpose, participation, inputs, outputs, decisions, mistakes, examples, and checklists. AC-008: Requested feature, defect, refactor, API, schema, testing, ambiguity, AI review, failed implementation, and changed-requirement tutorials include the required evidence sequence. AC-009: Every packaged skill appears in a complete skills inventory and passes deterministic contract and reference checks. AC-010: Issue, contradiction, assumption, installation, coverage, source, validation, and reviewer registers are current and linked. AC-011: Documentation source, unit, strict build, rendered links, compatibility, skill tests, diff hygiene, secret/local-path, and clean-tree checks pass. AC-012: Security, privacy, prompt-injection, secret, permissions, supply-chain, human review, and data-egress boundaries are explicit. AC-013: Public documentation clearly distinguishes stable release v1.2.0 from unreleased main behavior or an authorized release resolves the mismatch. AC-014: A repository owner selects and authorizes a license before organizational adoption or the final decision remains NOT READY. AC-015: Final adversarial review finds no new unresolved material repository-fixable issue. AC-016: All 44 live Skills.sh audit records have a durable disposition; flagged skills enforce credential redaction and untrusted-evidence boundaries; compatibility checking does not execute Python discovered under a supplied target root; focused security-contract tests pass.

## Out of Scope
Choosing legal terms; publishing a tag or GitHub release; changing branch protection or organization policy; validating every third-party AI host without access; proving causal productivity improvement; producing compliance certification; replacing product, engineering, QA, security, or legal accountability.

## Assumptions
The detailed user brief is accepted upstream requirements context. Quick-flow spec authoring is appropriate while independent evidence is gathered because changes are local and reversible; full regression gates are still required before handoff. Codex is the only host exercised in this audit unless another host is independently available. The Skills CLI and network are external dependencies. Generated site and context directories are disposable when ignored and reproducible.

## Open Questions
TODO(dm): The repository owner must select the license. TODO(dm): The release owner must decide whether to publish a new release, version the public site, or keep main documentation clearly marked as preview. TODO(dm): The owner must choose which host and operating-system combinations may be claimed as supported after conformance testing.

## Decision Status
The detailed user brief is an accepted assumption for upstream requirements. Repository-fixable implementation decisions are resolved through DEC-001, DEC-003, and DEC-004. TODO(dm): the legal owner must select a license; TODO(dm): the release owner must authorize publication or versioned deployment; TODO(dm): the platform owner must authorize supported host claims. These owner decisions block READY but do not block reversible repository corrections.
