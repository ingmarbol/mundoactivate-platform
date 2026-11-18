#!/usr/bin/env python3
import argparse, sys, yaml

def load(path):
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--classification", required=True)
    p.add_argument("--policy", required=True)
    p.add_argument("--flows", required=True)
    a=p.parse_args(); errors=[]
    c,pol,fl=load(a.classification),load(a.policy),load(a.flows)
    classes=c.get("classes",{}); datasets=c.get("datasets",[])
    required={"public","internal","confidential","restricted"}
    if set(classes)!=required: errors.append("classification tiers must be public/internal/confidential/restricted")
    for d in datasets:
        missing=[k for k in ("id","class","owner","purpose","retention_days","allowed_regions") if not d.get(k)]
        if missing: errors.append(f"{d.get('id','dataset')}: missing {','.join(missing)}")
        if d.get("pii") and not d.get("lawful_basis"): errors.append(f"{d['id']}: PII requires lawful_basis")
        if d.get("retention_days",9999)>365: errors.append(f"{d['id']}: retention exceeds 365-day lab maximum")
        if d.get("class") in {"confidential","restricted"}:
            if not d.get("tokenization"): errors.append(f"{d['id']}: sensitive data requires tokenization")
            if d.get("dlp_mode")!="block": errors.append(f"{d['id']}: sensitive data requires blocking DLP")
        if d.get("class")=="restricted":
            if not d.get("immutable_backup"): errors.append(f"{d['id']}: restricted data requires immutable backup")
            if not d.get("jit_access"): errors.append(f"{d['id']}: restricted data requires JIT access")
    required_controls=[("aws","macie_enabled"),("aws","kms_rotation"),("aws","s3_block_public_access"),
      ("azure","purview_classification"),("azure","dlp_enabled"),("azure","key_vault_purge_protection"),
      ("kubernetes","secrets_encryption_at_rest"),("kubernetes","external_secret_store"),
      ("governance","deletion_evidence"),("governance","immutable_backup")]
    for section,key in required_controls:
        if not pol.get(section,{}).get(key): errors.append(f"{section}.{key} must be true")
    denied=set(pol.get("observability",{}).get("deny_attributes",[]))
    for key in {"authorization","cookie","token","user.email","request.body"}:
        if key not in denied: errors.append(f"observability must deny {key}")
    flows=fl.get("flows",[])
    for f in flows:
        if not str(f.get("encryption_in_transit","")).startswith("tls"): errors.append(f"{f.get('id')}: TLS required")
        if not f.get("identity") or not f.get("residency"): errors.append(f"{f.get('id')}: identity and residency required")
        if f.get("classification")=="restricted" and f.get("logging") not in {"metadata-only","redacted"}: errors.append(f"{f.get('id')}: restricted logging must exclude payloads")
    if errors:
        for e in errors: print(f"FAIL {e}")
        print("RESULT: DATA PROTECTION BASELINE INVALID"); return 1
    print(f"PASS {len(classes)} classification tiers and {len(datasets)} datasets")
    print("PASS AWS/Azure/Kubernetes protections")
    print(f"PASS {len(flows)} flows encrypted and residency-controlled")
    print("PASS PII purpose, retention, tokenization and DLP")
    print("PASS telemetry redaction and deletion evidence")
    print("RESULT: DATA PROTECTION BASELINE VALID"); return 0
if __name__=="__main__": sys.exit(main())
