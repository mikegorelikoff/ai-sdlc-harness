---
title: Directory layout
description: Repository surfaces and the kind of delivery contract each one owns.
---

```text
ai-sdlc-harness/
├── skills/                 # Portable workflow packages
│   ├── _shared/            # Deterministic shared control-plane helpers
│   └── ai-sdlc-*/          # SKILL.md, scripts, tests, references
├── modules/                # Versioned capability manifests
├── guides/                 # Role and operating guides
├── concepts/               # Authoritative conceptual documentation
├── docs/                   # GitHub Pages source and generated catalogs
├── specs-refiniment/       # PM/BA/QA/Delivery refinement workspaces
├── specs/                  # Developer implementation SDD workspaces
├── compatibility/          # Release compatibility baseline
└── .github/workflows/      # CI and Pages automation
```

The historical `specs-refiniment` spelling is a compatibility-preserved canonical route. Migration helpers, rather than ad hoc renames, own any future transition.
