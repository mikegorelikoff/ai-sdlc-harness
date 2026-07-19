# Context Engine V2 Contract

## Topology

The engine builds a deterministic `ai-sdlc-repository-topology/v2` projection
from tracked safe files, CODEOWNERS-style ownership rules, source and test file
names, repository manifests, and detected validation commands. Ownership uses
last matching rule. Test links require a matching stem or a source-adjacent test
directory; similarity alone cannot create a link.

## Conditional selection

Built-in selectors choose repository guidance, exact requested paths, owning
feature specs, manifests, ownership evidence, and related tests. Optional
`ai-sdlc-context-selectors/v2` rules contain exact task/path/tag conditions,
bounded include globs, priority, per-file token cap, and an explanation.
Non-matching selectors record why they were skipped.

## Budget and exclusions

Token estimates use deterministic UTF-8 character approximation. Candidates
sort by descending priority then path. A candidate is clipped at its declared
cap and remaining pack budget; no selection may exceed the total budget.
Absolute paths, traversal, generated outputs, symlinks, oversized binaries,
secret-named paths, built-in secret directories, configured exclusions, and
content matching credential assignment patterns are excluded before content is
returned.

## Freshness

Each selected range carries a current content hash. The pack reports saved
project-context drift and any selected paths referenced by non-fresh evidence
ledger records. Missing or unreadable freshness projections become explicit
warnings, never silent `fresh` claims. Identical task inputs and repository
state produce byte-identical packs and fingerprints.
