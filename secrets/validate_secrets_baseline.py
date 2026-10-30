#!/usr/bin/env python3
import argparse
import pathlib
import sys
import yaml

FORBIDDEN = {"value", "password", "token", "secret_value", "private_key", "access_key", "client_secret"}

def walk(obj, path="root"):
    if isinstance(obj, dict):
        for key, value in obj.items():
            if str(key).lower() in FORBIDDEN:
                raise ValueError(f"plaintext-like field forbidden: {path}.{key}")
            walk(value, f"{path}.{key}")
    elif isinstance(obj, list):
        for idx, value in enumerate(obj):
            walk(value, f"{path}[{idx}]")

def require(condition, message):
    if not condition:
        raise ValueError(message)

def validate(path):
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    walk(data)
    aws = data["providers"]["aws"]
    azure = data["providers"]["azure"]
    require("Identity" in aws["authentication"], "AWS must use workload identity")
    require("Identity" in azure["authentication"], "Azure must use workload identity")
    require(azure.get("soft_delete") is True, "Azure soft delete must be enabled")
    require(azure.get("purge_protection") is True, "Azure purge protection must be enabled")
    for item in data.get("secrets", []):
        require(item.get("owner"), f"{item.get('name')} requires an owner")
        require(1 <= int(item.get("rotation_days", 0)) <= 90, f"{item.get('name')} rotation must be 1-90 days")
        require(item.get("consumers"), f"{item.get('name')} requires explicit consumers")
    pki = data["pki"]
    require(pki.get("private_keys_exportable") is False, "private keys must be non-exportable")
    require(int(pki["renew_before_hours"]) < int(pki["workload_certificate_validity_hours"]), "renewal must precede expiry")
    required_steps = {"identify_scope", "revoke_or_disable", "rotate_credential", "review_audit_logs"}
    require(required_steps.issubset(set(data.get("incident_response", []))), "incident runbook incomplete")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("path", nargs="?", default="secrets/secret-baseline.yaml")
    args = parser.parse_args()
    try:
        validate(pathlib.Path(args.path))
    except Exception as exc:
        print(f"FAIL: {exc}")
        return 1
    print("PASS provider identities")
    print("PASS rotation and ownership")
    print("PASS Azure deletion safeguards")
    print("PASS PKI lifecycle")
    print("PASS incident response")
    print("RESULT: SECRETS AND PKI BASELINE VALID")
    return 0

if __name__ == "__main__":
    sys.exit(main())

