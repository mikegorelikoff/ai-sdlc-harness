---
title: Sub-agent review reports
description: Independent reviewer perspectives, baseline decisions, requested changes, re-review evidence, and sign-off status.
---

# Sub-agent review reports

All initial reviews targeted isolated baseline commit
`38da30737c15fcbe53c8e4854cea09eae0446fd0`; reviewers were told not to read one
another's findings or edit the working tree. Every initial decision was
`NOT READY`.

| Reviewer | Baseline findings and requested changes | Evidence exercised | Re-review / decision |
| --- | --- | --- | --- |
| CTO | License; release/docs drift; Codex portability; PR docs gate; provenance/ownership/support | Clean install, docs/tests, tag/history | Local candidate signed off; overall `NOT READY` for license, corrected release, and remote-control evidence |
| VP Engineering | Undefined adoption path/hosts; release drift; broad install; multi-repo controls; missing roles | Clean consumer, adoption/role docs, config/policy checks | Local candidate signed off; fleet tooling is an accepted limitation |
| Lead Developer | Consumer/source paths; missing AGENTS fallback; caches; task authority; no merge path | Installed workflow, receipt/state and commit-readiness tests | Local candidate signed off |
| Trainee Developer | Missing fundamentals/prerequisites/recovery/roles/tutorials; jargon and partial PowerShell | Followed corrected onboarding, installation, and tutorial paths exactly | Local candidate signed off |
| Product Manager | Semantic `gaps[0]`; missing PM guide; vague/conflict/change workflows; weak priority/accountability | Decisions-only fixture, role guide, change patterns | Local candidate signed off |
| Product Owner | No PO guide; weak outcome-to-evidence acceptance; semantic gaps; role ambiguity | Graph/backlog/product-acceptance evidence and Task trailer tests | Local candidate signed off; historical trace gaps accepted |
| Business Analyst | Read-only analysis writes; BA stage contradiction; shape-only gates; no inspectable BA example | BA commands, semantic-gap fixture, state graph | Local candidate signed off |
| QA Engineer | Two omitted failing suites; broken release gate; fabricated PASS; no PR docs gate; tutorial/NFR gaps | Full shared/per-skill/docs regression, negative receipt tests, release characterization | Local candidate signed off after final receipt and race-regression verification |
| DevOps / Platform | Empty-cache offline failure; old-release smoke; mutable Actions; license; update/remove errors; unlocked deps | Real clean install, repeat/subset ownership tests, strict build, immutable-release smoke | Local candidate signed off; external license/release/settings remain blockers |
| Security | Secret egress; instruction elevation; self-asserted approval; bootstrap provenance; missing disclosure/egress controls | Credential/instruction fixtures, trust tests, path/evidence/approval negative regressions | Local candidate signed off after final defensive rerun |
| Technical Writer / IA | Missing foundations/roles/tutorials; consumer paths; undefined support; release drift; FAQ duplication; Mermaid/H1 concerns | Full public-doc inventory, terminology scan, strict build/render validator | Local candidate signed off after final audit-truth corrections |

## Adversarial baseline synthesis

Most likely failures were a consumer running a source-only command, a novice
assuming any agent host was supported, stale/fabricated validation being
accepted, context leaking a credential, an instruction-like document gaining
authority, and a company discovering too late that no license existed.

The most confusing boundary was source checkout versus installed consumer. The
weakest claim was “supported AI agent” without a matrix. The most likely
enterprise blockers were license/provenance, release mismatch, and absent
external enforcement evidence. The main uncovered scenario was a database/API
contract change after implementation began; it is now in change patterns.

No reviewer can sign off overall `READY` while the external blockers remain.
The initially fabricated validation claim was replaced by executable,
fingerprint-bound local evidence. Corrected-tree re-review records are appended
after each reviewer tests the affected areas rather than merely reading the
change summary.

## Corrected-tree evidence

- CTO, VP Engineering, Lead Developer, Trainee Developer, Product Manager,
  Product Owner, Business Analyst, and DevOps/Platform each found no remaining
  local Critical, High, or Medium defect in their corrected scope and signed
  off the local candidate. Their organizational/release decision remains
  `NOT READY` because license, corrected release, and remote platform evidence
  are external blockers.
- Security initially reproduced recovery traversal, symlink-parent writes,
  validation fail-open/output risks, approval-parser bypasses, and overstated
  hash trust. After three correction cycles, it reran path/state/artifact,
  receipt, approval, runtime, and per-skill regressions and granted **local
  security sign-off** with local evidence explicitly unauthenticated.
