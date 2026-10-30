# Session 27 - Secrets Management and multicloud PKI

This lab validates the security intent for the cumulative multicloud platform.
It stores no secret values, credentials, private keys, certificates or state.

## Run

```bash
python3 secrets/validate_secrets_baseline.py secrets/secret-baseline.yaml
```

Expected result: `RESULT: SECRETS AND PKI BASELINE VALID`.

## Negative test

Copy the baseline to a temporary file and change `EKS Pod Identity` to
`static_credentials`. The validator must return a non-zero exit code.

## Cloud sandbox extension

Create the referenced secret manually in a non-production vault, grant only the
named workload identity, then use server-side dry-run before applying the
`ExternalSecret`. Delete the test object, revoke access, and review audit logs.

## Security and cost

Use short-lived identity, least privilege, provider-side rotation, private
endpoints where justified, audit logs with redaction, and bounded retention.
Delete lab secrets, private CA resources and log workspaces after collecting
evidence. Managed HSM and private CA services can incur material hourly costs.
