---
title: Stage a rollout after the pilot
description: Convert a successful bounded pilot into a reversible, cohort-by-cohort adoption decision with explicit capacity, support, and rollback gates.
---

# Stage a rollout after the pilot

Pilot evidence is local evidence. It does not automatically generalize to
another team, repository, data class, agent host, or risk profile. Treat each
new cohort as a bounded change with its own owner, baseline, observation window,
and stop authority.

The staged approach follows the operational principle that changes should move
gradually, remain observable, and be reversible. See Google's
[configuration rollout guidance](https://sre.google/workbook/configuration-design/)
for the underlying canary and rollback rationale.

## Rollout contract

| Stage | Scope | Accountable owner | Entry gate | Capacity, baseline, and enablement | Observation and exit gate | Rollback unit and pause trigger | Decision forum/result |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Pilot | One team and one consumer repository. | Pilot owner and executive sponsor. | Charter, data/telemetry decision, install verification, baseline, and rollback rehearsal pass. | Named engineering, QA, security/privacy, support, and enablement capacity; pinned version/config; first-use training complete. | Two to four weeks; declared sample and evidence floors; no unresolved P0/P1 or safety incident. | Roll back that repository to its accepted install/config baseline; pause on safety, data, recovery, or evidence failure. | Pilot review forum decides stop, adjust, continue, or nominate limited cohort. |
| Limited cohort | Two to three comparable teams/repositories with the same risk and host profile. | Adoption owner with platform lead. | Pilot evidence is reviewed for transfer assumptions; each team accepts a local charter and baseline. | Platform/support queue has named capacity; version/config is immutable for the window; cohort training and office hours are scheduled. | Each cohort observes at least two representative weeks and its own sample; aggregate incidents/exceptions and compare definitions before promotion. | Roll back one cohort independently; pause the cohort or all promotion on repeated incident, support overload, or threshold breach. | Adoption forum reviews cohort packets and approves continue, narrow, pause, or broaden. |
| Broader cohort | Additional teams selected by explicit risk and similarity criteria. | Portfolio adoption owner. | Limited-cohort exit gates pass and unresolved transfer risks have owners. | Capacity forecast covers platform, security, support, enablement, and maintenance; release/config baseline and migration path are published. | Per-cohort window and aggregate review remain separate; evidence is stratified by team, repository, risk, and host. | Roll back the affected cohort or version; freeze new cohorts while incident/exception aggregation is reviewed. | Executive/product/engineering forum approves the next cohort or returns to limited. |
| Standard or hold | Organization standard, or an explicit decision not to standardize. | Engineering/product leadership. | Broader evidence, cost/resource ledger, governance acceptance, and support SLO are complete. | Long-term ownership, training, upgrade/deprecation budget, policy controls, and support/on-call coverage are funded. | Quarterly review of quality, risk, cost, support burden, and adoption; retire or revise when assumptions change. | Revert the standard, disable the capability, or hold adoption at the last safe cohort; preserve evidence and communicate scope. | Governance/release forum records standardize, hold, narrow, or retire. |

Attach this table to the pilot decision record before inviting a second team.

## Required rollout proposal

Do not write “scale” as the only next action. The proposal must name:

- cohort selection criteria and the evidence that makes the cohort comparable;
- accountable, responsible, consulted, and informed owners for adoption,
  platform, security/privacy, support, enablement, and repository decisions;
- pinned harness version, agent host, configuration, permissions, data classes,
  and migration/rollback boundary;
- training, office hours, support queue, incident commander, and capacity
  assumptions for the whole observation window;
- entry and exit thresholds for mechanism behavior, delivery outcomes,
  experience, safety, evidence freshness, and the cost/resource ledger;
- one observation window per cohort, sample size, missing-data rule, and an
  incident/exception aggregation method that preserves cohort identity;
- the smallest rollback unit, pause trigger, resume approval, and decision
  forum/date for the next promotion.

## Promotion checklist

1. Copy the proposal and change only the new cohort-specific fields.
2. Reconfirm data, installer telemetry, package origin, permissions, and policy.
3. Pin the same version/config for the observation window; record intentional
   differences before starting.
4. Train the cohort and rehearse stop, recovery, and rollback with a disposable
   change.
5. Collect the local mechanism, delivery, experience, safety, support, and cost
   evidence without merging incomparable samples.
6. Hold the named forum. Promotion is a human decision; an agent may assemble
   the packet but cannot authorize the next cohort.

If a cohort passes only because missing data was ignored, the correct result is
`hold` or `adjust`, not broader rollout. Preserve the packet, exceptions,
incidents, and limitations so the next decision starts from evidence.
