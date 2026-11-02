# NDTT — National Driving Theory Test

A Django web application for booking and taking the Nigerian driving theory test. It includes a public booking flow, a candidate exam portal, a staff dashboard, a REST API for bookings, and synchronization tooling for exam centers.

## Stack

| Component | Version / Detail |
| --- | --- |
| Python | 3.9 (the `.venv` in this repo uses 3.9.13) |
| Django | 1.11.17 (pinned, end-of-life) |
| Django REST Framework | 3.9.4 |
| Database | MySQL / MariaDB via `PyMySQL` (MySQLdb shim) |
| PDF generation | `xhtml2pdf`, `reportlab`, `pypdf` |
| Config | `python-dotenv` (`.env` at project root) |
| Server | Django dev server locally, Gunicorn in production |

> **Do not upgrade Django or Python independently.** The code uses `django.conf.urls.url` and `SessionAuthenticationMiddleware`, both removed in Django 2.0. Python 3.10+ also breaks Django 1.11. Keep Python on 3.9 until the project is migrated.

## Applications

| App | Responsibility |
| --- | --- |
| `welcome` | Public landing page |
| `custom` | Staff dashboard, bookings, scratch cards, payments, candidate exam flow, result PDFs and verification |
| `exam` | Exams, exam questions, participants, and marks |
| `question_bank` | Questions, options, media, categories, and translated content |
| `api` | REST API for bookings and reference data (`ExamCenterViewSet`, `ExamCategoryViewSet`, booking endpoint) |
| `sync` | Syncs bookings and results between local center and a remote server |

## Requirements

