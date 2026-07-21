# Project Context Contract

High-signal sources are repository guidance, README files, package and language
manifests, Makefiles, and common CI workflows. Claims require `path:line`
anchors. The fingerprint is SHA-256 over normalized relative path and content
for every consumed source. Secret-named, environment, key, token, credential,
and certificate paths are excluded.

Canonical outputs are `project-context.md` and
`_ai_sdlc/project-context.toon`. Both use the same revision and fingerprint.
Drift is true when either differs from the current repository scan.

## External specification snapshots

Automatic project context remains repository-bounded. A separately governed
specification checkout may be consumed only through an explicit snapshot of
selected UTF-8 Markdown files. The snapshot contract rejects path escape,
symlinks, oversized/binary content, credential-shaped content, and destination
collisions; writes top-level refinement evidence plus a portable manifest;
records source-relative paths, Git revision, byte sizes, and SHA-256 hashes;
labels content `evidence_only`; and never records the absolute source root or
deletes omitted sources automatically. Check mode compares source, local copy,
and manifest without writing.
