#!/usr/bin/env python3
import argparse
import datetime as dt
import json
import sys
from pathlib import Path

import yaml

REQUIRED_PHASES = [
    "preparation", "detection", "analysis", "containment",
    "eradication", "recovery", "lessons_learned",
]
REQUIRED_AWS = {"cloudtrail-organization-trail", "guardduty-findings", "eks-audit-logs"}
REQUIRED_AZURE = {"activity-log", "entra-signin-logs", "aks-audit-admin"}
DESTRUCTIVE = {"disable_identity", "isolate_workload", "revoke_sessions", "block_network_path", "delete_resource"}


def record(error_list, condition, message):
    if not condition:
        error_list.append(message)
        print(f"FAIL {message}")


def parse_time(value):
    if not value.endswith("Z"):
        raise ValueError("timestamp must use UTC Z suffix")
    return dt.datetime.fromisoformat(value.replace("Z", "+00:00"))


def main():
    parser = argparse.ArgumentParser(description="Validate incident response plan and synthetic timeline")
    parser.add_argument("--plan", required=True)
    parser.add_argument("--alerts", required=True)
    args = parser.parse_args()

    plan = yaml.safe_load(Path(args.plan).read_text())
    alerts = [json.loads(line) for line in Path(args.alerts).read_text().splitlines() if line.strip()]
    errors = []

    record(errors, plan.get("time_standard") == "UTC", "all evidence must use UTC")
    record(errors, plan.get("phases") == REQUIRED_PHASES, "incident phases are incomplete or out of order")
    roles = plan.get("roles", {})
    record(errors, all(roles.get(k) for k in ("incident_commander", "cloud_lead", "forensics_lead", "communications_lead")), "required roles are missing")

    containment = plan.get("containment", {})
    automatic = set(containment.get("automatic_actions", []))
    approved = set(containment.get("approval_required", []))
    record(errors, not automatic.intersection(DESTRUCTIVE), "destructive containment must not be automatic")
    record(errors, DESTRUCTIVE.issubset(approved), "destructive containment requires approval")

    evidence = plan.get("evidence", {})
    record(errors, evidence.get("hash_algorithm") == "sha256", "evidence must use sha256")
    record(errors, evidence.get("immutable_storage") is True, "evidence storage must be immutable")
    record(errors, evidence.get("chain_of_custody_required") is True, "chain of custody is required")
    record(errors, evidence.get("retention_days", 0) >= 365, "evidence retention must be at least 365 days")

    record(errors, REQUIRED_AWS.issubset(set(plan.get("aws", {}).get("data_sources", []))), "AWS evidence sources are incomplete")
    record(errors, REQUIRED_AZURE.issubset(set(plan.get("azure", {}).get("data_sources", []))), "Azure evidence sources are incomplete")
    record(errors, plan.get("aws", {}).get("identity") == "incident-response-role", "AWS response identity must be a dedicated role")
    record(errors, plan.get("azure", {}).get("identity") == "incident-response-managed-identity", "Azure response identity must be a managed identity")

    required_fields = {"timestamp", "provider", "source", "severity", "entity", "event", "correlation_id"}
    timestamps = []
    correlations = set()
    for number, alert in enumerate(alerts, 1):
        record(errors, required_fields.issubset(alert), f"alert {number} is missing required fields")
        try:
            timestamps.append(parse_time(alert["timestamp"]))
        except Exception as exc:
            record(errors, False, f"alert {number}: {exc}")
        correlations.add(alert.get("correlation_id"))
    record(errors, timestamps == sorted(timestamps), "timeline must be chronological")
    record(errors, len(correlations) == 1 and None not in correlations, "alerts must share one case correlation_id")

    recovery = plan.get("recovery", {})
    record(errors, recovery.get("known_good_artifacts_only") is True, "recovery requires known-good artifacts")
    record(errors, recovery.get("require_security_validation") is True, "security validation is required before closure")
    record(errors, recovery.get("require_business_validation") is True, "business validation is required before closure")

    if errors:
        print(f"RESULT: INCIDENT RESPONSE BASELINE INVALID ({len(errors)} errors)")
        return 1
    print("PASS roles and incident lifecycle")
    print("PASS approval gates for destructive containment")
    print("PASS immutable evidence and chain of custody")
    print("PASS AWS, Azure and Kubernetes data sources")
    print(f"PASS chronological timeline with {len(alerts)} events")
    print("PASS security and business recovery gates")
    print("RESULT: INCIDENT RESPONSE BASELINE VALID")
    return 0


if __name__ == "__main__":
    sys.exit(main())

