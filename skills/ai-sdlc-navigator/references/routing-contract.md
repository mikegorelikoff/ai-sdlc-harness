# Navigator Routing Contract

## Signal precedence

1. Explicit feature argument.
2. Feature with an active skill.
3. Feature slug contained in the current Git branch.
4. Most recently updated feature state.
5. Natural-language intent and repository shape.

## Required action fields

- `skill`: exact installed or expected skill name.
- `reason`: evidence-backed explanation.
- `command`: portable invocation guidance.
- `expected_artifact`: durable output or `none` for read-only work.

## Detected context fields

- repository root and branch;
- installed skill count;
- discovered feature slugs;
- selected feature and workspace;
- current and active lifecycle stage;
- dirty working-tree count.

## Safety

The navigator is read-only. Missing explicit features, blocked stages, corrupt
state, and missing recommended skills are blockers. Optional actions never
override a required lifecycle predecessor.
