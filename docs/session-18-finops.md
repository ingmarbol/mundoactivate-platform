# Session 18 - Multicloud FinOps and cost optimization

## Objective

Build a reproducible cost baseline for MundoActivate using synthetic data,
allocation dimensions, a monthly budget, and a business unit metric.

## Scope

- Synthetic multicloud cost dataset.
- Budget and allocation policy.
- Python report for cost, variance, coverage, and unit cost.
- No cloud resources, credentials, billing exports, or real customer data.

## Test procedure

```bash
python3 scripts/finops_report.py \
  --input finops/sample-costs.csv \
  --budget finops/budget.yaml \
  --output finops/report.md
```

## Expected result and evidence

The report shows totals by provider, environment, and owner; allocation
coverage; budget consumption and variance; and cost per active student.
Evidence includes the command output and a prioritized optimization backlog.

## Security and cost impact

The dataset is synthetic and contains no secrets or billing account identifiers.
The exercise creates no billable cloud resources. Tags must never contain PII,
credentials, or sensitive operational data.

## Cleanup

The generated `finops/report.md` may be removed after review. No cloud cleanup
is required.
