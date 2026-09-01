# ACTIVATE ONLINE — Observability Platform

Production-oriented monitoring and observability stack for the ACTIVATE ONLINE Moodle platform.

## Scope

This project adds observability without modifying the existing Moodle/MariaDB application stack. It runs as an isolated Docker Compose workload and monitors:

- Hetzner VPS host metrics with Node Exporter
- Docker/container metrics with cAdvisor
- Moodle HTTPS availability and latency with Blackbox Exporter
- Time-series collection and PromQL with Prometheus
- Dashboards with Grafana
- Public Grafana access through Nginx + TLS, while keeping Grafana bound to `127.0.0.1:3000`

## Current architecture

```text
Internet
   |
   | HTTPS :443
   v
Nginx
   |
   | reverse proxy
   v
127.0.0.1:3000
   |
   v
Grafana 13.2.0
   |
   | monitoring_net
   v
Prometheus 3.14.0
   |--------------------|---------------------|
   v                    v                     v
Node Exporter        cAdvisor          Blackbox Exporter
   |                    |                     |
   v                    v                     v
Linux VPS            Docker          https://aula.mundoactivate.com
```

## Production isolation

The existing Moodle workload remains separate:

```text
moodle_mundoactivate-internal  -> Moodle + MariaDB
monitoring_net                 -> Grafana + Prometheus + exporters
```

No monitoring container is attached to the Moodle internal Docker network.

## Public endpoints

- Moodle: `https://aula.mundoactivate.com`
- Grafana: `https://grafana.mundoactivate.com`

Prometheus and exporters are intentionally not published to the Internet.

## Repository structure

```text
observability/
├── README.md
├── compose.yml
├── prometheus/
│   └── prometheus.yml
├── blackbox/
│   └── blackbox.yml
├── grafana/
│   ├── dashboards/
│   │   └── activate-infrastructure.json
│   └── provisioning/
│       ├── dashboards/
│       │   └── dashboards.yml
│       └── datasources/
│           └── prometheus.yml
├── nginx/
│   └── grafana.mundoactivate.com.conf
└── docs/
    ├── architecture.md
    ├── installation.md
    ├── validation.md
    ├── operations.md
    ├── security.md
    └── troubleshooting.md
```

## Dashboard

The provisioned dashboard is named:

**ACTIVATE ONLINE — Infrastructure Overview**

It includes:

- Moodle status
- HTTP status
- CPU usage
- RAM usage
- root filesystem usage
- CPU/RAM history
- load average
- HTTP response time
- per-container CPU
- per-container memory

## Important implementation principle

The observability stack must not require changes to the production Moodle Compose file, its volumes, or its internal Docker network.

## Deployment summary

```bash
cd /opt/monitoring
docker compose -f compose.yml config
docker compose pull
docker compose up -d
```

The production implementation uses an externally created Docker network named `monitoring_net`.

## Validation

```bash
docker exec monitoring-prometheus promtool check config /etc/prometheus/prometheus.yml
curl -s http://127.0.0.1:3000/api/health
curl -I https://grafana.mundoactivate.com
curl -I https://aula.mundoactivate.com
```

Prometheus query examples:

```promql
up
probe_success
probe_http_status_code
node_load1
100 * (1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes))
100 - (avg by (instance) (rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)
100 * (1 - (node_filesystem_avail_bytes{mountpoint="/",fstype!="rootfs"} / node_filesystem_size_bytes{mountpoint="/",fstype!="rootfs"}))
```

## Status

Implemented and operational:

- Prometheus
- Grafana
- Node Exporter
- cAdvisor
- Blackbox Exporter
- Grafana provisioning
- Dashboard as code
- Nginx reverse proxy
- Let's Encrypt TLS

Planned next phase:

- Prometheus alerting rules
- Alertmanager
- Notification routing
- MariaDB exporter
- SSL expiry monitoring
