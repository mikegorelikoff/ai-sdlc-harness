---
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "007-context-and-prompt-engineering"
  artifact: "design.md"
  path: "specs/007-context-and-prompt-engineering/design.md"
  workspace: "implementation"
  skill: "ai-sdlc-sdd"
  flow_mode: "quick"
  state_file: "specs/007-context-and-prompt-engineering/_ai_sdlc/state.toon"
  decision_log: "specs/007-context-and-prompt-engineering/decision-log.md"
  status: "approved"
  owner: "Dev"
  created_at: "2026-07-20"
  updated_at: "2026-07-20"
  trace_ids: []
  related_artifacts:
    - "specs/007-context-and-prompt-engineering/decision-log.md"
    - "specs/007-context-and-prompt-engineering/qa.md"
    - "specs/007-context-and-prompt-engineering/requirements.md"
    - "specs/007-context-and-prompt-engineering/tasks.md"
    - "specs/007-context-and-prompt-engineering/test-cases.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-sdd"
    - "design"
    - "approved"
    - "research-backed"
---

# Design

## Overview
Upgrade the existing context engine rather than expanding the skill catalog. Task packs become goal-aware, authority-labeled, sufficiency-checked v3 records. Shared context packs read the same safe typed interaction profile so workflows can honor stable user preferences consistently without implicit memory.

## Architecture
The deterministic pipeline remains local:

1. Resolve safe candidates and exclusions.
2. Build normalized query terms from task, goal, tags, and relevant paths.
3. Score source lines and select one bounded contiguous range per candidate.
4. Label source authority and emit exact evidence.
5. Evaluate requested-path coverage, truncation, freshness, and budget omissions.
6. Resolve optional preferred-name metadata from the existing resolved configuration.
7. Fingerprint and render JSON, TOON, or Markdown.

No model inference or network retrieval enters the runtime.

## Components
- `skills/ai-sdlc-project-context/scripts/context_engine.py`: relevance selection, authority labels, sufficiency, v3 rendering.
- `skills/_shared/ai_sdlc_context.py`: safe preferred-name resolver and shared context-pack propagation.
- `skills/ai-sdlc-shared-runtime/scripts/ai_sdlc_context.py`: generated installed-runtime mirror.
- `config/ai-sdlc.defaults.json`: empty optional preferred-name default.
- Context pack schema and contract references.
- Project-context unit tests and shared runtime tests.
- Public foundation/how-to/configuration pages and generated reference docs.

## Interfaces and Contracts
`ai-sdlc-context-pack/v3` adds:

- `interaction.enabled`, `interaction.status`, `interaction.preferred_name`, `interaction.language`, `interaction.response_style`, `interaction.technical_depth`, `interaction.status_updates`, and `interaction.usage=presentation_only`;
- `content_handling.evidence_only` and `content_handling.repository_instruction`;
- selected-item fields `authority`, `selection_strategy`, `matched_terms`, and `relevance_score`;
- `sufficiency.status`, `sufficiency.reasons`, and `sufficiency.next_reads`.

The CLI adds no required arguments. Existing task, goal, path, tag, selector, budget, and format flags remain stable. The existing layered config supplies preferences and provenance.

## Data Model
Interaction resolution returns a stable typed object with status `configured`, `disabled`, `not_configured`, or `invalid`. Supported values are bounded enums or short strings; unsupported keys and invalid values are reported without being propagated. A selected range remains an exact excerpt of one source and includes start/end lines. Sufficiency reasons use stable codes and human detail. Fingerprints include the resolved interaction object and all new fields.

## Error Handling
Unsafe requested paths continue to fail before output. Missing or unreadable requested sources remain exclusions and make sufficiency `insufficient`. Invalid interaction preferences are ignored, marked `invalid`, and never block technical work. Disabled personalization emits no applied values. No-match relevance falls back to the prefix instead of failing.

## Security Considerations
Retrieved repository content is labeled evidence-only unless the path is a recognized repository instruction file. Interaction strings are type-checked, length-bounded, stripped of control characters, and cannot influence authority, permissions, protected gates, or evidence. The runtime never mines conversations or connected data. Existing credential and path exclusions remain unchanged.

## Observability
Each range reports strategy, matched terms, score, reason, token estimate, bounds, truncation, and hash. Sufficiency reasons and next reads explain why another retrieval or human review is required. Configuration provenance remains available through the existing resolver.

## Risks and Tradeoffs
Lexical ranking can miss synonyms and deeper semantic relationships, but it is deterministic, explainable, offline, and dependency-free. Selecting one contiguous range may omit multiple distant needles; next reads and `review_required` make this visible. Typed personalization is less flexible than free-form instructions, but prevents prompt bloat and conflicts. Preference use depends on agents consuming generated context, so docs establish the same contract. Contract v3 requires consumers validating the exact schema string to migrate.

## Validation Strategy
Add fixtures for a relevant phrase near the end, prefix fallback, authority classification, missing requested evidence, truncation/freshness review, configured and invalid names, deterministic output, and unchanged selection with personalization. Run focused project-context tests, shared runtime script tests, schema checks, generated catalog drift checks, docs validation, strict MkDocs, and SDD gates.

## Migration Notes
Consumers accepting only `ai-sdlc-context-pack/v2` must add v3 support. Selector and topology contracts do not change. Existing CLI calls remain valid. An absent resolved config behaves as `not_configured`; the default profile is disabled. Users opt in through a user-layer `interaction.enabled=true` and only the preferences they want.
