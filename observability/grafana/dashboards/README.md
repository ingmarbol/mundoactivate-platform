# Grafana Dashboard

The tested production dashboard is version-controlled in:

```text
activate-infrastructure.json
```

## Dashboard name

`ACTIVATE ONLINE — Infrastructure Overview`

## Included panels

| Panel | Purpose | Primary PromQL |
|---|---|---|
| Moodle Status | Moodle availability | `probe_success` |
| HTTP Status | Moodle HTTP response | `probe_http_status_code` |
| CPU Usage | Host CPU utilization | `100 - (avg by (instance) (rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)` |
| RAM Usage | Host RAM utilization | `100 * (1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes))` |
| Disk Usage / | Root filesystem utilization | `100 * (1 - (node_filesystem_avail_bytes{mountpoint="/",fstype!="rootfs"} / node_filesystem_size_bytes{mountpoint="/",fstype!="rootfs"}))` |
| CPU Usage Over Time | Host CPU trend | CPU query above |
| RAM Usage Over Time | Host RAM trend | RAM query above |
| Load Average | Linux load | `node_load1` |
| HTTP Response Time | Moodle latency | `probe_duration_seconds` |
| Container CPU Usage | Per-container CPU | cAdvisor metrics |
| Container Memory Usage | Per-container memory | cAdvisor metrics |

## Validate JSON

```bash
python3 -m json.tool activate-infrastructure.json > /dev/null && echo 'JSON OK'
```

## Production path

The production server uses:

```text
/opt/monitoring/grafana/dashboards/activate-infrastructure.json
```

Grafana loads this file automatically through the dashboard provisioning configuration in `../provisioning/dashboards/dashboards.yml`.

The dashboard file contains queries and visualization metadata only; no credentials or private keys are included.
