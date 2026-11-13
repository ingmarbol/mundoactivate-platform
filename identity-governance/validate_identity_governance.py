#!/usr/bin/env python3
"""Valida controles mínimos de Identity Governance sin acceder a Cloud."""
from __future__ import annotations
import argparse
from pathlib import Path
import sys
import yaml


def load(path: str) -> dict:
    with Path(path).open(encoding="utf-8") as stream:
        return yaml.safe_load(stream)


def require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def validate(baseline: dict, assignments: dict) -> list[str]:
    errors: list[str] = []
    aws = baseline["aws"]
    azure = baseline["azure"]
    k8s = baseline["kubernetes"]

    require(aws["workforce_identity"] == "iam_identity_center",
            "AWS workforce access must use IAM Identity Center", errors)
    require(aws["privileged_access"]["max_session_minutes"] <= 60,
            "AWS privileged sessions must be 60 minutes or less", errors)
    require(aws["privileged_access"]["approval_required"],
            "AWS privileged activation requires approval", errors)
    require(aws["privileged_access"]["phishing_resistant_mfa"],
            "AWS privileged activation requires phishing-resistant MFA", errors)
    require(aws["emergency_access_roles"] >= 2,
            "AWS requires at least two independent emergency paths", errors)

    pim = azure["pim"]
    require(pim["activation_max_minutes"] <= 60,
            "Azure PIM activation must be 60 minutes or less", errors)
    require(pim["approval_required"] and pim["justification_required"],
            "Azure PIM requires approval and justification", errors)
    require(pim["phishing_resistant_mfa"],
            "Azure PIM requires phishing-resistant MFA", errors)
    require(azure["access_reviews"]["cadence_days"] <= 90,
            "Azure access review cadence must be 90 days or less", errors)
    require(azure["access_reviews"]["apply_results"],
            "Azure access review results must be applied", errors)
    require(azure["emergency_access_accounts"] >= 2,
            "Azure requires at least two emergency access accounts", errors)

    require(k8s["human_access"] == "short_lived_federated",
            "Kubernetes human access must be short-lived and federated", errors)
    require(k8s["workload_identity_required"],
            "Kubernetes workloads must use workload identity", errors)
    require(not k8s["permanent_cluster_admin"],
            "Permanent cluster-admin access is forbidden", errors)

    for item in assignments.get("assignments", []):
        prefix = item.get("id", "unknown")
        require(bool(item.get("owner")), f"{prefix}: owner is required", errors)
        require(item.get("review_days", 999) <= 90,
                f"{prefix}: review must occur within 90 days", errors)
        if item.get("identity_type") == "human" and item.get("privilege") == "elevated":
            require(item.get("access") == "eligible",
                    f"{prefix}: elevated human access must be eligible/JIT, not permanent", errors)
            require(item.get("session_minutes", 999) <= 60,
                    f"{prefix}: elevated session must be 60 minutes or less", errors)
            require(bool(item.get("approval_group")),
                    f"{prefix}: elevated access requires an approval group", errors)
        if item.get("identity_type") == "workload":
            require(item.get("static_credentials") is False,
                    f"{prefix}: static workload credentials are forbidden", errors)
            require(item.get("access") in {"pod_identity", "workload_identity", "oidc_federation"},
                    f"{prefix}: workload must use federated identity", errors)
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--baseline", required=True)
    parser.add_argument("--assignments", required=True)
    args = parser.parse_args()
    errors = validate(load(args.baseline), load(args.assignments))
    if errors:
        for error in errors:
            print(f"FAIL {error}")
        print("RESULT: IDENTITY GOVERNANCE INVALID")
        return 1
    print("PASS AWS Identity Center, JIT and emergency paths")
    print("PASS Azure PIM, access reviews and emergency accounts")
    print("PASS Kubernetes federated human and workload identity")
    print("PASS 5 assignments have owners and <=90-day reviews")
    print("PASS no permanent admin or static workload credentials")
    print("RESULT: IDENTITY GOVERNANCE VALID")
    return 0


if __name__ == "__main__":
    sys.exit(main())
