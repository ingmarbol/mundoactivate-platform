# Installation Guide

## 1. Objective

Deploy an isolated observability stack alongside ACTIVATE ONLINE without altering the Moodle/MariaDB production Compose workload.

## 2. Directory structure

Production path:

```bash
/opt/monitoring
```

Create the required structure:

```bash
sudo mkdir -p /opt/monitoring/{prometheus/rules,blackbox,alertmanager,grafana/dashboards,grafana/provisioning/dashboards,grafana/provisioning/datasources}
```

Verify:

```bash
tree /opt/monitoring
```

## 3. Docker network

Create a dedicated bridge network:

```bash
docker network create monitoring_net
```

Verify:

```bash
docker network ls
docker network inspect monitoring_net
```

The production deployment observed the subnet `172.21.0.0/16`. Do not hard-code this subnet unless there is a networking requirement; Docker can allocate it.

## 4. Configuration files

Place the repository files in `/opt/monitoring` preserving their relative paths.

Validate Compose before starting anything:

```bash
cd /opt/monitoring
docker compose -f compose.yml config
```

Expected: configuration renders without errors.

## 5. Pull images

```bash
docker compose pull
```

Images used by the implemented stack:

```text
prom/prometheus:v3.14.0
grafana/grafana:13.2.0
quay.io/prometheus/node-exporter:latest
ghcr.io/google/cadvisor:v0.60.5
quay.io/prometheus/blackbox-exporter:latest
```

For long-term reproducibility, pin all `latest` images to tested versions before a future production rebuild.

## 6. Start the stack

```bash
docker compose up -d
```

Verify:

```bash
docker compose ps
```

Expected containers:

```text
monitoring-prometheus
monitoring-grafana
monitoring-node-exporter
monitoring-cadvisor
monitoring-blackbox
```

## 7. Confirm existing application is unaffected

```bash
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
```

Moodle and MariaDB must remain running/healthy.

## 8. Validate Prometheus configuration

```bash
docker exec monitoring-prometheus \
  promtool check config /etc/prometheus/prometheus.yml
```

Expected:

```text
SUCCESS: /etc/prometheus/prometheus.yml is valid prometheus config file syntax
```

Health endpoints:

```bash
docker exec monitoring-prometheus wget -qO- http://localhost:9090/-/healthy
docker exec monitoring-prometheus wget -qO- http://localhost:9090/-/ready
```

## 9. Grafana

Grafana is deliberately bound to loopback:

```text
127.0.0.1:3000 -> container:3000
```

Validate locally:

```bash
curl -s http://127.0.0.1:3000/api/health
```

Expected fields include:

```json
{
  "database": "ok",
  "version": "13.2.0"
}
```

## 10. Initial secure access with SSH tunnel

Before publishing Grafana through Nginx, it can be reached from an administrator workstation through SSH port forwarding. Example:

```bash
ssh -L 13000:127.0.0.1:3000 USER@VPS
```

Then browse to `http://localhost:13000`.

This is useful for administration and for proving that Grafana itself works before adding the reverse proxy.

## 11. Public Grafana reverse proxy

Install the Nginx virtual host using the reference file in `nginx/` and enable it according to the VPS Nginx layout.

Validate Nginx:

```bash
sudo nginx -t
```

Reload only after a successful validation:

```bash
sudo systemctl reload nginx
```

HTTP should redirect to HTTPS:

```bash
curl -I http://grafana.mundoactivate.com
```

## 12. TLS certificate

Use Certbot with the Nginx plugin for the Grafana hostname:

```bash
sudo certbot --nginx -d grafana.mundoactivate.com
```

Inspect installed certificates:

```bash
sudo certbot certificates
```

Validate the public Grafana API:

```bash
curl -s https://grafana.mundoactivate.com/api/health
```

## 13. Recreate only Grafana when provisioning changes

```bash
cd /opt/monitoring
docker compose up -d --no-deps --force-recreate grafana
```

This avoids unnecessary restarts of Prometheus and exporters.
