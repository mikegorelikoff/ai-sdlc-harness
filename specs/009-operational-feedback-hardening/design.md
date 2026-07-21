---
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "009-operational-feedback-hardening"
  artifact: "design.md"
  path: "specs/009-operational-feedback-hardening/design.md"
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
  related_artifacts: ["specs/009-operational-feedback-hardening/requirements.md", "specs/009-operational-feedback-hardening/test-cases.md"]
  validation: []
  metatags: ["ai-sdlc", "implementation", "ai-sdlc-sdd", "design", "review", "operational-feedback"]
---

# Design

## Overview
Harden discovery and cross-repository evidence without widening ambient filesystem authority. Keep host refresh, ownership, and organizational tools explicit.

## Architecture
Navigator discovery becomes a deterministic union of three roots: `root/skills`, `root/.agents/skills`, and the sibling skill root inferred from the executing script. Only directories containing `SKILL.md` count. The report includes portable root labels (`source`, `project`, `packaged`) rather than assuming that the host refreshed its in-memory registry.

External specification integration is an explicit snapshot operation owned by `ai-sdlc-project-context`. A new helper accepts a repository root, source root, feature slug, stable source identifier, and one or more source-relative Markdown paths. It validates every source before any write, copies content to top-level `specs-refiniment/<feature>/external-<slug>.md`, and writes `external-specs.json` with source identifier, Git revision when available, source-relative paths, destination paths, and SHA-256 values. `--check` compares the local snapshot, manifest, and current source without writing. It never removes an old snapshot automatically.

## Components
Navigator discovery/reporting; external snapshot writer/checker; canonical operational documentation; focused and repository-wide validation.

## Interfaces and Contracts
Navigator retains `ai-sdlc-navigator/v1` and adds `skill_roots`. Snapshot exposes `--write`/`--check`, explicit roots, source ID, feature, and repeatable sources; its manifest is `ai-sdlc-external-spec-snapshot/v1`.

## Data Model
Snapshot rows contain source, destination, SHA-256, and byte size. The manifest adds feature, logical source ID, source revision, evidence-only authority, and fingerprint without an absolute external path.

## Error Handling
Validation fails before writes. Check mode names drift. Writes are repository-bounded and atomic. Omitted previous sources fail rather than disappearing silently.

## Security Boundaries
The snapshot source root is explicit, but source files must remain inside it, be regular non-symlink Markdown files, be bounded in size, and contain no recognized credential shape. Destination paths are repository-bounded, cannot traverse symlinks, and use collision-checked deterministic names. External text is evidence-only and never instructions. The manifest excludes the absolute source root.

## Security Considerations
Treat external files as potential prompt injection and sensitive data. Screen credentials, reject traversal and symlinks, never execute content, and preserve human/provider policy review.

## Observability
Navigator reports roots/count. Snapshot JSON reports status, manifest, hashes, revision, and errors. Git diff, tests, catalogs, and lifecycle state provide durable evidence.

## Risks and Tradeoffs
Snapshots duplicate bytes and require refresh but improve provenance. Executing-root discovery may show an absolute local root ephemerally. Manual cleanup costs time but prevents ownership-based loss.

## Validation Strategy
Use isolated repositories for packaged and external fixtures, cover adversarial paths/content, then run all skill, compatibility, docs, build, and diff gates.

## Migration Notes
Existing project context needs no migration. Navigator consumers tolerate one new detected-context field. External content changes only after explicit snapshotting.

## Documentation Model
One operational field-feedback guide owns the end-to-end disposition and links to canonical installation, update, troubleshooting, workflow, context, security, and adoption pages. Canonical pages receive concise rules; the disposition does not duplicate full procedures.

## Failure And Recovery
Navigator reports a missing required skill as a blocker but still names every searched root. Snapshot validation fails before writes. A failed write can be rerun because each output is atomic and deterministic. Drift produces a non-zero check result and named diagnostics. Cleanup remains review-driven because ownership cannot be inferred safely from a directory name alone.

## Alternatives Rejected
Scanning all home-directory skill locations was rejected because it creates host-specific assumptions and wider filesystem reads. Transparent reads from arbitrary external repositories were rejected because they weaken repository-bounded context and provenance. Git symlinks and submodules as the only supported integration were rejected because checkout, trust, and host behavior vary; they remain optional upstream transport mechanisms before snapshotting.
