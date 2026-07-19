# Organization SSO Scenario

## Customer problem

Enterprise administrators provision local accounts manually. Onboarding a new
organization takes a median of three hours, offboarding can lag by one business
day, and security reviewers cannot prove that access follows the customer's
identity-provider policy.

## Audience and actors

- Organization administrator configures and tests identity settings.
- Organization member signs in through the configured provider.
- Support engineer diagnoses configuration failures without seeing secrets.
- Security owner reviews authentication, session, audit, and break-glass rules.
- QA owner accepts environments, test data, negative paths, and evidence.

## Candidate MVP

- OpenID Connect for one provider configuration per organization.
- Administrator-only configuration and a pre-activation connection test.
- Just-in-time member provisioning with explicit organization membership.
- Existing local authentication remains available during a phased migration.
- Audit events cover configuration, successful/failed login, and deactivation.

## Constraints

- SAML, SCIM, provider marketplace, and automated domain discovery are out of
  the first release.
- Secrets must use the existing secret store and never enter agent prompts or
  lifecycle artifacts.
- Break-glass access requires Security-owned policy and current audit evidence.
- Rollout is organization-scoped and reversible.

## Evidence and success signals

- Baseline median enterprise onboarding time: three hours.
- Baseline access-removal lag: up to one business day.
- Mechanism signals: refinement rework, decision latency, failed test count,
  rollout rollback count, and evidence freshness.
- Outcome hypotheses: reduce onboarding time and access-removal lag without
  increasing authentication incidents. A pilot does not prove causality.
