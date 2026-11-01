# Session 28 - Performance Engineering and Capacity Planning

This lab uses synthetic measurements. It does not create cloud resources or
send traffic to production.

## Run

```bash
python3 performance/capacity_plan.py \
  --config performance/capacity-baseline.yaml \
  --measurements performance/measurements.csv
```

Expected: `RESULT: CAPACITY BASELINE VALID`.

## Negative test

Copy the configuration to a temporary file, set `max_replicas: 4`, and run the
validator again. It must fail because the recommended peak capacity is higher.

## Optional smoke test

```bash
BASE_URL=http://127.0.0.1:8080 k6 run performance/k6-smoke.js
```

Never point the script at production without explicit authorization, a defined
blast radius, abort conditions and real-time monitoring.

## Cleanup and cost

The local model has no cloud cost. For a sandbox, remove temporary load
generators, node pools, dashboards and retained high-cardinality telemetry.
Review CloudWatch and Azure Monitor ingestion and retention after the test.
