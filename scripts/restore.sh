#!/usr/bin/env bash
set -Eeuo pipefail

if [[ $# -ne 1 ]]; then
  echo "Usage: $0 BACKUP_DIRECTORY" >&2
  exit 1
fi

if [[ ! -f .env ]]; then
  echo "Missing .env file." >&2
  exit 1
fi

BACKUP_PATH="$(realpath "$1")"
test -f "$BACKUP_PATH/moodle-db.sql.gz"
test -f "$BACKUP_PATH/moodle-data.tar.gz"

set -a
# shellcheck disable=SC1091
source .env
set +a

echo "WARNING: this operation replaces data in the target environment."
read -r -p "Type RESTORE to continue: " CONFIRMATION
[[ "$CONFIRMATION" == "RESTORE" ]] || exit 1

docker compose up -d mariadb
until docker compose exec -T mariadb healthcheck.sh --connect --innodb_initialized; do sleep 5; done

gzip -dc "$BACKUP_PATH/moodle-db.sql.gz" | docker compose exec -T \
  -e MARIADB_PWD="$MARIADB_ROOT_PASSWORD" mariadb mariadb \
  --user=root \
  "$MOODLE_DB_NAME"

docker compose up -d moodle
docker compose exec -T moodle sh -c 'find /var/www/moodledata -mindepth 1 -delete'
docker compose exec -T moodle tar -xzf - -C /var/www/moodledata \
  < "$BACKUP_PATH/moodle-data.tar.gz"

docker compose up -d
echo "Restore completed. Run scripts/health-check.sh and application tests."
