#!/usr/bin/env python3
import argparse, pathlib, sys, yaml
def docs(path):
    out=[]
    for f in sorted(path.glob("*.yaml")): out += [d for d in yaml.safe_load_all(f.read_text()) if d]
    return out
def main():
    p=argparse.ArgumentParser(); p.add_argument("--dir", default="governance")
    a=p.parse_args(); items=docs(pathlib.Path(a.dir)); errors=[]; by_kind={}
    for d in items: by_kind.setdefault(d["kind"],[]).append(d)
    ns=by_kind.get("Namespace",[])
    if not ns or ns[0].get("metadata",{}).get("labels",{}).get("pod-security.kubernetes.io/enforce") != "restricted": errors.append("namespace must enforce restricted Pod Security")
    if not by_kind.get("ResourceQuota") or not by_kind.get("LimitRange"): errors.append("quota and limit range are mandatory")
    nps=by_kind.get("NetworkPolicy",[])
    if not any(set(x.get("spec",{}).get("policyTypes",[]))=={"Ingress","Egress"} and not x.get("spec",{}).get("ingress") and not x.get("spec",{}).get("egress") for x in nps): errors.append("default-deny ingress/egress is mandatory")
    for r in by_kind.get("Role",[]):
        for rule in r.get("rules",[]):
            if "*" in rule.get("verbs",[]) or "*" in rule.get("resources",[]): errors.append("RBAC wildcard forbidden")
    if by_kind.get("ClusterRoleBinding"): errors.append("tenant baseline cannot create ClusterRoleBinding")
    for dep in by_kind.get("Deployment",[]):
        spec=dep["spec"]["template"]["spec"]
        if spec.get("automountServiceAccountToken",True): errors.append("service account token must not automount")
        for c in spec.get("containers",[]):
            sc=c.get("securityContext",{}); res=c.get("resources",{})
            if sc.get("allowPrivilegeEscalation") is not False or sc.get("capabilities",{}).get("drop") != ["ALL"]: errors.append("container hardening incomplete")
            if not res.get("requests") or not res.get("limits"): errors.append("requests and limits required")
    if errors:
        print("RESULT: GOVERNANCE INVALID"); [print("FAIL",x) for x in errors]; return 1
    for x in ["restricted Pod Security","quota and limits","default-deny network","least-privilege RBAC","workload hardening"]: print("PASS",x)
    print("RESULT: TENANT BASELINE VALID"); return 0
if __name__=="__main__": sys.exit(main())
