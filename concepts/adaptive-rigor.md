<!-- public-docs-canonical: ../docs/index.md -->

> **Internal, non-canonical design note.** The maintained public documentation starts at [AI SDLC Harness docs](../docs/index.md). This file is retained for repository history and maintainer context only.

# Adaptive Rigor

The harness can select an explainable delivery profile from eight scored risk
factors instead of using story count as a proxy for complexity.

Profiles are ordered:

1. `patch` — local, reversible, clear work;
2. `standard` — normal feature delivery;
3. `assured` — high-impact, novel, or multi-system work;
4. `regulated` — material compliance or critical security/data exposure.

Factors use scores from 0 to 3: blast radius, irreversibility, ambiguity,
security/data sensitivity, compliance, external dependencies, architectural
novelty, and rollout complexity.

Run `skills/_shared/ai_sdlc_rigor.py` for Markdown or TOON output. Explicit
`--quick-flow` requests patch rigor and `--full-flow` requests at least assured
rigor, but neither can reduce automatic risk or an organization
`--minimum-profile`. Every decision exposes automatic, requested, minimum, and
effective profiles plus factor scores and escalation reasons.
