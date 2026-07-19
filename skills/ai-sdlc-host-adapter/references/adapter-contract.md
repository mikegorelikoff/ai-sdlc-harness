# Host Adapter Contract

An adapter manifest is a capability claim, not authority. Native mappings must
declare equivalent semantics. Negotiation may use only the registered fallbacks:
parallel tasks become sequential `task.execute`, lifecycle hooks become explicit
`task.execute` steps, and approval requests become manual `user.prompt` gates.

Missing isolation or concurrency always reduces effective concurrency to one;
it never guesses a host sandbox. Missing required operations or capabilities
without a safe fallback makes the result incompatible.

Fixtures describe conformance classes only and make no product-version claims.
