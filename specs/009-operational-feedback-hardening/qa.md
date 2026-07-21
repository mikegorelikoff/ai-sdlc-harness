---
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "009-operational-feedback-hardening"
  artifact: "qa.md"
  path: "specs/009-operational-feedback-hardening/qa.md"
  workspace: "implementation"
  skill: "ai-sdlc-sdd"
  flow_mode: "quick"
  state_file: "specs/009-operational-feedback-hardening/_ai_sdlc/state.toon"
  decision_log: "specs/009-operational-feedback-hardening/decision-log.md"
  status: "review"
  owner: "Repository-maintainers"
  created_at: "2026-07-21"
  updated_at: "2026-07-21"
  trace_ids: ["AC-001", "AC-002", "AC-003", "AC-004", "AC-005", "AC-006", "AC-007"]
  related_artifacts: ["specs/009-operational-feedback-hardening/test-cases.md", "specs/009-operational-feedback-hardening/tasks.md"]
  validation: []
  metatags: ["ai-sdlc", "implementation", "ai-sdlc-sdd", "qa", "review", "operational-feedback"]
---

# QA Plan

## Change Summary
Extend navigator packaged discovery, add safe external Markdown snapshots, and align operational documentation with field evidence.

## Strategy
Use temporary repositories for all filesystem behavior. Prove global-layout discovery without reading or modifying the real home directory. Exercise external snapshots with synthetic content and verify that failed cases leave no partial outputs. Treat documentation claims as contracts and run the full repository regression after focused tests.

## Coverage
Positive, duplicate, missing, drift, collision, traversal, symlink, size, credential, atomicity, path portability, direct invocation, lifecycle ordering, cleanup ownership, host restart, secret handling, token budget, and external-tool boundary scenarios are required.

## Acceptance Scenarios
AC-001/002 use a packaged navigator fixture. AC-005 uses safe and adversarial external checkouts. AC-003/004/006 use canonical documentation review. AC-007 uses full regression.

## Regression Targets
Navigator, project context, every skill suite, shared helpers, installed mirror, compatibility, catalogs, indexes, links, strict build, and diff hygiene.

## Risk Notes
Primary risks are false availability blockers, filesystem escape, secret import, silent retirement, unsafe cleanup, and implied untested host support.

## Validation Commands
Run focused unit tests, SDD validators, catalog check, docs validation, strict build, shared/per-skill tests, compatibility, mirror check, and `git diff --check`.

## Manual Checks
Review dispositions, install-scope wording, directory guidance, direct-versus-stateful invocation, and manifest path portability.

## Signoff
Maintainer signoff requires all commands to pass and all external limitations to remain explicit.

## Exit Criteria
All focused and full regression commands pass; no output manifest contains an absolute source path; navigator does not falsely report a packaged sibling skill as missing; all field-feedback items have a documented disposition; no new generated or temporary file remains tracked or unignored.
