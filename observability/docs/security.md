# Security Design

## Security objectives

The monitoring stack was designed to expose only the minimum required surface to the Internet.

## Grafana exposure

Grafana publishes Docker port 3000 only on loopback:

```yaml
ports:
  - "127.0.0.1:3000:3000"
```

This prevents direct Internet access to TCP/3000. Public access is terminated at Nginx over HTTPS.

## Reverse proxy flow

```text
Client -> TCP/443 -> Nginx -> 127.0.0.1:3000 -> Grafana
```

Do not change the Grafana mapping to `3000:3000` unless direct exposure is explicitly required and protected by additional controls.

## Prometheus and exporters

Prometheus, Node Exporter, cAdvisor and Blackbox Exporter have no host `ports:` mappings. They communicate on the dedicated Docker bridge `monitoring_net`.

This avoids public exposure of:

- Prometheus 9090
- Node Exporter 9100
- cAdvisor 8080
- Blackbox Exporter 9115

## Network separation

Monitoring uses `monitoring_net`, separate from `moodle_mundoactivate-internal`. The monitoring workload does not need direct MariaDB access for the current scope.

## TLS

`grafana.mundoactivate.com` is protected with a Let's Encrypt certificate managed by Certbot/Nginx. HTTP is redirected to HTTPS.

Validate periodically:

```bash
sudo certbot certificates
sudo certbot renew --dry-run
```

## Secrets

Never commit the following to GitHub:

- Grafana administrator passwords
- database passwords
- `.env` production files
- private SSH keys
- Let's Encrypt private keys
- API tokens
- SMTP credentials
- Alertmanager webhook secrets

Only sanitized examples belong in the repository.

## cAdvisor privilege

cAdvisor requires broad host visibility and is configured as privileged in the current implementation. This is a security-sensitive component. Keep its image pinned to a tested release, do not expose its port publicly, and review the required mounts/privileges during future hardening.

## Grafana accounts

Recommended controls:

- use a unique administrator password
- create named administrator/operator accounts instead of sharing credentials
- disable anonymous access unless a deliberate public dashboard is required
- apply least privilege to viewer/editor roles
- enable MFA/SSO if later supported by the selected authentication architecture

## Firewall

The public service design should normally require only SSH administration and web traffic. Prometheus/exporter ports do not need public firewall rules.

## Repository sanitization

The repository intentionally documents hostnames and architecture useful for a technical portfolio, but excludes credentials, server IP addresses, private keys and database secrets.
