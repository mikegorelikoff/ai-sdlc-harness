---
title: Diagnose and plan an upgrade
description: Inspect installation health and preview versioned file, schema, backup, and rollback changes without applying them.
---

# Diagnose and plan an upgrade

Run from the root of an installed consumer repository. The doctor writes only
diagnostic evidence. Upgrade mode also requires two reviewed inventory JSON
files; create them from the schema/examples under
`.agents/skills/ai-sdlc-doctor/references/` and do not substitute guessed
hashes or version ranges.

Run the read-only installation doctor:

```bash
python3 .agents/skills/ai-sdlc-doctor/scripts/doctor.py . --doctor --write
```

Each check has a stable code, evidence, status, and remediation. Remediation is
advice, not an executed command.

To preview an upgrade, provide current and target inventories containing safe
paths, exact hashes, schema identities, versions, and harness API ranges:

```bash
python3 .agents/skills/ai-sdlc-doctor/scripts/doctor.py . --upgrade \
  --current current-inventory.json --target target-inventory.json \
  --upgrade-id upgrade-190 --write
```

Review every add, modify, remove, schema migration, backup destination, and
reverse-order rollback action in the TOON plan. An incompatible API range is a
hard blocker. Applying or rolling back the plan belongs to a separate explicitly
authorized workflow.
Success writes a diagnostic or upgrade plan below `_ai_sdlc/`. Any incompatible
API range, missing backup, unsafe path, or hash mismatch remains a blocker; fix
the inventories or selected release before applying anything.
