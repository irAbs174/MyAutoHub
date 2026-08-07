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

# Production must use PostgreSQL (Compose `db` service), never SQLite.
ensure_postgres_env() {
  local env_file="${APP_DIR}/.env"
  local tmp key val
  local postgres_db=myautohub postgres_user=myautohub postgres_password=myautohub
  local has_use_sqlite=0 has_django_env=0 has_database_url=0 has_postgres_host=0

  while IFS= read -r line || [[ -n "${line}" ]]; do
    case "${line}" in
      POSTGRES_DB=*) postgres_db="${line#POSTGRES_DB=}" ;;
      POSTGRES_USER=*) postgres_user="${line#POSTGRES_USER=}" ;;
      POSTGRES_PASSWORD=*) postgres_password="${line#POSTGRES_PASSWORD=}" ;;
    esac
  done < "${env_file}"

  tmp="$(mktemp)"
  while IFS= read -r line || [[ -n "${line}" ]]; do
    case "${line}" in
      USE_SQLITE=*)
        printf '%s\n' "USE_SQLITE=false"
        has_use_sqlite=1
        ;;
      DJANGO_ENV=*)
        printf '%s\n' "DJANGO_ENV=production"
        has_django_env=1
        ;;
      POSTGRES_HOST=*)
        printf '%s\n' "POSTGRES_HOST=db"
        has_postgres_host=1
        ;;
      DATABASE_URL=*)
        printf 'DATABASE_URL=postgres://%s:%s@db:5432/%s\n' \
          "${postgres_user}" "${postgres_password}" "${postgres_db}"
        has_database_url=1
        ;;
      *)
        printf '%s\n' "${line}"
        ;;
    esac
  done < "${env_file}" > "${tmp}"

  if [[ "${has_use_sqlite}" -eq 0 ]]; then
    printf '%s\n' "USE_SQLITE=false" >> "${tmp}"
  fi
  if [[ "${has_django_env}" -eq 0 ]]; then
    printf '%s\n' "DJANGO_ENV=production" >> "${tmp}"
  fi
  if [[ "${has_postgres_host}" -eq 0 ]]; then
    printf '%s\n' "POSTGRES_HOST=db" >> "${tmp}"
  fi
  if [[ "${has_database_url}" -eq 0 ]]; then
    printf 'DATABASE_URL=postgres://%s:%s@db:5432/%s\n' \
      "${postgres_user}" "${postgres_password}" "${postgres_db}" >> "${tmp}"
  fi

  mv "${tmp}" "${env_file}"
  export POSTGRES_DB="${postgres_db}"
  export POSTGRES_USER="${postgres_user}"
  export POSTGRES_PASSWORD="${postgres_password}"
  echo "==> Ensured PostgreSQL settings in .env (USE_SQLITE=false, POSTGRES_HOST=db)"
}

ensure_postgres_env

echo "==> Rebuilding containers (web + postgres)"
docker compose up -d --build --remove-orphans

echo "==> Waiting for postgres"
db_ok=0
for _ in $(seq 1 40); do
  if docker compose exec -T db pg_isready -U "${POSTGRES_USER:-myautohub}" -d "${POSTGRES_DB:-myautohub}" >/dev/null 2>&1; then
    db_ok=1
    break
  fi
  sleep 2
done
if [[ "${db_ok}" -ne 1 ]]; then
  echo "ERROR: postgres did not become ready" >&2
  docker compose ps >&2 || true
  docker compose logs --tail=80 db >&2 || true
  exit 1
fi

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

# Seed catalog + demo data (idempotent). Skip with RUN_SEEDERS=false in .env.
RUN_SEEDERS="$(grep -E '^RUN_SEEDERS=' "${APP_DIR}/.env" 2>/dev/null | cut -d= -f2- || true)"
RUN_SEEDERS="${RUN_SEEDERS:-true}"
if [[ "${RUN_SEEDERS}" =~ ^(1|true|yes|TRUE|YES)$ ]]; then
  echo "==> Running seeders on PostgreSQL"
  docker compose exec -T web python manage.py seed_brands
  docker compose exec -T web python manage.py seed_demo
else
  echo "==> Skipping seeders (RUN_SEEDERS=${RUN_SEEDERS})"
fi

echo "==> Pruning dangling images"
docker image prune -f >/dev/null
rm -f "${RELEASE_ARCHIVE}"

echo "==> Status"
docker compose ps
echo "==> Deploy complete: ${DEPLOY_SHA}"
