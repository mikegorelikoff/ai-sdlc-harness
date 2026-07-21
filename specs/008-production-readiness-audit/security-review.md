---
artifact_metadata:
  schema: "ai-sdlc-artifact-metadata/v1"
  status: "validated"
  owner: "Security-review"
---

# Security review

## Findings

No unresolved local Critical, High, or Medium security finding remains after
recovery-manifest, symlink/traversal, migration, feature-slug, approval-parser,
receipt-fingerprint, output-limit, timeout/descendant, and trust-language
regressions. Local hashes and approval records remain unauthenticated; protected
Git, trusted continuous integration, provider controls, and external audit logs
are required for independent assurance.

## Skills.sh follow-up

All 44 live Skills.sh records and 132 provider results were reconciled against
the candidate. Thirty-three skills had no provider warning/failure and eleven
were flagged. Confirmed local corrections are:

| Provider challenge | Source correction | Evidence |
| --- | --- | --- |
| Snyk credential handling | Approval commands are redacted before capture, prompting, tool use, logging, or output and unsafe originals are never echoed. | Marketplace security contract PASS. |
| Snyk indirect prompt injection | Nine affected skills declare repository, requirement, Git, and reviewer content data-only; context, graph, council, and project-context output carries trust markers. | Marketplace security contract plus per-skill suites PASS. |
| Agent Trust Hub dynamic loading | BA and commit runtime paths are bounded beneath the installed skills root; dynamic test imports are replaced by a fixed subprocess contract. | Both focused skill suites PASS. |
| Socket target-root execution anomaly | Compatibility uses static flag/module inspection and byte comparison; the optional Git binary must resolve absolutely outside the target root. | Malicious target fixture is inspected without creating its execution marker. |

Repository fixes cannot change a prior audit snapshot. The candidate must be
committed, published, and rescanned before external warnings can be called
cleared. Any remaining warning on intentional bounded local command execution
requires provider-specific review rather than a blanket waiver.
