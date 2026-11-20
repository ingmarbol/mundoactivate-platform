#!/usr/bin/env python3
import argparse, sys, yaml

def load(path):
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--inventory", required=True)
    p.add_argument("--waves", required=True)
    p.add_argument("--policy", required=True)
    a=p.parse_args(); errors=[]
    inv,waves,pol=load(a.inventory),load(a.waves),load(a.policy)
    items=inv.get("workloads",[]); ids={x.get("id") for x in items}
    allowed=set(pol.get("allowed_strategies",[]))
    required=("id","name","owner","source","criticality","strategy","target","wave",
              "data_classification","rto_minutes","rpo_minutes","rollback_defined")
    for w in items:
        missing=[k for k in required if w.get(k) is None]
        if missing: errors.append(f"{w.get('id','workload')}: missing {','.join(missing)}")
        if w.get("strategy") not in allowed: errors.append(f"{w.get('id')}: invalid migration strategy")
        unknown=set(w.get("dependencies",[]))-ids
        if unknown: errors.append(f"{w.get('id')}: unknown dependencies {sorted(unknown)}")
        if not w.get("rollback_defined"): errors.append(f"{w.get('id')}: rollback required")
        if w.get("strategy")!="retire" and w.get("observability") in {None,"none"}:
            errors.append(f"{w.get('id')}: observability required")
        if w.get("rpo_minutes",99999)>w.get("rto_minutes",0):
            errors.append(f"{w.get('id')}: RPO cannot exceed RTO in this lab baseline")
    wave_list=waves.get("waves",[]); wave_ids={x.get("id") for x in wave_list}
    assigned=[]
    for wave in wave_list:
        assigned += wave.get("workloads",[])
        for key in ("entry_gate","exit_gate","rollback_window_minutes","cost_ceiling_usd"):
            if not wave.get(key): errors.append(f"{wave.get('id')}: {key} required")
    if set(assigned)!=ids or len(assigned)!=len(ids):
        errors.append("each workload must be assigned to exactly one wave")
    for w in items:
        members=next((x.get("workloads",[]) for x in wave_list if x.get("id")==w.get("wave")),[])
        if w.get("wave") not in wave_ids or w.get("id") not in members:
            errors.append(f"{w.get('id')}: inventory/wave assignment mismatch")
    for section in ("foundation","security","delivery","validation","post_migration"):
        for key,value in pol.get(section,{}).items():
            if value is not True: errors.append(f"{section}.{key} must be true")
    cut=waves.get("cutover",{})
    for key in ("freeze_window","dns_ttl_reduced","final_sync_required","business_validation_required"):
        if not cut.get(key): errors.append(f"cutover.{key} must be true")
    if not cut.get("rollback_trigger") or not cut.get("hypercare_hours"):
        errors.append("cutover rollback trigger and hypercare required")
    if errors:
        for e in errors: print(f"FAIL {e}")
        print("RESULT: MIGRATION FACTORY PLAN INVALID"); return 1
    strategies={x["strategy"] for x in items}
    print(f"PASS {len(items)} workloads use approved 7R strategies: {', '.join(sorted(strategies))}")
    print(f"PASS {len(wave_list)} waves include entry, exit, rollback and cost gates")
    print("PASS landing zone, identity, security and delivery controls")
    print("PASS functional, security, performance, restore and business validation")
    print("PASS cutover, rollback, hypercare and decommission controls")
    print("RESULT: MIGRATION FACTORY PLAN VALID"); return 0

if __name__=="__main__": sys.exit(main())
