#!/usr/bin/env python3
import argparse
from pathlib import Path
import yaml

def load(path):
    with Path(path).open(encoding="utf-8") as handle:
        return yaml.safe_load(handle)

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--catalog", required=True)
    p.add_argument("--slos", required=True)
    p.add_argument("--policy", required=True)
    a = p.parse_args()
    catalog, slos, policy = load(a.catalog), load(a.slos), load(a.policy)
    errors = []
    services = catalog.get("services", [])
    ids = {s.get("id") for s in services}
    required = {"owner", "runbook", "dashboard", "on_call"}
    for s in services:
        missing = sorted(k for k in required if not s.get(k))
        if missing:
            errors.append(f"{s.get('id')}: missing {', '.join(missing)}")
        if set(s.get("telemetry", [])) != {"metrics", "logs", "traces"}:
            errors.append(f"{s.get('id')}: telemetry must contain metrics, logs and traces")
        unknown = set(s.get("dependencies", [])) - ids
        if unknown:
            errors.append(f"{s.get('id')}: unknown dependencies {sorted(unknown)}")
    slo_items = slos.get("slos", [])
    for item in slo_items:
        if item.get("service") not in ids:
            errors.append(f"SLO: unknown service {item.get('service')}")
        if not 99 <= float(item.get("target_percent", 0)) < 100:
            errors.append(f"{item.get('name')}: target out of range")
        if item.get("window_days") != 30:
            errors.append(f"{item.get('name')}: window must be 30 days")
        if len(item.get("burn_rate_alerts", [])) < 2:
            errors.append(f"{item.get('name')}: two burn-rate alerts required")
    must_true = {
        "incident": ["severity_model", "incident_commander", "blameless_postmortem", "stakeholder_communications"],
        "automation": ["idempotent_runbooks", "destructive_action_approval", "rollback_required", "audit_trail"],
        "readiness": ["backup_restore_test", "capacity_review", "dependency_review", "security_review", "cost_review"],
    }
    for section, keys in must_true.items():
        for key in keys:
            if policy.get(section, {}).get(key) is not True:
                errors.append(f"{section}.{key} must be true")
    aiops = policy.get("aiops", {})
    for key in ["human_in_the_loop", "evidence_links_required", "confidence_required", "destructive_auto_actions_forbidden", "feedback_loop"]:
        if aiops.get(key) is not True:
            errors.append(f"aiops.{key} must be true")
    toil = policy.get("toil", {})
    if not toil.get("quarterly_measurement") or not toil.get("automation_backlog"):
        errors.append("toil measurement and backlog required")
    if int(toil.get("max_manual_operational_work_percent", 101)) > 50:
        errors.append("manual operational work threshold must be <= 50%")
    if errors:
        for e in errors:
            print(f"FAIL {e}")
        print("RESULT: SRE OPERATIONS BASELINE INVALID")
        return 1
    print(f"PASS {len(services)} services have ownership, runbooks and telemetry")
    print(f"PASS {len(slo_items)} SLOs define targets, windows and burn-rate alerts")
    print("PASS incident, automation and operational readiness controls")
    print("PASS AIOps requires evidence, human approval and safe actions")
    print("PASS toil budget and improvement backlog")
    print("RESULT: SRE OPERATIONS BASELINE VALID")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
