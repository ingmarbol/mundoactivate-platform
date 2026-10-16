#!/usr/bin/env python3
"""Evaluate a dependency-free platform scorecard using JSON-compatible YAML."""
import argparse
import json
from pathlib import Path
def load(path):
    try: return json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc: raise SystemExit(f"FAIL invalid file {path}: {exc}")
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--catalog",required=True); ap.add_argument("--policy",required=True)
    args=ap.parse_args(); catalog,policy=load(args.catalog),load(args.policy); weights=policy["weights"]
    if sum(weights.values()) != 100: raise SystemExit("FAIL policy weights must total 100")
    failed=False
    for service in catalog.get("services",[]):
        name=service.get("name","<unnamed>")
        missing=[key for key in weights if not service.get(key)]
        blocking=sorted(set(missing).intersection(policy["blocking"]))
        score=sum(weight for key,weight in weights.items() if service.get(key))
        status="PASS" if score >= policy["minimum_score"] and not blocking else "FAIL"
        print(f"{status} {name}: {score}/100")
        if missing: print("  gaps:",", ".join(missing))
        if blocking: print("  blocking:",", ".join(blocking))
        failed |= status == "FAIL"
    if failed: raise SystemExit("RESULT: PLATFORM SCORECARD FAILED")
    print("RESULT: PLATFORM SCORECARD PASSED")
if __name__=="__main__": main()
