# Test Environment Resolution

- Owner: QA Platform lead.
- Environment: isolated OIDC simulator in the non-production integration tier.
- Data: synthetic organizations, members, claims, clock offsets, and revoked
  sessions; no production identity data.
- Availability: reserved for smoke and regression suites before release review.
- Evidence: simulator version, configuration fingerprint, suite run identity,
  timestamps, and retained failure output.
- Escalation: Security and QA jointly approve any change to negative assertion,
  clock-skew, or session-revocation coverage.
