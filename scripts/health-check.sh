#!/usr/bin/env bash
set -Eeuo pipefail

MOODLE_URL="${MOODLE_URL:-http://127.0.0.1:${MOODLE_HOST_PORT:-8080}}"

docker compose ps
docker compose exec -T mariadb healthcheck.sh --connect --innodb_initialized
curl --fail --silent --show-error --head "$MOODLE_URL" >/dev/null

echo "MundoActivate health check passed."
