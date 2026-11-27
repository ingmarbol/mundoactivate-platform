# Sesión 39 - Secure Software Architecture y Modern Application Patterns

Este laboratorio convierte decisiones arquitectónicas en fitness functions ejecutables. El catálogo define cuatro bounded contexts con owner, API, database ownership y workload identity. La policy exige security, resilience, progressive delivery, observability, strangler evolution y límites para cell-based architecture.

## Ejecución

    python3 architecture/validate_architecture.py \
      --catalog architecture/component-catalog.yaml \
      --policy architecture/architecture-policy.yaml

Resultado esperado: RESULT: SECURE ARCHITECTURE BASELINE VALID.

## Prueba negativa

Copie component-catalog.yaml y asigne database_owner learning al componente reporting. El validador debe rechazar shared database ownership y devolver SECURE ARCHITECTURE BASELINE INVALID.

## Seguridad, costos y limpieza

- No incluya passwords, tokens, connection strings, private keys ni datos reales.
- Use IAM roles, Pod Identity o Azure Workload Identity por componente.
- El aislamiento aumenta costo: justifique microservices y cells por cambio, escala o riesgo.
- El laboratorio es local; elimine solo la copia temporal negativa.

## Evidencias

Comparta catálogo, dependency graph, decisiones de boundary, salida positiva y negativa, strangler roadmap, un failure-mode table, fitness functions y un rollback plan.
