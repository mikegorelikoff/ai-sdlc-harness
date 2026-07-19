# Package Trust And Local Metrics Contract

The manifest inventory is authoritative only after every path is proven safe,
regular, non-symlinked, and hash-matching. The package digest hashes normalized
inventory records. Origin, compatibility, capabilities, integrity, and
provenance are independent controls; any required failure denies trust.

Metrics are local, deterministic aggregates. Allowed values are schemas,
fingerprints, statuses, booleans, and numeric counts or budgets. Content,
prompt, command, diff, source text, artifact paths, and file bodies are forbidden.
No network operation exists in either helper.
