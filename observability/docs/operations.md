# Operations Runbook

## Start

```bash
cd /opt/monitoring
docker compose up -d
```

## Stop

```bash
cd /opt/monitoring
docker compose down
```

`docker compose down` does not delete named volumes unless `-v` is explicitly supplied. Do not use `-v` in routine operations.

## Status

```bash
cd /opt/monitoring
docker compose ps
```

## Logs

```bash
docker logs monitoring-prometheus --tail 100
docker logs monitoring-grafana --tail 100
docker logs monitoring-node-exporter --tail 100
docker logs monitoring-cadvisor --tail 100
docker logs monitoring-blackbox --tail 100
```

Follow a log stream:

```bash
docker logs -f monitoring-grafana
```

## Validate before changing Prometheus

Always run:

```bash
docker exec monitoring-prometheus \
  promtool check config /etc/prometheus/prometheus.yml
```

After a valid configuration change, reload Prometheus without rebuilding the entire stack:

```bash
docker kill --signal=HUP monitoring-prometheus
```

## Grafana provisioning changes

After changing datasource/dashboard provisioning:

```bash
cd /opt/monitoring
docker compose up -d --no-deps --force-recreate grafana
```

## Image updates

Do not blindly update production images. Review release notes, back up persistent data, then:

```bash
cd /opt/monitoring
docker compose pull
docker compose up -d
```

Prefer version pinning rather than `latest` for reproducible production deployments.

## Persistent data

Named volumes:

```text
monitoring_prometheus_data
monitoring_grafana_data
```

List them:

```bash
docker volume ls | grep monitoring
```

Never remove these volumes during normal maintenance.

## VPS reboot behavior

All monitoring services use:

```yaml
restart: unless-stopped
```

With Docker enabled at boot, the containers are expected to return automatically after a VPS reboot.

Check Docker:

```bash
systemctl is-enabled docker
systemctl is-active docker
```

Then verify monitoring:

```bash
docker compose -f /opt/monitoring/compose.yml ps
```

## Capacity checks

Host disk:

```bash
df -h
```

Docker disk usage:

```bash
docker system df
```

Docker root directory:

```bash
docker info --format '{{.DockerRootDir}}'
```

Size:

```bash
sudo du -sh "$(docker info --format '{{.DockerRootDir}}')"
```

## Public checks

```bash
curl -I https://aula.mundoactivate.com
curl -I https://grafana.mundoactivate.com
```

## Backup priorities

Back up:

- `/opt/monitoring/compose.yml`
- `/opt/monitoring/prometheus/`
- `/opt/monitoring/blackbox/`
- `/opt/monitoring/grafana/provisioning/`
- `/opt/monitoring/grafana/dashboards/`
- Grafana persistent volume when local UI state/users must be preserved

The Git repository provides configuration-as-code backup for sanitized configuration and dashboards, but it is not a substitute for persistent-data backups.
