---
title: Extend skills and modules
description: Add or change skills, helpers, references, schemas, modules, catalogs, and compatibility without creating hidden runtime or documentation contracts.
---

# Extend skills and modules

Extend the smallest authority surface that owns the behavior. A skill owns one
bounded agent workflow. A module registers a coherent capability group. Shared
runtime owns reusable deterministic mechanics. Public docs translate these
contracts but do not replace them.

## 1. Define the contract

Before files, state:

- user and problem;
- use and non-use situations;
- required inputs and source authority;
- accountable and supporting roles;
- allowed reads/writes and protected actions;
- quick/full behavior;
- artifact paths, schemas, state/index effects, and handoff;
- deterministic helper need, failure semantics, and recovery;
- compatibility, migration, deprecation, and rollback impact.

Use `ai-sdlc-sdd` for a medium or large change. Do not make a package because a
prompt is long; make it because a stable bounded capability needs portable
authority and validation.

## 2. Create or change a skill

A skill package uses:

```text
skills/ai-sdlc-<name>/
├── SKILL.md
├── scripts/        # optional deterministic helpers
├── references/     # optional detailed contracts and schemas
└── tests/          # focused behavior and failure tests
```

`SKILL.md` needs frontmatter identity, a complete Skill Card, required inputs,
clarification rules, flow flags, output rules, artifact routing, state,
metadata, index behavior, source/reference routing, helper usage, success gate,
edge cases, and scope boundary. Its public guide is generated; never hand-edit
`docs/reference/skills/<skill>.md`.

Add an explicit selection boundary to `SKILL_SELECTION_BOUNDARIES`. Generation
must fail if the new skill lacks a concrete “use another capability instead”
case.

## 3. Add deterministic helpers

Use a helper for parsing, scaffolding, validation, indexing, migration,
fingerprinting, routing, or reproducible reporting—not for hidden product
judgment.

Helpers should:

- have a module docstring and useful `--help`;
- validate types, schemas, paths, and mode conflicts;
- default to read/check/preview/emit behavior where practical;
- require explicit write/apply/execute modes for mutation;
- write atomically, fail closed, and return stable non-zero exits;
- avoid secrets and avoid network unless the owning contract requires it;
- emit complete TOON for agent control-plane state;
- keep JSON at schema/interoperability/recovery boundaries;
- report exact outputs and recovery action;
- include positive, negative, and mutation tests.

If a helper imports `skills/_shared`, keep the portable installed fallback and
run the skill-only install scaffold smoke test.

## 4. Change shared runtime

Canonical shared source lives under `skills/_shared`. Portable mirrors live
under `skills/ai-sdlc-shared-runtime/scripts` and are generated copies.

!!! terminal "Run in terminal — source checkout"

    ```bash
    python3 skills/_shared/sync_installed_runtime.py --write
    python3 skills/_shared/sync_installed_runtime.py --check
    python3 skills/_shared/ai_sdlc_install_smoke.py --mode emulated
    ```

Review source and mirror changes together. Never fix only a mirror.

## 5. Register a module

Create `modules/<id>/module.json` using the versioned module schema. Declare a
stable ID, semantic version, kind, harness API range, dependencies,
description, and skill entries. Validation rejects duplicate IDs, missing
dependencies, incompatible API ranges, unknown skill paths, and traversal.

Optional modules must remain optional. Core navigation cannot acquire a hidden
dependency on a domain module.

## 6. Evolve schemas and representation

Prefer additive fields inside a compatible schema. A breaking change needs a
new version, migration, compatibility decision, fixtures, failure tests, and
release notes. Human delivery detail remains Markdown; complete agent state and
indexes are TOON-first. JSON is valid for JSON Schema, external
interoperability, exact recovery, and JSONL journals.

Never add a lossy machine projection. Every field required for correct routing,
authority, or recovery must survive serialization.

## 7. Regenerate and validate discovery

!!! terminal "Run in terminal — source checkout"

    ```bash
    python3 docs/scripts/build_catalog.py
    python3 docs/scripts/build_catalog.py --check
    python3 -m unittest docs.tests.test_docs
    python3 docs/scripts/validate_docs.py
    ```

The generator must close the complete skill, module, and script inventories.
Review guide semantics, not only counts. Update MkDocs navigation when adding a
hand-authored public page.

## 8. Compatibility and deprecation

Run compatibility against the accepted baseline. Preserve stable skill names,
flow flags, artifact routes, handoff shape, configuration, module ranges, and
task-to-commit rules unless an approved major change says otherwise.

Deprecation needs:

- replacement and migration path;
- first deprecated release and planned removal boundary;
- warnings in source, docs, compatibility, and release notes;
- fixtures for old and new forms;
- rollback and support statement;
- explicit owner and decision record.

Deleting a capability without inventory, migration, compatibility, and docs
updates is not a deprecation process.
