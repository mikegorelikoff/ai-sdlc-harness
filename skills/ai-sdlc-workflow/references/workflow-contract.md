# Declarative Workflow Contract

Workflow definitions are immutable planner inputs. Steps use exact typed actions
and dependencies. Conditions are data comparisons, not expressions or code.
Capabilities must be declared at workflow level and repeated by the steps or
hooks that need them.

Approval steps are exclusive waves and remain pending external evidence. Hooks
are ordered declarations around one exact step; planning records them but never
executes them. Parallel waves require host concurrency, host isolation support,
isolated steps, and parallel-safe step types. Any missing property produces
deterministic sequential waves with explicit fallback reasons.

Generated TOON is the default agent representation. JSON is retained for schema
interoperability and Markdown for human review.
