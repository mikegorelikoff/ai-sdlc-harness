---
title: Artifact routing
description: Canonical locations for refinement, implementation, state, plans, decisions, indexes, and supporting evidence.
---

| Artifact class | Canonical route |
| --- | --- |
| PM, BA, discovery, backlog, delivery, QA refinement | `specs-refiniment/<feature>/` |
| Developer implementation SDD | `specs/<feature>/` |
| Feature lifecycle state | `<workspace>/<feature>/_ai_sdlc/state.toon` |
| Machine execution plan | `specs/<feature>/_ai_sdlc/plan.toon` |
| Human execution plan | `specs/<feature>/plan.md` |
| Implementation decision log | `specs/<feature>/decision-log.md` |
| Refinement decision log | `specs-refiniment/<feature>/decision-log.md` |
| Workspace machine index | `<workspace>/_ai_sdlc/specs-index.toon` |
| Workspace human index | `<workspace>/specs-index.md` |

Legacy paths migrate through shared helpers on the next write. Do not manually merge divergent legacy and canonical files. Markdown remains authoritative for detailed truth; TOON files are bounded control projections.
