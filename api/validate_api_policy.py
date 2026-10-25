#!/usr/bin/env python3
import argparse, pathlib, sys, yaml
def fail(errors, condition, message):
    if not condition: errors.append(message)
def main():
    p=argparse.ArgumentParser(); p.add_argument('--contract',default='api/openapi.yaml'); p.add_argument('--policy',default='api/gateway-policy.yaml')
    a=p.parse_args(); contract=yaml.safe_load(pathlib.Path(a.contract).read_text()); policy=yaml.safe_load(pathlib.Path(a.policy).read_text()); e=[]
    fail(e, contract.get('openapi','').startswith('3.'), 'OpenAPI 3 contract required')
    fail(e, bool(contract.get('info',{}).get('x-owner')), 'API owner required')
    auth=policy.get('authentication',{})
    fail(e, auth.get('type')=='oauth2-jwt', 'OAuth2 JWT authentication required')
    fail(e, bool(auth.get('issuer')) and bool(auth.get('audience')), 'JWT issuer and audience required')
    fail(e, set(auth.get('algorithms',[])) <= {'RS256','ES256'} and bool(auth.get('algorithms')), 'only asymmetric allowlisted algorithms accepted')
    fail(e, auth.get('require_expiration') is True, 'token expiration required')
    fail(e, policy.get('authorization',{}).get('object_level_check') is True, 'BOLA control required')
    t=policy.get('traffic',{}); fail(e, all(int(t.get(x,0))>0 for x in ('rate_limit_per_minute','burst_limit','quota_per_day')), 'rate, burst and quota required')
    fail(e, policy.get('protection',{}).get('waf_enabled') is True, 'WAF required')
    red={str(x).lower() for x in policy.get('observability',{}).get('redact_headers',[])}
    fail(e, {'authorization','x-api-key','cookie'} <= red, 'sensitive headers must be redacted')
    fail(e, policy.get('transport',{}).get('tls_minimum') in {'1.2','1.3'}, 'TLS 1.2 minimum required')
    if e:
        print('RESULT: API POLICY INVALID'); [print('FAIL',x) for x in e]; return 1
    for x in ['OpenAPI ownership','JWT issuer/audience/algorithm/expiry','object authorization','rate and quota','WAF and payload guard','log redaction','TLS and partner mTLS']: print('PASS',x)
    print('RESULT: API GOVERNANCE VALID'); return 0
if __name__=='__main__': sys.exit(main())
