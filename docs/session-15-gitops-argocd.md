# Sesión 15 - GitOps y despliegue continuo con Argo CD

## Objetivo

Separar CI de CD y convertir Git en la fuente declarativa del estado Kubernetes. Argo CD reconcilia el clúster con manifests versionados, detecta drift y permite promoción y rollback mediante Pull Requests.

## Flujo

```text
Developer -> Pull Request -> tests/security -> build immutable image
          -> update image tag in GitOps overlay -> review/merge
          -> Argo CD pulls desired state -> diff -> sync -> health
          -> CloudWatch/Azure Monitor/OpenTelemetry observe runtime
```

## Contenido del laboratorio

- `argocd-project.yaml`: limita repositorio, namespace y recursos RBAC.
- `application-dev.yaml`: Application con auto-sync, self-heal y prune deshabilitado inicialmente.
- `base/`: Deployment y Service comunes.
- `overlays/dev/`: personalización Kustomize para desarrollo.

## Validación local

```bash
python3 -c "import yaml,glob; [list(yaml.safe_load_all(open(f))) for f in glob.glob('session15/**/*.yaml', recursive=True)]"
kubectl kustomize session15/overlays/dev
kubectl apply --dry-run=client -k session15/overlays/dev
```

El laboratorio no instala Argo CD ni toca un clúster por sí solo. Antes de aplicar, inspeccione el render, use un clúster local/sandbox y confirme que el destino no es producción.

## Seguridad

- No almacenar Secrets en texto claro en Git.
- Preferir External Secrets Operator, Secrets Store CSI Driver o Sealed Secrets según threat model.
- Restringir AppProject, repositorios, destinations, namespaces y recursos cluster-scoped.
- Requerir PR, branch protection y revisión para overlays de producción.
- Usar image digest o tags inmutables en producción.
- Mantener `prune: false` hasta comprender el impacto; habilitarlo con controles y backups.

## Evidencias

1. Render de Kustomize y dry-run exitoso.
2. Diagrama CI -> GitOps repo -> Argo CD -> cluster.
3. Cambio de replicas o image tag mediante PR.
4. Captura de Synced/Healthy o simulación documentada.
5. Prueba de drift y self-heal en sandbox.
6. Rollback mediante `git revert`.
7. Confirmación de que no hay secretos ni credenciales Cloud.

## Cleanup

```bash
kubectl delete -f session15/application-dev.yaml --ignore-not-found
kubectl delete -f session15/argocd-project.yaml --ignore-not-found
kubectl delete namespace mundoactivate-dev --ignore-not-found
```

No elimine Argo CD completo si el clúster lo comparte con otras aplicaciones. Verifique recursos, finalizers y persistent volumes antes del cleanup.

