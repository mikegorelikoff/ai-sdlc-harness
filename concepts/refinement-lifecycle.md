<!-- public-docs-canonical: ../docs/index.md -->

> **Internal, non-canonical design note.** The maintained public documentation starts at [AI SDLC Harness docs](../docs/index.md). This file is retained for repository history and maintainer context only.

# Refinement Lifecycle

The refinement lifecycle turns an initial problem signal into a complete,
implementation-ready delivery package. It contains 18 canonical stages shared
by the state machine, artifact profiles, status checker, and skill instructions.
The profile registry is the single source of stage order, predecessors, output
names, required sections, and table contracts.

## Canonical Stage Order

| # | Stage | Skill | Output | Required predecessor |
| ---: | --- | --- | --- | --- |
| 1 | Discovery | `ai-sdlc-working-backwards-discovery` | `discovery.md` | — |
| 2 | PRFAQ synthesis | `ai-sdlc-prfaq-package-synthesis` | `prfaq.md` | Discovery |
| 3 | Delivery-package gap review | `ai-sdlc-delivery-package-gap-review` | `delivery-gap-review.md` | PRFAQ |
| 4 | Requirements readiness | `ai-sdlc-requirements-readiness-review` | `requirements-readiness.md` | Delivery-package gap review |
| 5 | Goal/capability/epic mapping | `ai-sdlc-goal-capability-and-epic-mapping` | `goal-capability-map.md` | Requirements readiness |
| 6 | Backlog gap review | `ai-sdlc-backlog-requirements-gap-review` | `backlog-gap-review.md` | Goal mapping |
| 7 | Backlog decomposition | `ai-sdlc-backlog-decomposition-and-task-planning` | `backlog.md` | Backlog gap review |
| 8 | Story decomposition | `ai-sdlc-user-story-decomposition` | `user-stories.md` | Backlog decomposition |
| 9 | Release slicing | `ai-sdlc-release-slicing-and-backlog-readiness-review` | `release-slicing.md` | Backlog decomposition |
| 10 | BA context | `ai-sdlc-ba` | `business-context.md` | Story decomposition |
| 11 | Delivery spec | `ai-sdlc-delivery-spec-synthesis` | `delivery-spec.md` | BA context |
| 12 | QA plan | `ai-sdlc-qa` | `qa.md` | Requirements readiness |
| 13 | QA gap review | `ai-sdlc-qa-requirements-gap-review` | `qa-gap-review.md` | QA plan |
| 14 | Test strategy | `ai-sdlc-test-scope-and-strategy-design` | `qa-strategy.md` | QA gap review |
| 15 | Test cases | `ai-sdlc-test-cases` | `test-cases.md` | Test strategy |
| 16 | Test suite | `ai-sdlc-test-case-and-suite-synthesis` | `test-suite.md` | Test cases |
| 17 | QA traceability/readiness | `ai-sdlc-qa-traceability-and-readiness-review` | `qa-readiness.md` | Test suite |
| 18 | Delivery handoff | `ai-sdlc-delivery-handoff-review` | `delivery-handoff-review.md` | Delivery spec and QA readiness |

The table is an execution order for a complete cascade. The predecessor graph
also permits focused work: for example, QA planning can begin after requirements
readiness even while the product/backlog branch continues. A full end-to-end
cascade still uses the canonical order so each later artifact sees the richest
available feature package.

## What Each Phase Establishes

### Discovery And Working Backwards

Stages 1–4 establish the customer problem, intended value, business framing,
initial requirements, contradictions, and whether the package is ready for
structured planning. These stages prevent a polished backlog from hiding a weak
problem definition.

### Goal And Backlog Design

Stages 5–9 connect business outcomes to capabilities, epics, stories, tasks,
priorities, dependencies, and release slices. They create a planning model that
can be traced back to value rather than merely listing requested work.

### Business Analysis And Delivery Specification

Stages 10–11 make actors, permissions, workflows, rules, acceptance behavior,
exceptions, data, and handoff risks explicit. The delivery spec becomes the
main upstream contract for implementation SDD.

### QA Design And Evidence

Stages 12–17 turn requirements into risk-based strategy, executable cases,
suites, and traceability evidence. QA readiness is not equivalent to “test
cases exist”; it means important requirements and risks have visible coverage
and execution dependencies are known.

### Final Handoff

Stage 18 joins both branches. It cannot complete from delivery-spec evidence
alone or QA evidence alone. It verifies ownership, decision coverage,
implementation inputs, dependencies, and remaining blockers.

## Optional Versus Mandatory

Release slicing is optional in the general state model because not every focused
feature requires a release plan. It is mandatory for a declared complete
18-stage cascade. If release slicing is genuinely not applicable, the cascade
produces an evidence-backed N/A `release-slicing.md` and marks the stage done;
it does not silently omit the artifact.

This distinction prevents two bad outcomes:

- forcing heavyweight release planning into every small focused task;
- claiming a complete refinement package while one canonical stage is absent.

## Single-Stage Full Flow Versus Complete Cascade

`--full-flow` controls the strictness of one selected skill. It does not, by
itself, authorize or trigger all 18 stages.

A complete cascade starts only when the user explicitly asks for complete,
full, end-to-end refinement or every refinement artifact. The cascade status
commands use the strict gate:

```bash
python3 skills/_shared/refinement_status.py \
  --feature <feature> --gate full --format toon

python3 skills/_shared/refinement_status.py \
  --feature <feature> --gate full --format markdown
```

The strict gate requires all stages done, all canonical artifacts present, and
every artifact marked `flow_mode: full` with blocking quality checks satisfied.

## Cascade Execution Algorithm

For each reported `next_skill`:

1. Read state, decision log, indexes, and the current feature context.
2. Check that the stage predecessor is complete.
3. Mark the stage in progress only when durable work starts.
4. Run the stage analysis with `--format toon --budget-tokens 24000`.
5. Follow all targeted `next_reads` before writing.
6. Emit the canonical template and read the skill reference.
7. Write every section through the stage script.
8. Finalize with `--full-flow`; resolve blocking quality issues.
9. Record material decisions and complete the state transition.
10. Confirm the refreshed index reflects the new state.
11. Re-run strict refinement status and continue until `18/18`.

The agent returns checkpoint summaries in its response. It does not create a
separate cascade-summary text file.

## Resume And Repair

A cascade is restartable. On a new session, the agent does not assume the last
chat step was committed successfully. It runs strict status and resumes from
the earliest blocking stage.

Common repair cases:

- **Artifact exists, stage not done:** validate the artifact, then complete the
  state transition if the evidence supports it.
- **Stage done, artifact missing:** restore or regenerate the artifact; never
  accept state alone as proof.
- **Default artifact in a full cascade:** regenerate or enrich it in full flow.
- **Index missing an artifact:** rebuild the index after artifact/state repair.
- **Legacy and canonical names both exist:** run migration checking and resolve
  divergent content before continuing.

## Implementation Handoff

Implementation SDD depends on `delivery_spec` and `qa_traceability`. The
implementation workspace may reference refinement state as upstream evidence,
but creates its own state, decisions, requirements, design, tasks, QA artifact,
and execution plan under `specs/<feature>/`.

The handoff is therefore a boundary, not a folder move: refinement retains why
and what the feature must achieve; implementation defines how the repository
will deliver and validate it.