- Technical Writing/Information Architecture validated 166 public pages, 44
  skills, 5 modules, 115 scripts, 13 role guides, ten tutorial patterns, 633
  versionable files, terminology, navigation, strict rendering, and generated
  catalogs. Final content sign-off followed expansion of the remaining
  first-use acronyms. Its final audit-truth pass then identified three stale
  report statements; the counts, QA decision record, and readiness wording were
  corrected. No other local Critical, High, or Medium IA issue remained.
- QA repeatedly challenged the evidence rather than accepting prose. It found
  the final core artifact/state symlink escape and untracked fingerprinting
  issues; both now have negative regressions. Its last rerun then found an
  intermittent timeout termination race. After the runner handled the
  already-exited-process case, five focused and three consecutive 97-test
  aggregate runs passed. QA independently verified the current six-command
  receipt, completed state, plan links, and diff hygiene and granted **local QA
  sign-off** with no local Critical, High, or Medium defect remaining.

## Final adversarial review

Every perspective was asked to assume defects remained and to identify three
likely failures, the most confusing section, weakest claim, likely beginner
mistake, enterprise blocker, and an uncovered scenario. Material findings were
either corrected or retained below as explicit external/accepted limitations.

- **CTO:** correctly challenged premature audit-state claims, ambiguous
  candidate-versus-release support, missing license, and mixed-version emergency
  rollback. Audit state is finalized only after executable evidence; the matrix
  now separates candidate testing from released support. License/release/fleet
  rollback remain blockers or deliberate tooling exclusions.
- **VP Engineering:** challenged prose-only fleet management and nonstandardized
  adoption-decision artifacts. These are explicitly accepted limitations for a
  repository harness rather than silently claimed executable capabilities; an
  organization must supply fleet inventory, rollout automation, and governed
  decision systems before scale-out.
- **Lead Developer:** found durable validation missing from the first-feature
  tutorial and an overstated tutorial-regression claim. The tutorial now uses a
  canonical plan/receipt/state sequence and records post-commit acceptance as a
  separate protected evidence change. Concurrent Git projection merges remain
  an adopter-owned recovery scenario.
- **Trainee Developer:** exposed unexplained shell forms, ambiguous failed-install
  cleanup, and “complete state” overclaims. The primer now explains variables,
  substitution, quoting, loops, redirects, tests, and recursive deletion;
  cleanup routes to the ownership-safe procedure; state claims are bounded.
- **Product Manager:** challenged an absolute prevention claim and missing
  retirement/adoption schemas. Product intent is now described as visible and
  reviewable, not guaranteed; retirement and adoption-system schemas remain
  explicit scope opportunities.
- **Product Owner:** challenged “accepted 18/18,” semantic validation, stale
  product acceptance, and partial increment acceptance. The lifecycle title and
  language now distinguish structural handoff from human acceptance. Automated
  product-acceptance freshness remains an accepted external merge-control gap.
- **Business Analyst:** challenged provisional story readiness, semantic limits,
  release-slice reconciliation, and effective-dated rules. The later BA challenge
  and structural-only validation boundary are explicit; jurisdiction/effective
  dating requires domain extensions and accountable stakeholder review.
- **QA:** found stale counts, missing failure/recovery evidence, external-link
  overreach, descendant-timeout coverage, and premature lifecycle evidence.
  Counts were corrected; exact `404 != 200` recovery was run; timeout descendants
  are tested, including repeated race regression; arbitrary external link uptime
  is explicitly not claimed; the final receipt/state was independently verified.
- **DevOps:** found missing `config/**` workflow triggers and interrupted-update
  ambiguity. CI paths now include configuration; update records a durable marker
  and retired set with an exact same-revision recovery sequence. A corrected
  release remains mandatory.
- **Security:** found migration-before-boundary, feature traversal, approval
  wrapper, rollback-language, and silent-child pipe risks. Feature slugs and all
  migration paths are bounded, approval variants are conservative, rollback is
  described as attempted, and runner process groups are terminated after leader
  exit. Focused and aggregate regressions pass.
- **Technical Writer/IA:** challenged the stable/candidate learning path,
  summary-pattern depth, a “full lifecycle” title, and unsupported depth claims.
  The title now states refinement-to-implementation scope and the audit limits
  depth evidence to mechanical coverage plus required pilot feedback. Compact
  patterns remain inspectable transfers rather than falsely fixture-backed.
