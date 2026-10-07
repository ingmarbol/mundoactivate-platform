# Session 17 - Chaos Engineering and reliability testing

## Objective

Design and execute a small, observable, reversible Kubernetes experiment that
tests a recovery hypothesis without authorizing production disruption.

## Scope

- Experiment plan as YAML.
- PodDisruptionBudget for the development workload.
- Preflight, execution, abort, evidence, and debrief checklist.

## Test procedure

```bash
python3 - <<'PY'
import pathlib, yaml
for file in pathlib.Path("reliability").glob("*.yaml"):
    list(yaml.safe_load_all(file.read_text()))
    print("OK", file)
PY

kubectl apply --dry-run=client -f reliability/pdb.yaml
```

Run only against a local or development cluster after verifying the current
context. Observe the baseline for five minutes before deleting exactly one pod.

## Expected result and evidence

The YAML parses, the PDB passes client dry-run, request success remains at or
above 95 percent, and the Deployment restores steady state within 120 seconds.
Record timestamped probes, events, recovery time, verdict, gaps, and actions.

## Security and cost impact

No secrets, credentials, or cloud resources are included. Production is
explicitly unauthorized. A future AWS FIS or Azure Chaos Studio experiment
requires least-privilege identity, stop conditions, monitoring, approval, and a
bounded cost estimate.

## Cleanup

Stop all probe loops, confirm desired replicas and healthy endpoints, remove
only temporary test resources, and retain non-sensitive evidence.
