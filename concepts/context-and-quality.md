# Context And Quality Gates

Every lifecycle artifact must be useful in a later stage and a later session.
The harness therefore treats context collection and artifact quality as related
but separate concerns:

- context packs make source evidence affordable to inspect;
- self-contained Markdown preserves the resulting feature understanding;
- quality gates prevent structurally complete but unusable artifacts from being
  finalized.

## Source Resolution

For default and full refinement flow, an explicit input is priority evidence,
not the complete source set. The context builder unions:

- explicit files supplied to the skill;
- visible Markdown in the matching feature folder;
- artifacts found through the workspace specs index;
- feature state, decisions, and relevant implementation/refinement auxiliaries.

Quick flow with explicit files stays focused and does not automatically union
the whole feature package.

The target artifact and derived context files are excluded from their own
source set. This prevents self-referential amplification and stops generated
TOON from being treated as new product evidence.

## Context Records

Default and full analysis maintain two derived records:

```text
<feature>/_ai_sdlc/context/<skill>.toon
<feature>/_ai_sdlc/feature-context.toon
```

The per-skill file is an `ai-sdlc-context/v2` snapshot containing the exact
evidence contract used by that skill. The feature context file is a
skill-neutral, deterministic source inventory. One stage can update the feature
inventory without replacing another stage's saved anchors or source hashes.

Both are derived. They are excluded from specs indexes and should be ignored by
Git. If removed, rerunning analysis recreates them from durable sources.

## Context Pack Shape

An `ai-sdlc-context/v2` pack contains:

- `sources`: path, content hash, and current/missing status;
- `anchors`: exact source excerpts with section and line location;
- `gaps`: deterministic missing-source or blocker signals;
- `next_reads`: targeted source ranges that did not fit the active budget;
- `trace_ids`: the complete discovered ID set;
- fingerprint and budget status for cache validation.

Anchors are evidence excerpts, not AI-authored summaries. When a range is listed
under `next_reads`, the agent must open it before claiming complete source
coverage.

## Token Budgets

| Flow | Context budget | Final artifact cap | Intended behavior |
| --- | ---: | ---: | --- |
| Quick | 4,000 | 24,000 | Focused evidence and assumptions |
| Default | 24,000 | 24,000 | Whole-feature context with pragmatic warnings |
| Full | 24,000 | 24,000 | Whole-feature context with strict depth and blocker handling |

The budget is a ceiling for the generated pack or artifact, not permission to
drop a feature dimension. When sources exceed the context budget, the pack
preserves high-priority anchors and emits targeted reads. When an artifact
approaches its cap, condense repeated wording while preserving scope, workflows,
rules, risks, decisions, success measures, and source coverage.

## Self-Contained Artifact Contract

Every default/full refinement artifact includes these shared sections:

1. Feature Summary
2. Actors and Stakeholders
3. Scope and Boundaries
4. Workflows and Failure Paths
5. Requirements and Business Rules
6. Data, Integrations, and Non-Functional Requirements
7. Dependencies, Risks, and Constraints
8. Decisions, Assumptions, and Open Questions
9. Success Measures
10. Source Coverage

Stage-specific sections follow the shared context. Quick artifacts use only the
canonical stage sections to remain compact.

Self-contained does not mean copying every upstream file verbatim. It means a
reader can understand the feature, boundaries, critical behavior, uncertainty,
and evidence relevant to this stage without relying on chat history.

## Deterministic And Heuristic Gates

Quality checks produce structured issues with `error` or `warning` severity.

| Check | Quick | Default | Full |
| --- | --- | --- | --- |
| Artifact exceeds 24,000 tokens | Error | Error | Error |
| Required section missing or placeholder-only | Not applied | Error | Error |
| Required table columns or populated rows missing | Not applied | Error | Error |
| Consumed source absent from Source Coverage | Not applied | Error | Error |
| Saved source missing or hash-stale | Not applied | Error | Error |
| Section has weak detail | Not applied | Warning | Error |
| Open marker lacks owner, impact, and resolution/next step | Not applied | Warning | Error |

Deterministic gates enforce contracts the runtime can prove. Heuristic gates
estimate whether prose is sufficiently useful. Default flow surfaces heuristic
weakness without turning every draft into a blocker; full flow promotes the same
signals to blocking errors.

## Source Freshness

Each snapshot records source hashes. Finalization compares those hashes with
the current files. If an upstream artifact changed after analysis, the artifact
cannot safely claim it used current context. The agent reruns analysis, reviews
the changed evidence, updates affected sections, and finalizes again.

This is optimistic consistency: source files remain editable, but a finalizer
cannot silently rely on an obsolete snapshot.

## Source Coverage

`Source Coverage` lists the sources actually consumed for the artifact and
states what each contributed. A good entry is specific:

```markdown
- `specs-refiniment/payment-retry/discovery.md` — customer pain, current
  workaround, and adoption measure.
- `specs-refiniment/payment-retry/decision-log.md` — accepted retry ownership
  and rollout decision `DEC-004`.
```

A bare claim such as “all files reviewed” is not enough when the source
inventory identifies individual paths. Coverage provides provenance; it does
not imply stakeholder approval.

## Full Package Status

`refinement_status.py --gate full` evaluates package-level consistency:

- lifecycle stages are done;
- all 18 canonical files exist and are indexed;
- decision log and both indexes exist;
- artifacts use full flow;
- blocking artifact quality checks pass.

Warnings are counted separately from blockers. Under the full gate, the
depth/open-marker heuristics are already promoted to errors, so `18/18` means
the complete cascade met the strict contract.

## Failure And Recovery Examples

- **`minimum_overflow`:** even the pack envelope exceeds budget. Reduce source
  metadata overhead or split/target the request; do not claim full coverage.
- **`next_reads_required`:** open every listed range before writing or
  finalizing the affected sections.
- **Stale source:** rerun the skill analysis and review the changed upstream
  artifact.
- **Placeholder section:** replace the scaffold marker with evidence,
  documented assumptions, or an explicit evidence-backed N/A.
- **Default warning:** improve it when practical and surface residual risk; it
  does not automatically fail default finalization.
- **Full error:** stop finalization until resolved or return the concrete
  blocker to the user.
