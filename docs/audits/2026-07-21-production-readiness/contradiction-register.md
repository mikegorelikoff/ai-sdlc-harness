---
title: Contradiction register
description: Conflicting instructions and concepts, their chosen resolution, and regression evidence.
---

# Contradiction register

| ID | Conflict / affected files | Competing interpretations | Chosen resolution | Regression check |
| --- | --- | --- | --- | --- |
| CR-001 | Stable `v1.2.0` install vs main docs | Main is stable; main is preview | Main is labeled maintainer preview; stable's shallow smoke is distinguished from its reproducible complete-workflow defect | Candidate and exact-release clean smokes |
| CR-002 | `skills/...` commands vs `.agents/skills/...` installation | Source-only path; consumer path | Every skill defines logical path resolution; consumer how-tos use `.agents` | All-skill contract test; consumer helper smoke |
| CR-003 | “supported agent” vs installer target count | CLI recognition means support; support requires evidence | Support matrix separates tested, limited, candidate, and installer-recognized | Docs coverage/link checks |
| CR-004 | Codex-specific output wording vs portability | Only Codex; host-neutral skill | “active agent response” is canonical; compatibility validator accepts v1 wording alias | 44-skill contract and compatibility tests |
| CR-005 | `tasks.md` vs `plan.toon` authority | Machine status wins; task checkbox wins | Reviewed `tasks.md` checkbox is authority; both plans are regenerated projections | SDD plan-link tests |
| CR-006 | Mandatory `AGENTS.md` vs consumer fixture without it | Block always; invent a rule | Use repository guidance when present; otherwise record default risk rubric | SDD guide/catalog validation |
| CR-007 | Product Manager vs Product Owner accountability | Both own priority/acceptance | PM owns strategy/outcomes; delegated PO owns daily ordering/acceptance; one local accountable owner per gate | Role guides and RACI review |
| CR-008 | BA before stories vs executable BA stage after story draft | BA absent early; BA formal stage only | BA contributes evidence early; formal post-draft BA gate challenges and consolidates before delivery spec | Role guide and stage-contract validator |
| CR-009 | Approval record vs authenticated human authority | Valid JSON proves approval; protected system proves approval | Helper reports structural validity only; external protected authorization is required | Change-apply test asserts limitation status |
| CR-010 | Context documents vs executable instructions | Any `.instructions.md` has authority; evidence is untrusted | Only conservative root/host paths get instruction authority; all other content is evidence-only | Adversarial context test |
| CR-011 | Zero `gaps` vs semantically incomplete source | Gaps mean access only; gaps imply readiness | TOON reports missing required Markdown evidence sections explicitly | Decisions-only regression fixture |
| CR-012 | Read-only analysis vs implicit context writes | Full analysis always caches; writes require request | Derived context writes occur only through explicit cache/write intent | Shared context tests |
| CR-013 | Release audit vs legitimate later commits | Exact range must end at roadmap; completed history can have maintenance | Audit requires exact ordered sequence at base and allows later maintenance | Compatibility tests and documented command |
| CR-014 | Offline first build vs empty cache | First use is offline; offline requires cache | First resolution is online; offline is a second verification or mirror path | Empty-cache baseline record and updated guide |
| CR-015 | `skills update` vs repair/upgrade | CLI update repairs or advances release; portable local-source install has no updateable lock | Both repair and upgrade use exact-commit reinstall; retired managed skills require a human ownership checkpoint | Update guide and clean reinstall review |
| CR-016 | Local receipt vs authenticated execution proof | A matching self-hash proves execution; a workspace writer can recompute it | Receipt proves current local structure and recorded exits only; protected CI attestation supplies independent authority | Forge/re-hash and stale/nonzero receipt tests |
| CR-017 | State `done` vs artifact evidence | Direct CLI completion can assert done; completion must bind evidence | Completion requires a begun matching stage and an existing canonical artifact; full refinement also requires finalized metadata | State-machine direct-CLI attack test |
| CR-018 | Generated spec index vs source graph | Every discovered index row is source evidence; root projections duplicate/invent graph nodes | Root generated indexes are excluded as graph sources; canonical artifacts remain authoritative | Delivery-graph projection regression test |
| CR-019 | Lifecycle product acceptance vs implementation completion | Passing code/tests implies product acceptance; accountable Product Owner records outcome | Product acceptance is a separate canonical decision-log record linked to requirement and validation evidence | Product-acceptance guide and trace review |
| CR-020 | Resolved configuration vs enforced policy | Any resolved rigor/gate value changes workflows; only interaction is consumed | Installed configuration is presentation-only; `ai-sdlc-policy` plus repository/platform settings enforce delivery controls | Installed configuration smoke and policy tests |
| CR-021 | Historical task gaps vs prospective commit policy | Historical gaps are merely observed; future traced commits prevent recurrence | Preserve 41 immutable gaps, but require canonical `Task: TNNN` in every traced/full SDD commit | Conventional-commit tests and PO re-review |
| CR-022 | Managed inventory vs all installed skills | Harness owns every `.agents/skills` directory; harness owns only its recorded selection | Inventory names harness-managed paths, validates full/subset selection, and permits unrelated skill directories | Install-record coexistence/subset tests |
| CR-023 | Receipt freshness vs lifecycle writes | Every later evidence write invalidates validation; derived recording must not invalidate its prerequisite | Finalize `validation.md` first; receipt binds source/spec/test/plan; canonical state/index/downstream review records are explicit derived exclusions | Source-stale plus post-state/review-current receipt tests |
| CR-024 | SDD abbreviation | SDD means this repository's lifecycle; SDD always means a Software Design Document | Canonical term is Specification-driven development; other uses are explicitly distinguished | Foundation/glossary/nav/catalog checks |
| CR-025 | Local hashes vs authenticated evidence | Runtime/validation hashes were described in language that could imply independent proof | Hashes provide local structure and staleness detection only; protected Git, trusted CI, or external audit logs provide independent assurance | Security regressions and trust-language review |

No unresolved conceptual contradiction is accepted as canonical. Legal license
selection and external platform settings are limitations, not competing
repository instructions.
