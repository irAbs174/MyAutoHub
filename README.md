# MyAutoHub Application (`app.domain.com`)

Django + Django REST Framework app for the MyAutoHub product surface. The marketing landing site lives in `../landing/` (`domain.com`).

## Stack

- Django / DRF / Django templates
- PostgreSQL
- Docker Compose (`web` + `db`)

Redis is not used in this phase.

## Quick start (Docker)

```bash
cd application
cp .env.example .env
docker compose up --build
```

Open http://localhost:8000

Create a superuser:

```bash
docker compose exec web python manage.py createsuperuser
```

## Local start (without Docker DB)

```bash
cd application
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# edit .env:
#   USE_SQLITE=true
python manage.py migrate
python manage.py runserver
```

## Apps

| Path | App |
|------|-----|
| `/` | Hub dashboard |
| `/accounts/` | Auth, profile, saved locations |
| `/emergency/` | Emergency services (HTML) |
| `/api/emergency/` | Emergency API |
| `/pricing/` | Pricing reference |
| `/marketplace/` | Buy & sell |
| `/cars/` | Car catalog |
| `/youtube/` | YouTube contents |
| `/stories/` | Stories |
| `/admin/` | Django admin |

## Emergency operators

A Django auth group named `emergency_operators` is created by migration.

- Operators can accept requests (`wait_for_accept` → `processing_request`)
- Operator admins (`is_staff` + group) can finish (`finish_success` / `finish_failed`)
- Requesters can cancel, buzz, and leave a public review after finish

## Hosting `app.domain.com`

Point DNS for `app.domain.com` at this service. Set in `.env`:

```
DJANGO_ALLOWED_HOSTS=app.domain.com
DJANGO_CSRF_TRUSTED_ORIGINS=https://app.domain.com
DJANGO_ENV=production
DJANGO_DEBUG=false
```

`DJANGO_ENV=production` loads production settings (`DEBUG=False`) so branded
`400`/`403`/`404`/`500` pages are shown instead of Django’s default debug pages.
Run with Compose (gunicorn when `DJANGO_ENV=production`).
