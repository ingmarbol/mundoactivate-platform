# Troubleshooting

## Moodle does not start

```bash
docker compose ps
docker compose logs --tail=200 mariadb
docker compose logs --tail=200 moodle
```

Confirm that MariaDB is healthy and that database variable names match between both services.

## Nginx returns 502

```bash
curl -I http://127.0.0.1:8080
sudo nginx -t
sudo journalctl -u nginx --since "30 minutes ago"
```

If loopback access fails, inspect the Moodle container. If it succeeds, inspect the Nginx upstream, hostname, and TLS configuration.

## Database authentication fails

Do not print secrets. Confirm that the application user, database name, and container network are consistent. When a database volume already exists, changing initialization variables does not automatically recreate database users.

## Disk usage is high

```bash
df -h
docker system df
du -sh backups/* 2>/dev/null
```

Do not delete volumes blindly. Identify whether growth comes from Moodle data, MariaDB, Docker layers, logs, or local backups, and take a verified backup before any cleanup.

## Certificate problems

```bash
sudo nginx -t
sudo certbot certificates
```

Verify DNS, certificate paths, expiry, renewal timers, and inbound access to the ACME challenge path.
