# AI SDLC Skill Library

This repository contains reusable, tool-agnostic AI SDLC skills for AI-ready software delivery workflows.

The library is generic: skills here are not tied to one client, account, project, or technology stack. They provide repeatable Markdown output patterns for product discovery, BA refinement, QA planning, test design, delivery handoff, developer implementation, validation, review, and commit preparation.

The skills are plain Markdown instruction folders. They are not tied to Codex, Claude, Cursor, or any other specific tool. Any AI assistant, agent runner, internal automation, or workflow engine that can read `SKILL.md` files can use them.

## Purpose

Use this repository as a shared AI SDLC skill library for turning fragmented delivery context into structured artifacts that humans and AI tools can use consistently.

The package helps teams:

- clarify product and business intent before implementation
- turn discovery notes into PRFAQ, BRD, backlog, and story artifacts
- review requirements for BA, PM, QA, and delivery readiness
- generate QA strategy, test cases, suites, and traceability matrices
- convert approved refinement artifacts into developer implementation specs
- enforce implementation discipline through SDD, validation, review, branching, and commit workflows
- keep PM, BA, QA, Dev, and Delivery outputs separated by the right artifact workspace

## Artifact Routing

This library separates refinement work from developer implementation work.

Use `specs-refiniment/` for PM, BA, QA, Delivery, discovery, planning, refinement, and readiness artifacts:

```text
specs-refiniment/
  <feature-name>/
    prfaq.md
    requirements-readiness.md
    backlog.md
    user-stories.md
    delivery-spec.md
    qa-strategy.md
    test-cases.md
    qa-readiness.md
```

Use `specs/` only for developer implementation SDD packages:

```text
specs/
  <feature-name>/
    requirements.md
    design.md
    test-cases.md
    qa.md
    tasks.md
```

Rule of thumb:

- PM / BA / QA / Delivery output goes to `specs-refiniment/<feature-name>/<file.md>`
- Dev implementation SDD output goes to `specs/<feature-name>/<file.md>`
- `specs-refiniment/` is upstream context for Dev work
- `specs/` should not be used for discovery, planning, QA refinement, or readiness outputs

## Guides

The `guides/` folder explains the operating model behind the skills.

- `guides/workflow.md` — end-to-end AI-ready QA/BA operating model and skill selection map
- `guides/ba.md` — BA responsibilities, context engineering, artifact generation, and BA skill usage
- `guides/qa.md` — QA responsibilities, QA-first workflow, validation artifacts, and QA skill usage

Read the guides when you need to understand how the skills fit together. Use individual skills when you need to execute a specific workflow step.

## Skill Folders

### PM / Product / Planning

- `skills/ai-sdlc-working-backwards-discovery/` — staged discovery interview for customer problem, audience, MVP, risks, and success metrics
- `skills/ai-sdlc-prfaq-package-synthesis/` — PRFAQ, FAQ package, and BRD synthesis from validated discovery notes
- `skills/ai-sdlc-goal-capability-and-epic-mapping/` — business goals, capabilities, roles, and outcome-oriented epic mapping
- `skills/ai-sdlc-backlog-decomposition-and-task-planning/` — feature, story, acceptance summary, and cross-functional task decomposition
- `skills/ai-sdlc-release-slicing-and-backlog-readiness-review/` — MVP/release slicing, sequencing, backlog readiness, and planning risk review

### BA / Requirements / Delivery Refinement

- `skills/ai-sdlc-ba/` — business context, actors, workflows, rules, assumptions, acceptance criteria, and open questions
- `skills/ai-sdlc-requirements-readiness-review/` — strict readiness review for PRFAQ, BRD, or requirements packages
- `skills/ai-sdlc-backlog-requirements-gap-review/` — backlog-planning gap review before decomposition
- `skills/ai-sdlc-delivery-package-gap-review/` — delivery gap review for discovery packages before stories or specs
- `skills/ai-sdlc-user-story-decomposition/` — epics, user stories, acceptance criteria, scenario coverage, and priority signals
- `skills/ai-sdlc-delivery-spec-synthesis/` — structured delivery specification for engineering and cross-functional planning
- `skills/ai-sdlc-delivery-handoff-review/` — final delivery handoff readiness review

