#!/usr/bin/env python3
import argparse,csv,pathlib,sys,yaml

def require(ok,msg):
    if not ok: raise ValueError(msg)

def validate(plan_path,evidence_path):
    p=yaml.safe_load(pathlib.Path(plan_path).read_text())
    rows=list(csv.DictReader(pathlib.Path(evidence_path).open()))
    o=p['objectives']; c=p['controls']
    require(o['rpo_minutes']>0 and o['rto_minutes']>0,'RPO/RTO must be positive')
    require(o['minimum_retention_days']>=30,'retention below baseline')
    require(o['restore_test_frequency_days']<=90,'restore tests must be at least quarterly')
    for key in ('immutable','cross_account_or_subscription_copy','separate_recovery_identity','multi_party_approval','audit_logging'):
        require(c.get(key) is True,f'missing cyber recovery control: {key}')
    require(c.get('encryption')=='customer_managed_key','customer-managed encryption required')
    owners={w.get('owner') for w in p.get('workloads',[])}
    require(None not in owners and len(owners)>=2,'workload ownership incomplete')
    seq=p.get('recovery_sequence',[])
    require(seq[:2]==['establish_clean_room','recover_identity_and_network'],'unsafe recovery sequence')
    require(rows,'restore evidence missing')
    for r in rows:
        require(int(r['recovery_point_age_minutes'])<=o['rpo_minutes'],f"RPO failed: {r['workload']}")
        require(int(r['restore_duration_minutes'])<=o['rto_minutes'],f"RTO failed: {r['workload']}")
        require(r['integrity_check']=='pass' and r['business_check']=='pass',f"validation failed: {r['workload']}")
        require(r['cleanup_complete']=='true',f"cleanup incomplete: {r['workload']}")
    return len(rows),max(int(r['restore_duration_minutes']) for r in rows)

def main():
    a=argparse.ArgumentParser();a.add_argument('--plan',default='recovery/recovery-plan.yaml');a.add_argument('--evidence',default='recovery/restore-evidence.csv');x=a.parse_args()
    try: count,worst=validate(x.plan,x.evidence)
    except Exception as e: print(f'FAIL: {e}');return 1
    print('PASS immutable and isolated backup controls')
    print('PASS RPO for all restore evidence')
    print(f'PASS RTO for {count} workloads; worst={worst} minutes')
    print('PASS integrity and business validation')
    print('PASS cleanup evidence')
    print('RESULT: CYBER RECOVERY BASELINE VALID')
    return 0
if __name__=='__main__':sys.exit(main())

