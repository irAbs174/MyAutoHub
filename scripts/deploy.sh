#!/usr/bin/env bash
# Unpack a release archive into the live app directory and rebuild containers.
# Expected env:
#   APP_DIR          - live app path (default /var/www/myautohub/application)
#   RELEASE_ARCHIVE  - path to myautohub-release.tar.gz
#   DEPLOY_SHA       - optional commit sha for logging
set -euo pipefail

APP_DIR="${APP_DIR:-/var/www/myautohub/application}"
RELEASE_ARCHIVE="${RELEASE_ARCHIVE:-/tmp/myautohub-release.tar.gz}"
DEPLOY_SHA="${DEPLOY_SHA:-unknown}"

if [[ ! -f "${RELEASE_ARCHIVE}" ]]; then
  echo "ERROR: release archive not found: ${RELEASE_ARCHIVE}" >&2
  exit 1
fi

if [[ ! -f "${APP_DIR}/.env" ]]; then
  echo "ERROR: missing production .env at ${APP_DIR}/.env" >&2
  exit 1
fi

echo "==> Deploying ${DEPLOY_SHA} into ${APP_DIR}"

# Keep runtime data outside the extract so tar does not wipe it
TMP_ENV="$(mktemp)"
cp "${APP_DIR}/.env" "${TMP_ENV}"
mkdir -p "${APP_DIR}/uploads" "${APP_DIR}/media" "${APP_DIR}/staticfiles"

# Extract over the live tree (does not remove untracked runtime dirs)
tar -xzf "${RELEASE_ARCHIVE}" -C "${APP_DIR}"

# Restore production env (never deploy .env from CI)
cp "${TMP_ENV}" "${APP_DIR}/.env"
rm -f "${TMP_ENV}"

chmod +x "${APP_DIR}/entrypoint.sh" "${APP_DIR}/scripts/deploy.sh"

cd "${APP_DIR}"

echo "==> Rebuilding containers"
docker compose up -d --build --remove-orphans

echo "==> Waiting for web"
ok=0
for _ in $(seq 1 40); do
  code="$(curl -s -o /dev/null -w '%{http_code}' http://127.0.0.1:8000/ || true)"
  if [[ "${code}" =~ ^(200|301|302|303|307|308)$ ]]; then
    ok=1
    break
  fi
  sleep 3
done

if [[ "${ok}" -ne 1 ]]; then
  echo "ERROR: web did not become healthy (last HTTP ${code:-none})" >&2
  docker compose ps >&2 || true
  docker compose logs --tail=80 web >&2 || true
  exit 1
fi

echo "==> Pruning dangling images"
docker image prune -f >/dev/null
rm -f "${RELEASE_ARCHIVE}"

echo "==> Status"
docker compose ps
echo "==> Deploy complete: ${DEPLOY_SHA}"
