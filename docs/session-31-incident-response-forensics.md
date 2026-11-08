# Sesión 31 - Incident Response y Forensics multicloud

El laboratorio valida un plan de respuesta para AWS, Azure y Kubernetes y construye una evidencia local sintética con hash SHA-256. No ejecuta acciones en cuentas Cloud.

## Requisitos

```bash
python3 -m pip install pyyaml
```

## Validación positiva

```bash
python3 incident-response/validate_incident.py \
  --plan incident-response/incident-plan.yaml \
  --alerts incident-response/alerts.jsonl
```

Resultado esperado: `RESULT: INCIDENT RESPONSE BASELINE VALID`.

## Adquisición de evidencia sintética

```bash
python3 incident-response/collect_evidence.py \
  --case-id IR-2026-031 \
  --source incident-response/alerts.jsonl \
  --output /tmp/ir-2026-031
sha256sum /tmp/ir-2026-031/alerts.jsonl
```

El hash debe coincidir con `manifest.json`.

## Prueba negativa

Sobre una copia temporal, cambie `immutable_storage: true` por `false`. El validador debe terminar con código distinto de cero.

## Evidencias para revisión

- Salida positiva y negativa del validador.
- `manifest.json` y verificación independiente del hash.
- Timeline UTC correlacionado por `case_id`.
- Matriz de roles y decisiones de contención.
- Checklist de recuperación y lessons learned.

## Seguridad, costos y limpieza

No use datos reales, tokens, credenciales, Secret objects, memoria o discos de producción en este laboratorio. En Cloud, considere costos de retención, ingestión, consultas, snapshots y cuentas de forensics. Elimine únicamente `/tmp/ir-2026-031` al finalizar; conserve la evidencia real según política y legal hold.

