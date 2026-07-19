<!-- public-docs-canonical: ../docs/index.md -->

> **Internal, non-canonical design note.** The maintained public documentation starts at [AI SDLC Harness docs](../docs/index.md). This file is retained for repository history and maintainer context only.

# Optional Modules

The core harness and optional domain capabilities share a versioned manifest
contract without sharing installation requirements. Every module declares its
ID, version, kind, supported harness API range, dependencies, and owned skills
in `modules/<id>/module.json` using `ai-sdlc-module/v1`.

Core never requires an optional module. Discovery validates every installed
manifest, skill path, dependency, API range, module ID, and skill owner before
listing compatible capabilities:

```bash
python3 skills/_shared/ai_sdlc_modules.py --format toon
```

Optional compatible skills are discoverable even when disabled. Enabling an
uninstalled or incompatible module fails instead of silently shrinking the
requested capability set. Resolved layered configuration can supply
`values.modules.enabled`; `--enable` supports explicit one-run selection.
