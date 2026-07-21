# Delivery Graph Contract

## Identity and authority

The graph is a deterministic generated projection. Trace IDs are scoped by
feature (`trace:<feature>:<ID>`), while artifacts, components, evidence,
commits, and releases use type-prefixed repository-stable identities. Every
node and edge carries a content fingerprint and at least one exact evidence
anchor. Markdown and Git remain authoritative.

## Derivation

- A stable ID at the beginning of a Markdown list item, heading, table row, or
  `ID:` field is a declaration. Other occurrences are references.
- A declared task referencing a requirement creates `traces-to`; a declared
  test referencing a requirement creates `verifies`.
- `Component: <path> -> <ID>` creates `implemented-by` from the trace node.
- `Evidence: <path> -> <ID>` creates `proves` from evidence to the trace node.
- `Task:` in a commit body creates `implements`; a Git tag creates `releases`.
- No lexical or embedding similarity is permitted to create an edge.

## Queries and gaps

Trace paths traverse semantic edges in either direction and omit artifact
declaration edges unless the artifact is an endpoint. Short keys must resolve
to exactly one scoped node. Gap analysis reports explicitly declared leaf
acceptance criteria without tasks or tests, tasks and tests without requirement
links, and commits without task links. Other requirement declarations remain
inventory and trace/orphan evidence. Orphans are non-artifact nodes with no
semantic edge.

Identical authoritative bytes and Git references must produce byte-identical
graph JSON, gap ordering, orphan ordering, and query paths.
