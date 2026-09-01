# Validation Runbook

Use this runbook after installation, maintenance, upgrades, or a VPS reboot.

## Docker status

```bash
cd /opt/monitoring
docker compose ps

docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
```

Expected monitoring services are `Up`; cAdvisor should report healthy when its health check is available.

## Production application health

```bash
docker inspect mundoactivate-db \
  --format='MariaDB={{.State.Status}} Health={{.State.Health.Status}} RestartCount={{.RestartCount}}'

docker inspect mundoactivate-moodle \
  --format='Moodle={{.State.Status}} RestartCount={{.RestartCount}}'
```

## Moodle HTTP validation

```bash
curl -s -o /dev/null \
  -w 'ACTIVATE ONLINE: HTTP %{http_code} | Tiempo: %{time_total}s\n' \
  https://aula.mundoactivate.com
```

Expected HTTP code: `200`.

## Grafana health

```bash
curl -s http://127.0.0.1:3000/api/health
curl -s https://grafana.mundoactivate.com/api/health
```

## Prometheus health

```bash
docker exec monitoring-prometheus wget -qO- http://localhost:9090/-/healthy
docker exec monitoring-prometheus wget -qO- http://localhost:9090/-/ready
```

## Prometheus configuration

```bash
docker exec monitoring-prometheus \
  promtool check config /etc/prometheus/prometheus.yml
```

## Query all targets

```bash
docker exec monitoring-prometheus \
  wget -qO- 'http://localhost:9090/api/v1/query?query=up'
```

The result should show the Prometheus, Node Exporter and cAdvisor targets with value `1`. Blackbox health is validated through `probe_success`.

## Blackbox probe

```bash
docker exec monitoring-prometheus \
  wget -qO- 'http://localhost:9090/api/v1/query?query=probe_success'
```

Expected value for `https://aula.mundoactivate.com`: `1`.

HTTP status:

```bash
docker exec monitoring-prometheus \
  wget -qO- 'http://localhost:9090/api/v1/query?query=probe_http_status_code'
```

Expected value: `200`.

## Host metrics

Load average:

```promql
node_load1
```

RAM utilization percentage:

```promql
100 * (1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes))
```

CPU utilization percentage:

```promql
100 - (
  avg by (instance) (
    rate(node_cpu_seconds_total{mode="idle"}[5m])
  ) * 100
)
```

Root filesystem utilization:

```promql
100 * (
  1 - (
    node_filesystem_avail_bytes{mountpoint="/",fstype!="rootfs"}
    /
    node_filesystem_size_bytes{mountpoint="/",fstype!="rootfs"}
  )
)
```

## Container metrics

Confirm cAdvisor is being scraped:

```promql
container_last_seen
```

Additional dashboard queries can use `container_cpu_usage_seconds_total` and `container_memory_working_set_bytes`.

## Network isolation

```bash
docker network inspect monitoring_net
docker network inspect moodle_mundoactivate-internal
```

Monitoring containers should be on `monitoring_net`; Moodle and MariaDB remain on the Moodle internal network.

## Listening ports

```bash
sudo ss -lntp | grep ':3000'
```

Expected Grafana listener:

```text
127.0.0.1:3000
```

Grafana must not listen on `0.0.0.0:3000` in this architecture.
