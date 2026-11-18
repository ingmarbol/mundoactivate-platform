# Sesión 35 — Data Protection, Privacy Engineering y Data Security multicloud

Laboratorio seguro del proyecto **Plataforma multicloud segura y observable**. Modela clasificación, propósito, retención, residencia, cifrado, tokenización, DLP, protección de secretos, redacción de telemetry y evidencia de borrado.

## Ejecutar

```bash
python3 data-protection/validate_data_protection.py \
  --classification data-protection/data-classification.yaml \
  --policy data-protection/protection-policy.yaml \
  --flows data-protection/data-flows.yaml
```

Resultado esperado: `RESULT: DATA PROTECTION BASELINE VALID`.

## Prueba negativa

En una copia temporal de `data-classification.yaml`, cambie `payment-reference.tokenization` a `false`. El validator debe devolver `INVALID` y salir con código distinto de cero.

## Evidencias

- Output positivo y negativo.
- Diagrama de data flows y owners.
- Capturas de clasificación Macie/Purview sin datos reales.
- Evidencia de CMK, private access, DLP y redacción, sin IDs sensibles.
- Estimación de costos, retención y cleanup.

No almacene secretos, `.env`, claves, certificados, `*.tfstate`, datos personales ni payloads reales.
