#!/usr/bin/env python3
import argparse
import datetime as dt
import sys
from pathlib import Path

import yaml


def fail(message, errors):
    errors.append(message)
    print(f"FAIL {message}")


def main():
    parser = argparse.ArgumentParser(description="Validate the session 30 compliance baseline")
    parser.add_argument("--baseline", required=True)
    parser.add_argument("--workloads", required=True)
    args = parser.parse_args()

    baseline = yaml.safe_load(Path(args.baseline).read_text())
    workloads = yaml.safe_load(Path(args.workloads).read_text())["workloads"]
    errors = []

    aws = baseline["cloud"]["aws"]
    azure = baseline["cloud"]["azure"]
    if len(aws.get("preventive", [])) < 2 or len(aws.get("detective", [])) < 2:
        fail("AWS needs preventive and detective controls", errors)
    if azure.get("remediation") != "managed_identity":
        fail("Azure remediation must use managed_identity", errors)

    kube = baseline["kubernetes"]
    if kube.get("failure_action_prod") != "Enforce":
        fail("production policies must use Enforce", errors)
    if kube.get("failure_action_nonprod") != "Audit":
        fail("non-production rollout must begin in Audit", errors)
    if not all(kube.get("required", {}).values()):
        fail("all Kubernetes guardrails must be enabled", errors)

    evaluation_date = dt.date.fromisoformat(str(baseline["evaluation_date"]))
    for exception in baseline.get("exceptions", []):
        expires = dt.date.fromisoformat(str(exception["expires_on"]))
        if expires <= evaluation_date or (expires - evaluation_date).days > 90:
            fail(f"{exception['id']} must expire within 90 days", errors)
        for field in ("owner", "justification", "ticket"):
            if not exception.get(field):
                fail(f"{exception['id']} missing {field}", errors)

    for workload in workloads:
        name = workload["name"]
        context = workload.get("security_context", {})
        if not context.get("run_as_non_root"):
            fail(f"{name} must run as non-root", errors)
        if not context.get("read_only_root_filesystem"):
            fail(f"{name} needs a read-only root filesystem", errors)
        if context.get("privileged") is not False:
            fail(f"{name} must not be privileged", errors)
        resources = workload.get("resources", {})
        if not resources.get("requests") or not resources.get("limits"):
            fail(f"{name} needs requests and limits", errors)
        if "@sha256:" not in workload.get("image", ""):
            fail(f"{name} image must be pinned by digest", errors)

    evidence = baseline.get("evidence", {})
    if evidence.get("retention_days", 0) < 365 or not evidence.get("owner"):
        fail("evidence needs an owner and at least 365 days retention", errors)

    if errors:
        print(f"RESULT: COMPLIANCE BASELINE INVALID ({len(errors)} errors)")
        return 1
    print("PASS AWS preventive and detective control sets")
    print("PASS Azure remediation identity and policy sets")
    print("PASS Kubernetes Audit-to-Enforce rollout")
    print("PASS time-bound exceptions and evidence ownership")
    print(f"PASS {len(workloads)} workloads satisfy security guardrails")
    print("RESULT: COMPLIANCE BASELINE VALID")
    return 0


if __name__ == "__main__":
    sys.exit(main())
