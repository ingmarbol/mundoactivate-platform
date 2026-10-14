#!/usr/bin/env python3
"""Dependency-free validator for the Session 20 synthetic data contract."""
import argparse, json, re, sys
from pathlib import Path
SENSITIVE = {"email", "password", "token", "secret", "access_key", "private_key"}
UTC = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
def parse_simple_yaml(path):
    result, current = {}, None
    for raw in Path(path).read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"): continue
        if line.startswith("- "):
            result.setdefault(current, []).append(line[2:].strip()); continue
        key, value = [x.strip() for x in line.split(":", 1)]
        current = key
        if not value: result[key] = []
        elif value.isdigit(): result[key] = int(value)
        else: result[key] = value
    return result
def fail(message):
    print(f"FAIL: {message}", file=sys.stderr); raise SystemExit(1)
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--catalog", required=True); ap.add_argument("--records", required=True)
    args = ap.parse_args(); catalog = parse_simple_yaml(args.catalog)
    for key in ("product","owner","classification","retention_days","rto_minutes","rpo_minutes","required_fields"):
        if not catalog.get(key): fail(f"catalog missing {key}")
    if catalog["rpo_minutes"] > catalog["rto_minutes"]: fail("rpo_minutes must be <= rto_minutes")
    seen, records = set(), []
    for number, raw in enumerate(Path(args.records).read_text(encoding="utf-8").splitlines(), 1):
        try: record = json.loads(raw)
        except json.JSONDecodeError as exc: fail(f"line {number}: invalid JSON: {exc.msg}")
        missing = [f for f in catalog["required_fields"] if not record.get(f)]
        if missing: fail(f"line {number}: missing {','.join(missing)}")
        if record["event_id"] in seen: fail(f"line {number}: duplicate event_id {record['event_id']}")
        if not UTC.match(record["occurred_at"]): fail(f"line {number}: occurred_at must be UTC ISO-8601")
        found = SENSITIVE.intersection(k.lower() for k in record)
        if found: fail(f"line {number}: sensitive fields present: {','.join(sorted(found))}")
        seen.add(record["event_id"]); records.append(record)
    print(f"PASS catalog: {catalog['product']}")
    print(f"PASS records: {len(records)}")
    print(f"PASS unique_event_id: {len(seen)}")
    print("PASS sensitive_fields: none")
    print("RESULT: DATA CONTRACT VALID")
if __name__ == "__main__": main()
