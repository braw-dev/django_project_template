# Production Architecture & Deployment

This template provides a production-oriented starting point, not a finished platform. It includes application settings, container files, and runtime integrations, but you still need to choose and document your own hosting, reverse proxy, backups, and operational processes for each generated product.

## What is scaffolded today

- Django application configuration via `.env` and `.env.local` using [`pydantic-settings`](https://docs.pydantic.dev/latest/concepts/pydantic_settings/)
- `docker/Dockerfile.dev` and `docker/Dockerfile.prod`
- `compose.dev.yaml` and `compose.yaml` as starting points
- Gunicorn app runtime in the production Dockerfile
- Optional Celery worker support
- PostgreSQL/PostGIS via `DB_DEFAULT_URL`
- Redis-compatible cache/broker via `CACHE_DEFAULT_URL` and `CELERY_BROKER_URL`
- WhiteNoise static file serving
- Optional S3-compatible media storage via `django-storages`
- Structured logging via `django-structlog`
- Optional error reporting via `SENTRY_DSN`

## What is not scaffolded yet

- no Ansible or Podman deployment automation
- no complete reverse-proxy config in this repo
- no built-in search service such as Meilisearch
- no backup system configuration
- no metrics/tracing/dashboard stack
- no container registry or CI/CD pipeline
- no finished legal/trust or subprocessor documentation set

Treat the Compose files as examples, not as a one-command production deployment.

## App configuration

[`pydantic-settings`](https://docs.pydantic.dev/latest/concepts/pydantic_settings/) is used to manage configuration in `settings.py`. Copy `.env.dist` to `.env` and update the values as needed. If local overrides are required, put them into `.env.local`. Required settings fail fast during Django startup if they are missing or blank.

## Runtime components

### Web application

`{{ project_name }}` is a Django application served by Gunicorn in the production Dockerfile.

### Database

The template parses `DB_DEFAULT_URL` and supports:

- PostgreSQL / PostGIS
- SQLite
- MySQL

The default `.env.dist` uses PostGIS. Test runs switch to in-memory SQLite automatically.

#### Migrations

The template includes standard Django migrations. It does **not** scaffold CI/CD migration orchestration. If you adopt zero-downtime migration rules for a product, document and enforce them in that product's delivery process.

### Cache and async work

Caching uses Django's cache framework with a Redis-compatible backend when `CACHE_DEFAULT_URL` points at Redis/Dragonfly. Celery is configured to use `CELERY_BROKER_URL` and stores task results in the database via `django-celery-results`.

The included production Compose file uses Dragonfly as the cache service, but the Django settings only require a Redis-compatible URL.

### Static and media files

- Static files are served by WhiteNoise.
- User-uploaded media defaults to local filesystem storage.
- In production you can switch media storage to an S3-compatible backend via the existing `AWS_*` settings.

### Logging and error reporting

The template currently supports:

- console logging
- rotating JSON log files under `logs/`
- optional Sentry error reporting via `SENTRY_DSN`

It does **not** currently scaffold metrics, tracing, Grafana, or New Relic.

## Security-related deployment notes

### Authentication

[`django-allauth`](https://docs.allauth.org/en/latest/introduction/index.html) is configured for local accounts with:

- email as the login identifier
- mandatory email verification
- MFA via TOTP or passkeys

`ACCOUNT_LOGIN_BY_CODE_ENABLED` is currently `False`, so login-by-code is not enabled by default.

### Authorization

Team-scoped authorization is handled by the template's own tenancy and permission helpers built on top of `rules`. `django-guardian` is not part of the current implementation.

### Password hashing

Passwords are hashed with Argon2id by default.

### Subresource Integrity

[SRI](https://developer.mozilla.org/en-US/docs/Web/Security/Subresource_Integrity) SHA-512 hashes are added to static JS and CSS resources via [`django-sri`](https://github.com/RealOrangeOne/django-sri).

## Security contact

The template does not provision a real disclosure process or mailbox. Replace any placeholder security contact details in a generated product with your own support/security contact information and incident process.
