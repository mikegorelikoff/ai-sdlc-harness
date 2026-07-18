---
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "001-adaptive-harness-roadmap"
  artifact: "design.md"
  path: "specs/001-adaptive-harness-roadmap/design.md"
  workspace: "implementation"
  skill: "ai-sdlc-sdd"
  flow_mode: "quick"
  state_file: "specs/001-adaptive-harness-roadmap/_ai_sdlc/state.toon"
  decision_log: "specs/001-adaptive-harness-roadmap/decision-log.md"
  status: "approved"
  owner: "Dev"
  created_at: "2026-07-18"
  updated_at: "2026-07-18"
  trace_ids: []
  related_artifacts:
    - "specs/001-adaptive-harness-roadmap/decision-log.md"
    - "specs/001-adaptive-harness-roadmap/requirements.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-sdd"
    - "design"
    - "approved"
---

# Design

## Overview
Add a thin guidance and extensibility layer above the existing repository-resident control plane. Shared deterministic Python registries perform routing, risk classification, configuration resolution, module discovery, evidence shaping, and compatibility checks. Skills remain portable instruction packages that call those helpers and route durable artifacts through existing scaffold, metadata, state, and index machinery.

## Architecture
The architecture keeps visible Markdown authoritative and TOON as bounded machine projections. New core registries are pure and dependency-free. Navigator and workflow handoff consume state, indexes, Git signals, installed manifests, configuration, and project context. Optional domain modules register capabilities through manifests. Quality, change, retrospective, and council outputs are proposals or evidence records and cannot silently mutate authoritative artifacts or policy.

## Components
- Navigator router: discovers context and ranks actions.
- Handoff contract: normalizes result and next-action output.
- Rigor policy engine: scores risk factors and applies safe overrides.
- Project-context profiler: extracts evidence-backed repository rules and drift identity.
- Quality lens registry: defines reusable review lenses and finding contracts.
- Change and retrospective engines: calculate impact and improvement proposals.
- Configuration resolver: merges defaults, team, and user layers with provenance.
- Module registry: validates manifests and discovers optional capabilities.
- Optional Architecture, UX, and Research skills.
- Evidence council: produces structured multi-lens review briefs.
- Compatibility validator: protects existing public contracts.

## Interfaces and Contracts
- Every new CLI supports human-readable Markdown and compact TOON where machine consumption matters.
- Existing --quick-flow and --full-flow flags retain precedence over automatic policy.
- Module manifests declare schema, id, version, compatibility, skills, artifacts, and protected capabilities.
- Configuration resolution exposes effective value, source layer, and rejected weakening attempts.
- Handoff fields are result, blockers, next_required, next_optional, reason, command, and expected_artifact.
- Council adapters describe simulated or independent execution without assuming one agent host.

## Data Model
- Existing state.toon, plan.toon, specs-index.toon, feature-context.toon, and artifact metadata schemas remain canonical inputs.
- New policy, context, configuration, module, findings, change, retrospective, and council records use versioned schemas.
- Cross-record references use feature slug, artifact path, DEC IDs, AC IDs, TC IDs, task IDs, evidence locations, and validation commands.
- Configuration provenance is stored per effective key rather than only per file.

## Error Handling
- Missing optional context produces explicit absence signals and conservative recommendations.
- Invalid configuration or manifests fail with exact file and key diagnostics.
- Protected-gate weakening fails closed.
- Unknown risk values cannot reduce rigor.
- Missing independent-agent primitives fall back only when the user accepts simulated mode or the request allows it.
- Stale project context is reported and never presented as current evidence.

## Security Considerations
- Never read or emit secret values while profiling repositories or resolving configuration.
- Ignore known credential and environment-secret locations by default.
- Customization cannot disable protected security, approval, or evidence gates without an explicit accepted decision and compatible policy.
- Council and retrospective outputs are non-authoritative proposals.
- Module discovery validates paths and rejects traversal outside declared roots.

## Observability
- Deterministic CLIs expose selected profile, factor scores, recommendation reasons, effective configuration provenance, module compatibility, drift status, and rejected policy changes.
- Post-workflow handoffs make blockers and residual risk visible.
- Validation commands and commit hashes remain attached to task completion evidence.

## Risks and Tradeoffs
- More guidance may increase core complexity; mitigate with small pure registries and optional modules.
- Automated rigor selection can create false confidence; mitigate with explanations, minimum policies, and explicit override precedence.
- Customization can fragment behavior; mitigate with schemas, provenance, and compatibility validation.
- Independent review can be expensive; keep simulated mode available and independence explicit.
- Updating all workflow handoffs is broad; introduce a shared contract and compatibility tests before mechanical adoption.

## Validation Strategy
- Unit-test every new registry and CLI with deterministic fixtures.
- Add skill-local script tests and shared contract tests.
- Run the repository-wide skill script suite for every task that changes shared helpers.
- Run SDD clarify, checklist, analyze, plan, and structural validation before each commit.
- Run git diff --check for every commit.
- Finish with cross-capability compatibility and end-to-end navigator scenarios.

## Migration Notes
- No breaking migration is planned.
- Existing quick/full modes and artifact routes remain valid.
- New adaptive profiles are additive and map to existing enforcement until capabilities opt in.
- Configuration and module schemas are versioned from v1.
- Deprecated behavior, if discovered, will require a separate accepted decision and compatibility note.
