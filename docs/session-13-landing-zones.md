# Sesión 13 - Landing zones y gobierno multicloud

## Objetivo

Diseñar una base empresarial para AWS y Azure que separe workloads, centralice identidad, auditoría y costos, y aplique guardrails mediante policy as code sin bloquear el aprendizaje.

## Arquitectura objetivo

```text
Identity Provider / Workforce identity
        |                         |
AWS Organizations           Microsoft Entra ID
  Management account          Tenant root group
  Security OU                 Platform MG
  Infrastructure OU           Landing Zones MG
  Workloads OU                Sandbox MG
        |                         |
Accounts dev/test/prod       Subscriptions dev/test/prod
```

Los entornos se separan por account/subscription cuando cambian el riesgo, el presupuesto, la administración o el blast radius. Los resource groups y tags ayudan a organizar, pero no sustituyen esos límites.

## Laboratorio seguro

Este directorio contiene una baseline portable y dos policies en modo pedagógico:

- `governance-baseline.yaml`: decisiones mínimas de identidad, seguridad, costos y operación.
- `aws-tag-policy.json`: estandariza tags dentro de AWS Organizations; no concede permisos.
- `azure-tag-policy.json`: audita resource groups que no contienen tags obligatorios; no bloquea ni modifica recursos.

Validación local:

```bash
jq empty session13/aws-tag-policy.json
jq empty session13/azure-tag-policy.json
python3 -c "import yaml; yaml.safe_load(open('session13/governance-baseline.yaml'))"
```

## Orden de adopción

1. Inventariar tenants, organizations, accounts, subscriptions y owners.
2. Definir naming, tagging, regiones permitidas, presupuestos y data classification.
3. Separar security/log archive, shared services, networking, sandbox y workloads.
4. Federar identidad humana; usar workload identities para automatización.
5. Centralizar audit logs antes de imponer controles preventivos.
6. Aplicar `audit/detective` primero, medir impacto y después evaluar `deny/preventive`.
7. Versionar policies, probarlas en sandbox/canary y documentar excepciones con caducidad.

## Evidencias

- Diagrama AWS/Azure con jerarquía y límites.
- Matriz account/subscription, owner, environment y presupuesto.
- JSON/YAML validados.
- Resultado simulado o real de compliance sin secretos.
- Una excepción documentada con owner, justificación, compensación y expiry.
- Cálculo de costos de foundation y procedimiento de rollback/cleanup.

## Seguridad y costos

No use la management account o tenant root para workloads. Proteja break-glass accounts, centralice audit logs y evite access keys/client secrets duraderos. AWS Control Tower, Config, GuardDuty, CloudTrail, Azure Monitor, Defender for Cloud y Log Analytics pueden generar cargos; estime volumen, regiones, retención y número de recursos antes de habilitar a escala.

## Cleanup

El laboratorio local no crea recursos Cloud. Si prueba policies reales, quite primero assignments/attachments de sandbox, verifique que no haya dependencias y conserve audit logs según la política de retención. No elimine organizations, management groups o cuentas de seguridad como parte de un laboratorio.

