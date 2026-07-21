---
title: Skills by role
description: Choose AI SDLC capabilities by Software Engineer, PM, PO, QA, or BA responsibility.
---

# Skills by role

Use this page when you know your responsibility but not the capability name. Each skill has one canonical guide and can appear under several roles. **Choose by task** lists common entry points for that role's work; **Shared and handoff** means the role contributes, reviews, or consumes evidence without implying ownership.

Role labels are discovery aids, not an authority model. Local policy and named decision owners still control repository permissions and protected decisions.

| Role | Jump to |
| --- | --- |
| QA | [QA skills](#qa) |
| BA | [BA skills](#ba) |
| PM | [PM skills](#pm) |
| PO | [PO skills](#po) |
| Software Engineer | [Software Engineer skills](#software-engineer) |

## QA

Own testability, coverage strategy, acceptance evidence, and QA readiness; product and release risk acceptance stays with the named human owner.

### Choose by task

| Choose when… | Role relationship | Start with | Required input | Next handoff |
| --- | --- | --- | --- | --- |
| Plan acceptance or regression work | Own or run QA work | [`ai-sdlc-qa`](skills/ai-sdlc-qa.md) | Accepted behavior and changed surface | QA gap review or test strategy |
| Find testability blockers | Own or run QA work | [`ai-sdlc-qa-requirements-gap-review`](skills/ai-sdlc-qa-requirements-gap-review.md) | Stories, specification, or QA scope | Requirements owner or test strategy |
| Choose coverage and execution priorities | Own or run QA work | [`ai-sdlc-test-scope-and-strategy-design`](skills/ai-sdlc-test-scope-and-strategy-design.md) | Testable requirements and risk context | Test-case design |
| Derive verifiable implementation scenarios | Own or run QA work | [`ai-sdlc-test-cases`](skills/ai-sdlc-test-cases.md) | Requirement IDs and expected outcomes | Automated tests or suite synthesis |
| Assemble executable suites | Own or run QA work | [`ai-sdlc-test-case-and-suite-synthesis`](skills/ai-sdlc-test-case-and-suite-synthesis.md) | Detailed cases and QA strategy | QA readiness review |
| Decide whether QA can execute | Own or run QA work | [`ai-sdlc-qa-traceability-and-readiness-review`](skills/ai-sdlc-qa-traceability-and-readiness-review.md) | Requirements, cases, suites, data, and environment | QA execution or earliest missing producer |
| Run focused implementation checks | Own or run QA work | [`ai-sdlc-validation`](skills/ai-sdlc-validation.md) | Changed files, expected behavior, and available commands | Code review or release handoff |

### Shared and handoff skills

| Group | Role relationship | Skill |
| --- | --- | --- |
| Entry and context | Supply intent or evidence | [`ai-sdlc-navigator`](skills/ai-sdlc-navigator.md) |
| Governance and operations | Consult or apply within role authority | [`ai-sdlc-policy`](skills/ai-sdlc-policy.md) |
| Handoff and recovery | Produce, consume, or reopen evidence | [`ai-sdlc-change-impact`](skills/ai-sdlc-change-impact.md) |
| Handoff and recovery | Produce, consume, or reopen evidence | [`ai-sdlc-delivery-graph`](skills/ai-sdlc-delivery-graph.md) |
| Handoff and recovery | Produce, consume, or reopen evidence | [`ai-sdlc-delivery-handoff-review`](skills/ai-sdlc-delivery-handoff-review.md) |
| Planning and delivery | Collaborate or resolve inputs | [`ai-sdlc-sdd`](skills/ai-sdlc-sdd.md) |
| Review and assurance | Contribute risk or review evidence | [`ai-sdlc-code-review`](skills/ai-sdlc-code-review.md) |
| Review and assurance | Contribute risk or review evidence | [`ai-sdlc-evidence-council`](skills/ai-sdlc-evidence-council.md) |
| Review and assurance | Contribute risk or review evidence | [`ai-sdlc-quality-lenses`](skills/ai-sdlc-quality-lenses.md) |
| Review and assurance | Contribute risk or review evidence | [`ai-sdlc-requirements-readiness-review`](skills/ai-sdlc-requirements-readiness-review.md) |
| Review and assurance | Contribute risk or review evidence | [`ai-sdlc-security-testing`](skills/ai-sdlc-security-testing.md) |

[Return to all roles](#skills-by-role)

## BA

Own actors, workflows, business rules, assumptions, and acceptance logic; product value and implementation design remain with their accountable roles.

### Choose by task

| Choose when… | Role relationship | Start with | Required input | Next handoff |
| --- | --- | --- | --- | --- |
| Clarify actors, rules, and behavior | Own or produce analysis | [`ai-sdlc-ba`](skills/ai-sdlc-ba.md) | Feature request or known business ambiguity | Gap review or story decomposition |
| Check discovery-package completeness | Own or produce analysis | [`ai-sdlc-delivery-package-gap-review`](skills/ai-sdlc-delivery-package-gap-review.md) | Discovery notes or PRFAQ package | Story decomposition or missing discovery producer |
| Gate requirements before planning | Own or produce analysis | [`ai-sdlc-requirements-readiness-review`](skills/ai-sdlc-requirements-readiness-review.md) | PRFAQ/BRD package and resolved delivery gaps | Goal/epic mapping or requirements owner |
| Check planning inputs before backlog work | Own or produce analysis | [`ai-sdlc-backlog-requirements-gap-review`](skills/ai-sdlc-backlog-requirements-gap-review.md) | Goals, roles, capabilities, and epics | Backlog decomposition or planning owner |
| Turn clarified scope into stories | Own or produce analysis | [`ai-sdlc-user-story-decomposition`](skills/ai-sdlc-user-story-decomposition.md) | Goals/epics and resolved delivery gaps | Delivery specification |
| Create the engineering behavior contract | Own or produce analysis | [`ai-sdlc-delivery-spec-synthesis`](skills/ai-sdlc-delivery-spec-synthesis.md) | Clarified stories, rules, and scenarios | QA strategy and delivery handoff |

### Shared and handoff skills

| Group | Role relationship | Skill |
| --- | --- | --- |
| Entry and context | Supply intent or evidence | [`ai-sdlc-navigator`](skills/ai-sdlc-navigator.md) |
| Entry and context | Supply intent or evidence | [`ai-sdlc-research`](skills/ai-sdlc-research.md) |
| Entry and context | Supply intent or evidence | [`ai-sdlc-working-backwards-discovery`](skills/ai-sdlc-working-backwards-discovery.md) |
| Handoff and recovery | Produce, consume, or reopen evidence | [`ai-sdlc-change-impact`](skills/ai-sdlc-change-impact.md) |
| Handoff and recovery | Produce, consume, or reopen evidence | [`ai-sdlc-delivery-graph`](skills/ai-sdlc-delivery-graph.md) |
| Handoff and recovery | Produce, consume, or reopen evidence | [`ai-sdlc-delivery-handoff-review`](skills/ai-sdlc-delivery-handoff-review.md) |
| Planning and delivery | Collaborate or resolve inputs | [`ai-sdlc-backlog-decomposition-and-task-planning`](skills/ai-sdlc-backlog-decomposition-and-task-planning.md) |
| Planning and delivery | Collaborate or resolve inputs | [`ai-sdlc-goal-capability-and-epic-mapping`](skills/ai-sdlc-goal-capability-and-epic-mapping.md) |
| Planning and delivery | Collaborate or resolve inputs | [`ai-sdlc-prfaq-package-synthesis`](skills/ai-sdlc-prfaq-package-synthesis.md) |
| Planning and delivery | Collaborate or resolve inputs | [`ai-sdlc-release-slicing-and-backlog-readiness-review`](skills/ai-sdlc-release-slicing-and-backlog-readiness-review.md) |
| Planning and delivery | Collaborate or resolve inputs | [`ai-sdlc-ux`](skills/ai-sdlc-ux.md) |
| Review and assurance | Contribute risk or review evidence | [`ai-sdlc-qa-requirements-gap-review`](skills/ai-sdlc-qa-requirements-gap-review.md) |
| Review and assurance | Contribute risk or review evidence | [`ai-sdlc-quality-lenses`](skills/ai-sdlc-quality-lenses.md) |

[Return to all roles](#skills-by-role)

## PM

Own customer problem, value, outcomes, scope, priority, and product trade-offs; agents may synthesize evidence but never accept these decisions.

### Choose by task

| Choose when… | Role relationship | Start with | Required input | Next handoff |
| --- | --- | --- | --- | --- |
| Find the smallest safe next action | Own product decision inputs | [`ai-sdlc-navigator`](skills/ai-sdlc-navigator.md) | Request plus current repository control records | One owning skill |
| Frame an unclear customer problem | Own product decision inputs | [`ai-sdlc-working-backwards-discovery`](skills/ai-sdlc-working-backwards-discovery.md) | Audience, observed problem, and available evidence | PRFAQ synthesis |
| Create a decision-ready product package | Own product decision inputs | [`ai-sdlc-prfaq-package-synthesis`](skills/ai-sdlc-prfaq-package-synthesis.md) | Validated discovery notes | Requirements readiness |
| Map outcomes to delivery structure | Own product decision inputs | [`ai-sdlc-goal-capability-and-epic-mapping`](skills/ai-sdlc-goal-capability-and-epic-mapping.md) | Ready requirements package | Backlog gap review |
| Create delivery backlog and stories | Own product decision inputs | [`ai-sdlc-backlog-decomposition-and-task-planning`](skills/ai-sdlc-backlog-decomposition-and-task-planning.md) | Ready goals, capabilities, and epics | Release slicing |
| Define MVP/release sequence | Own product decision inputs | [`ai-sdlc-release-slicing-and-backlog-readiness-review`](skills/ai-sdlc-release-slicing-and-backlog-readiness-review.md) | Decomposed backlog and dependencies | Delivery handoff or planning approval |

### Shared and handoff skills

| Group | Role relationship | Skill |
| --- | --- | --- |
| Entry and context | Supply intent or evidence | [`ai-sdlc-research`](skills/ai-sdlc-research.md) |
| Governance and operations | Consult or apply within role authority | [`ai-sdlc-policy`](skills/ai-sdlc-policy.md) |
| Handoff and recovery | Produce, consume, or reopen evidence | [`ai-sdlc-change-impact`](skills/ai-sdlc-change-impact.md) |
| Handoff and recovery | Produce, consume, or reopen evidence | [`ai-sdlc-delivery-graph`](skills/ai-sdlc-delivery-graph.md) |
| Handoff and recovery | Produce, consume, or reopen evidence | [`ai-sdlc-delivery-handoff-review`](skills/ai-sdlc-delivery-handoff-review.md) |
| Handoff and recovery | Produce, consume, or reopen evidence | [`ai-sdlc-retrospective`](skills/ai-sdlc-retrospective.md) |
| Planning and delivery | Collaborate or resolve inputs | [`ai-sdlc-ba`](skills/ai-sdlc-ba.md) |
| Planning and delivery | Collaborate or resolve inputs | [`ai-sdlc-backlog-requirements-gap-review`](skills/ai-sdlc-backlog-requirements-gap-review.md) |
| Planning and delivery | Collaborate or resolve inputs | [`ai-sdlc-delivery-package-gap-review`](skills/ai-sdlc-delivery-package-gap-review.md) |
| Planning and delivery | Collaborate or resolve inputs | [`ai-sdlc-user-story-decomposition`](skills/ai-sdlc-user-story-decomposition.md) |
| Planning and delivery | Collaborate or resolve inputs | [`ai-sdlc-ux`](skills/ai-sdlc-ux.md) |
| Review and assurance | Contribute risk or review evidence | [`ai-sdlc-evidence-council`](skills/ai-sdlc-evidence-council.md) |
| Review and assurance | Contribute risk or review evidence | [`ai-sdlc-qa-requirements-gap-review`](skills/ai-sdlc-qa-requirements-gap-review.md) |
| Review and assurance | Contribute risk or review evidence | [`ai-sdlc-quality-lenses`](skills/ai-sdlc-quality-lenses.md) |
| Review and assurance | Contribute risk or review evidence | [`ai-sdlc-requirements-readiness-review`](skills/ai-sdlc-requirements-readiness-review.md) |

[Return to all roles](#skills-by-role)

## PO

Own day-to-day backlog readiness, acceptance clarity, sequencing, and product handoffs within delegated product authority.

### Choose by task

| Choose when… | Role relationship | Start with | Required input | Next handoff |
| --- | --- | --- | --- | --- |
| Find the smallest safe next action | Use to route work | [`ai-sdlc-navigator`](skills/ai-sdlc-navigator.md) | Request plus current repository control records | One owning skill |
| Check planning inputs before backlog work | Collaborate and review | [`ai-sdlc-backlog-requirements-gap-review`](skills/ai-sdlc-backlog-requirements-gap-review.md) | Goals, roles, capabilities, and epics | Backlog decomposition or planning owner |
| Create delivery backlog and stories | Prioritize and review | [`ai-sdlc-backlog-decomposition-and-task-planning`](skills/ai-sdlc-backlog-decomposition-and-task-planning.md) | Ready goals, capabilities, and epics | Release slicing |
| Turn clarified scope into stories | Collaborate and accept clarity | [`ai-sdlc-user-story-decomposition`](skills/ai-sdlc-user-story-decomposition.md) | Goals/epics and resolved delivery gaps | Delivery specification |
| Gate requirements before planning | Review and resolve product gaps | [`ai-sdlc-requirements-readiness-review`](skills/ai-sdlc-requirements-readiness-review.md) | PRFAQ/BRD package and resolved delivery gaps | Goal/epic mapping or requirements owner |
| Define MVP/release sequence | Own sequencing within delegation | [`ai-sdlc-release-slicing-and-backlog-readiness-review`](skills/ai-sdlc-release-slicing-and-backlog-readiness-review.md) | Decomposed backlog and dependencies | Delivery handoff or planning approval |

### Shared and handoff skills

| Group | Role relationship | Skill |
| --- | --- | --- |
| Entry and context | Supply intent or evidence | [`ai-sdlc-working-backwards-discovery`](skills/ai-sdlc-working-backwards-discovery.md) |
| Handoff and recovery | Produce, consume, or reopen evidence | [`ai-sdlc-change-impact`](skills/ai-sdlc-change-impact.md) |
| Handoff and recovery | Produce, consume, or reopen evidence | [`ai-sdlc-delivery-graph`](skills/ai-sdlc-delivery-graph.md) |
| Handoff and recovery | Produce, consume, or reopen evidence | [`ai-sdlc-delivery-handoff-review`](skills/ai-sdlc-delivery-handoff-review.md) |
| Handoff and recovery | Produce, consume, or reopen evidence | [`ai-sdlc-retrospective`](skills/ai-sdlc-retrospective.md) |
| Planning and delivery | Collaborate or resolve inputs | [`ai-sdlc-ba`](skills/ai-sdlc-ba.md) |
| Planning and delivery | Collaborate or resolve inputs | [`ai-sdlc-delivery-spec-synthesis`](skills/ai-sdlc-delivery-spec-synthesis.md) |
| Planning and delivery | Collaborate or resolve inputs | [`ai-sdlc-prfaq-package-synthesis`](skills/ai-sdlc-prfaq-package-synthesis.md) |
| Planning and delivery | Collaborate or resolve inputs | [`ai-sdlc-test-scope-and-strategy-design`](skills/ai-sdlc-test-scope-and-strategy-design.md) |
| Review and assurance | Contribute risk or review evidence | [`ai-sdlc-qa-requirements-gap-review`](skills/ai-sdlc-qa-requirements-gap-review.md) |
| Review and assurance | Contribute risk or review evidence | [`ai-sdlc-qa-traceability-and-readiness-review`](skills/ai-sdlc-qa-traceability-and-readiness-review.md) |
| Review and assurance | Contribute risk or review evidence | [`ai-sdlc-quality-lenses`](skills/ai-sdlc-quality-lenses.md) |

[Return to all roles](#skills-by-role)

## Software Engineer

Own technical design, implementation correctness, testable task boundaries, review resolution, and engineering risk recommendations.

### Choose by task

| Choose when… | Role relationship | Start with | Required input | Next handoff |
| --- | --- | --- | --- | --- |
| Find the smallest safe next action | Own or execute engineering work | [`ai-sdlc-navigator`](skills/ai-sdlc-navigator.md) | Request plus current repository control records | One owning skill |
| Ground work in repository evidence | Own or execute engineering work | [`ai-sdlc-project-context`](skills/ai-sdlc-project-context.md) | Repository sources and one task intent | Navigator or SDD |
| Create or verify the task branch | Own or execute engineering work | [`ai-sdlc-branching`](skills/ai-sdlc-branching.md) | Accepted task/spec and Git state | SDD or implementation |
| Specify a behavior or architecture change | Own or execute engineering work | [`ai-sdlc-sdd`](skills/ai-sdlc-sdd.md) | Clear behavior and affected system | Bounded implementation tasks |
| Derive verifiable implementation scenarios | Own or execute engineering work | [`ai-sdlc-test-cases`](skills/ai-sdlc-test-cases.md) | Requirement IDs and expected outcomes | Automated tests or suite synthesis |
| Run focused implementation checks | Own or execute engineering work | [`ai-sdlc-validation`](skills/ai-sdlc-validation.md) | Changed files, expected behavior, and available commands | Code review or release handoff |
| Review a completed change | Own or execute engineering work | [`ai-sdlc-code-review`](skills/ai-sdlc-code-review.md) | Diff plus accepted contract and tests | Finding resolution or commit prep |
| Prepare an auditable atomic commit | Own or execute engineering work | [`ai-sdlc-commit-prep`](skills/ai-sdlc-commit-prep.md) | Completed scope, validation, and review evidence | Human commit/release workflow |

### Shared and handoff skills

| Group | Role relationship | Skill |
| --- | --- | --- |
| Entry and context | Supply intent or evidence | [`ai-sdlc-research`](skills/ai-sdlc-research.md) |
| Governance and operations | Consult or apply within role authority | [`ai-sdlc-approvals-sandbox`](skills/ai-sdlc-approvals-sandbox.md) |
| Governance and operations | Consult or apply within role authority | [`ai-sdlc-doctor`](skills/ai-sdlc-doctor.md) |
| Governance and operations | Consult or apply within role authority | [`ai-sdlc-host-adapter`](skills/ai-sdlc-host-adapter.md) |
| Governance and operations | Consult or apply within role authority | [`ai-sdlc-package-trust`](skills/ai-sdlc-package-trust.md) |
| Governance and operations | Consult or apply within role authority | [`ai-sdlc-policy`](skills/ai-sdlc-policy.md) |
| Governance and operations | Consult or apply within role authority | [`ai-sdlc-runtime`](skills/ai-sdlc-runtime.md) |
| Governance and operations | Consult or apply within role authority | [`ai-sdlc-shared-runtime`](skills/ai-sdlc-shared-runtime.md) |
| Governance and operations | Consult or apply within role authority | [`ai-sdlc-workflow`](skills/ai-sdlc-workflow.md) |
| Handoff and recovery | Produce, consume, or reopen evidence | [`ai-sdlc-change-impact`](skills/ai-sdlc-change-impact.md) |
| Handoff and recovery | Produce, consume, or reopen evidence | [`ai-sdlc-change-set`](skills/ai-sdlc-change-set.md) |
| Handoff and recovery | Produce, consume, or reopen evidence | [`ai-sdlc-conventional-commit`](skills/ai-sdlc-conventional-commit.md) |
| Handoff and recovery | Produce, consume, or reopen evidence | [`ai-sdlc-delivery-graph`](skills/ai-sdlc-delivery-graph.md) |
| Handoff and recovery | Produce, consume, or reopen evidence | [`ai-sdlc-delivery-handoff-review`](skills/ai-sdlc-delivery-handoff-review.md) |
| Handoff and recovery | Produce, consume, or reopen evidence | [`ai-sdlc-retrospective`](skills/ai-sdlc-retrospective.md) |
| Planning and delivery | Collaborate or resolve inputs | [`ai-sdlc-architecture`](skills/ai-sdlc-architecture.md) |
| Planning and delivery | Collaborate or resolve inputs | [`ai-sdlc-delivery-spec-synthesis`](skills/ai-sdlc-delivery-spec-synthesis.md) |
| Planning and delivery | Collaborate or resolve inputs | [`ai-sdlc-qa`](skills/ai-sdlc-qa.md) |
| Planning and delivery | Collaborate or resolve inputs | [`ai-sdlc-ux`](skills/ai-sdlc-ux.md) |
| Review and assurance | Contribute risk or review evidence | [`ai-sdlc-evidence-council`](skills/ai-sdlc-evidence-council.md) |
| Review and assurance | Contribute risk or review evidence | [`ai-sdlc-quality-lenses`](skills/ai-sdlc-quality-lenses.md) |
| Review and assurance | Contribute risk or review evidence | [`ai-sdlc-security-testing`](skills/ai-sdlc-security-testing.md) |

[Return to all roles](#skills-by-role)

## When the role is shared

Use the relationship shown here to find the guide, then use the project's RACI to identify who supplies inputs, who reviews, and who approves. Do not copy a guide into a role-specific page or let overlap imply authority.

Need an alphabetical lookup? Use the [complete skill catalog](skills.md). Need lifecycle order? Use the [workflow map](workflow-map.md).
