---
title: Choose a flow mode
description: Select quick, full, or adaptive rigor from delivery risk instead of feature size alone.
---

## Use quick flow

Choose `--quick-flow` when the change is bounded, reversible, low-risk, and supported by clear repository evidence. The skill may make documented assumptions and run focused checks, but it must still expose uncertainty and preserve protected controls.

## Use full flow

Choose `--full-flow` when requirements are ambiguous, several roles must approve, or the work affects security, regulated data, money movement, migrations, external contracts, or difficult rollback. Full flow stops on missing upstream decisions and verifies the complete handoff chain.

## Use adaptive policy

When neither explicit flag is supplied, the rigor engine can classify risk as
patch, standard, assured, or regulated. Inspect factor scores and escalation
reasons. Automatic selection never outranks an explicit full-flow request. An
organization minimum applies only when supplied to the rigor helper or required
by enforced delivery policy; presentation configuration is not that control.

## Record the decision

If flow choice materially changes validation or approval behavior, add it to the feature decision log. “Small change” is not enough evidence; name reversibility, blast radius, data sensitivity, contract impact, and uncertainty.