### QA / Test Engineering

- `skills/ai-sdlc-qa/` — QA planning, acceptance validation, regression scope, manual checks, and validation evidence
- `skills/ai-sdlc-qa-requirements-gap-review/` — QA-blocking requirements and testability gap review
- `skills/ai-sdlc-test-scope-and-strategy-design/` — QA scope, strategy, suite intent, data needs, and risk focus
- `skills/ai-sdlc-test-cases/` — scenario matrix and implementation-oriented test case planning
- `skills/ai-sdlc-test-case-and-suite-synthesis/` — detailed test cases plus smoke, regression, and UAT suites
- `skills/ai-sdlc-qa-traceability-and-readiness-review/` — requirements-to-test traceability, coverage gaps, blockers, and QA readiness

### Dev / Implementation / Governance

- `skills/ai-sdlc-sdd/` — developer spec-driven development workflow using the five-file SDD package under `specs/`
- `skills/ai-sdlc-branching/` — task branch creation and branch/spec alignment
- `skills/ai-sdlc-validation/` — focused deterministic validation command selection and reporting
- `skills/ai-sdlc-code-review/` — findings-first code review against specs, tests, contracts, security, and scope
- `skills/ai-sdlc-security-testing/` — security review, abuse-case analysis, trust-boundary review, and validation gaps
- `skills/ai-sdlc-commit-prep/` — safe staging, commit readiness, validation evidence, and post-commit traceability
- `skills/ai-sdlc-conventional-commit/` — Conventional Commit message drafting and validation
- `skills/ai-sdlc-approvals-sandbox/` — sandbox escalation, command approval, and prefix-rule guidance

## Output Rules

Skills in this repository should generate Markdown artifacts unless a user explicitly requests another format.

Every skill is self-contained through its `SKILL.md` plus optional local resources:

- `references/` — templates, checklists, structures, and domain-specific guidance loaded only when needed
- `scripts/` — deterministic helper scripts for validation, planning, or formatting

General output rules:

- use concise, structured Markdown
- ask clarification questions when required inputs are missing
- mark unknown optional fields as `TBD`, `Not provided`, or `Assumption`
- separate confirmed facts from assumptions and open questions
- make gaps, risks, blockers, and ownership explicit
- do not invent requirements, business rules, budgets, scope, timelines, rates, or technical constraints
- route PM/BA/QA/Delivery artifacts to `specs-refiniment/<feature-name>/<file.md>`
- route developer implementation SDD artifacts to `specs/<feature-name>/<file.md>`

## Naming

Use lowercase kebab-case for generated folders and files.

Feature names should be stable and human-readable:

```text
specs-refiniment/payment-retry-policy/qa-strategy.md
specs-refiniment/payment-retry-policy/test-cases.md
specs-refiniment/payment-retry-policy/delivery-handoff-review.md

specs/payment-retry-policy/requirements.md
specs/payment-retry-policy/design.md
specs/payment-retry-policy/tasks.md
```

When the feature name is not known, use a temporary slug:

```text
specs-refiniment/tbd-checkout-risk-review/requirements-readiness.md
```

## Usage

Each skill folder is intended to be consumed by any AI tool or automation layer that can load Markdown instructions. The skills define how to turn raw notes, requirements, delivery updates, QA concerns, implementation requests, or repository diffs into structured AI SDLC Markdown.

Use one skill at a time by lifecycle stage. Do not load the whole library unless the task is repository setup or skill maintenance.

## Use From GitHub

This repository is intended to work with the Skills CLI:

```bash
npx skills
```

For one-off usage without installing a skill permanently, use:

```bash
npx skills use mikegorelikoff/ai-sdlc-harness@<skill-name>
```

Example:

