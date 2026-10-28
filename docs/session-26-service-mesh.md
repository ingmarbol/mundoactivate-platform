# Sesión 26 - Service Mesh y Zero Trust east-west

Baseline educativo con Istio ambient, mTLS STRICT, deny-by-default, identidad por ServiceAccount, canary 90/10, timeouts, retries y outlier detection.

## Validación local

```bash
python3 mesh/validate_mesh.py --dir mesh
```

## Prueba negativa

En una copia temporal cambie `mode: STRICT` por `PERMISSIVE`. El validator debe fallar.

## Sandbox opcional

```bash
kubectl config current-context
kubectl apply --dry-run=server -f mesh/mesh-baseline.yaml
kubectl apply --dry-run=server -f mesh/workloads.yaml
```

No ejecute `apply` hasta confirmar un clúster local o de desarrollo. El laboratorio no contiene secretos, certificados ni credenciales Cloud.

## Nota actual

AWS App Mesh terminó soporte el 30 de septiembre de 2026; no se propone para nuevas arquitecturas. El add-on Istio administrado de AKS usa sidecars y todavía no soporta ambient mode.
