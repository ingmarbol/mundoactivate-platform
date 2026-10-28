#!/usr/bin/env python3
import argparse, pathlib, sys, yaml

def main():
    p=argparse.ArgumentParser(); p.add_argument('--dir',default='mesh'); a=p.parse_args(); docs=[]
    for f in pathlib.Path(a.dir).glob('*.yaml'): docs += [d for d in yaml.safe_load_all(f.read_text()) if d]
    kinds={}; errors=[]
    for d in docs: kinds.setdefault(d['kind'],[]).append(d)
    ns=kinds.get('Namespace',[])
    if not ns or ns[0].get('metadata',{}).get('labels',{}).get('istio.io/dataplane-mode')!='ambient': errors.append('namespace must opt into ambient mode')
    peers=kinds.get('PeerAuthentication',[])
    if not peers or not any(x.get('spec',{}).get('mtls',{}).get('mode')=='STRICT' for x in peers): errors.append('STRICT mTLS required')
    aps=kinds.get('AuthorizationPolicy',[])
    if not any(x.get('metadata',{}).get('name')=='default-deny' and x.get('spec')=={} for x in aps): errors.append('default-deny authorization required')
    allows=[x for x in aps if x.get('spec',{}).get('action')=='ALLOW']
    if not allows: errors.append('explicit ALLOW policy required')
    for x in allows:
      principals=[]
      for rule in x.get('spec',{}).get('rules',[]):
        for source in rule.get('from',[]): principals += source.get('source',{}).get('principals',[])
      if any(p=='*' or p.endswith('/sa/*') for p in principals): errors.append('wildcard identity forbidden')
    vs=kinds.get('VirtualService',[])
    for x in vs:
      for rule in x.get('spec',{}).get('http',[]):
        if not rule.get('timeout'): errors.append('HTTP timeout required')
        attempts=int(rule.get('retries',{}).get('attempts',0))
        if attempts<1 or attempts>3: errors.append('retries must be bounded from 1 to 3')
        if sum(r.get('weight',0) for r in rule.get('route',[]))!=100: errors.append('route weights must total 100')
    for d in kinds.get('Deployment',[]):
      for c in d['spec']['template']['spec'].get('containers',[]):
        if not c.get('resources',{}).get('requests') or not c.get('resources',{}).get('limits'): errors.append('workload requests and limits required')
    if errors:
      print('RESULT: MESH BASELINE INVALID'); [print('FAIL',x) for x in errors]; return 1
    for x in ['ambient enrollment','STRICT mTLS','default deny and explicit identity','bounded retries and timeout','canary weights','workload resources']: print('PASS',x)
    print('RESULT: SERVICE MESH BASELINE VALID'); return 0
if __name__=='__main__': sys.exit(main())