- Python 3.9
- MySQL or MariaDB running locally (on Windows, XAMPP's MySQL is what this setup uses)
- Database credentials with permission to create/alter the `ndtt` database

## Quick start (Windows, current machine)

From the project root (`C:\Users\talk2\OneDrive\Desktop\project\ndtt`):

```powershell
# 1. Make sure MySQL is running (XAMPP Control Panel -> MySQL -> Start)

# 2. Create the local config if it does not exist
Copy-Item .env.example .env

# 3. Install dependencies (the bundled .venv already has them)
.\.venv\Scripts\python.exe -m pip install -r requirements.txt

# 4. Apply database migrations
.\.venv\Scripts\python.exe manage.py migrate

# 5. Start the development server
.\.venv\Scripts\python.exe manage.py runserver 127.0.0.1:8000
```

Or activate the virtualenv first and use plain `python`:

```powershell
.\.venv\Scripts\Activate.ps1
python manage.py runserver 127.0.0.1:8000
```

Open <http://127.0.0.1:8000/>.

Use `127.0.0.1:8000` explicitly: the landing template only shows the sync links when `request.get_host == '127.0.0.1:8000'`.

## Environment variables

Configuration is loaded from `.env` in the project root (see `.env.example`).

| Variable | Default | Notes |
| --- | --- | --- |
| `APP_ENV` | `DEVELOPMENT` | Set to `PRODUCTION` for the production static/media paths |
| `DEBUG` | `True` | Must be `False` in production |
| `SECRET_KEY` | built-in fallback | Set a unique value in every real environment |
| `ALLOWED_HOSTS` | `*` | Comma-separated hostnames in production |
| `DATABASE_BACKEND` | `django.db.backends.mysql` | MySQL only; the SQLite fallback in `settings.py` is commented out |
| `DATABASE_NAME` | `ndtt` | |
| `DATABASE_USER` | `root` | |
| `DATABASE_PASS` | empty | |
| `DATABASE_HOST` | `127.0.0.1` | |
| `DATABASE_PORT` | `3306` | |
| `PIE_SECRET_KEY` | empty | Required for online payment verification against `pie.ng` |

`REMOTE_URL` (the sync server, currently `https://test.ndtt.ng/synchro/`) is hardcoded in `ndtt/settings.py`.

## Database setup

The project has no SQLite fallback — it always connects to MySQL. On a fresh machine:

```sql
CREATE DATABASE ndtt CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

Then update `.env` and run:

```powershell
.\.venv\Scripts\python.exe manage.py migrate
```

Migrations live in `custom`, `exam`, `question_bank`, and `sync`. `api` and `welcome` have no models of their own.

## Key URLs

| URL | Purpose |
| --- | --- |
| `/` | Public landing page |
| `/admin/` | Django admin |
| `/myadmin/` | Staff dashboard entry (login required) |
| `/ap/login/` | Staff login |
| `/ap/select/category/` | Start a booking |
| `/ap/booking_verification` | Verify a scratch card / pay online |
| `/ap/candidate_verification?type=exam` | Candidate check-in (also `type=practice`) |
| `/ap/photo_capture` | Candidate photo capture step |
| `/ap/driving_test` | Candidate exam screen |
| `/ap/candidate_result` | Candidate result page |
| `/ap/result/pdf/` | Result PDF |
| `/ap/verify_result` | Public QR result verification |
| `/api/booking/` | POST a booking (DRF) |
| `/api/exam_venues/`, `/api/exam_categories/` | Reference data |
| `/api/states/`, `/api/gender/`, `/api/languages/`, `/api/drive-test-type/` | Lookup lists |
| `/api/docs/` | DRF API documentation |
| `/synchro/confirm/center/` | Sync center UI and endpoints (no route at `/synchro/` itself) |

## Staff access

Staff users must be both active and members of staff (`is_staff`); dashboard views are guarded by `@login_required` and `@staff_member_required`.

```powershell
.\.venv\Scripts\python.exe manage.py createsuperuser
```

## Project layout

```
.
├── manage.py
├── config.py                 # App name/description used by the context processor
├── gunicorn.conf.py          # Production server config
├── ndtt/                     # Settings, root URLs, WSGI, context processors
├── custom/                   # Dashboard, bookings, payments, candidate flow
├── exam/                     # Exam and participant models
├── question_bank/            # Questions, options, translations
├── api/                      # DRF serializers, views, routers
├── sync/                     # Center-to-center sync
├── welcome/                  # Landing page
├── static/                   # App static assets
├── media/                    # Uploaded photos, question media, translated files
├── logs/                     # Gunicorn access/error logs
├── requirements.txt
└── .env.example
```

Templates for the dashboard and candidate flows are under `custom/templates/` (`core/` and `custom/`); the landing page is `welcome/templates/welcome/index.html`.

## Production deployment

The server target is Linux with Gunicorn behind a reverse proxy.

```bash
cd /www/wwwroot/ogun.ndtt.ng
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt gunicorn
cp .env.example .env    # then fill in production values
mkdir -p logs
python manage.py migrate
python manage.py collectstatic --noinput
gunicorn ndtt.wsgi:application -c gunicorn.conf.py
```

Production `.env` values at minimum:

```dotenv
APP_ENV=PRODUCTION
DEBUG=False
SECRET_KEY=<unique-secret>
ALLOWED_HOSTS=ogun.ndtt.ng
DATABASE_BACKEND=django.db.backends.mysql
DATABASE_NAME=ndtt
DATABASE_USER=<prod-user>
DATABASE_PASS=<prod-password>
DATABASE_HOST=localhost
DATABASE_PORT=3306
PIE_SECRET_KEY=<real-payment-key>
```

`gunicorn.conf.py` binds to `127.0.0.1:8088` by default (override with `GUNICORN_BIND`), uses `cpu_count * 2 + 1` sync workers, 2 threads, and writes to `logs/access.log` / `logs/error.log`.

Sample systemd unit (the `redme.txt` notes reference `deploy/ndtt.service`, but no `deploy/` directory exists in this repo):

```ini
[Unit]
Description=NDTT Django application
After=network.target mysql.service

[Service]
User=www-data
Group=www-data
WorkingDirectory=/www/wwwroot/ogun.ndtt.ng
Environment="PATH=/www/wwwroot/ogun.ndtt.ng/venv/bin"
ExecStart=/www/wwwroot/ogun.ndtt.ng/venv/bin/gunicorn ndtt.wsgi:application -c gunicorn.conf.py
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
sudo cp ndtt.service /etc/systemd/system/ndtt.service
sudo systemctl daemon-reload
sudo systemctl enable --now ndtt
sudo systemctl status ndtt
```

In `APP_ENV=PRODUCTION`, Django serves `/static/` and `/media/` itself through `django.views.static.serve` with `show_indexes=True`. Prefer letting Nginx/Apache serve those directories instead, especially for `media/`.

## Operational notes

- **Django 1.11 is unsupported** and has known security issues. Keep the app off the public internet or budget time for an upgrade.
- `ndtt/urls.py` registers `url(r'^$', include('welcome.urls'))`, which produces `urls.W001`. It works for the single welcome route, but should become `r'^'` if more routes are added.
- Online bookings call `https://pie.ng/transaction/verify/<ref>` in `custom/utils.py`; without a valid `PIE_SECRET_KEY` those payments will fail verification.
- The `welcome` page switches between sync links and candidate links based on the request host (see above).
- `media/` contains committed uploads and is large; consider moving uploads to object storage or outside version control.
- The `pkg_resources is deprecated` warning printed by every management command comes from `coreapi` and is harmless.
- The `tests.py` files are Django stubs; there is no real test suite.
- No license file is included in this repository.

## Troubleshooting

| Symptom | Fix |
| --- | --- |
| `Can't connect to MySQL server` | Start MySQL (XAMPP Control Panel on Windows) and confirm `DATABASE_HOST`/`DATABASE_PORT` in `.env` |
| `Access denied for user` | Correct `DATABASE_USER` / `DATABASE_PASS` in `.env` |
| `Table 'ndtt.xxx' doesn't exist` | Run `python manage.py migrate` |
| `ModuleNotFoundError: No module named 'pymysql'` | Use the project virtualenv (`ndtt/__init__.py` calls `pymysql.install_as_MySQLdb()`) |
| Static files 404 in production | Run `collectstatic` and configure the web server for `/static/` and `/media/` |
| `ModuleNotFoundError: No module named 'collections'` aliases / middleware import errors | You are on Python 3.10+ or Django 2+; switch back to the Python 3.9 virtualenv |
#   n d t t  
 #   n d t t  
 