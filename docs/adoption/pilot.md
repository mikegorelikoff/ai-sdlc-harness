---
title: Run a bounded pilot
description: Plan and operate a two-to-four-week, one-team, one-repository AI SDLC Harness pilot with checkpoints, stop conditions, rollback, and a scale decision.
---

# Run a bounded pilot

A useful pilot is small enough to stop safely and real enough to expose delivery
friction. Use one team, one repository, two to four weeks, and a representative
but non-critical set of changes. Do not begin with regulated production access,
secrets, autonomous deployment, or an organization-wide rollout.

## 1. Write the charter

Complete this table before installation.

| Field | Required decision |
| --- | --- |
| Problem | Which delivery failure or cost are we trying to reduce? |
| Repository | One named consumer repository and default branch. |
| Workload | Three to eight representative changes, including one defect or recovery case. |
| Exclusions | Production deployment, live secrets, regulated data, or other prohibited scope. |
| Pilot owner | Person accountable for schedule, evidence, and final recommendation. |
| Cost/resource owner | Person accountable for the cost/resource ledger, ranges, missing data, and capacity assumptions. |
| Role owners | Product/BA, engineering, QA, security, delivery/release, and repository maintainer. |
| Agent boundary | Approved host, models, tools, network access, filesystem scope, and escalation process. |
| Installer telemetry decision | Whether the third-party Skills CLI may send its anonymous skill-name/file/timestamp telemetry, opt-out setting, policy owner, and retention decision. |
| Baseline window | Comparable recent work or at least one pre-pilot observation period. |
| Checkpoints | Kickoff, end of week one, midpoint, final review, and incident reviews. |
| Decision date | Date and forum for stop, adjust, continue, or scale. |

If an accountable owner, comparison baseline, or stop condition is missing, the
pilot is not ready.

## 2. Capture the baseline

Use existing systems where possible. Do not backfill precision the team never
measured. For each selected signal record its definition, source, time window,
sample size, missing data, and known confounders.

Minimum baseline:

- time from accepted intent to review-ready change;
- review rounds and material review findings;
- escaped defects or failed validation associated with comparable changes;
- rework caused by misunderstood scope or missing context;
- time needed for another person to resume interrupted work;
- team confidence and perceived ceremony burden;
- incremental people, tool, model/API, platform, training, governance, support,
  upgrade, and incident/remediation cost ranges, with an owner and uncertainty;
- current deployment throughput and instability signals, if available.

The baseline is a local comparison, not an industry ranking.

## 3. Prepare safely

!!! warning "Human checkpoint"

    The repository owner and security owner approve installation scope, package
    origin, data classes, permissions, network use, retention, and rollback.

1. Choose a disposable branch or low-risk repository slice.
2. Follow the [canonical project-scoped install](../how-to/install.md).
3. Record the installed inventory, telemetry opt-out/approval, and accepted Git baseline.
4. Complete [the first 30 minutes](../onboarding/first-30-minutes.md).
5. Run the [first-feature tutorial](../tutorials/first-feature.md) before real work.
6. Confirm the [troubleshooting runbook](../operations/troubleshooting.md) and incident owner.

## 4. Operate the weeks

| Time | Work | Required evidence | Decision |
| --- | --- | --- | --- |
| Day 0 | Charter, baseline, governance, install, training. | Signed scope, inventory, owners, thresholds. | Start or do not start. |
| Week 1 | One bounded quick-flow change. | Navigator handoff, artifacts, validation, corrections, user notes. | Continue, narrow, or stop. |
| Week 2 | Two representative changes and one interrupted handoff. | Trace links, resume evidence, review findings, time/effort observations. | Continue or adjust controls. |
| Week 3 | One higher-rigor or cross-role change, if safe. | Human gates, security/QA evidence, exception log. | Proceed only if earlier controls held. |
| Week 4 | Repeat a common work type and close analysis. | Metric comparison, qualitative evidence, incidents, residual risks. | Stop, adjust, continue, or propose scale. |

Two weeks can be enough for a narrow fit decision. Four weeks provides more
opportunity to observe handoff, recovery, and repeated use. Time alone is not
evidence; record completed samples.

## 5. Use explicit thresholds

Set thresholds from the baseline and risk tolerance before seeing pilot results.
Examples of decision rules—not universal targets—include:

- stop if a secret or prohibited data class reaches an unapproved agent service;
- stop if the agent performs an unapproved destructive, release, or permission-expanding action;
- pause if repository recovery cannot restore the accepted baseline;
- adjust if required evidence completion remains below the team's agreed floor;
- adjust if median ceremony effort exceeds the tolerated budget without an offsetting quality benefit;
- continue if handoff completeness, reviewability, or recovery improves with acceptable burden;
- consider scale only after multiple representative changes and all P0/P1 pilot findings close.

Record actual numeric floors in the charter. Do not copy example thresholds as
if they were validated for your team.

## Pilot decision contract

| Stage | Evidence | Threshold / trigger | Accountable owner | Allowed result |
| --- | --- | --- | --- | --- |
| Baseline | Definitions, sources, window, sample, missing data, confounders. | Every decision metric has an owner and pre-pilot definition. | Pilot owner | Ready or not ready. |
| Kickoff | Scope, repository, workload, exclusions, permissions, rollback. | All protected boundaries approved; any missing owner stops start. | Pilot and security owners | Start or do not start. |
| Week 1 | First real change, corrections, evidence completeness, burden. | Any safety stop fires immediately; other local floors trigger adjust/review. | Team lead | Continue, narrow, pause, or stop. |
| Midpoint | Multiple samples, interrupted handoff, incidents, qualitative evidence. | Required sample and evidence floors met or explicitly insufficient. | Pilot owner | Continue, adjust, or stop. |
| Final | Baseline comparison, limitations, incidents, residual risk, support readiness. | All declared scale conditions pass and no P0/P1 remains; otherwise no scale. | Executive/adoption owner | Stop, adjust, continue, or propose scale. |

## 6. Roll back without erasing evidence

Rollback means returning the consumer project to its last accepted installation
and policy baseline. Preserve the pilot branch, decision log, validation output,
incident records, and review notes according to retention policy.

1. Stop new agent mutations.
2. Capture `git status --short`, installed inventory, current branch, and exact failure.
3. Revoke or narrow temporary permissions and credentials.
4. Use the documented [installation rollback](../how-to/install.md#update-remove-or-roll-back).
5. Restore accepted files through reviewed Git changes; do not delete evidence to make status green.
6. Validate the repository and record why the pilot stopped.

## 7. Make the final decision

| Decision | When it is defensible | Required next action |
| --- | --- | --- |
| Stop | Controls failed, burden outweighed benefit, or evidence is insufficient and more exposure is unjustified. | Roll back, retain evidence, assign remediation only if worthwhile. |
| Adjust | The problem remains valid but scope, training, policy, or workflow needs change. | Write a new bounded charter and changed thresholds. |
| Continue | More representative samples are needed within the same risk boundary. | Extend time, not scope, and name the missing evidence. |
| Scale | Repeated evidence meets predeclared thresholds, the cost/resource ledger is decision-ready, and governance/capacity can support more teams. | Create the [staged rollout proposal](rollout.md) with cohort owners, observation windows, capacity, and rollback boundaries. |

The final report must include the [cost/resource ledger](metrics.md#cost-and-resource-ledger)
and separate observed facts, participant opinions, inferences, and untested
hypotheses. “No incident observed” is not proof that an incident cannot occur.
