#!/usr/bin/env bash
set -Eeuo pipefail

if [[ ! -f .env ]]; then
  echo "Missing .env file." >&2
  exit 1
fi

set -a
# shellcheck disable=SC1091
source .env
set +a

BACKUP_DIR="${BACKUP_DIR:-./backups}"
BACKUP_RETENTION_DAYS="${BACKUP_RETENTION_DAYS:-14}"
TIMESTAMP="$(date -u +%Y%m%dT%H%M%SZ)"
TARGET="$BACKUP_DIR/$TIMESTAMP"

mkdir -p "$TARGET"
umask 077

docker compose exec -T -e MARIADB_PWD="$MARIADB_ROOT_PASSWORD" mariadb mariadb-dump \
  --user=root \
  --single-transaction \
  --routines \
  --triggers \
  "$MOODLE_DB_NAME" | gzip -9 > "$TARGET/moodle-db.sql.gz"

docker compose exec -T moodle \
  tar -czf - -C /var/www/moodledata . > "$TARGET/moodle-data.tar.gz"

sha256sum "$TARGET"/* > "$TARGET/SHA256SUMS"
find "$BACKUP_DIR" -mindepth 1 -maxdepth 1 -type d -mtime "+$BACKUP_RETENTION_DAYS" -print \
  > "$TARGET/RETENTION_REVIEW.txt"

echo "Backup created in $TARGET"
echo "Copy it to encrypted off-site storage and test restoration regularly."
