# Session 33 - Identity Governance y Privileged Access multicloud

## Objective

Implement an auditable baseline for least privilege, JIT elevation, periodic
access review, workload federation and emergency access across AWS, Azure and
Kubernetes.

## Test

```bash
python3 identity-governance/validate_identity_governance.py \
  --baseline identity-governance/governance-baseline.yaml \
  --assignments identity-governance/access-assignments.yaml
```

Expected result: `RESULT: IDENTITY GOVERNANCE VALID`.

## Negative test

Work on a temporary copy and change `aws-prod-operator.access` from `eligible`
to `permanent`. The validator must return a non-zero exit code and identify the
standing privileged assignment.

## Evidence

- Positive and negative validator output.
- PIM/Identity Center configuration screenshots without sensitive identifiers.
- Access review export with owners and decisions.
- Break-glass quarterly test record.

## Security and cost

The examples contain no credentials. Licensing, internal-access analysis,
log ingestion and retention must be estimated before production rollout.

## Cleanup

Delete only temporary negative-test copies. Preserve the baseline, assignments,
review evidence and runbook as versioned governance records.
