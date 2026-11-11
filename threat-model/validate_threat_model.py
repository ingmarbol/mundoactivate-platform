#!/usr/bin/env python3
import argparse
import sys
from pathlib import Path

import yaml

STRIDE = {"Spoofing", "Tampering", "Repudiation", "Information Disclosure", "Denial of Service", "Elevation of Privilege"}
RESPONSES = {"mitigate", "eliminate", "transfer", "accept"}


def fail(errors, message):
    errors.append(message)
    print(f"FAIL {message}")


def main():
    parser = argparse.ArgumentParser(description="Validate architecture and threat model")
    parser.add_argument("--architecture", required=True)
    parser.add_argument("--threats", required=True)
    args = parser.parse_args()
    architecture = yaml.safe_load(Path(args.architecture).read_text())
    model = yaml.safe_load(Path(args.threats).read_text())
    errors = []

    boundaries = {item["id"] for item in architecture.get("trust_boundaries", [])}
    components = {item["id"]: item for item in architecture.get("components", [])}
    entities = {item["id"] for item in architecture.get("external_entities", [])}
    if len(boundaries) < 3:
        fail(errors, "at least three trust boundaries are required")
    for component in components.values():
        if component.get("boundary") not in boundaries:
            fail(errors, f"component {component['id']} references an unknown boundary")
    valid_nodes = entities | set(components)
    for flow in architecture.get("data_flows", []):
        if flow.get("source") not in valid_nodes or flow.get("destination") not in valid_nodes:
            fail(errors, f"flow {flow.get('id')} has an unknown endpoint")
        if flow.get("crosses_boundary") and flow.get("protocol") not in {"https", "tls", "otlp-tls"}:
            fail(errors, f"flow {flow.get('id')} crosses a boundary without protected transport")

    policy = model.get("risk_policy", {})
    critical = int(policy.get("critical_threshold", 20))
    ids = set()
    for threat in model.get("threats", []):
        tid = threat.get("id")
        if not tid or tid in ids:
            fail(errors, f"duplicate or missing threat id {tid}")
        ids.add(tid)
        if threat.get("stride") not in STRIDE:
            fail(errors, f"{tid} has invalid STRIDE category")
        if threat.get("component") not in components:
            fail(errors, f"{tid} references an unknown component")
        likelihood = int(threat.get("likelihood", 0))
        impact = int(threat.get("impact", 0))
        if not 1 <= likelihood <= 5 or not 1 <= impact <= 5:
            fail(errors, f"{tid} likelihood and impact must be 1..5")
        score = likelihood * impact
        if threat.get("response") not in RESPONSES:
            fail(errors, f"{tid} has invalid response")
        for field in ("asset", "attack_path", "owner", "acceptance_criteria"):
            if not threat.get(field):
                fail(errors, f"{tid} missing {field}")
        if threat.get("response") == "mitigate" and not threat.get("controls"):
            fail(errors, f"{tid} mitigation has no controls")
        if score >= critical and threat.get("status") not in {"mitigated", "closed"}:
            fail(errors, f"{tid} is critical and unresolved")
        if threat.get("response") == "accept":
            required = policy.get("accepted_risk_requires", [])
            for field in required:
                if not threat.get(field):
                    fail(errors, f"{tid} accepted risk missing {field}")

    if not architecture.get("security_requirements"):
        fail(errors, "security requirements are missing")
    if errors:
        print(f"RESULT: THREAT MODEL INVALID ({len(errors)} errors)")
        return 1
    print(f"PASS {len(components)} components and {len(boundaries)} trust boundaries")
    print(f"PASS {len(architecture.get('data_flows', []))} protected data flows")
    print(f"PASS {len(model.get('threats', []))} threats with owners and responses")
    print("PASS critical risks have a resolved status")
    print("PASS mitigations have testable acceptance criteria")
    print("RESULT: THREAT MODEL VALID")
    return 0


if __name__ == "__main__":
    sys.exit(main())

