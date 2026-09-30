# Sesión 14 - Identity federation y Zero Trust multicloud

## Objetivo

Diseñar acceso humano y de workloads con credenciales temporales, condiciones explícitas y least privilege para AWS, Azure, Kubernetes y GitHub Actions.

## Flujo principal

```text
Human -> corporate IdP -> SAML/OIDC -> IAM Identity Center / Microsoft Entra ID
       -> MFA + Conditional Access -> short session -> role / RBAC assignment

GitHub Actions -> OIDC JWT -> AWS STS or Microsoft Entra token exchange
               -> temporary token -> narrowly scoped deployment role
```

## Laboratorio local

Los ejemplos son plantillas y no realizan login Cloud:

```bash
jq empty session14/aws-github-oidc-trust-policy.json
jq empty session14/azure-federated-credential.json
python3 -c "import yaml; yaml.safe_load(open('session14/identity-baseline.yaml'))"
python3 -c "import yaml; yaml.safe_load(open('session14/github-actions-oidc-example.yml'))"
```

Antes de aplicar, reemplace placeholders mediante IaC, confirme issuer, audience y subject, y use un environment protegido para producción. No agregue access keys, client secrets, tokens o certificados al repositorio.

## Decisiones de seguridad

- Personas: federación, MFA, sesiones cortas y permission sets/roles por función.
- CI/CD: `id-token: write` solo en el job que autentica; `contents: read` por defecto.
- AWS: trust policy restringida por `aud` y `sub`; role permissions separadas del trust.
- Azure: federated identity credential restringida por issuer, subject y audience; Azure RBAC mínimo.
- EKS/AKS: identidad por service account/workload, no credenciales compartidas.
- Break-glass: dos cuentas, uso alertado, credenciales protegidas y pruebas periódicas.

## Evidencias

1. Diagrama workforce/workload federation.
2. Matriz principal, recurso, acción y condición.
3. JSON/YAML validados sin secretos.
4. Explicación de issuer, audience, subject y token lifetime.
5. Threat scenario y respuesta ante token o credencial comprometida.
6. Pull Request y checks.

## Cleanup

El laboratorio local no crea recursos Cloud. Si prueba en cuentas sandbox, elimine federated credentials, OIDC providers o role assignments creados exclusivamente para la prueba, revoque sesiones cuando corresponda y conserve audit logs según retention.

