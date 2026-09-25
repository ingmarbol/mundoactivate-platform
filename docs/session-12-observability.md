# Sesión 12 - Observabilidad multicloud e integración final

## Objetivo

Aplicar métricas, logs y traces como un sistema coherente; definir SLI/SLO y alertas accionables; relacionar OpenTelemetry con Amazon CloudWatch y Azure Monitor; y defender la arquitectura acumulativa de la plataforma.

## Alcance

- OpenTelemetry Collector local con recepción OTLP para traces, metrics y logs.
- Procesamiento con `memory_limiter`, `resource` y `batch`.
- Exporter `debug` para un laboratorio sin credenciales Cloud.
- Guía de mapeo posterior hacia CloudWatch/ADOT y Azure Monitor.
- Runbook, SLO, pruebas, evidencias, costos y cleanup.

## Flujo

```text
Aplicación/SDK -> OTLP -> OpenTelemetry Collector
                           |-> CloudWatch / X-Ray (AWS)
                           |-> Azure Monitor / Application Insights (Azure)
                           `-> backend local para aprendizaje
```

## Laboratorio local

```bash
docker compose -f session12/docker-compose.observability.yml config --quiet
docker compose -f session12/docker-compose.observability.yml up -d
curl -fsS http://127.0.0.1:13133/
docker compose -f session12/docker-compose.observability.yml logs --tail=50
```

El resultado esperado es un Collector saludable, sin puertos de ingestión expuestos fuera de localhost. La configuración inicial usa `debug`; no contiene access keys, connection strings ni tokens.

## SLI y SLO inicial

- SLI de disponibilidad: solicitudes HTTP satisfactorias / solicitudes válidas.
- SLO: 99,9 % en ventana móvil de 30 días.
- Error budget: 0,1 %, aproximadamente 43,2 minutos en 30 días.
- Latencia: p95 menor o igual a 500 ms para navegación crítica.
- Alerta: burn rate sostenido, no una alarma por cada error aislado.

## Pruebas y diagnóstico

```bash
docker compose -f session12/docker-compose.observability.yml ps
docker compose -f session12/docker-compose.observability.yml exec otel-collector \
  /otelcol-contrib validate --config=/etc/otelcol-contrib/config.yaml
docker stats --no-stream
```

Si no hay telemetría, verifique en orden: instrumentación y endpoint OTLP, DNS/red, receiver, processors, exporter y permisos del backend. No habilite retries ilimitados ni imprima atributos sensibles.

## Seguridad y costos

- Preferir IAM Roles/IRSA o EKS Pod Identity en AWS y Workload Identity en Azure.
- Aplicar least privilege al exporter y cifrado TLS fuera del host local.
- Eliminar cookies, authorization headers, query strings y PII antes de exportar.
- Limitar cardinalidad, retención y volumen de logs; muestrear traces conscientemente.
- Separar alertas que requieren acción de dashboards exploratorios.

## Evidencias

1. Salida de `docker compose ... config --quiet`.
2. Estado `healthy` del Collector y extracto de logs sin secretos.
3. Diagrama de flujo y explicación de una correlación trace-log-metric.
4. SLI, SLO, error budget y una alerta con owner/runbook.
5. Captura de un dashboard CloudWatch o Azure Monitor, si se ejecuta la extensión Cloud.
6. Defensa de 8 minutos y respuesta a preguntas de seguridad, HA, costos y cleanup.

## Cleanup

```bash
docker compose -f session12/docker-compose.observability.yml down --remove-orphans
docker image rm otel/opentelemetry-collector-contrib:0.136.0 2>/dev/null || true
```

En AWS o Azure, confirme por separado la eliminación de clusters, workspaces, log groups, dashboards, alarms, managed identities y recursos de red creados durante laboratorios.

