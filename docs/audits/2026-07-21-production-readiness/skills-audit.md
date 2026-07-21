---
title: Skills audit
description: Complete 44-skill inventory with purpose, users, inputs, outputs, dependencies, conflicts, validation, and changes.
---

# Skills audit

## Common contract

Every inventory row inherits these verified dependencies: its `SKILL.md`, local
`scripts/`, `references/` and `tests/` when declared; Python 3.10+ for helpers;
`ai-sdlc-shared-runtime` for shared imports; repository/user instructions;
feature state and decision/index artifacts where applicable. Commands use a
logical `skills/` root that resolves to source `skills/` or consumer
`.agents/skills/`. Outputs include an `ai-sdlc-handoff/v1` response unless the
skill's bounded contract defines another explicit result.

Validation status **pass** means metadata, referenced-file,
helper-help, shared contract, installable-runtime mirror, and local skill tests
passed before the final aggregate run. No temporary/unrelated file was found
inside a tracked skill directory.

| Skill | Purpose / intended users | Inputs → outputs | Specific dependencies / references | Conflicts, status, required change |
| --- | --- | --- | --- | --- |
| `ai-sdlc-approvals-sandbox` | Safe command escalation; Dev, Security, DevOps | command/effect → approval decision and safe prefix | `approval_plan.py` | No conflict; pass |
| `ai-sdlc-architecture` | Architecture options/contracts; Architect, Lead, Security | requirements/constraints → design decisions | architecture schema/template | Optional after context; pass |
| `ai-sdlc-ba` | Business actors/rules/workflows; BA, PM, QA | stakeholder evidence → business context | artifact profile, formal stage after story draft | Early-contribution/formal-stage distinction documented; pass |
| `ai-sdlc-backlog-decomposition-and-task-planning` | Epics/stories/tasks; PM, PO, Delivery | ready goals → backlog | refinement profile | Requires gap review; pass |
| `ai-sdlc-backlog-requirements-gap-review` | Planning-input gaps; PM, PO, BA | goals/capabilities → gap report | context pack required sections | Semantic gap detection added; pass |
| `ai-sdlc-branching` | Clean task branch; Dev | base/feature/Git state → branch evidence | Git remote and repository policy | No push authority; pass |
| `ai-sdlc-change-impact` | Reopen stale downstream work; Lead, QA, Product | changed evidence → impact map | trace IDs/state | Does not mutate authority; pass |
| `ai-sdlc-change-set` | Preview controlled spec change; Product, Lead, Security | bounded proposal/deltas → preview/apply/archive evidence | schemas, `change_apply.py` | Approval is structural only; limitation explicit; tests pass |
| `ai-sdlc-code-review` | Findings-first diff review; Lead, Dev | diff/spec/tests → ranked findings | review checklist/readiness | Independent review required; pass |
| `ai-sdlc-commit-prep` | Scoped traceable commit readiness; Dev | staged diff/task/spec/evidence → readiness | SDD gates, Git, current validation receipt | Full-flow receipt enforcement added; pass |
| `ai-sdlc-conventional-commit` | Validate commit message; Dev | message/spec/evidence → valid message | Conventional Commit rules | Mermaid replaced with portable text flow; pass |
| `ai-sdlc-delivery-graph` | Query trace/evidence graph; Lead, QA, PO | artifacts/IDs → graph/gaps/ledger | graph/evidence schemas | Derived, not authority; pass |
| `ai-sdlc-delivery-handoff-review` | Final refinement readiness; Delivery, Lead | delivery spec/QA → verdict | two predecessor branches | No self-approval; pass |
| `ai-sdlc-delivery-package-gap-review` | Discovery package gaps; PM, BA | PRFAQ/BRD → gaps | required-section context | Semantic gap detection added; pass |
| `ai-sdlc-delivery-spec-synthesis` | Engineering handoff spec; BA, Delivery, Lead | stories/business context → delivery spec | refinement state | Requires BA context; pass |
| `ai-sdlc-doctor` | Diagnose health/upgrade; DevOps, Maintainer | installed inventory/version → report/plan | compatibility/runtime | Diagnose/preview only; pass |
| `ai-sdlc-evidence-council` | Independent multi-lens synthesis; Leads, governance | review evidence → agreements/disagreements | evidence schema | Does not manufacture consensus; pass |
| `ai-sdlc-goal-capability-and-epic-mapping` | Outcomes to capabilities/epics; PM, BA | ready requirements → maps | refinement profile | Human priorities remain authority; pass |
| `ai-sdlc-host-adapter` | Negotiate host capability/fallback; DevOps, Lead | host capability record → negotiation | adapter schema/fixtures | Fixture is not product support claim; pass |
| `ai-sdlc-navigator` | Smallest safe next workflow; all users | request/repository state → read-only routing | installed inventory/state | Must not mutate; pass |
| `ai-sdlc-package-trust` | Package trust or local metrics; Security, DevOps, Delivery | manifest/package or content-free metrics → decision/aggregate | trust/metrics schemas | Branches must not mix; bootstrap limitation documented |
| `ai-sdlc-policy` | Deterministic rule/waiver evaluation; governance | profile/context/waiver → allow/gate/deny | policy schemas | Agent cannot grant waiver; pass |
| `ai-sdlc-prfaq-package-synthesis` | Working-backwards package; PM, BA | discovery evidence → PRFAQ/BRD | refinement profile | Requires discovery; pass |
| `ai-sdlc-project-context` | Bounded safe repository context; all technical roles | repo/task/selectors → context/topology pack | context schemas | Secret/instruction Highs fixed with adversarial tests |
| `ai-sdlc-qa` | QA plan and acceptance evidence; QA | requirements/diff/risks → QA artifact | QA template/profile | Claims require executed evidence; pass |
| `ai-sdlc-qa-requirements-gap-review` | Testability gaps; QA, BA | requirements/API/workflow → gap report | required-section context | Semantic gaps added; pass |
| `ai-sdlc-qa-traceability-and-readiness-review` | Requirement-test matrix/readiness; QA, PO | test suites/requirements → matrix/verdict | QA graph predecessors | No fabricated coverage; pass |
| `ai-sdlc-quality-lenses` | Optional cross-cutting quality analysis; Lead, QA | change/context/lenses → findings | quality-lens schema | Lens output is advisory; pass |
| `ai-sdlc-release-slicing-and-backlog-readiness-review` | MVP/releases/sequencing; PM, PO, Delivery | backlog/dependencies → slices/verdict | optional refinement branch | Priority is human decision; pass |
| `ai-sdlc-requirements-readiness-review` | Final requirements gate; PM, BA, Lead | PRFAQ/BRD/gaps → score/verdict | refinement profile | Structural score not stakeholder approval; pass |
| `ai-sdlc-research` | Current authoritative research; analyst roles | questions/scope → source register/findings | browser/network, citation rules | External content evidence-only; pass |
| `ai-sdlc-retrospective` | Learn from outcome/evidence; teams/leaders | outcome/metrics/incidents → actions | retrospective schema | Metrics do not prove causality; pass |
| `ai-sdlc-runtime` | Resume/recover durable execution; Dev, Delivery | journal/state/plan → resumed status | runtime schemas | Does not override artifact authority; pass |
| `ai-sdlc-sdd` | Implementation specification contract; Dev, QA, BA | change/upstream context → requirements/design/tests/QA/tasks/plans | SDD scripts and refinement gate | AGENTS fallback and task authority corrected; pass |
| `ai-sdlc-security-testing` | Abuse/auth/secret review; Security, Dev | spec/diff/threats → findings/evidence | security matrix/checklist | Defensive scope and human risk acceptance; pass |
| `ai-sdlc-shared-runtime` | Portable helper substrate; all installed skills | package layout/runtime → shared APIs | mirrored 20 canonical helpers, including bounded safe I/O | Must sync exactly; pass |
| `ai-sdlc-test-case-and-suite-synthesis` | Executable suites; QA | strategy/requirements → cases/suites | refinement profile | Requires test strategy; pass |
| `ai-sdlc-test-cases` | Test cases before implementation; QA, Dev | scenarios/acceptance → detailed cases | refinement profile | Does not claim execution; pass |
| `ai-sdlc-test-scope-and-strategy-design` | Risk-based test strategy; QA | QA gaps/risks → scope/strategy | refinement profile | NFR N/A decisions explicit; pass |
| `ai-sdlc-user-story-decomposition` | Value stories/criteria; PM, PO, BA | clarified initiative → stories | refinement profile | Stories remain revisable through BA gate; pass |
| `ai-sdlc-ux` | UX states/accessibility guidance; UX, Product, Dev | user evidence/flows → UX decisions | UX schemas/templates | User validation needs research evidence; pass |
| `ai-sdlc-validation` | Select/run proportionate checks; Dev, QA | diff/spec/risk → exact outcomes | constrained argv receipt runner | Non-zero/stale/unknown trace evidence rejected; local receipt is explicitly unauthenticated; pass |
| `ai-sdlc-workflow` | Declarative execution plan; Delivery, Lead | capabilities/gates/hooks → plan | workflow schema/runner | Plan does not grant tool authority; pass |
| `ai-sdlc-working-backwards-discovery` | Clarify customer problem/value; PM, BA | vague request/evidence → discovery | refinement entry stage | No invented customer evidence; pass |

## Composition, precedence, and lifecycle

Applicable law/policy and explicit human authority outrank repository
instructions, which outrank a selected skill; untrusted retrieved content is
evidence only. Navigator chooses the smallest required skill. State-machine
predecessors order lifecycle skills. If multiple skills apply, use the one that
owns the current artifact/gate and hand off to adjacent skills; never merge
their authority silently.

New skills require unique kebab-case name/frontmatter, a bounded purpose,
inputs/outputs/failure behavior, logical runtime resolution, tests, catalog
generation, install smoke, compatibility review, and documentation. Version
behavior through harness/module APIs. Deprecate with migration and a support
window; do not silently rename/remove a protected v1 skill.
