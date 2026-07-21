---
title: Assumptions and remaining limitations
description: Provisional assumptions, validation methods, external constraints, accepted risks, and exclusions.
---

# Assumptions and remaining limitations

## Assumptions register

| ID | Assumption | Reason / impact | Confidence | Validation method | Final status |
| --- | --- | --- | --- | --- | --- |
| AS-001 | The detailed user brief was sufficient for quick-flow SDD audit setup | Avoided a blocking interview; implementation scope remained repository-only | High | Clarify/checklist/analyze/spec validation | Accepted |
| AS-002 | A license must not be inferred | Legal choice changes redistribution rights | Certain | Owner/legal decision and committed license | External blocker |
| AS-003 | Installer target recognition is not host certification | CLI reported 73 targets without behavioral proof | High | Per-host first-feature pilot | Canonical assumption |
| AS-004 | Main documentation is a maintainer preview | Main has unreleased behavior beyond v1.2.0 | High | Compare tag/HEAD and cut matching release | Accepted until release |
| AS-005 | Product Manager and Product Owner can be separate or combined | Organizations differ; gates still need one accountable owner | High | Local RACI/delegation record | Canonical convention |
| AS-006 | Python 3.10 minimum behavior is covered by CI | Local 3.10/Docker unavailable | Medium | Required remote Python 3.10 job | Pending external CI evidence |
| AS-007 | GitHub security settings are absent unless evidenced | Repository files cannot prove platform enforcement | High | Settings/API export or screenshots | Unverified external |
| AS-008 | Historical `concepts/` and `guides/` are retained intentionally | Git preserves history but current removal could affect unknown consumers | Medium | Reference scan and owner decision | Accepted deprecation risk |
| AS-009 | Local validation receipts are structural, not authenticated attestations | Any workspace writer can recompute the unkeyed fingerprint | Certain | Forge timestamp, recompute fingerprint, verify documented limitation | Canonical trust boundary |
| AS-010 | The stable release's shallow install result does not imply workflow readiness | The strengthened exact-release smoke fails at the first SDD artifact | Certain | Run immutable remote smoke with exact expected diagnostic | External release blocker |
| AS-011 | Current Ubuntu support is pending remote evidence; WSL is candidate-only | Local audit could not execute either environment | High | Required Ubuntu CI and a WSL first-feature pilot | Pending external evidence |
| AS-012 | Historical commits without `Task:` trailers remain visible rather than rewritten | Rewriting shared history would be destructive and would not create genuine past trace evidence | High | Delivery graph reports the fixed baseline count; current commits require task references | Accepted historical limitation |
| AS-013 | Source/render checks are not Web Content Accessibility Guidelines (WCAG) conformance evidence | This audit checked headings, alt attributes, navigation, and rendered links but had no assistive-technology participants or full keyboard/focus/contrast audit | Certain | Human keyboard and screen-reader sessions plus a reviewed automated WCAG audit | Accepted residual risk; accessibility owner required for pilot |

## Remaining limitations

- No license is selected. Default copyright blocks a production adoption claim.
- No signed tag, immutable GitHub release setting, release attestation, or SBOM
  is evidenced for v1.2.0.
- Local structured approval records do not authenticate people; branch
  protection or another protected external system must enforce authority.
- The validation receipt proves current local structure, recorded process exits,
  and declared trace references for a reviewed argv plan. Its self-hash is not
  authentication: a workspace writer can forge it, and the selected tests can
  still express the wrong requirement. Protected CI evidence plus independent
  product, engineering, QA, and security review remain mandatory.
- Provider/model data retention, training use, geography, and deletion depend
  on the adopter's selected service and contract.
- Native Windows/PowerShell, multiple named agent hosts, and multi-repository
  fleet management are not continuously tested.
- Fleet inventory, rollout-wave automation, revocation, mixed-version emergency
  rollback, and proof of removal are adopter-owned platform capabilities; this
  repository supplies guidance and per-repository records, not a fleet control
  plane.
- Pilot charters, cost ledgers, promotion packets, support objectives, and
  adoption decisions are documented guidance but not versioned executable
  schemas. Organizations must choose canonical systems and accountable owners
  before comparing multiple cohorts.
- The scenario patterns are inspectable transfer guides; only the health
  fixture is fully runnable end to end in this repository.
- Historical noncanonical notes remain searchable outside the built site.
- Documentation checks do not establish WCAG conformance. Keyboard order,
  visible focus, contrast, landmarks, screen-reader behavior, zoom/reflow, and
  assistive-technology usability remain unexecuted pilot checks owned by the
  adopting accessibility/documentation lead.
- The delivery graph reports 41 historical commits without task links. Current
  acceptance-criterion coverage is 100/100 for tasks and tests; history is not
  rewritten to manufacture older commit traceability.
- GitHub branch rules, private disclosure, secret scanning, push protection,
  environment approvers, and required status settings require external proof.

These are explicit product/organizational boundaries, not hidden assumptions.
