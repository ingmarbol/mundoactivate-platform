# Architecture

## Context

ACTIVATE ONLINE runs Moodle and MariaDB as Docker containers on an Ubuntu VPS. The observability implementation was intentionally introduced as a separate workload to reduce the risk of affecting the production LMS.

## Logical architecture

```text
                         INTERNET
                            |
                         HTTPS/443
                            |
                    +-------v-------+
                    |     Nginx     |
                    +-------+-------+
                            |
                     127.0.0.1:3000
                            |
                    +-------v-------+
                    |    Grafana    |
                    +-------+-------+
                            |
                       Prometheus
                            |
             +--------------+---------------+
             |              |               |
      Node Exporter      cAdvisor       Blackbox
             |              |               |
          Ubuntu VPS      Docker        Moodle HTTPS
```

## Docker topology

### Application network

`moodle_mundoactivate-internal`

Contains the production application services, including:

- `mundoactivate-moodle`
- `mundoactivate-db`

During validation this network used Docker bridge addressing in `172.18.0.0/16`.

### Monitoring network

`monitoring_net`

Contains:

- `monitoring-prometheus`
- `monitoring-grafana`
- `monitoring-node-exporter`
- `monitoring-cadvisor`
- `monitoring-blackbox`

During implementation Docker allocated `172.21.0.0/16`.

These addresses are operational observations, not configuration requirements.

## Component responsibilities

### Prometheus

Scrapes and stores time-series metrics. Retention is configured for 15 days in the current deployment.

### Grafana

Visualizes Prometheus metrics. Prometheus is provisioned automatically as the default datasource. Dashboards are provisioned from JSON files so the visualization layer can be version-controlled.

### Node Exporter

Exposes Linux host metrics such as CPU, memory, load, filesystem and operating-system statistics.

### cAdvisor

Exposes Docker/container resource metrics. It receives read-only access to relevant host paths and Docker runtime information.

### Blackbox Exporter

Performs an external-style HTTP/HTTPS probe against `https://aula.mundoactivate.com`. This validates the application through its public endpoint instead of merely checking whether a container process exists.

### Nginx

Acts as the Internet-facing reverse proxy for Grafana. TLS terminates at Nginx and traffic is proxied to Grafana over loopback.

## Availability model

The current stack observes multiple layers:

```text
Application availability -> Blackbox Exporter
Host health              -> Node Exporter
Container health/load    -> cAdvisor
Metrics pipeline         -> Prometheus
Visualization            -> Grafana
```

This is more useful than monitoring only Docker container state because a running container does not guarantee that Moodle is reachable through DNS, TLS and Nginx.

## Future extension

Alertmanager and alert rules are intentionally a separate phase. MariaDB-specific monitoring can later be introduced through a database exporter using a dedicated least-privilege monitoring account.
