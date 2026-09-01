# Troubleshooting

## Prometheus reports `bad address`

Example:

```text
wget: bad address 'node-exporter:9100'
```

Cause: the target name does not match the actual Docker Compose service/container DNS name available on `monitoring_net`.

Use the deployed service names:

```text
monitoring-node-exporter:9100
monitoring-cadvisor:8080
monitoring-blackbox:9115
monitoring-prometheus:9090
```

After editing `prometheus.yml`:

```bash
docker exec monitoring-prometheus \
  promtool check config /etc/prometheus/prometheus.yml

docker kill --signal=HUP monitoring-prometheus
```

Then validate:

```bash
docker exec monitoring-prometheus \
  wget -qO- 'http://localhost:9090/api/v1/query?query=up'
```

## `getent` not found inside Prometheus

The Prometheus container image is intentionally minimal and may not include utilities such as `getent`. Do not treat that as a Prometheus failure.

Prefer Prometheus API queries, `wget` available in the image, or inspect Docker networking from the host:

```bash
docker network inspect monitoring_net
```

## Grafana appears empty after provisioning

Validate the provisioning structure:

```bash
tree /opt/monitoring/grafana
```

Expected:

```text
grafana/
├── dashboards/
└── provisioning/
    ├── dashboards/
    │   └── dashboards.yml
    └── datasources/
        └── prometheus.yml
```

Validate dashboard JSON:

```bash
python3 -m json.tool \
  /opt/monitoring/grafana/dashboards/activate-infrastructure.json \
  > /dev/null && echo 'JSON OK'
```

Recreate Grafana only:

```bash
docker compose up -d --no-deps --force-recreate grafana
```

Inspect logs:

```bash
docker logs monitoring-grafana --since 5m
```

## Grafana works through SSH tunnel but not on the Internet

This normally means Grafana itself is healthy and the problem is in DNS, Nginx, firewall or TLS.

Check local Grafana:

```bash
curl -s http://127.0.0.1:3000/api/health
```

Check Nginx syntax:

```bash
sudo nginx -t
```

Check HTTP redirect:

```bash
curl -I http://grafana.mundoactivate.com
```

Check HTTPS:

```bash
curl -s https://grafana.mundoactivate.com/api/health
```

Check certificates:

```bash
sudo certbot certificates
```

## `Failed to fetch` in Grafana Explore

First distinguish a browser/UI transient failure from a datasource failure. Test the same PromQL query again and validate Prometheus directly through its API.

For example:

```bash
docker exec monitoring-prometheus \
  wget -qO- 'http://localhost:9090/api/v1/query?query=probe_http_status_code'
```

If Prometheus returns data and Grafana later renders it, the monitoring pipeline is functional.

## Dashboard CPU appears around 10% while load average is low

CPU percentage and Linux load average measure different things. Do not compare their numeric values directly. CPU utilization is a percentage of CPU time; load average represents runnable/uninterruptible workload demand.

## Disk percentage slowly increases

A slowly rising root filesystem percentage is normal when Prometheus is retaining metrics and Docker/application logs are growing. Monitor the trend and implement retention/log rotation before capacity becomes critical.
