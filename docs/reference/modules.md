---
title: Module catalog
description: Installed capability modules, compatibility ranges, dependencies, and registered skills.
---

# Module catalog

<div class="grid cards" markdown>

-   **Architecture** · `optional` · `v1.0.0`

    Traceable system architecture decisions, interfaces, risks, and validation.

    **Harness API:** ≥ 1.0.0 and < 2.0.0

    **Requires:** core

    **Skills:** ai-sdlc-architecture

    [Open manifest →](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/modules/architecture/module.json)

-   **Core** · `core` · `v1.8.0`

    Core AI SDLC lifecycle, control-plane, and delivery skills.

    **Harness API:** ≥ 1.0.0 and < 2.0.0

    **Requires:** none

    **Skills:** ai-sdlc-approvals-sandbox, ai-sdlc-ba, ai-sdlc-backlog-decomposition-and-task-planning, ai-sdlc-backlog-requirements-gap-review, ai-sdlc-branching, ai-sdlc-change-set, ai-sdlc-change-impact, ai-sdlc-code-review, ai-sdlc-commit-prep, ai-sdlc-conventional-commit, ai-sdlc-delivery-handoff-review, ai-sdlc-delivery-graph, ai-sdlc-delivery-package-gap-review, ai-sdlc-delivery-spec-synthesis, ai-sdlc-goal-capability-and-epic-mapping, ai-sdlc-navigator, ai-sdlc-policy, ai-sdlc-prfaq-package-synthesis, ai-sdlc-project-context, ai-sdlc-qa, ai-sdlc-qa-requirements-gap-review, ai-sdlc-qa-traceability-and-readiness-review, ai-sdlc-quality-lenses, ai-sdlc-release-slicing-and-backlog-readiness-review, ai-sdlc-requirements-readiness-review, ai-sdlc-retrospective, ai-sdlc-host-adapter, ai-sdlc-runtime, ai-sdlc-workflow, ai-sdlc-sdd, ai-sdlc-security-testing, ai-sdlc-test-case-and-suite-synthesis, ai-sdlc-test-cases, ai-sdlc-test-scope-and-strategy-design, ai-sdlc-user-story-decomposition, ai-sdlc-validation, ai-sdlc-working-backwards-discovery

    [Open manifest →](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/modules/core/module.json)

-   **Evidence Council** · `optional` · `v1.0.0`

    Authority-safe simulated and independent evidence review orchestration.

    **Harness API:** ≥ 1.0.0 and < 2.0.0

    **Requires:** core

    **Skills:** ai-sdlc-evidence-council

    [Open manifest →](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/modules/evidence-council/module.json)

-   **Research** · `optional` · `v1.0.0`

    Sourced research questions, evidence inventory, confidence, limitations, and delivery traces.

    **Harness API:** ≥ 1.0.0 and < 2.0.0

    **Requires:** core

    **Skills:** ai-sdlc-research

    [Open manifest →](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/modules/research/module.json)

-   **Ux** · `optional` · `v1.0.0`

    Traceable actors, journeys, interaction states, accessibility, and UX acceptance.

    **Harness API:** ≥ 1.0.0 and < 2.0.0

    **Requires:** core

    **Skills:** ai-sdlc-ux

    [Open manifest →](https://github.com/mikegorelikoff/ai-sdlc-harness/blob/main/modules/ux/module.json)

</div>

Module discovery validates schema, ID uniqueness, dependency presence, API compatibility, skill paths, and protected capability rules before navigation exposes a module.
