---
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "009-operational-feedback-hardening"
  artifact: "requirements.md"
  path: "specs/009-operational-feedback-hardening/requirements.md"
  workspace: "implementation"
  skill: "ai-sdlc-sdd"
  flow_mode: "quick"
  state_file: "specs/009-operational-feedback-hardening/_ai_sdlc/state.toon"
  decision_log: "specs/009-operational-feedback-hardening/decision-log.md"
  status: "review"
  owner: "Repository-maintainers"
  created_at: "2026-07-21"
  updated_at: "2026-07-21"
  trace_ids: ["AC-001", "AC-002", "AC-003", "AC-004", "AC-005", "AC-006", "AC-007", "DEC-001", "DEC-002", "DEC-003"]
  related_artifacts: ["specs/009-operational-feedback-hardening/design.md", "specs/009-operational-feedback-hardening/test-cases.md", "specs/009-operational-feedback-hardening/tasks.md"]
  validation: []
  metatags: ["ai-sdlc", "implementation", "ai-sdlc-sdd", "requirements", "review", "operational-feedback"]
---

# Requirements

## Goal
Resolve reproducible harness difficulties reported in field use: installation scope confusion, stale skill discovery, unsafe cleanup assumptions, ambiguous workflow ordering, weak external-specification integration, and insufficient validation and security guidance.

## Problem Statement
Meeting evidence reports that globally installed skills can be invisible to the navigator, broad global installation can target unsupported hosts, local installation can create apparently duplicate agent directories, old managed skills require risky manual cleanup, users do not know which workflow follows a specification, and specifications maintained in another repository are not automatically visible to repository-bounded context tools. The same evidence asks for stronger result validation, token controls, safe script execution, and secret handling.

## Scope
Correct global skill discovery in the navigator; expose the discovered roots in its report; document project versus workstation scope, host-generated directories, context restart, repair/update/uninstall ownership, and direct invocation; provide a safe reviewed snapshot workflow for external Markdown specifications; document the post-spec lifecycle, validation loop, token controls, secrets boundary, and host/editor boundary; retain a disposition for every meeting-note topic; add focused and regression tests.

## Actors
Developers and trainees; product, business analysis, QA, security, delivery, and platform roles; maintainers; AI hosts; navigator and context helpers.

## Inputs
The supplied meeting notes; installation/update procedures; navigator and project-context code; workflow, security, validation, adoption, and troubleshooting guidance.

## Outputs
Corrected discovery; a tested external-spec snapshot helper; canonical operational guidance and dispositions; generated references and validation evidence.

## Functional Requirements
FR-001: Navigator discovery must include the packaged skill root from which it is executing, in addition to repository source and project-scoped roots. FR-002: Navigator output must identify discovery roots and must not recommend unavailable optional skills. FR-003: Installation documentation must explain why `--all --global` creates unsupported-host failures, which generated directories are authoritative, when a host restart is necessary, and how project and global installations differ. FR-004: Update and cleanup guidance must preserve locally modified or unowned skills and make deliberate manual review an explicit safety property. FR-005: Documentation must define when direct skill invocation is safe and when lifecycle order and state checks are mandatory. FR-006: A deterministic helper must import explicitly selected external Markdown specifications as repository-local reviewed snapshots with provenance and integrity hashes, without following symlinks, copying credential-shaped content, recording machine-specific source paths, or deleting retired files. FR-007: A field-feedback disposition must classify every harness-related note as resolved, already covered, limitation, organizational decision, or out of scope.

## Non-Functional Requirements
NFR-001 Safety: no helper may delete files, follow symlinks, execute source content, expose secrets, or write outside the repository. NFR-002 Reproducibility: tests must cover project, source, and packaged/global navigator layouts plus snapshot write/check/drift behavior. NFR-003 Usability: commands must state working directory, expected output, recovery, and ownership. NFR-004 Portability: documented guarantees are limited to validated hosts; editor and language-server behavior remains an adapter concern. NFR-005 Traceability: all material changes map to acceptance criteria and field-feedback items.

## Acceptance Criteria
AC-001: Running navigator from a packaged/global skill tree while the target repository has no local skills discovers sibling packaged skills and does not report them missing. AC-002: Navigator Markdown and TOON identify the roots used for discovery and optional actions remain limited to available skills. AC-003: Install/update/troubleshooting guidance resolves the 88-failure message, `.agents` versus host-link confusion, restart behavior, local/global precedence, safe cleanup, and multi-environment update strategy. AC-004: Documentation states that navigator use is optional when the exact skill is known, while stateful lifecycle stages cannot be run in arbitrary order. AC-005: An external-spec snapshot command copies only explicit safe Markdown sources into the selected refinement feature, writes a portable provenance manifest, detects source drift, and rejects symlinks, path escape, collisions, oversized or credential-shaped content. AC-006: The operational guide covers manual validation, small-step execution, post-spec automation choices, token budgets, secrets brokers, shared-directory safety, feedback/training, and editor/language-server boundaries. AC-007: Focused tests, documentation validation, generated catalog checks, per-skill tests, compatibility, and diff hygiene pass.

## Constraints
Do not claim automatic context refresh by an AI host, cross-host conformance, Dexter or Elixir support, a specific secrets product, or automatic safe deletion of user-modified skills. Do not persist external absolute paths. Do not add network access to runtime helpers.

## Assumptions
The meeting notes are accepted field evidence. Project-scoped installation remains the team default. Global installation is workstation state. Explicit external specification snapshots are safer and more auditable than transparent reads outside the repository boundary. Editor-specific indexing and subscription policy are organizational integration concerns.

## Open Questions
None block repository changes. Each organization must still choose approved hosts, secrets infrastructure, cost limits, language servers, and whether an external specifications repository is authoritative.

## Out of Scope
Implementing or benchmarking editors, Dexter, Elixir language servers, vaults, or provider billing; publishing a release; guaranteeing untested hosts; automatically deleting ambiguous files.

## Decision Status
The reversible repository decisions are accepted through DEC-001 to DEC-003. Organizational product, security, host, and budget choices remain explicit adopter-owned decisions.
