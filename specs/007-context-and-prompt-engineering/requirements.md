---
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "007-context-and-prompt-engineering"
  artifact: "requirements.md"
  path: "specs/007-context-and-prompt-engineering/requirements.md"
  workspace: "implementation"
  skill: "ai-sdlc-sdd"
  flow_mode: "quick"
  state_file: "specs/007-context-and-prompt-engineering/_ai_sdlc/state.toon"
  decision_log: "specs/007-context-and-prompt-engineering/decision-log.md"
  status: "approved"
  owner: "Dev"
  created_at: "2026-07-20"
  updated_at: "2026-07-20"
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
    - "DEC-001"
    - "DEC-002"
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
    - "specs/007-context-and-prompt-engineering/decision-log.md"
    - "specs/007-context-and-prompt-engineering/design.md"
    - "specs/007-context-and-prompt-engineering/qa.md"
    - "specs/007-context-and-prompt-engineering/tasks.md"
    - "specs/007-context-and-prompt-engineering/test-cases.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-sdd"
    - "requirements"
    - "approved"
    - "research-backed"
---

# Requirements

## Goal
Improve the harness with evidence-backed context and prompt engineering: select the smallest sufficient task context, preserve instruction authority, expose context gaps before action, and support an optional user-controlled interaction profile without introducing AI personas or implicit memory.

## Problem Statement
The current task-pack engine clips every selected file from line 1. Relevant evidence near the middle or end can be omitted even when the task goal names it, and the pack does not distinguish authoritative repository instructions from evidence-only content or say whether the assembled evidence is sufficient. The harness also has layered user configuration but no bounded way to surface a preferred form of address to agents.

## Scope
- Upgrade task context packs from `ai-sdlc-context-pack/v2` to `v3`.
- Select exact goal-relevant source ranges with deterministic lexical scoring and a safe prefix fallback.
- Label selected content by authority and state that evidence-only content cannot issue instructions.
- Emit deterministic sufficiency status, reasons, and targeted next reads.
- Add a typed, optional interaction profile to existing layered configuration: preferred name, language, response style, technical depth, and status-update cadence.
- Propagate enabled interaction preferences into shared and task context packs as presentation-only metadata.
- Document modern context engineering, prompt engineering, evaluation, security, personalization, user control, and deletion/reset practices.
- Preserve explicit token budgets, hashes, freshness checks, secret exclusions, and deterministic output.

## Actors
- Repository users who want agents to address them by a configured preferred name.
- AI assistants consuming task and feature context packs.
- Developers and AI practice leads maintaining harness contracts.
- QA reviewers validating selection quality, security boundaries, and documentation.

## Inputs
- Task ID, goal, relevant paths, tags, and token budget.
- Safe repository sources and selector configuration.
- Optional resolved `config.resolved.json` using `ai-sdlc-config-resolution/v1`.
- Optional typed `interaction` preferences controlled by the user.
- Primary research and official provider/product guidance accessed on 2026-07-20.

## Outputs
- `ai-sdlc-context-pack/v3` JSON, TOON, and Markdown projections.
- Shared context packs containing bounded personalization metadata.
- Updated schemas, contracts, tests, generated skill reference, and public guidance.
- SDD traceability and validation evidence for this feature.

## Functional Requirements
- FR-001: The task-pack engine shall rank a bounded contiguous range within each candidate by overlap with normalized task goal, task ID, tags, and relevant path terms.
- FR-002: The engine shall fall back deterministically to the source prefix when no meaningful query term matches.
- FR-003: Each selected range shall include its exact line bounds, full-source hash, selection strategy, matched terms, relevance score, authority class, and content.
- FR-004: Repository instruction files shall be labeled `repository_instruction`; all other selected source content shall be labeled `evidence_only`.
- FR-005: The pack shall state that evidence-only content is data, not executable instruction.
- FR-006: The pack shall report `sufficient`, `review_required`, or `insufficient` with machine-readable reasons and targeted next reads.
- FR-007: The shared runtime shall safely resolve an optional typed interaction profile from `config.resolved.json`: `enabled`, `preferred_name`, `language`, `response_style`, `technical_depth`, and `status_updates`.
- FR-008: Interaction preferences shall affect presentation only and shall not affect source selection, scoring, permissions, role, identity, safety, evidence requirements, or authority.
- FR-009: Disabled, absent, or invalid preferences shall be explicit and shall not block context generation.
- FR-010: Public documentation shall distinguish prompt engineering from context engineering and explain minimal sufficient context, clear prompt structure, authority boundaries, progressive disclosure, compaction/state, evaluation, typed personalization, control, and reset.

