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
- installed skill count and the source, project, or executing packaged roots
  that supplied it;
- discovered feature slugs;
- selected feature and workspace;
- current and active lifecycle stage;
- dirty working-tree count.

## Safety

The navigator is read-only. Missing explicit features, blocked stages, corrupt
state, and missing recommended skills are blockers. Optional actions never
override a required lifecycle predecessor.

Skill discovery is a de-duplicated union of `<repository>/skills`,
`<repository>/.agents/skills`, and the sibling skill root inferred from the
executing navigator script. It does not scan arbitrary home directories. This
supports a packaged/global installation while keeping discovery bounded to the
package that was explicitly executed.
