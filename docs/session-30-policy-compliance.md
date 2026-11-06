# Sesión 30 — Policy as Code y Compliance Automation

Este laboratorio convierte requisitos de seguridad en controles versionados y verificables para AWS, Azure y Kubernetes.

## Ejecutar

```bash
python3 -m pip install pyyaml
python3 policy/validate_compliance.py \
  --baseline policy/compliance-baseline.yaml \
  --workloads policy/workloads.yaml
```

Resultado esperado: `RESULT: COMPLIANCE BASELINE VALID`.

## Prueba negativa

Trabaje sobre una copia temporal y cambie `failure_action_prod: Enforce` por `Audit`. El validador debe finalizar con código distinto de cero y reportar que producción requiere `Enforce`.

## Evidencias

- Salida positiva y negativa del validador.
- Matriz control–riesgo–owner–evidencia.
- Plan de rollout Audit → Enforce.
- Excepción con owner, ticket, justificación y expiración.
- Captura de checks del Pull Request.

## Seguridad y costos

No contiene credenciales ni datos sensibles. El laboratorio es local. En Cloud, estimar costos de AWS Config, logs, remediaciones, Azure Policy/Log Analytics y Kyverno antes de ampliar el alcance.

## Limpieza

Eliminar únicamente las copias temporales usadas para la prueba negativa. Si se despliega en un clúster de pruebas, retirar primero assignments/policies y luego el clúster temporal después de conservar evidencia.
