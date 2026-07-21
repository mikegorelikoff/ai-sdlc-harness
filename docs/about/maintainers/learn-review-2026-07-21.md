---
title: "Learn curriculum review record — 2026-07-21"
description: "Frozen-snapshot reviewer findings, parent decisions, corrections, rechecks, and unresolved owner decisions for the Learn knowledge base."
---

# Learn curriculum review record — 2026-07-21

This record preserves the independent, read-only review of the first complete
Learn implementation. It is evidence for maintainers, not publication approval
or legal advice. The parent documentation agent owned every repository edit.

## Execution record

- **Initial execution mode:** nine actual isolated subagents, read-only.
- **Shared snapshot:** working-tree diff from base commit
  `faccb4354464a1a3cc309b7b2dfa65e8efaf3529`, frozen before review.
- **Common input:** curriculum mission, Learn contract, token range, adaptation
  rule, identical changed-file scope, role questions, and finding schema.
- **Roles:** New learner; PM/PO; Business Analyst; QA; Developer/Architect;
  Security/Governance/Accessibility; AI Practice/Documentation Maintainer;
  Source Provenance/Adaptation; Depth/Duplication/Anti-padding.
- **Edit ownership:** reviewers did not edit; the parent synthesized and patched.
- **Decision rule:** evidence and canonical ownership, never reviewer count.

Initial reports found no blocker after classification normalization, eight
high-severity findings, multiple medium and low findings, and no concrete sign
of copied lessons, examples, quizzes, diagrams, close paraphrase, or cloned
external structure. Counts overlap where reviewers found the same defect.

## Agreements and conflicts

Reviewers agreed that tracked lab inputs, source-note verification, clean-host
dependency guidance, role prerequisites, and SDD traceability needed correction.
They also agreed that reviewer consensus cannot approve a product, security,
release, licensing, or publication decision.

There was no material contradiction between reviewer facts. PM/PO and the New
Learner reviewer described the role fast lane from different perspectives; the
resolution requires both prerequisite evidence and role-specific conditional
routing. The missing repository license remains an owner decision.

## Initial finding register

Every source report used the full required schema. This compact register keeps
the durable disposition; detailed evidence is recoverable from the named file,
heading, and correction.

| Finding IDs | Severity | Classification | Evidence location | Parent decision and correction | Status |
| --- | --- | --- | --- | --- | --- |
| NL-001, DEV-ARCH-001 | blocker/high | fact | Guided Practice, Labs 3–5, 7, 9–11 | Added tracked fixtures and aligned feature/lifecycle scenarios with canonical tutorials. | corrected |
| NL-002 | high | fact | Multi-role Review practice | Added immutable unsafe-draft fixture with stable headings and an evidence-only boundary. | corrected |
| DEV-ARCH-002 | high | fact | Validation reference | Documented the pinned `uv` environment and missing-`tiktoken` recovery. | corrected |
| QA-001, DOCMAINT-004/005, PROV-005/006/007 | high/medium | fact/risk | Source notes, registry, source validator | Added structured links and metadata, exact destinations, bidirectional checks, and negative tests. | corrected |
| PROV-002 | high | fact | Adaptable-source summaries | Added idea, relevance, harness translation, original replacement, structural difference, and exclusions. | corrected |
| DOCMAINT-001, BA-004 | high/medium | fact | Feature tasks and plans | Added AC/TC/task/artifact links, accurate states, and generated projections. | corrected |
| DOCMAINT-002, PROV-001 | high | risk | Repository license | Preserved an explicit repository-owner blocker; no license was invented. | deferred_with_owner |
| NL-003/004, PMPO-001 | medium | fact | Diagnostic and fast lanes | Defined three-state checkboxes and equivalent-evidence prerequisites. | corrected |
| PMPO-002, BA-001, QA-003, DEV-ARCH-003 | medium | fact | Role paths | Added conditional product/analysis routes and QA suite synthesis. | corrected |
| BA-002 | medium | fact | BA exercise | Added a tracked subscription-policy source pack. | corrected |
| BA-003 | medium | fact | AI SDLC trace | Split Product outcome and Operations policy owner rows. | corrected |
| QA-002 | medium | fact | Token normalization | Made comment removal fence-aware and added a test. | corrected |
| SEC-A11Y-001/002 | medium | risk/fact | Agent/context lessons | Added approval integrity details and split the wide evidence table. | corrected |
| DEPTH-001 | medium | fact | Role headings | Removed duplicate manual anchors. | corrected |
| DOCMAINT-003 | medium | fact | Entry pages | Made Learn the beginner entry and kept operating steps under Use. | corrected |
| PROV-003/004 | medium | fact | DAIR/OWASP records | Fixed the license path and narrowed OWASP source identity. | corrected |
| NL-005, DOCMAINT-007, DEV-ARCH-004 | low | fact | Terminology | Expanded acronyms and TOON; defined `subagent` as preferred spelling. | corrected |
| PMPO-003 | low | proposal | Scope terminology | Retained **non-scope** as the task-contract label; exclusions describe boundaries. | accepted |
| SEC-A11Y-003, DEPTH-002 | low | fact | Answers and lab navigation | Added descriptive answer labels and all twelve lab links. | corrected |
| DOCMAINT-006, PROV-008 | medium/low | risk/fact | Source review status | Replaced premature review claims with author verification pending recheck. | corrected |

## Source provenance and adaptation

The independent provenance reviewer verified the declared Git commits and found
the curriculum examples and structures harness-specific. It did not provide
legal approval. It identified the missing repository license, DAIR license
path, OWASP identity, transformation records, visible links, destination checks,
and premature status. Agent-owned corrections were applied; license selection
remains with the repository owner.

## Post-correction recheck

Pending. The corrected snapshot must be frozen and reviewed read-only by New
Learner, Documentation Maintainer, Source Provenance, and Depth/Anti-padding.
Record each decision and any new finding here before final regression.

## Approval boundary

Passing validation and reviewer rechecks supports readiness. It does not grant
publication authority, select a repository license, accept security risk, or
approve organizational adoption. Those decisions remain with assigned humans.
