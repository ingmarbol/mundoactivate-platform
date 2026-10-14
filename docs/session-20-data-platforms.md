# Sesión 20 — Data Platforms multicloud

## Objetivo
Diseñar la persistencia de MundoActivate desde los access patterns, con un system of record por dominio, contratos de datos, seguridad, observabilidad, RTO/RPO y control de costos en AWS y Azure.

## Alcance
- Matriz AWS/Azure para object storage, relational, NoSQL, analytics y streaming.
- Zonas raw, curated y serving.
- Identidad sin credenciales estáticas, cifrado y acceso privado.
- Alta disponibilidad, backup, restore y disaster recovery.
- Laboratorio local sin cuentas cloud ni datos personales.

## Prueba
Ejecute `python3 data-platform/validate_data_contract.py --catalog data-platform/data-products.yaml --records data-platform/sample-records.jsonl`.

Resultado esperado: `RESULT: DATA CONTRACT VALID` y código de salida 0. Para la prueba negativa, duplique un event_id en una copia temporal; debe salir con código distinto de cero.

## Evidencias
Salida positiva, prueba negativa, diagrama, Data SLOs y justificación de RTO/RPO.

## Seguridad y costos
Las muestras son sintéticas y no contienen secretos ni PII. En cloud, use IAM Roles o Managed Identities, private endpoints, cifrado y least privilege. Los drivers son capacidad, IOPS, compute, RU/s, analytics, stream partitions, observability y egress.

## Limpieza
El laboratorio no crea recursos cloud. Elimine solo copias temporales de prueba.
