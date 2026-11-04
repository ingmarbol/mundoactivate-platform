# Clean-room restore runbook

1. Declare the incident and freeze destructive automation.
2. Establish an isolated recovery account/subscription and clean administration workstation.
3. Recover identity, DNS, network and KMS/Key Vault dependencies through approved break-glass access.
4. Select the latest known-good recovery point that satisfies the ransomware dwell-time decision.
5. Scan artifacts and data before reconnecting production networks.
6. Restore databases first, then cluster state, persistent volumes and applications from trusted images.
7. Validate checksums, schema, authentication and one synthetic business transaction.
8. Record actual RPO/RTO, skipped objects, exceptions and cost.
9. Obtain business/security authorization before failover or failback.
10. Delete temporary restore resources, revoke access and preserve audit evidence.

Never paste credentials, private keys or backup data into tickets or logs.

