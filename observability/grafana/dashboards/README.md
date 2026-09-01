# Grafana Dashboard

The production dashboard is provisioned from:

```text
activate-infrastructure.json
```

The JSON file should be exported/copied from the tested production dashboard before merging this feature into `main` so that the repository remains the source of truth for the exact visual definition.

## Dashboard name

`ACTIVATE ONLINE — Infrastructure Overview`

## Expected panels

| Panel | Purpose | Primary PromQL |
|---|---|---|
| ACTIVATE ONLINE status | Moodle availability | `probe_success` |
| HTTP status | Moodle HTTP response | `probe_http_status_code` |
| CPU | Host CPU utilization | `100 - (avg by (instance) (rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)` |
| RAM | Host RAM utilization | `100 * (1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes))` |
| Disk | Root filesystem utilization | `100 * (1 - (node_filesystem_avail_bytes{mountpoint="/",fstype!="rootfs"} / node_filesystem_size_bytes{mountpoint="/",fstype!="rootfs"}))` |
| CPU Usage Over Time | Host CPU trend | CPU query above |
| RAM Usage Over Time | Host RAM trend | RAM query above |
| Load Average | Linux load | `node_load1` |
| HTTP Response Time | Moodle latency | `probe_duration_seconds * 1000` |
| Container CPU Usage | Per-container CPU | cAdvisor metrics |
| Container Memory Usage | Per-container memory | cAdvisor metrics |

## Validate JSON

```bash
python3 -m json.tool activate-infrastructure.json > /dev/null && echo 'JSON OK'
```

## Production export

The production server currently stores the dashboard file at:

```text
/opt/monitoring/grafana/dashboards/activate-infrastructure.json
```

Before replacing this documentation placeholder with the exact JSON, sanitize the file and verify it contains no secrets. Grafana dashboard JSON normally contains queries and metadata, not credentials, but it must still be reviewed before publication.
