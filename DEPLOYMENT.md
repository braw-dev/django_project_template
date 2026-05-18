# Production Architecture & Deployment

This template provides a production-oriented starting point, not a finished platform. It includes application settings, container files, and runtime integrations, but you still need to choose and document your own hosting, reverse proxy, backups, and operational processes for each generated product.

## Opinionated default deployment path

If you want one boring sovereignty-friendly default for a generated project, prefer this stack:

- **Application host**: a Hetzner VPS in the EU
- **App runtime**: rootless Podman containers managed by per-project `systemd --user` units
- **Edge proxy + TLS**: one root-managed Caddy on the VPS, configured outside this repo
- **CDN**: Bunny.net in front of Caddy for static/media and edge caching
- **Database**: PostgreSQL managed somewhere you trust in-region; provider intentionally undecided here
- **Cache / broker**: Dragonfly on the same VPS or on a small sister instance in the same private network

This is the default direction the docs assume. It is intentionally optimized for running many small B2B SaaS products cheaply on a small number of machines.

### Why this default

This path keeps the moving parts boring and cheap:

- Podman keeps the runtime close to container workflows you already know from Docker/Compose
- rootless containers reduce blast radius compared with running every app as root
- `systemd` gives simple restart policy, startup ordering, logs, and boot persistence without introducing Kubernetes yet
- separate Unix users per project give a clean boundary between apps on the same VPS
- Caddy centralizes certificates and reverse proxying once, instead of per-project TLS config
- Bunny.net gives a simple CDN layer without changing the Django app architecture

It also leaves a future path open to k3s later because you are still building and shipping container images, not bespoke VM-only processes

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
- no generated `systemd` unit files for Podman services
- no complete reverse-proxy config in this repo
- no built-in search service such as Meilisearch
- no backup system configuration
- no metrics/tracing/dashboard stack
- no container registry or CI/CD pipeline
- no finished legal/trust or subprocessor documentation set
- no opinionated managed PostgreSQL provider choice yet

Treat the Compose files as examples, not as a one-command production deployment.

## Host layout for many apps on one VPS

If you are running several small products on one Hetzner VPS, prefer a layout like this:

- one Unix user per product, for example `app_acme`, `app_widget`, `app_docs`
- each app user owns only that project's checkout, env files, volumes, and rootless Podman services
- root owns the shared reverse proxy, firewall, SSH, and system-level hardening
- root Caddy proxies public traffic to high localhost ports or private container ports for each app
- Dragonfly may be shared, but document database numbers, credentials, and failure domains clearly if you do that

This template does **not** generate the Unix users or host-level config for you. The point here is to recommend a repeatable shape, not pretend the repo already automates it.

### Suggested responsibility split

#### Root-managed, outside this repo

- Caddy config
- TLS certificates
- firewall rules
- SSH hardening
- Fail2ban or equivalent host protections
- host monitoring and backups

#### Per-project, inside each generated repo

- app container image build
- Django config and env files
- static collection
- migration process
- app-specific Podman service definition and deployment commands

## App configuration

[`pydantic-settings`](https://docs.pydantic.dev/latest/concepts/pydantic_settings/) is used to manage configuration in `settings.py`. Copy `.env.dist` to `.env` and update the values as needed. If local overrides are required, put them into `.env.local`. Required settings fail fast during Django startup if they are missing or blank.

## Runtime components

### Web application

`{{ project_name }}` is a Django application served by Gunicorn in the production Dockerfile.

For the default Hetzner path, treat that production image as the thing your rootless Podman service runs under `systemd --user`.

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

For the default deployment path, prefer either:

- Dragonfly on the same VPS for the cheapest setup, or
- Dragonfly on a small sister instance in the same private network if you want cleaner isolation or independent scaling

If multiple apps share one Dragonfly instance, treat that as an explicit operational choice and document the blast radius.

### Static and media files

- Static files are served by WhiteNoise.
- User-uploaded media defaults to local filesystem storage.
- In production you can switch media storage to an S3-compatible backend via the existing `AWS_*` settings.

For the default Hetzner + Bunny.net path:

- keep WhiteNoise as the application origin for static files unless you have a reason to move away from it
- let Bunny.net cache public static assets at the edge
- decide explicitly whether media should stay on local disk, move to object storage, or be fronted by Bunny Storage/CDN in a generated project

### Logging, errors, and performance signals

The template currently supports:

- console logging
- rotating JSON log files under `logs/`
- optional Sentry error reporting via `SENTRY_DSN`
- one structured request-performance log event per request, including:
  - request duration
  - DB query count
  - total DB time
  - slow-request / slow-DB flags

This is the supported observability path for generated projects:

- **exceptions**: Sentry
- **application-level observability**: structured JSON logs from Django
- **host metrics and log shipping**: Grafana Alloy on the VPS
- **querying and dashboards**: Grafana Cloud

The template does **not** currently scaffold distributed tracing or require OpenTelemetry.

If you want more, add it in a generated project deliberately. The default here is to start with logs, health checks, and exceptions, then derive the dashboards that actually matter.

### Suggested first dashboards

If you ship the JSON logs to Grafana Cloud via Alloy, the first useful dashboards are usually:

- request count by path or view name
- request latency percentiles
- slow request count over time
- DB time contribution per request
- 4xx / 5xx rates
- exception count from Sentry
- uptime from the health check endpoint and host metrics

That is enough to spot availability issues, performance regressions, and the slow endpoints worth improving.

## Reverse proxy and edge

This repo does not include the final reverse-proxy config. For the default path, assume:

- Caddy terminates TLS and proxies requests to the app containers
- Caddy is managed once at the host level, outside any single product repo
- Bunny.net sits in front of Caddy where CDN or edge caching is useful
- app containers do not bind directly to the public internet unless you have a specific reason

That split keeps product repos focused on application concerns while the host handles ingress and certificates centrally.

### Proxy header contract

Generated projects trust proxy headers only when the connecting peer is listed in `TRUSTED_PROXY_IPS`.

For the default Caddy-on-the-same-host shape, keep the app private and set `TRUSTED_PROXY_IPS` to the address or CIDR that Caddy uses when proxying to Django. Examples:

- `TRUSTED_PROXY_IPS=127.0.0.1`
- `TRUSTED_PROXY_IPS=10.0.0.0/8`
- `TRUSTED_PROXY_IPS=127.0.0.1,10.0.0.0/8`

Leave it empty if Django is not behind a trusted reverse proxy yet. In that state, forwarded headers are ignored and `SECURE_PROXY_SSL_HEADER` is not enabled.

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

## Practical rollout order for a new generated project

If you are deploying a new product with this default path, the boring order is:

1. provision a Hetzner VPS in your target EU region
2. harden the host and install root-managed Caddy
3. create a dedicated Unix user for the product
4. install rootless Podman for that user
5. build and run the app container under a user `systemd` unit
6. point Caddy at the app service
7. optionally place Bunny.net in front once the origin is stable
8. wire PostgreSQL and Dragonfly over private networking where possible
9. configure Alloy to collect host metrics and ship app logs
10. create a first Grafana dashboard for request latency, error rate, and slow requests
11. document backups, restore steps, and where customer data actually lives

## Security contact

The template does not provision a real disclosure process or mailbox. Replace any placeholder security contact details in a generated product with your own support/security contact information and incident process.
