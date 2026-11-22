# Sesión 37 — Cloud Operations Model, SRE y AIOps multicloud

Este laboratorio convierte cuatro servicios de la plataforma acumulativa en un modelo operativo verificable. El catálogo asigna owner, on-call, runbook, dashboard, dependencias y telemetry; los SLOs usan ventanas de 30 días y alertas multi-window; la política exige incident management, automation segura, operational readiness y AIOps con supervisión humana.

## Ejecución

    python3 sre-operations/validate_sre_operations.py \
      --catalog sre-operations/service-catalog.yaml \
      --slos sre-operations/slo-policy.yaml \
      --policy sre-operations/operations-policy.yaml

Resultado esperado: RESULT: SRE OPERATIONS BASELINE VALID.

## Prueba negativa

Copie operations-policy.yaml, cambie human_in_the_loop a false y ejecute el validador contra la copia. Debe terminar con código distinto de cero y reportar SRE OPERATIONS BASELINE INVALID.

## Seguridad, costos y limpieza

- No incluya incident payloads, credenciales, datos personales ni tokens.
- AIOps recomienda; acciones destructivas requieren aprobación, rollback y audit trail.
- Controle cardinality, log retention y sampling para contener costos de observabilidad.
- El laboratorio es local; elimine solo la copia temporal creada para la prueba negativa.

## Evidencias

Comparta salida positiva y negativa, catálogo, SLOs, policy, dashboard conceptual, una decisión de error budget y un runbook hipotético. La aprobación y el merge quedan bajo control de Marco.
