---
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  feature: "007-context-and-prompt-engineering"
  artifact: "decision-log.md"
  path: "specs/007-context-and-prompt-engineering/decision-log.md"
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
  related_artifacts: []
  validation: []
  metatags:
    - "ai-sdlc"
    - "implementation"
    - "ai-sdlc-sdd"
    - "decision-log"
    - "approved"
    - "research-backed"
---

# Decision Log

| ID | Date | Status | Owner | Decision | Context/Evidence | Options Considered | Affected Artifacts | Validation/Trace Links |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| DEC-001 | 2026-07-20 | accepted | Dev / Head of AI Practice | Upgrade the existing context engine with deterministic goal-relevant ranges, authority labels, and an explicit sufficient-context gate instead of adding another skill. | Anthropic recommends the smallest high-signal context, progressive disclosure, and context-efficient tools; Lost in the Middle shows position-sensitive long-context degradation; Sufficient Context distinguishes generation failure from missing evidence. Sources: https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents ; https://arxiv.org/abs/2307.03172 ; https://arxiv.org/abs/2411.06037 | Add a new skill; document practices only; upgrade the existing engine (selected). | context engine, v3 schema/contracts, tests, context docs | AC-001 through AC-005; TC-001 through TC-005 |
| DEC-002 | 2026-07-20 | superseded | User / Dev | Support only a preferred user name as address-only personalization; do not add AI personas or infer identity, authority, expertise, demographics, or permission. | The user clarified that calling them by name was an example of a broader personalization feature, so the preferred-name-only scope is too narrow. | AI naming; expert persona; preferred user name only. | layered config, shared/task context metadata, tests, public guidance | Superseded by DEC-004 |
| DEC-003 | 2026-07-20 | accepted | Dev | Publish the behavioral additions as ai-sdlc-context-pack/v3 while keeping selector v2, topology v2, and existing CLI arguments compatible. | New required fields change the machine contract. Explicit versioning is safer than silently widening v2. OpenAI guidance also favors structured prompt boundaries, explicit instruction hierarchy, representative fixtures, and evaluation before prompt changes. Source: https://developers.openai.com/api/docs/guides/prompt-engineering | Mutate v2 in place; add optional unversioned fields; version v3 (selected). | schema, contract, skill, data contracts, migration docs | AC-003, AC-008, AC-010; TC-003, TC-008, TC-010 |
| DEC-004 | 2026-07-20 | accepted | User / Dev | Add a typed, opt-in interaction profile covering preferred address, language, response style, technical depth, and status-update cadence; keep it presentation-only, inspectable, removable, and separate from implicit memory or personas. | The user clarified that preferred name was an example. OpenAI, Anthropic, GitHub, and Google expose persistent personal preferences/custom instructions, project-scoped instructions, styles, and user controls. Typed fields fit this harness better than unbounded instructions or hidden chat mining. Sources: https://help.openai.com/en/articles/8096356-chat-preferences-for-chatgpt ; https://support.anthropic.com/en/articles/10185728-understanding-claude-s-personalization-features ; https://docs.github.com/en/copilot/concepts/prompting/response-customization ; https://support.google.com/gemini/answer/16598625 | Preferred-name only; arbitrary custom instructions; implicit chat memory; typed interaction profile (selected). | config defaults/resolver, shared/task context, tests, public docs | AC-006, AC-007, AC-008, AC-009; TC-006, TC-007, TC-008, TC-009 |
