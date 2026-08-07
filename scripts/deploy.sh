#!/usr/bin/env bash
# Pull latest main and rebuild Docker services on the production host.
set -euo pipefail

APP_DIR="${APP_DIR:-/var/www/myautohub/application}"
BRANCH="${DEPLOY_BRANCH:-main}"

cd "$APP_DIR"

echo "==> Deploying $(basename "$APP_DIR") from origin/${BRANCH}"

if [[ ! -d .git ]]; then
  echo "ERROR: ${APP_DIR} is not a git repository" >&2
  exit 1
fi

if [[ ! -f .env ]]; then
  echo "ERROR: missing .env in ${APP_DIR}" >&2
  exit 1
fi

git fetch --prune origin "${BRANCH}"
git reset --hard "origin/${BRANCH}"

echo "==> Rebuilding containers"
docker compose up -d --build --remove-orphans

echo "==> Waiting for web container"
for _ in $(seq 1 30); do
  if docker compose exec -T web python -c "import socket; s=socket.socket(); s.settimeout(1); s.connect(('127.0.0.1', 8000)); s.close()" 2>/dev/null; then
    break
  fi
  sleep 2
done

echo "==> Pruning dangling images"
docker image prune -f >/dev/null

echo "==> Status"
docker compose ps
echo "==> Deploy complete: $(git rev-parse --short HEAD)"
