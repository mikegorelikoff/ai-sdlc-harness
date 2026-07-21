---
name: ai-sdlc-research
description: Optional AI SDLC research workflow. Use when an AI assistant needs to investigate a customer, market, domain, technology, regulation, competitor, operational question, or implementation uncertainty and produce a routed source inventory plus synthesized findings with confidence, limitations, open questions, and delivery trace targets. Supports `--quick-flow` for focused evidence and `--full-flow` for multi-source and source-diversity gates.
---

# ai-sdlc-research: Sourced Delivery Evidence

> Optional domain skill, not required by the core module.
> Every rule below is important to follow. None of it can be skipped.
> Research informs decisions; it does not silently become a requirement or approval.

## 0. Skill Card

- Skill name: `ai-sdlc-research`
- Primary audience: Research, PM, BA, Architecture
- Supporting audience: Dev, QA, Security, Delivery
- Audience tags: Research, PM, BA, Architecture, Dev
- SDLC stage: Discovery, refinement, and design evidence
- Purpose: Preserve questions, sources, findings, confidence, and limitations.
- Output: `research.md` and `_ai_sdlc/research.toon`

### 0.1 Required Inputs

- Owning feature root.
- Research input using `ai-sdlc-research-input/v1`.
- Verifiable source locators and delivery trace targets.
- Internet access through the host web or browser tool for external or current questions.

### 0.2 Clarification Rules

- Ask when topic, decision to inform, source boundary, or freshness requirement is unclear.
- Separate sourced findings from inference and unresolved questions.
- Record contradictory sources and limitations; do not average them away.
- Do not claim current facts, legal conclusions, or user evidence without verification.

### 0.2.1 Flow Mode Flags

- Support `--quick-flow` and `--full-flow`; full flow takes precedence.
- Quick flow permits one strong source when scope is explicitly narrow.
- Full flow requires at least two sources and two source types for each report.
- External and mixed scopes require an internet search and at least one direct
  `http://` or `https://` source locator; do not cite search-result pages.
- Both modes require every finding to cite registered sources and trace targets.

### 0.3 Output Rules

- Return question, source, finding, confidence, blocker, and output path counts
  directly in the active agent response.
- Before the final response, emit `ai-sdlc-handoff/v1` with `result`,
  `blockers`, `next_required`, and `next_optional`; every action includes
  `reason`, `command`, and `expected_artifact`.
- Do not create `summary.txt`, `*-summary.txt`, or uncited research prose.
- Keep quotes within source rights and use concise paraphrase by default.

### 0.4 Artifact Routing

- Write `<feature-root>/research.md`.
- Write `<feature-root>/_ai_sdlc/research.toon`.
- Keep downloaded or licensed source files outside generated output unless allowed.
- Link research to requirements and decisions; do not overwrite them.

## 0.4.1 Runtime Path Resolution

- Treat `skills/` in commands as a logical skill root. In a harness source checkout, use `skills/`; in a project-scoped consumer installation, resolve it to `.agents/skills/`. Before running a helper, verify that the selected root contains both this skill and `ai-sdlc-shared-runtime`; block with the missing path if neither layout exists.

## 0.5 Feature State Machine

- Read `<feature-root>/_ai_sdlc/state.toon` before durable research writes.
- Research is optional and does not add a core lifecycle stage.
- `--state-check` is read-only; `--begin-state` and `--complete-state` are rejected.
- Accepted implications move through decisions, requirements, SDD, or change impact.

## 0.6 Artifact Metadata And Metatags

- Markdown starts with `artifact_metadata` using schema `ai-sdlc-research-metadata/v1`.
- Include `metatags` for `ai-sdlc`, `research`, `evidence`, and `traceable`.
- Record feature, workspace, flow mode, state file, trace IDs, and review status.

## 0.7 Specs Index

- Read the relevant `specs/_ai_sdlc/specs-index.toon` or
  `specs-refiniment/_ai_sdlc/specs-index.toon` before broad reads.
- Refresh the matching `specs/specs-index.md` or
  `specs-refiniment/specs-index.md` only after durable writes.
- Keep research inside the feature whose decisions it informs.

## References

- Read `references/research-contract.md` for source and finding requirements.
- Read `references/web-research-protocol.md` before external or current research.
- Use `scripts/research.py` to validate citations and route canonical outputs.

## Script Usage

```bash
python3 skills/ai-sdlc-research/scripts/research.py specs-refiniment/payments --input /tmp/research.json --emit --quick-flow
python3 skills/ai-sdlc-research/scripts/research.py specs/payments --input /tmp/research.json --write --full-flow --format toon
```

## Purpose

Add disciplined evidence gathering when delivery uncertainty warrants it without
forcing research ceremony or internet access into every core workflow.

## Inputs

- Frame answerable questions connected to delivery traces.
- Register source title, locator, type, access date, credibility, and notes.
- Cite source IDs from each synthesized finding.
- Record confidence, limitations, and unresolved owner/action pairs.

## Steps

1. Define the decision to inform, research questions, and `internal`, `external`,
   or `mixed` evidence boundary.
2. For external or current questions, search the internet with the available
   web/browser tool, open direct result pages, compare publication and event
   dates, and prioritize primary or official sources.
3. Gather internal evidence when applicable and keep it distinguishable from web sources.
4. Register source identity, direct locator, access date, freshness, type, and credibility.
5. Synthesize findings separately from quotations and assumptions.
6. Record confidence, limitations, conflicts, and open questions.
7. Finalize routed Markdown and TOON outputs.
8. Route accepted implications through owning decisions and artifacts.

## Output Spec

`ai-sdlc-research/v1` contains topic, questions, sources, findings, source IDs,
confidence, limitations, trace targets, and owned open questions.

Quality gate:

- Pass when source IDs resolve, findings have confidence plus limitations, and
  delivery traces explain why the evidence matters.
- Full flow fails without two sources, two source types, or any open question owner.

## Examples

A valid finding cites `SRC-001/SRC-003`, states medium confidence, names data
freshness limitations, and traces to `DEC-022`. “Competitors all do this” is
invalid without registered sources, boundary, or confidence.

## Edge Cases

- A source may support and contradict different findings; keep both links.
- A blocked source remains registered only if its unavailability matters.
- Time-sensitive sources include an explicit access date and freshness limitation.
- Full flow source diversity counts distinct `type` values, not duplicate URLs.
- If internet access is unavailable for external scope, report a blocker and do
  not present cached model knowledge as completed research.

## Scope Boundary

- Do not fabricate sources, quotes, dates, or research participants.
- Do not turn findings into accepted decisions or requirements automatically.
- Do not provide legal or regulatory conclusions without qualified review.
- Do not hide conflicting or low-confidence evidence.
- Use `$ai-sdlc-change-impact` when accepted research changes downstream artifacts.
