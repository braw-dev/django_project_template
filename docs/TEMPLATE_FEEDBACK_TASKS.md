# Template feedback tasks

Aim: Make this a stronger foundation for a solo, EU-focused B2B micro-SaaS business.

Principles:

- keep the stack boring
- prefer Django built-ins
- security before convenience
- minimal, repeatable changes that pay rent across many products
- EU-first where it affects privacy, billing, localisation, and deployment

Perspectives - take these into account as key stakeholders:

1. As a solopreneur/company-of-one using the template to build B2B micro-SaaS products as part of a SaaS factory;
2. A technical expert performing a Technical Due Diligence for a VC/investor or potential acquirer;
3. A customer of one of the micro-SaaS products built with this template focused on data privacy, security, performance, end-user experience and customer satisfaction.

## Overall assessment

The template is already in unusually good shape for a one-person SaaS factory: team-first multi-tenancy with explicit permission checks, audit events for security-sensitive mutations, allauth + MFA + axes, structlog with a request-performance middleware, seeded trust pages (`terms`, `subprocessors`), a privacy module for GDPR export/erasure, a webhook-deduplicating billing app, an i18n-ready URL layout, and a single CI workflow that generates a fresh project and runs lint/format/type/pytest/Playwright/Docker build. That foundation is sound.

The gaps below are the deltas that, in my view, would meaningfully raise the EU B2B-readiness and TDD-pass-rate of every product spun out of this template. I have **not** invented priorities to fill buckets - if a bucket has no entry, that is intentional.

## P0 — fix first

None

## P1 — important for EU B2B readiness

None

## P2 — important for product quality and repeatability

- **Backup, restore, and a _tested_ restore drill using borg + borgmatic + Hetzner Storage Box.** `DEPLOYMENT.md` honestly says backups are not scaffolded. For a portfolio of unattended SaaS products, scaffold encrypted, deduplicated, append-only backups using `borg` driven by `borgmatic`, with a Hetzner Storage Box as the off-site repository (SSH/SFTP target, cheap, EU-located). Concretely:
  - Ship a `borgmatic.yaml` (or `config.yaml` under `/etc/borgmatic.d/`) template in the generated project with: repository pointing at `ssh://<user>@<box>.your-storagebox.de:23/./repo`, `repokey-blake2` encryption, sensible `keep_daily`/`keep_weekly`/`keep_monthly` retention, a `before_backup` hook that runs `pg_dump --format=custom` to a staging path (or uses borgmatic's built-in `postgresql_databases:` hook), and `checks: [repository, archives]` running on a weekly cadence.
  - Add a `just db-backup` recipe that invokes `borgmatic create --verbosity 1 --stats` and a `just db-backup-check` recipe that runs `borgmatic check`.
  - Add a `just db-restore-drill` recipe that: pulls the latest archive into a throwaway directory via `borgmatic extract --archive latest`, restores the `pg_dump` into a disposable Postgres container, runs `manage.py migrate --check` and a smoke query, then tears the container down. The recipe must exit non-zero on any step failure so it can be wired to a cron/systemd timer and Sentry cron monitor.
  - Provide a systemd `borgmatic.service` + `borgmatic.timer` unit pair (daily) and a separate `borgmatic-restore-drill.timer` (weekly) under `deploy/systemd/`.
  - Store the borg passphrase and Storage Box SSH key path in env vars (`BORG_PASSPHRASE`, `BORG_RSH`) loaded from the existing secrets mechanism; never in the repo.
  - Document in `docs/backups.md`: how to provision a Hetzner Storage Box, how to initialise the repo (`borgmatic init --encryption repokey-blake2`), retention policy, passphrase rotation, the weekly restore-drill cadence, and how to recover end-to-end from a total host loss. Data loss is the only failure mode `MOTIVATION.md` explicitly calls out as unacceptable.

## P3 — useful later

- **Per-project cost telemetry.** `MOTIVATION.md` describes a BI dashboard with revenue/expenses/profit per project. Today nothing in the template emits cost-side data. A small `core/costs.py` module that consumes Hetzner + Bunny + Scaleway billing APIs and writes a daily `CostSnapshot` row is enough to start; the dashboard itself can live outside the template.

- **OpenTelemetry exporter, opt-in.** The structlog setup is good. An optional OTEL bridge (gated behind an env var, off by default) would let any single product graduate to traces without re-architecting logging.

- **MoR fallback - Stripe abstraction.** `billing/services.py-tpl` is Polar-specific. If a product ever needs Stripe (some EU enterprise customers refuse non-Stripe checkout), a thin `BillingProvider` protocol with Polar as the only implementation is cheap to add now and expensive to retrofit later. Only do this once the second implementation is actually needed - speculative abstractions violate the grug-brain rule.

- **PWA + offline shell for the marketing site.** Low cost, helps Lighthouse / Core Web Vitals scores, which Google uses for ranking. Skip until the first product proves it cares.

- **`just doctor` for the generated project.** Beyond the Day-1 checklist - an idempotent recipe that re-checks all envs, all secrets, that `ADMINS` is set, that Sentry receives a test event, that the health check passes, that the latest backup is younger than N hours.

## Definition of done for each task

Prefer each task to be considered done only when:

- the generated project contains the change
- at least one test covers the core behaviour if practical
- docs reflect the final behaviour
- no new abstraction was added unless it clearly pays rent across multiple SaaS products
