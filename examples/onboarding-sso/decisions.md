# Accepted Tutorial Decisions

| ID | Owner | Decision | Reason |
| --- | --- | --- | --- |
| DEC-001 | Product | MVP supports OpenID Connect; SAML and SCIM are excluded. | Bound the first customer promise and integration surface. |
| DEC-002 | Security | Existing local sign-in remains during phased rollout; break-glass use is logged and reviewed. | Preserve recoverability without silently weakening authentication policy. |
| DEC-003 | Product / BA | Just-in-time provisioning creates only an explicitly mapped organization member. | Prevent cross-organization account creation and make membership behavior testable. |
| DEC-004 | Delivery | Rollout is opt-in by organization with monitor and rollback owners. | Limit blast radius and retain a reversible adoption path. |

These decisions are inputs, not permission for an agent to approve later
architecture, threat, QA, rollout, or release gates on behalf of their owners.