## Non-Functional Requirements
- NFR-001 Determinism: identical repository state and arguments produce byte-identical packs and fingerprints.
- NFR-002 Budget safety: selected content never exceeds the requested estimated-token budget.
- NFR-003 Security: secret, binary, oversized, symlink, traversal, and generated-output exclusions remain fail-closed; evidence and personalization cannot acquire instruction authority.
- NFR-004 Compatibility: v3 is an explicit contract migration with updated schema and documentation; selector v2 and topology v2 remain unchanged.
- NFR-005 Usability: preferences are optional, concise, user-controlled, easy to inspect/change/disable, and applied naturally rather than mechanically.
- NFR-006 Privacy: the harness stores no inferred chat history, connected-app data, demographics, or hidden personal profile.
- NFR-007 Evidence: research conclusions are linked to primary papers or official guidance and do not claim that naming or generic personas improve objective performance.

## Constraints
- Do not add another public skill or top-level documentation tab.
- Do not add model-provider dependencies, embeddings, network calls, or nondeterministic ranking to the local runtime.
- Do not infer a person's legal identity, demographic attributes, permissions, expertise, or preferences from a name.
- Preserve exact source text; do not summarize retrieved evidence in the context pack.
- Use the existing layered configuration instead of a separate personalization store.

## Acceptance Criteria
- AC-001: Given a long requested file whose goal-relevant phrase occurs near the end, the selected range contains that phrase and starts after line 1.
- AC-002: Given no query-term match, selection uses a deterministic prefix fallback and remains within budget.
- AC-003: Every selected item declares `authority`, `selection_strategy`, `matched_terms`, `relevance_score`, exact line bounds, source hash, and content.
- AC-004: Repository guidance is `repository_instruction`; code, specs, tests, manifests, and documentation are `evidence_only`; the pack exposes the handling rule.
- AC-005: Missing or unreadable requested paths yield `insufficient`; truncation, freshness warnings, or omitted high-priority evidence yield `review_required`; complete clean context yields `sufficient`.
- AC-006: A valid enabled interaction profile appears in shared and task context packs with only supported typed fields and does not change selected sources.
- AC-007: Disabled, missing, or invalid interaction configuration produces an explicit status, no unsafe values, and no context-generation failure.
- AC-008: The v3 JSON schema, project-context skill contract, data-contract reference, configuration docs, and migration notes agree.
- AC-009: Public docs give copyable prompt/context and personalization patterns; they cover preferred address, language, response style, technical depth, and update cadence while explaining user control and the limits of persona prompting.
- AC-010: Focused unit tests, repository script tests, catalog generation, docs validation, strict MkDocs build, and SDD gates pass.

## Out of Scope
- AI character personas, demographic simulation, emotional attachment, or anthropomorphic behavior.
- A claim that calling an AI or user by name improves factual accuracy or reasoning.
- Passive mining of chat history, connected apps, email, calendars, or personal files.
- Free-form custom instructions that can conflict with governance or safety controls.
- Semantic embeddings, vector databases, remote retrieval, model calls, or provider-specific prompt APIs.
- Automatic edits to a consumer's private user configuration.
- Replacing host-level system or developer instruction hierarchy.

## Assumptions
- Quick flow is appropriate because changes are local, reversible, and covered by deterministic tests.
- `config.resolved.json` is the canonical local resolved configuration when present.
- Interaction preferences are explicit user choices, not verified identity or inferred memory.
- A typed profile is safer, smaller, and more testable than arbitrary persistent instructions.
- Lexical goal relevance is a transparent improvement over prefix-only clipping even though it is not semantic retrieval.
- Main-branch implementation is accepted from the user's ongoing direct workflow.

## Open Questions
No blocking questions. Future evaluation may compare lexical range selection with semantic or hybrid retrieval on a representative task corpus; that is intentionally outside this dependency-free change.

## Decision Status
All blocking decisions are resolved by DEC-001, DEC-003, and DEC-004. DEC-004 supersedes the preferred-name-only scope in DEC-002: preferred name remains one optional field inside a broader typed interaction profile. The change adds no new skill, persona, or implicit conversational memory.
