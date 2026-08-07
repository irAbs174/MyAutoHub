#!/bin/sh
set -e

echo "Waiting for database..."
python <<'PY'
import os
import time

import dj_database_url
import psycopg2

url = os.environ.get("DATABASE_URL")
if url:
    cfg = dj_database_url.parse(url)
    for attempt in range(30):
        try:
            conn = psycopg2.connect(
                dbname=cfg["NAME"],
                user=cfg["USER"],
                password=cfg["PASSWORD"],
                host=cfg.get("HOST") or "localhost",
                port=cfg.get("PORT") or 5432,
            )
            conn.close()
            break
        except Exception as exc:  # noqa: BLE001
            print(f"DB not ready ({attempt + 1}/30): {exc}")
            time.sleep(1)
    else:
        raise SystemExit("Database never became ready")
PY

python manage.py migrate --noinput
python manage.py collectstatic --noinput

if [ "${DJANGO_ENV}" = "production" ]; then
  exec gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 3
else
  exec python manage.py runserver 0.0.0.0:8000
fi
