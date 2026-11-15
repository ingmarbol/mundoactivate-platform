# Session 34 - Security Testing, Attack Simulation y Purple Team multicloud

## Objective

Validate Cloud, Kubernetes and application security controls through approved,
non-destructive simulations with measurable detection and response outcomes.

## Test

Run:

    python3 purple-team/validate_purple_team.py \
      --plan purple-team/exercise-plan.yaml \
      --scenarios purple-team/scenarios.yaml \
      --observations purple-team/observations.yaml

Expected result: RESULT: PURPLE TEAM PLAN VALID.

## Negative test

Work on a temporary copy and change authorization.approved from true to false.
The validator must return a non-zero exit code before any simulation.

## Evidence

- Signed scope and authorization record.
- ATT&CK mapping and scenario success criteria.
- Alert, incident and audit identifiers without secrets or personal data.
- Detection coverage, MTTD, MTTR and remediation backlog.
- Cleanup verification for the isolated environment.

## Security and cost

The repository contains only synthetic/sample definitions. Do not run a
simulation against production. GuardDuty, Defender plans, Sentinel, CloudWatch,
Azure Monitor and log retention may generate charges.

## Cleanup

Delete test namespaces and temporary fixtures, close sample incidents with a
benign exercise classification, verify that no test resources remain and retain
only the approved evidence for the defined period.
