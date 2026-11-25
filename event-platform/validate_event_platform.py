#!/usr/bin/env python3
import argparse
import json
from datetime import datetime
from pathlib import Path
import yaml

def load_yaml(path):
    with Path(path).open(encoding="utf-8") as handle:
        return yaml.safe_load(handle)

def iso_utc(value):
    try:
        return value.endswith("Z") and datetime.fromisoformat(value.replace("Z", "+00:00")).tzinfo is not None
    except (AttributeError, ValueError):
        return False

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--contract", required=True)
    parser.add_argument("--policy", required=True)
    parser.add_argument("--events", required=True)
    args = parser.parse_args()
    contract = load_yaml(args.contract)
    policy = load_yaml(args.policy)
    events = [json.loads(line) for line in Path(args.events).read_text(encoding="utf-8").splitlines() if line.strip()]
    errors, ids = [], set()
    required_envelope = {"specversion", "id", "source", "type", "subject", "time", "datacontenttype", "correlation_id", "traceparent", "data"}
    required_data = set(contract["schema"]["required"])
    for row, event in enumerate(events, 1):
        missing = required_envelope - event.keys()
        if missing:
            errors.append(f"row {row}: missing envelope fields {sorted(missing)}")
        if event.get("id") in ids:
            errors.append(f"row {row}: duplicate id {event.get('id')}")
        ids.add(event.get("id"))
        expected = {
            "specversion": str(contract.get("specversion")),
            "source": contract.get("source"),
            "type": contract.get("event_type"),
            "datacontenttype": contract.get("datacontenttype"),
        }
        for key, value in expected.items():
            if event.get(key) != value:
                errors.append(f"row {row}: {key} differs from contract")
        if not iso_utc(event.get("time")):
            errors.append(f"row {row}: time must be ISO-8601 UTC")
        data = event.get("data", {})
        missing_data = required_data - data.keys()
        if missing_data:
            errors.append(f"row {row}: missing data fields {sorted(missing_data)}")
        if not iso_utc(data.get("completed_at")):
            errors.append(f"row {row}: completed_at must be ISO-8601 UTC")
        if not event.get("subject", "").startswith(f"tenant/{data.get('tenant_id', '')}/"):
            errors.append(f"row {row}: subject and tenant_id do not match")
    checks = {
        "delivery.idempotent_consumers": policy["delivery"]["idempotent_consumers"],
        "delivery.duplicate_detection": policy["delivery"]["duplicate_detection"],
        "delivery.dead_letter.enabled": policy["delivery"]["dead_letter"]["enabled"],
        "delivery.retry.exponential_backoff": policy["delivery"]["retry"]["exponential_backoff"],
        "delivery.retry.jitter": policy["delivery"]["retry"]["jitter"],
        "ordering.global_ordering_forbidden": policy["ordering"]["global_ordering_forbidden"],
        "replay.approval_required": policy["replay"]["approval_required"],
        "replay.checkpoint_required": policy["replay"]["checkpoint_required"],
        "security.workload_identity": policy["security"]["workload_identity"],
        "security.encryption_in_transit": policy["security"]["encryption_in_transit"],
        "security.encryption_at_rest": policy["security"]["encryption_at_rest"],
        "security.least_privilege": policy["security"]["least_privilege"],
        "observability.trace_context_propagation": policy["observability"]["trace_context_propagation"],
        "observability.logs_redacted": policy["observability"]["logs_redacted"],
        "governance.schema_compatibility_gate": policy["governance"]["schema_compatibility_gate"],
    }
    for name, value in checks.items():
        if value is not True:
            errors.append(f"{name} must be true")
    if policy["security"]["public_network_access"] is not False:
        errors.append("security.public_network_access must be false")
    if policy["delivery"]["semantic"] != "at-least-once":
        errors.append("delivery.semantic must document at-least-once")
    if len(policy["observability"]["metrics"]) < 5:
        errors.append("observability must include publish, consume, lag, retry and DLQ metrics")
    if errors:
        for error in errors:
            print(f"FAIL {error}")
        print("RESULT: EVENT PLATFORM BASELINE INVALID")
        return 1
    print(f"PASS contract {contract['event_type']} version {contract['contract_version']}")
    print(f"PASS {len(events)} CloudEvents envelopes and unique event IDs")
    print("PASS idempotency, retry, dead-letter, ordering and replay controls")
    print("PASS workload identity, encryption, private access and least privilege")
    print("PASS trace context, redaction, metrics and schema compatibility gate")
    print("RESULT: EVENT PLATFORM BASELINE VALID")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
