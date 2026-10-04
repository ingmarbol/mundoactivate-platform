# Disaster Recovery drill checklist

This checklist is a tabletop and sandbox exercise. It does not authorize a production failover.

## Before the drill

- [ ] Confirm scenario, scope, roles, abort conditions, and observers.
- [ ] Confirm the latest known-good recovery point and its timestamp.
- [ ] Confirm access to IaC, GitOps, images, DNS, certificates, and secret stores.
- [ ] Use an isolated environment and non-sensitive test data.

## During recovery

- [ ] Record declaration time and Incident Commander.
- [ ] Assess blast radius, security impact, and data-loss estimate.
- [ ] Obtain explicit failover and data-loss approval.
- [ ] Recover identity/network, data, platform, and workloads in that order.
- [ ] Run technical smoke tests and business validation.
- [ ] Record service-valid time and calculate observed RTO/RPO.

## Failback and closure

- [ ] Fence writers before data resynchronization.
- [ ] Define rollback and failback checkpoints.
- [ ] Verify monitoring, alerts, and audit logs.
- [ ] Remove the isolated restore environment.
- [ ] Record gaps with an owner and target date.
