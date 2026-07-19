---
title: Query the delivery graph
description: Build deterministic lifecycle traceability and inspect paths, gaps, and orphan nodes.
---

# Query the delivery graph

Build the current graph from canonical specs and traceable Git history:

```bash
python3 skills/ai-sdlc-delivery-graph/scripts/delivery_graph.py . \
  --index --write --format toon --quick-flow
```

The command writes complete deterministic TOON for agents, Markdown for human
review, and JSON only for schema/interoperability consumers below `_ai_sdlc/`.
These files are generated views; source Markdown, commit messages, and tags
remain authoritative.

## Follow a trace

Use stable short IDs when they are unique:

```bash
python3 skills/ai-sdlc-delivery-graph/scripts/delivery_graph.py . \
  --trace AC-004 --to T006 --format toon
```

If the same ID exists in multiple features, use the reported scoped ID, for
example `trace:payments:AC-001`. A path includes ordered nodes, edges, exact
evidence anchors, and the graph fingerprint used for the answer.

## Find delivery gaps

```bash
python3 skills/ai-sdlc-delivery-graph/scripts/delivery_graph.py . \
  --gaps --format markdown

python3 skills/ai-sdlc-delivery-graph/scripts/delivery_graph.py . \
  --orphans --format toon
```

Resolve a missing relationship in its authoritative artifact. Do not edit the
generated graph or add broad links merely to increase a coverage count.

For relationships that cannot be expressed with normal stable references, use
an explicit line in lifecycle Markdown:

```text
Component: src/payments.py -> T006
Evidence: evidence/payments-validation.json -> TC-004
```
