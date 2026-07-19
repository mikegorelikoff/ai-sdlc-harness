---
title: Interpret pilot metrics
description: Define, collect, and interpret local AI SDLC pilot signals without turning deterministic counts into causal productivity or ROI claims.
---

# Interpret pilot metrics

Metrics support a decision; they do not make it. A small pilot usually has too
few samples and too many simultaneous changes to establish causality. Pair
quantitative signals with artifact review, participant evidence, incidents, and
known confounders.

## Three evidence classes

| Class | Examples | What it can say |
| --- | --- | --- |
| Mechanism | Schema pass rate, fresh evidence coverage, blocked gates, helper exit status. | Whether declared harness controls behaved as specified. |
| Delivery outcome | Change lead time, review rework, failed deployment recovery, escaped defects. | What happened to the team's delivery system during the window. |
| Experience | Confidence, ease of resumption, clarity, perceived burden. | How participants experienced the workflow. |

Do not claim the harness caused an outcome merely because the metric moved after
installation.

## Local metric dictionary

| Signal | Definition | Source | Interpretation trap |
| --- | --- | --- | --- |
| Evidence coverage | Requirements with fresh evidence / requirements in scope. | Evidence ledger and review. | High coverage can still contain weak evidence. |
| Gate pass rate | Gates passed / gates attempted, reported with failure reasons. | Validation and policy results. | Fewer attempted gates can inflate the rate. |
| Retry count | Attempts after the first attempt for bounded tasks. | Runtime state. | Retrying can mean learning or instability. |
| Blocked duration | Time from explicit blocker to owned resolution. | State and handoff timestamps. | A blocker can reflect healthy fail-closed behavior. |
| Handoff completeness | Required handoff fields populated and independently usable. | `ai-sdlc-handoff/v1` review. | Presence does not prove accuracy. |
| Resume success | Interrupted cases resumed without rediscovery or evidence loss. | Recovery exercise. | One scripted tutorial is not representative. |
| Review rework | Material review changes after review-ready handoff. | Pull-request evidence. | Review style and change complexity differ. |
| Escaped defect count | Confirmed defects attributable to pilot changes after acceptance. | Incident/defect system. | Small samples create large variance. |
| Ceremony effort | Human time spent creating/reviewing harness artifacts. | Time sample or survey. | Self-reported time is approximate. |
| Agent correction effort | Human time correcting agent misunderstanding or unsafe action. | Work log and review notes. | Missing logging understates the cost. |
| Change lead time | Commit-to-successful-production interval when deployment data exists. | Version control and deployment system. | The harness does not observe deployment by itself. |
| Deployment frequency | Successful production deployments in a period. | Deployment system. | Higher is not always better for every product. |
| Failed deployment recovery | Time to recover a deployment requiring immediate intervention. | Incident/deployment system. | Do not substitute chat response time. |
| Change fail rate | Deployments requiring immediate intervention / deployments. | Deployment and incident systems. | Classification must stay stable. |
| Deployment rework rate | Unplanned corrective deployments / deployments. | Deployment system. | Separate planned follow-up from emergency rework. |

