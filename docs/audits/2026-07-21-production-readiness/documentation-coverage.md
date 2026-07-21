---
title: Documentation coverage matrix
description: Required concepts, roles, tutorials, adoption concerns, and their canonical pages.
---

# Documentation coverage matrix

| Required coverage | Canonical pages | Status |
| --- | --- | --- |
| Software development, SDLC stages/roles/failures/debt/scope | [Software delivery foundations](../../foundations/software-delivery.md) | Covered |
| AI, ML, LLM, generative AI, prompts, tokens, context, probability, confabulation | [AI foundations](../../foundations/ai-foundations.md), [glossary](../../foundations/glossary.md) | Covered |
| AI-assisted development, tool use, planning/code/test/review/debug/refactor, accountability | [AI SDLC](../../foundations/ai-sdlc.md), [responsibilities](../../foundations/responsibilities.md) | Covered |
| SDD, request/requirement/spec/plan/task/evidence, FR/NFR, AC, assumptions, risks, trace, ready/done | [Software delivery foundations](../../foundations/software-delivery.md), [SDD](../../foundations/sdd.md) | Covered |
| Agents/sub-agents/orchestration/isolation/delegation/disagreement/injection/recovery | [Agents and skills](../../foundations/agents-and-skills.md) | Covered |
| Skill vs prompt/command/agent/template/workflow; inputs/outputs/precedence/version/test/deprecation | [Agents and skills](../../foundations/agents-and-skills.md), [skills audit](skills-audit.md) | Covered |
| Harness purpose/structure/lifecycle/install/config/first use/artifacts/gates/customization/troubleshooting/security/limits | [Start](../../start.md), [Install](../../how-to/install.md), [Directory layout](../../reference/directory-layout.md), [Governance](../../operations/governance.md), [Limitations](../../explanation/maturity-limitations.md) | Covered |
| Git/terminal prerequisites and Codex host bootstrap | [Git and terminal primer](../../foundations/git-and-terminal-primer.md), [Set up Codex](../../how-to/setup-codex.md), [Supported environments](../../reference/supported-environments.md) | Covered; Codex 0.144.1 pilot only |
| Presentation preferences versus enforceable delivery policy | [Customize presentation and policy](../../how-to/customize.md), [Configuration](../../explanation/configuration.md), [Evaluate policy](../../how-to/evaluate-policy.md) | Covered with installed default and explicit trust boundary |
| Trainee, engineer, lead, QA, BA, PO, PM, Delivery, Engineering Manager, VP, CTO, DevOps, Security | [Role index](../../roles/index.md) and its 13 child guides | Covered |
| Small feature | [First feature](../../tutorials/first-feature.md) | Runnable |
| Defect, refactor, API, DB schema, tests, unclear request, AI review, failed work, changed requirements | [Change patterns](../../tutorials/change-patterns.md) | Inspectable patterns; not all fixture-backed |
| Pilot, tools, controls, classification, audit, metrics, training, rollout, ownership, support, compliance, standardization, exceptions, improvement | [Adoption](../../adoption/index.md), [Governance](../../operations/governance.md), [Operating model](../../operations/operating-model.md), [Support](../../operations/index.md) | Covered with organization-specific decisions required |
| Install prerequisites/host matrix/update/uninstall/offline/recovery | [Install](../../how-to/install.md), [Supported environments](../../reference/supported-environments.md), [Update](../../how-to/update.md) | Covered |
| Review, PR, merge, product acceptance, rollback | [Review and merge](../../how-to/review-and-merge.md), [Record product acceptance](../../how-to/record-product-acceptance.md) | Covered |

Depth is distributed through linked chapter groups rather than one inflated
page. Topic coverage and navigation are mechanically checked; comprehension
and adequacy of depth still require role-based pilot feedback.
