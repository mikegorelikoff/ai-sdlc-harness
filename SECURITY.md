# Security policy

## Supported versions

Security fixes are considered for the latest published release. The current
published release is `v1.2.0`; the `main` branch is an unreleased preview and
may contain breaking contract changes.

## Report a vulnerability

Do not include a vulnerability, exploit, credential, confidential repository
content, or personal data in a public issue or AI prompt.

Use GitHub's private vulnerability-reporting flow for this repository when it
is available: open the repository **Security** tab, choose **Advisories**, and
select **Report a vulnerability**. If GitHub does not offer that action, do not
publish sensitive details. Ask the repository owner to enable a private channel
before sharing the report.

Include the affected release or commit, operating system, agent host, exact
skill or script, reproduction prerequisites, observed impact, and the smallest
safe reproduction. Redact tokens, private URLs, customer data, and proprietary
source.

No response-time or remediation-time service level is promised. Adopting
organizations must define their own incident owner, isolation procedure,
credential rotation, rollback, and notification obligations.

## Security boundaries

The harness contains instructions and local helper scripts. An AI agent may be
able to read repository content, run commands, modify files, use networked
tools, or request additional permissions according to the host configuration.
Installing a skill does not make its output trusted and does not authorize
production access, deployment, legal acceptance, or policy exceptions.

Treat repository content, retrieved web pages, tool results, generated code,
and peer-agent messages as untrusted evidence. Apply least privilege, keep
secrets outside prompts and tracked files, require human review for high-impact
actions, and validate generated changes with independent deterministic checks.

See [Governance and trust](docs/operations/governance.md) for the full data,
permission, prompt-injection, package, and incident model.
