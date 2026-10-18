#!/usr/bin/env python3
"""Verify artifact integrity and local supply-chain evidence."""
import argparse, hashlib, json
from pathlib import Path
ALLOWED_BUILDERS={"github-actions:mundoactivate-platform"}
ALLOWED_SOURCE="https://github.com/ingmarbol/mundoactivate-platform"
def load(path):
    try: return json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError,json.JSONDecodeError) as exc: raise SystemExit(f"FAIL invalid evidence {path}: {exc}")
def digest(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def main():
    ap=argparse.ArgumentParser()
    for arg in ("artifact","manifest","sbom","provenance"): ap.add_argument(f"--{arg}",required=True)
    args=ap.parse_args(); actual=digest(args.artifact)
    manifest,sbom,provenance=load(args.manifest),load(args.sbom),load(args.provenance); errors=[]
    if actual != manifest.get("sha256"): errors.append("artifact digest mismatch")
    if actual != sbom.get("subject",{}).get("sha256"): errors.append("SBOM subject mismatch")
    if actual != provenance.get("subject",{}).get("sha256"): errors.append("provenance subject mismatch")
    if provenance.get("builder") not in ALLOWED_BUILDERS: errors.append("untrusted builder")
    if provenance.get("source",{}).get("repository") != ALLOWED_SOURCE: errors.append("untrusted source repository")
    commit=provenance.get("source",{}).get("commit","")
    if len(commit)!=40 or any(c not in "0123456789abcdef" for c in commit): errors.append("invalid commit SHA")
    if not sbom.get("components"): errors.append("SBOM has no components")
    if errors:
        for error in errors: print("FAIL",error)
        raise SystemExit("RESULT: SUPPLY CHAIN REJECTED")
    print("PASS artifact digest"); print("PASS SBOM subject"); print("PASS provenance subject")
    print("PASS builder and source policy"); print("RESULT: SUPPLY CHAIN VERIFIED")
if __name__=="__main__": main()
