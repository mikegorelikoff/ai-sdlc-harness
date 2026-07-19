# Doctor And Upgrade Contract

Checks are deterministic observations with stable codes. A failed check provides
remediation text but never executes it. Upgrade inventories describe package
content by safe path, exact SHA-256, and optional schema identity.

Modified and removed files require backups. Added files roll back by removal;
modified and removed files roll back by restore. Schema identity changes create
explicit migration actions. API incompatibility or invalid inventory blocks the
plan before any apply authority exists.
