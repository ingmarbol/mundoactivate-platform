#!/usr/bin/env python3
import argparse, csv, math, pathlib, sys, yaml

def fail(msg):
    raise ValueError(msg)

def run(config_path, measurements_path):
    cfg=yaml.safe_load(pathlib.Path(config_path).read_text())
    rows=list(csv.DictReader(pathlib.Path(measurements_path).open()))
    if not rows: fail('measurements are empty')
    w=cfg['workload']; a=cfg['autoscaling']; r=cfg['resources']; s=cfg['slo']; g=cfg['guardrails']
    for key in ('cpu_request_millicores','cpu_limit_millicores','memory_request_mib','memory_limit_mib'):
        if float(r[key]) <= 0: fail(f'{key} must be positive')
    if r['cpu_request_millicores'] > r['cpu_limit_millicores']: fail('CPU request exceeds limit')
    if r['memory_request_mib'] > r['memory_limit_mib']: fail('memory request exceeds limit')
    if not (1 <= a['min_replicas'] <= a['max_replicas']): fail('invalid replica bounds')
    if a['scale_down_stabilization_seconds'] < 180: fail('scale-down stabilization must be at least 180s')
    if not all(g[k] is True for k in ('require_pdb','require_topology_spread','forbid_production_load_test')): fail('safety guardrails incomplete')
    concurrency=w['peak_rps'] * w['average_service_time_ms']/1000
    concurrency_with_headroom=concurrency*(1+w['concurrency_headroom_percent']/100)
    replicas=math.ceil(w['peak_rps']/w['max_rps_per_pod']*(1+w['concurrency_headroom_percent']/100))
    if replicas > a['max_replicas']: fail(f'max_replicas too low; recommendation={replicas}')
    peak=next((x for x in rows if x['scenario']=='peak'),None)
    if not peak: fail('peak measurement missing')
    if float(peak['p95_ms']) > s['latency_p95_ms']: fail('peak p95 violates SLO')
    if float(peak['error_rate_percent']) > s['error_rate_percent']: fail('peak error rate violates SLO')
    return concurrency,concurrency_with_headroom,replicas

def main():
    p=argparse.ArgumentParser(); p.add_argument('--config',default='performance/capacity-baseline.yaml'); p.add_argument('--measurements',default='performance/measurements.csv'); args=p.parse_args()
    try:
        c,ch,reps=run(args.config,args.measurements)
    except Exception as exc:
        print(f'FAIL: {exc}'); return 1
    print(f'PASS Little Law concurrency={c:.1f}')
    print(f'PASS concurrency with headroom={ch:.1f}')
    print(f'PASS recommended peak replicas={reps}')
    print('PASS SLO at measured peak')
    print('PASS autoscaling and safety guardrails')
    print('RESULT: CAPACITY BASELINE VALID')
    return 0
if __name__=='__main__': sys.exit(main())

