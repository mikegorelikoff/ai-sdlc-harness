---
title: Negotiate a host adapter
description: Map portable operations to explicit native support or safe deterministic fallbacks.
---

# Negotiate a host adapter

Validate an adapter manifest before trusting any capability claim:

```bash
python3 skills/ai-sdlc-host-adapter/scripts/adapter.py . \
  --adapter adapters/team-host.json --validate
```

Then negotiate an exact request:

```bash
python3 skills/ai-sdlc-host-adapter/scripts/adapter.py . \
  --adapter adapters/team-host.json --negotiate \
  --request workflow-capabilities.json --write
```

The complete TOON result distinguishes native mappings, registered fallbacks,
unsupported operations, missing capabilities, and requested versus effective
limits. Missing concurrency or isolation reduces work to sequential execution;
it never creates an implicit sandbox. An incompatible result must block host
handoff rather than silently dropping workflow semantics.

The bundled full, sequential, and read-only fixtures are conformance classes,
not claims about named products or their current versions.
