---
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "007-context-and-prompt-engineering"
  artifact: "test-cases.md"
  path: "specs/007-context-and-prompt-engineering/test-cases.md"
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
  related_artifacts:
    - "specs/007-context-and-prompt-engineering/decision-log.md"
    - "specs/007-context-and-prompt-engineering/design.md"
    - "specs/007-context-and-prompt-engineering/qa.md"
    - "specs/007-context-and-prompt-engineering/requirements.md"
    - "specs/007-context-and-prompt-engineering/tasks.md"
  validation: []
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-sdd"
    - "test-cases"
    - "approved"
    - "research-backed"
---

# Test Cases

## Scope
Validate task-aware range selection, authority separation, sufficient-context decisions, personalization safety, budget determinism, compatibility documentation, and rendered guidance.

## Scenario Matrix
| ID | Acceptance | Scenario | Expected |
| --- | --- | --- | --- |
| TC-001 | AC-001 | Relevant phrase is near the end of a long requested file. | Selected range starts after line 1 and contains the phrase. |
| TC-002 | AC-002 | Goal has no term in a candidate. | Strategy is `prefix_fallback`; output is deterministic and in budget. |
| TC-003 | AC-003 | Build a normal task pack. | Every selected row includes all v3 range metadata. |
| TC-004 | AC-004 | Select AGENTS.md and source code. | AGENTS is repository instruction; source is evidence-only; handling rule is present. |
| TC-005 | AC-005 | Request a missing file, then a truncated current file. | Missing is insufficient; truncation is review_required with a targeted next read. |
| TC-006 | AC-006 | Enable preferred address, language, concise style, practitioner depth, and milestone updates. | Both pack families expose the typed presentation-only profile; technical selection is unchanged. |
| TC-007 | AC-007 | Omit, disable, and provide invalid interaction configuration. | Status is not_configured, disabled, or invalid; unsafe values are absent. |
| TC-008 | AC-008 | Inspect schemas and contracts. | Every task-pack reference names v3 and required fields agree. |
| TC-009 | AC-009 | Review public practice and configuration guidance. | Docs cover modern customization patterns, user control, typed fields, and why this is not persona or implicit memory. |
| TC-010 | AC-010 | Run focused code, docs, generation, build, and SDD gates. | All commands exit zero. |

## Layer Mapping
- Unit: query normalization, range selection, authority, sufficiency, personalization parsing.
- Integration: CLI JSON/TOON/Markdown output, fingerprints, config resolution, catalog generation.
- Documentation: source validator, strict MkDocs, rendered link validation.
- Governance: SDD clarify, checklist, plan, analyze, and validate gates.

## Automation Plan
Extend `test_context_engine.py`, `test_config.py`, and shared script tests. Reuse the existing documentation and catalog validators. Add no network-dependent tests.

## Open Gaps
No model-based quality benchmark or implicit-memory system is added. Lexical retrieval quality and real-user preference usefulness should later be evaluated on representative tasks before expanding the profile or considering semantic retrieval.
