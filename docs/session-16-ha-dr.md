# Session 16 — High Availability and multicloud Disaster Recovery

## Objective

Define measurable recovery objectives and a testable recovery plan for the cumulative MundoActivate platform without confusing High Availability, backups, and Disaster Recovery.

## Scope

- Service tiers with RTO/RPO, owners, backup cadence, and restore-test cadence.
- A tabletop/sandbox DR drill checklist.
- A non-applied Velero schedule example for the development namespace.

## Test procedure

```bash
python3 - <<'PY'
import pathlib, yaml
for file in pathlib.Path("reliability").glob("*.yaml"):
    list(yaml.safe_load_all(file.read_text()))
    print("OK", file)
PY
```

Review all objectives and run the checklist in a sandbox. The Velero manifest is an example and must not be applied to production without provider, storage, retention, and restore validation.

## Expected result and evidence

The YAML parses successfully, every service has positive RTO and non-negative RPO, and the drill records declaration time, latest recovery point, service-validation time, observed RTO/RPO, gaps, owners, and cleanup.

## Security and cost impact

No credentials or sensitive values are present. Production design should use encrypted immutable backups, isolated cross-account/subscription copies, least privilege, and audited break-glass access. Cross-region replication, storage retention, egress, standby compute, and drill environments create cost and must be aligned to service tiers.

## Cleanup

Delete only the isolated restore namespace/environment created for the drill after evidence is retained. Do not delete backup repositories or production recovery points.