The last five align with the current
[DORA software delivery performance metrics](https://dora.dev/guides/dora-metrics/).
DORA groups throughput and instability signals and recommends using them for
continuous improvement; this harness does not calculate production deployment
facts from repository state.

## Content-free local metrics

`ai-sdlc-package-trust` Branch B can aggregate local run state and evidence
counts into `_ai_sdlc/metrics/local.{toon,json,md}`. It allows schemas,
fingerprints, statuses, booleans, and numeric counts or budgets. It forbids
content, prompts, commands, diffs, source text, artifact paths, messages,
reasons, and file bodies, and it has no network operation.

An `insufficient-data` result is correct when no eligible local record exists.
It must not be converted to zeros that imply observed activity.

## Establish thresholds

1. Choose the decision the signal informs.
2. Fix the definition, source, owner, window, and calculation before the pilot.
3. Capture baseline distribution or explicitly record that none exists.
4. Set a floor, ceiling, or review trigger from local risk tolerance.
5. Name confounders such as workload mix, staffing, release freeze, training, or tool changes.
6. Keep raw decision evidence according to governance while sharing only approved aggregates.

Avoid universal “good” numbers. A five-minute gate can be excessive for a typo
and negligible for a security-sensitive migration.

## Cost and resource ledger

The pilot owner and cost/resource owner maintain a separate ledger for the
baseline and pilot windows. This is a decision aid, not a promise of ROI. The
FinOps Foundation describes total cost of ownership as including acquisition,
management, support, communications, end-user expense, labor, downtime,
training, and productivity loss; use that breadth when it is material to the
decision. See its [TCO terminology](https://framework.finops.org/assets/terminology/)
and [unit-economics guidance](https://www.finops.org/framework/capabilities/unit-economics/).

| Cost/resource category | Definition and unit | Source / accountable owner | Baseline and pilot window/allocation | Uncertainty to record |
| --- | --- | --- | --- | --- |
| Model/API consumption | Provider tokens, requests, or subscription increment attributable to the pilot. | Provider bill or approved estimate / platform or finance owner. | Same calendar window and cohort allocation. | Shared plans, rate changes, and unmetered use. |
| Agent/tooling and license | Incremental host, CLI, seat, plugin, or tool cost. | Procurement/billing / platform owner. | Baseline seats versus pilot seats. | Discounts, unused seats, and renewal exposure. |
| Installation and supply chain | Review, package verification, mirror, network, and dependency effort. | Install evidence and package policy / maintainer. | One-time setup plus per-cohort refresh. | Provider behavior, cache, and network variability. |
| Onboarding and training | Participant and enablement time to learn, practice, and attend support. | Time sample / enablement owner. | Comparable training window and participant count. | Recall bias and non-pilot learning spillover. |
| Workflow participation and rework | Human time for artifact creation, review, correction, and recovery. | Work log/PR evidence / delivery owner. | Same task mix and role rates. | Workload complexity and staffing changes. |
| Platform and maintenance | Runtime packaging, upgrades, policy maintenance, and internal support. | Platform backlog / platform owner. | Allocated hours and release window. | Shared infrastructure and future upgrade load. |
| Governance and assurance | Security, privacy, legal, compliance, audit, and exception review effort. | Review records / security or compliance owner. | Baseline policy effort versus pilot increment. | Jurisdiction, risk class, and review depth. |
| Support and enablement | Office hours, triage, incident response, documentation, and coaching. | Support queue / support owner. | Ticket hours and cohort count. | Early-adopter intensity and unrecorded help. |
| Upgrade and deprecation | Migration, compatibility, retraining, and retirement effort. | Release/maintenance plan / maintainer. | Expected window and affected cohorts. | Vendor changes and unknown migration scope. |
| Incident and remediation | Recovery, containment, rework, downtime, and risk-remediation effort. | Incident/defect records / incident owner. | Include zero only when zero was actually observed. | Severity, counterfactuals, and unpriced risk. |

For each row, record a low/central/high range, the unit, sample, missing data,
and owner. Compare incremental resource ranges with observed delivery, quality,
experience, and risk evidence. Use best/central/worst scenarios and explicit
decision thresholds; do not turn an unmeasured benefit into a universal ROI
claim. Require the ledger in every final pilot decision and every staged
rollout promotion packet.

## Weekly review

For each signal record:

- numerator, denominator, sample size, and missing records;
- baseline and pilot windows;
- observed value and uncertainty;
- qualitative corroboration or contradiction;
- incidents, exceptions, and policy changes;
- the decision it changed—or “no decision.”

Use medians and ranges for small time samples rather than reporting a false
precision average. Never rank individual developers from these pilot metrics.

## Claims language

| Evidence | Defensible wording | Avoid |
| --- | --- | --- |
| Contract test passed | “The tested helper rejected this invalid state.” | “The harness prevents all invalid states.” |
| Pilot lead time decreased | “Median lead time was lower in this pilot window.” | “The harness increased productivity by X%.” |
| Reviewers found handoffs clearer | “Four participants reported easier resumption.” | “Handoffs are objectively solved.” |
| No incident occurred | “No incident was observed in N cases.” | “The workflow is secure.” |

When evidence is incomplete, say so and name the next observation. Honest
insufficient data is safer than a scale decision built from invented certainty.
