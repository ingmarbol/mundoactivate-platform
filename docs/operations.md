# Operations runbook

## Daily checks

```bash
docker compose ps
./scripts/health-check.sh
docker stats --no-stream
df -h
```

## Logs

```bash
docker compose logs --since=1h moodle
docker compose logs --since=1h mariadb
sudo journalctl -u nginx --since "1 hour ago"
```

## Controlled restart

```bash
docker compose restart moodle
docker compose ps
```

Restart MariaDB only with a documented reason and after verifying that a current backup exists.

## Backup

```bash
chmod +x scripts/*.sh
./scripts/backup.sh
```

The local script is only the first stage. Copy backups to encrypted off-site storage with restricted access and retention appropriate to the business.

## Restore test

Never test restoration against production. Create an isolated host or project, load sanitized configuration, and run:

```bash
./scripts/restore.sh ./backups/YYYYMMDDTHHMMSSZ
./scripts/health-check.sh
```

Record recovery time, validation results, and any manual steps. A backup is not proven until it has been restored successfully.

## Update workflow

1. Read release notes and security advisories.
2. Create and verify a backup.
3. Test the change outside production.
4. Pin the desired versions.
5. Build and validate the images.
6. Schedule and communicate the maintenance.
7. Deploy, verify, and retain a rollback path.
