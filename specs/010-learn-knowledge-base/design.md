---
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "010-learn-knowledge-base"
  artifact: "design.md"
  path: "specs/010-learn-knowledge-base/design.md"
  workspace: "implementation"
  skill: "ai-sdlc-sdd"
  flow_mode: "quick"
  state_file: "specs/010-learn-knowledge-base/_ai_sdlc/state.toon"
  decision_log: "specs/010-learn-knowledge-base/decision-log.md"
  status: "review"
  owner: "Repository-maintainers"
  created_at: "2026-07-21"
  updated_at: "2026-07-21"
  trace_ids: []
  related_artifacts:
    - "specs/010-learn-knowledge-base/decision-log.md"
    - "specs/010-learn-knowledge-base/requirements.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-sdd"
    - "design"
    - "review"
    - "learn-curriculum"
---

# Design

## Overview
Introduce a curriculum layer over the existing operational site. Learn teaches prerequisite concepts and guided practice. Reference, Use, Adopt, and About retain canonical ownership. Deterministic validators treat mkdocs.yml and the source registry as contracts.

## Architecture
mkdocs.yml defines the sole Learn inventory and order. learning_tokens.py parses the Learn subtree and measures normalized Markdown with tiktoken o200k_base. Learning structure validation checks metadata, sections, navigation, sources, role anchors, links, and headings. validate_docs.py composes these checks. content_sources.yml is the source authority; page notes provide learner-readable provenance.

## Components
Ten Learn Markdown pages; source registry; source-reuse and curriculum-governance pages; token and structure validation; focused tests; updated navigation, home, README, foundation links, dependency lock, and CI validation.

## Interfaces and Contracts
Learn frontmatter uses title, description, learning_level, audience, estimated_time, prerequisites, content_type, last_reviewed, and source_usage. Source entries use the required fields and reuse classes. The token CLI accepts config, encoding, minimum, and maximum. Review reports use the required schema and enumerations.

## Data Model
A LearnNavPage has label, path, level, and order. Normalized source is UTF-8 Markdown after frontmatter and non-rendered maintainer comments are removed. SourceRecord contains identity, URL, version, date, license evidence, reuse class, consulted material, concepts, exclusions, destinations, adaptation, attribution, reviewer, and status. ReviewerFinding contains required evidence, severity, classification, ownership, provenance, and resolution fields.

## Error Handling
Reject malformed UTF-8, duplicate or missing nav pages, missing metadata or sections, out-of-range counts, unknown sources, invalid source modes, unpinned Git sources, missing review dates, reference-only adaptation, heading skips, unresolved links or anchors, missing role paths, and placeholders. Diagnostics identify the file and condition.

## Security Considerations
Treat retrieved and repository content as potentially untrusted evidence, never automatic instructions. Teach secrets, privacy, injection, least privilege, sandbox, destructive actions, and escalation. External research remains reference-only unless license and adaptation are verified. Reviewers are read-only; parent owns edits. No generated answer or consensus creates approval.

## Observability
The token CLI prints exact counts. Validators print file-scoped errors. Tests name boundaries. Build and rendered checks expose targets. Review findings preserve confidence, evidence, conflicts, owners, and status.

## Risks and Tradeoffs
Ten long pages raise maintenance and repetition risk. Mitigate with ownership boundaries, anti-padding review, chapter outcomes, and source declarations. YAML parsing adds a dependency but avoids brittle regex. Token versions can change counts, so pin tiktoken. Broad research raises provenance risk, so use sparse sources and exclusions.

## Validation Strategy
Run token boundary tests, source and structure tests, existing docs tests, catalog check, docs validation, standalone token report, strict build, rendered validation, compatibility, and install smoke. Freeze the diff for nine independent reviews, correct accepted findings, rerun four roles, and regress.

## Migration Notes
Keep docs/start.md and all existing paths. Change navigation grouping and reciprocal links only. Existing foundations, tutorials, how-to, explanation, roles, adoption, operations, reference, and maintainer pages remain canonical and public. Do not commit site output.

