#!/usr/bin/env python3
"""Validate a local multi-cloud network topology without cloud access."""
import argparse, ipaddress, json
from pathlib import Path
def load(path):
    try: return json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError,json.JSONDecodeError) as exc: raise SystemExit(f"FAIL invalid topology: {exc}")
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--topology",required=True)
    topology=load(ap.parse_args().topology); errors=[]; networks={}
    for item in topology.get("networks",[]):
        name=item.get("name")
        if not name or name in networks: errors.append(f"invalid or duplicate network name: {name}"); continue
        try: networks[name]={"cidr":ipaddress.ip_network(item["cidr"],strict=True),"segment":item["segment"]}
        except (KeyError,ValueError) as exc: errors.append(f"{name}: invalid network: {exc}")
    names=list(networks)
    for i,left in enumerate(names):
        for right in names[i+1:]:
            if networks[left]["cidr"].overlaps(networks[right]["cidr"]): errors.append(f"CIDR overlap: {left} and {right}")
    for route in topology.get("routes",[]):
        source,target=route.get("from"),route.get("to")
        if source not in networks or target not in networks: errors.append(f"orphan route: {source} -> {target}"); continue
        if {networks[source]["segment"],networks[target]["segment"]}=={"prod","nonprod"}: errors.append(f"prod/nonprod route forbidden: {source} -> {target}")
        if route.get("via")!="inspection": errors.append(f"inspection bypass: {source} -> {target}")
    zones={r.get("zone") for r in topology.get("dns_resolvers",[]) if r.get("zone")}
    if len(zones)<2: errors.append("DNS resolver HA requires at least two zones")
    if topology.get("default_route_owner")!="security": errors.append("default route owner must be security")
    if errors:
        for error in errors: print("FAIL",error)
        raise SystemExit("RESULT: NETWORK TOPOLOGY REJECTED")
    print("PASS CIDR plan: no overlaps"); print("PASS route references"); print("PASS segment policy")
    print("PASS inspection paths"); print("PASS DNS resolver HA"); print("RESULT: NETWORK TOPOLOGY VALID")
if __name__=="__main__": main()
