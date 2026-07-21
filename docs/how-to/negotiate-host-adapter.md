---
title: Negotiate a host adapter
description: Map portable operations to explicit native support or safe deterministic fallbacks.
---

# Negotiate a host adapter

Run these commands from a consumer repository after installing the full skill
set. Create the adapter and request JSON files from the schemas and fixtures in
`.agents/skills/ai-sdlc-host-adapter/references/`; replace the example names
below with the reviewed files you created. Start with `adapter.py --help` if
the installed version exposes different options.

Validate an adapter manifest before trusting any capability claim:

```bash
python3 .agents/skills/ai-sdlc-host-adapter/scripts/adapter.py . \
  --adapter adapters/team-host.json --validate
```

Then negotiate an exact request:

```bash
python3 .agents/skills/ai-sdlc-host-adapter/scripts/adapter.py . \
  --adapter adapters/team-host.json --negotiate \
  --request workflow-capabilities.json --write
```

The complete TOON result distinguishes native mappings, registered fallbacks,
unsupported operations, missing capabilities, and requested versus effective
limits. Missing concurrency or isolation reduces work to sequential execution;
it never creates an implicit sandbox. An incompatible result must block host
handoff rather than silently dropping workflow semantics.

Success is a zero exit with a negotiation report below `_ai_sdlc/adapters/`.
If validation names an unknown capability or incompatible API range, correct
the manifest/request source; do not edit the generated decision or claim a
fallback the host has not implemented.

The bundled full, sequential, and read-only fixtures are conformance classes,
not claims about named products or their current versions.
