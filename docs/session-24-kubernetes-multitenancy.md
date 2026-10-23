# Sesión 24 - Kubernetes multi-tenancy y governance

Baseline local para un tenant con Namespace, Pod Security Admission, ResourceQuota, LimitRange, RBAC, NetworkPolicy y workload endurecido.

## Validar

```bash
python3 governance/validate_governance.py --dir governance
kubectl apply --dry-run=server -f governance/tenant-baseline.yaml
kubectl auth can-i --as-group=platform-tenant-blue-developers create deployments -n tenant-blue
```

El server dry-run requiere un clúster sandbox. Compruebe el contexto antes de usar apply. No se incluyen secretos ni credenciales.

## Prueba negativa

En una copia temporal, cambie pod-security.kubernetes.io/enforce: restricted por privileged. El validator debe devolver código distinto de cero.

## Limpieza

```bash
kubectl delete namespace tenant-blue
```
