---
title: Manage evidence freshness
description: Register evidence identity, propagate repository drift, and query fresh-only requirement coverage.
---

# Manage evidence freshness

Store an `ai-sdlc-evidence-source/v1` manifest below an `evidence/` directory
with the suffix `.evidence.json`. The record names its lifecycle subjects,
producer, capture time, evidence artifact, direct dependencies, and any
upstream evidence records.

```json
{
  "schema": "ai-sdlc-evidence-source/v1",
  "id": "payments-validation",
  "kind": "validation",
  "subjects": ["trace:payments:AC-004"],
  "producer": "QA",
  "captured_at": "2026-07-19T10:00:00Z",
  "expires_at": "2026-08-19T10:00:00Z",
  "artifact": {
    "path": "evidence/payments-validation.txt",
    "sha256": "<captured-sha256>"
  },
  "dependencies": [
    {
      "path": "specs/payments/requirements.md",
      "sha256": "<captured-sha256>"
    }
  ],
  "depends_on": []
}
```

Build the ledger using an explicit date when evidence expiry is relevant:

```bash
python3 skills/ai-sdlc-delivery-graph/scripts/evidence_ledger.py . \
  --index --as-of 2026-07-19 --write --format toon
```

## Inspect stale paths and coverage

```bash
python3 skills/ai-sdlc-delivery-graph/scripts/evidence_ledger.py . \
  --stale --as-of 2026-07-19 --format json

python3 skills/ai-sdlc-delivery-graph/scripts/evidence_ledger.py . \
  --coverage --as-of 2026-07-19 --format markdown
```

Resolve the first changed, missing, or expired record in a stale chain, rerun
the producing validation, and capture new identities. Do not edit a generated
ledger status: the next rebuild will derive it again from authoritative bytes.
