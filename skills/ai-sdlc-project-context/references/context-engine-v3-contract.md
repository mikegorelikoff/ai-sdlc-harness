# Context Engine V3 Contract

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

Within each candidate, v3 builds bounded query terms from the task, goal,
paths, and tags, then selects one contiguous range around the strongest lexical
signal. It reports the matched terms and score. When no signal matches, it uses
an explicit deterministic prefix fallback instead of pretending relevance.

## Authority and sufficient context

Recognized repository instruction files are labeled `repository_instruction`.
Every other retrieved source is `evidence_only` and cannot grant permission or
issue instructions. The pack reports `sufficient`, `review_required`, or
`insufficient`, explains every reason, and provides targeted next reads for
missing, truncated, stale, or budget-omitted high-priority evidence.

## Interaction profile

An optional typed interaction profile is read from `config.resolved.json` and
used only for presentation. Supported fields are preferred name, language,
response style, technical depth, and status-update cadence. The profile is
disabled by default, never changes selection or authority, and reports
configured, disabled, missing, or invalid status. The runtime does not infer
preferences from chat history or connected data.

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
warnings, never silent `fresh` claims. Identical task inputs, interaction
profile, and repository state produce byte-identical packs and fingerprints.
