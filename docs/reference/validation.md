---
title: Validation commands
description: Deterministic repository gates for skills, specifications, modules, configuration, compatibility, and documentation.
---

```bash
# Repository skill/script contracts
python3 skills/_shared/test_all_skill_scripts.py
python3 skills/_shared/test_each_skill_tests.py

# Release compatibility
python3 skills/_shared/ai_sdlc_compatibility.py --format toon

# Active SDD structure and links
python3 skills/ai-sdlc-sdd/scripts/validate_spec.py specs/NNN-feature --quick-flow
python3 skills/ai-sdlc-sdd/scripts/plan_links.py specs/NNN-feature --check --quick-flow

# Documentation catalogs and source
python3 docs/scripts/build_catalog.py --check
python3 docs/scripts/validate_docs.py
```

Use `ai-sdlc-validation` to choose the smallest relevant set. Commands above are contracts, not a requirement to run every suite for every tiny change. Always record exact outcomes and skipped risk.