```bash
npx skills use mikegorelikoff/ai-sdlc-harness@ai-sdlc-qa
```

## Install Skills

Install all skills from the repository:

```bash
npx skills add mikegorelikoff/ai-sdlc-harness --all
```

Install selected skills only:

```bash
npx skills add mikegorelikoff/ai-sdlc-harness --skill ai-sdlc-ba ai-sdlc-qa ai-sdlc-sdd
```

Install globally:

```bash
npx skills add mikegorelikoff/ai-sdlc-harness -g --all
```

List available skills without installing:

```bash
npx skills add mikegorelikoff/ai-sdlc-harness --list
```

Use `--full-depth` if the CLI does not discover all skill folders under `skills/`:

```bash
npx skills add mikegorelikoff/ai-sdlc-harness --list --full-depth
```

## Tool-Agnostic Setup

These skills are plain `SKILL.md` folders with optional `references/` and `scripts/` subfolders. The Skills CLI is only a convenient distribution mechanism. The skills themselves are portable.

Use with any AI tool in one of three ways:

- install through the Skills CLI if the tool supports it
- run `npx skills use ...` and paste or pipe the produced instruction prompt into the tool
- copy the needed `SKILL.md` and `references/` files into the tool's native rules, memory, prompt, or workflow system

### Skills CLI

```bash
npx skills add mikegorelikoff/ai-sdlc-harness --all
```

Use one skill without installing it:

```bash
npx skills use mikegorelikoff/ai-sdlc-harness@ai-sdlc-working-backwards-discovery
```

Install globally when the consuming tool reads user-level skills:

```bash
npx skills add mikegorelikoff/ai-sdlc-harness -g --all
```

### Optional Tool-Specific Install Examples

If your tool supports Skills CLI tool targeting, you can pass the relevant `--agent` value:

```bash
npx skills add mikegorelikoff/ai-sdlc-harness --agent codex --all
npx skills add mikegorelikoff/ai-sdlc-harness --agent claude-code --all
npx skills add mikegorelikoff/ai-sdlc-harness --agent cursor --all
```

You can also use a skill as a prompt for tools that do not install skills directly:

```bash
npx skills use mikegorelikoff/ai-sdlc-harness@ai-sdlc-delivery-spec-synthesis --agent claude-code
```

### Manual Or Internal Tooling

For Windsurf, Continue, Aider, custom internal workflows, CI workflows, or any tool without native Skills CLI support, use one of two approaches:

```bash
npx skills use mikegorelikoff/ai-sdlc-harness@ai-sdlc-requirements-readiness-review
```

Pipe or paste the generated prompt into the tool session.

Or install/copy manually:

```bash
npx skills add mikegorelikoff/ai-sdlc-harness --all --copy
```

Then point the tool to the needed skill folder under its installed skills directory, or paste the contents of:

```text
skills/<skill-name>/SKILL.md
skills/<skill-name>/references/
```

## Private Repo Access

If this repository is private, each machine or tool environment must have GitHub access configured before running `npx skills`.

Recommended options:

- SSH key with access to `mikegorelikoff/ai-sdlc-harness`
- GitHub CLI login with `gh auth login`
- HTTPS credential helper with a token that can read the repo

## Maintenance

When creating or updating AI SDLC knowledge, preserve refinement and implementation state separately:

- PM/BA/QA/Delivery refinement artifacts belong in `specs-refiniment/<feature-name>/<file.md>`
- developer implementation SDD artifacts belong in `specs/<feature-name>/<file.md>`
- guide-level operating model docs belong in `guides/`
- reusable skill behavior belongs in `skills/<skill-name>/SKILL.md`
- detailed templates and checklists belong in `skills/<skill-name>/references/`
- deterministic helper logic belongs in `skills/<skill-name>/scripts/`

Do not move refinement artifacts into `specs/` just because they are useful for developers. Treat `specs-refiniment/` as upstream context and convert it into `specs/` only when implementation work is explicitly in scope.
