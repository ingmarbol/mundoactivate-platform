# Sesión 38 - Enterprise Integration, Messaging y Event Streaming multicloud

El laboratorio define un contrato CloudEvents para CourseCompleted, dos eventos sintéticos y una policy operativa. El objetivo es demostrar idempotency, retry con backoff y jitter, dead-letter handling, ordering por tenant, replay gobernado, workload identity y observabilidad end-to-end.

## Ejecución

    python3 event-platform/validate_event_platform.py \
      --contract event-platform/event-contract.yaml \
      --policy event-platform/integration-policy.yaml \
      --events event-platform/sample-events.jsonl

Resultado esperado: RESULT: EVENT PLATFORM BASELINE VALID.

## Prueba negativa

Copie sample-events.jsonl, duplique el id del segundo evento y ejecute el validador contra la copia. Debe terminar con código distinto de cero y mostrar EVENT PLATFORM BASELINE INVALID.

## Seguridad y costos

- No incluya payloads reales, PII, secrets, access keys ni connection strings.
- Use IAM roles o Azure Managed Identities con private endpoints.
- Controle retention, throughput units, partitions, egress, log volume y DLQ age.
- El laboratorio es local y solo requiere eliminar la copia temporal negativa.

## Evidencias

Comparta contrato, policy, salidas positiva y negativa, diagrama de producer-broker-consumer, tabla de servicios AWS/Azure, estrategia de replay, métricas de lag y DLQ, y decisión de ordering.
