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

- **VAT identity capture on `Team`, even if Polar does the tax math.** `billing/README.md` correctly delegates tax to Polar, but the `Team` model has no `billing_country`, `vat_number`, or `vat_validated_at` fields. Without those, every product has to retrofit them later, and there is no Django-side hook for "remind admin to enter VAT before first invoice." Add nullable fields + a one-shot VIES validation service (`tenancy/services.py`) that records validated state and a `tenancy.vat_validated` audit event. Keep actual tax calculation with Polar; this is just _capture_ and _display_ on invoices/receipts surfaced in-app.

- **Document and verify the Polar / merchant-of-record posture for EU customers.** Polar is a US-incorporated MoR. For a German or French B2B buyer doing vendor review, this is a question on every procurement form. Add a short section to `billing/README.md` and `docs/PRODUCT_OVERVIEW.md` (or a new `docs/billing-eu.md`) that says exactly: who is the contracting party, who issues invoices, where is data stored, what is the fallback if Polar coverage changes. No code change required, but the doc has to exist for the trust-pages to be honest.

- **A real "subprocessors changed" notification path.** The seeded `subprocessors` page is good, but there is no mechanism for the `subprocessor_notifications` mailing list described in customer DPAs (this is what EU enterprise buyers actually ask for). Reuse the existing `NewsletterSignup` model with a `purpose` field (`marketing` vs `subprocessor_updates`) and a separate confirmation flow, or add a tiny `SubprocessorSubscription` model. Either is fine; pick one and wire it on the subprocessors page.

- **Session lifetime + reauthentication for sensitive actions.** `settings.py-tpl` leaves `SESSION_COOKIE_AGE` at Django's two-week default and does not set `SESSION_EXPIRE_AT_BROWSER_CLOSE`. For B2B SaaS the expected baseline is shorter sessions, optional idle timeout, and a `reauthentication_required` decorator gating things like "delete team", "rotate API token", "change billing email". Allauth already exposes the primitives - wire them on the team/token/billing services and add a `reauthenticate` template under `templates/account/`.

- **Login + security-event email notifications.** `core/audit.py-tpl` records security events but never notifies the user. For B2B, "new sign-in from a new device" and "MFA disabled" / "recovery codes regenerated" / "API token created" are table stakes. Add a small `users/notifications.py` that subscribes to the audit-event signal and sends a transactional email for a narrow allowlist of event types, gated behind a per-user preference.

- **Rate-limit the non-login attack surface.** `django-axes` covers login, but newsletter signup, newsletter confirmation resend, allauth password reset, allauth email confirmation resend, and the team-invitation accept endpoint are all unauthenticated and reachable. Use a single boring abstraction (e.g. `django-ratelimit` with Redis/Dragonfly) and apply it to those views; add a test per endpoint that hits the limit and asserts the 429 response uses the existing template.

- **Frontend i18n is missing despite the i18n-first claim.** `frontend/project_name/package.json` has no `i18next` / `react-intl` / `formatjs` dependency, and the `internationalisation-first` doc only covers the Django side. Either add `i18next` + a `useTranslation` shim wired through Django-rendered `<html lang>` and a JSON catalogue per `LANGUAGES`, or explicitly document that "frontend stays English-only until requested" so generated projects don't ship half-translated UIs. My preference: add the shim - this is high-leverage and cheap once, expensive per project.

## P2 — important for product quality and repeatability

- **First-run / Day-1 generated-project checklist.** `README.md` is comprehensive but it is not a checklist - a founder reading it after `django-admin startproject` does not have a 10-item "before customers" list (rotate `SECRET_KEY`, fill `PRODUCT_OVERVIEW.md`, replace placeholder trust-page bodies, set `ADMINS`, set `EMAIL_DOMAIN`, configure Sentry DSN, configure Polar, set Plausible domain, take a first backup, run a restore drill). Add `docs/NEW_PROJECT_CHECKLIST.md` and link it from the top of the generated README. Bonus: a `just doctor` recipe that checks the obvious env/secret/host invariants and prints what is missing.

- **Backup, restore, and a _tested_ restore drill using borg + borgmatic + Hetzner Storage Box.** `DEPLOYMENT.md` honestly says backups are not scaffolded. For a portfolio of unattended SaaS products, scaffold encrypted, deduplicated, append-only backups using `borg` driven by `borgmatic`, with a Hetzner Storage Box as the off-site repository (SSH/SFTP target, cheap, EU-located). Concretely:
  - Ship a `borgmatic.yaml` (or `config.yaml` under `/etc/borgmatic.d/`) template in the generated project with: repository pointing at `ssh://<user>@<box>.your-storagebox.de:23/./repo`, `repokey-blake2` encryption, sensible `keep_daily`/`keep_weekly`/`keep_monthly` retention, a `before_backup` hook that runs `pg_dump --format=custom` to a staging path (or uses borgmatic's built-in `postgresql_databases:` hook), and `checks: [repository, archives]` running on a weekly cadence.
  - Add a `just db-backup` recipe that invokes `borgmatic create --verbosity 1 --stats` and a `just db-backup-check` recipe that runs `borgmatic check`.
  - Add a `just db-restore-drill` recipe that: pulls the latest archive into a throwaway directory via `borgmatic extract --archive latest`, restores the `pg_dump` into a disposable Postgres container, runs `manage.py migrate --check` and a smoke query, then tears the container down. The recipe must exit non-zero on any step failure so it can be wired to a cron/systemd timer and Sentry cron monitor.
  - Provide a systemd `borgmatic.service` + `borgmatic.timer` unit pair (daily) and a separate `borgmatic-restore-drill.timer` (weekly) under `deploy/systemd/`.
  - Store the borg passphrase and Storage Box SSH key path in env vars (`BORG_PASSPHRASE`, `BORG_RSH`) loaded from the existing secrets mechanism; never in the repo.
  - Document in `docs/backups.md`: how to provision a Hetzner Storage Box, how to initialise the repo (`borgmatic init --encryption repokey-blake2`), retention policy, passphrase rotation, the weekly restore-drill cadence, and how to recover end-to-end from a total host loss. Data loss is the only failure mode `MOTIVATION.md` explicitly calls out as unacceptable.

- **Audit-log retention + read-only enforcement at the DB level.** `AuditEvent` is "read-only in admin" but ORM `.delete()` works fine, and there is no retention story. For B2B/TDD, add: (a) a `delete()` override on the model that raises unless an explicit `_allow_delete=True` flag is passed, (b) a `just audit-prune` management command that deletes events older than a configurable retention window in batches, with its _own_ `audit.retention_pruned` event before deleting, (c) a check in `settings.py-tpl` that the retention window is set in production.

- **Account deletion with a grace window.** `users/privacy.py-tpl` deletes immediately. A 30-day soft-delete window (user is anonymised and disabled at request time, hard-deleted by a Celery beat job) is both the GDPR-friendly default and a real-world necessity for support cases. Add a `deletion_requested_at` field, change `delete_user_data` to a two-phase flow, and add the matching audit events.

- **Health checks need to reflect what actually goes down.** `core/health.py-tpl` exposes a readiness endpoint, but it is not visible whether Celery broker, Celery worker liveness, and storage (S3) are checked. `django-health-check` is already in dependencies - register the cache, db, celery, and storage backends with it, and add a `/api/v1/health/live` for liveness vs readiness so the systemd-under-Podman default deployment can wire both probes correctly.

- **One transactional email template kit.** `templates/account/` has the allauth templates, but billing receipts, dunning emails, invitation emails, deletion-confirmation emails, and audit-notification emails will be invented per product. Add a `templates/email/base.html` (table-based, light/dark-safe, plain-text sibling), and at least the four most common templates (invitation, billing-receipt, dunning, security-notification) as cotton components fed by a thin `users/emails.py` service. Pays rent across every product.

- **Factories + a single conftest for the generated project.** `factory-boy` is in dev deps but there are no factories. Cross-team-denial tests, billing tests, and tokens tests would all be shorter and clearer with `UserFactory`, `TeamFactory`, `TeamMembershipFactory`, `SubscriptionFactory`. Add `project_name/tests/factories.py` and a `conftest.py` exposing pytest fixtures for the common shapes (`user`, `team`, `owner_membership`, `another_team`).

- **Marketing-conversion event hooks for Plausible.** Plausible is wired as a script, but there are no `plausible('Signup', ...)` / `plausible('Trial started')` calls anywhere. Add a tiny `core/analytics.py` server-side helper (Plausible has an events API) and call it from the signup, newsletter-confirm, trial-start, and subscription-active code paths. This is the data the BI dashboards described in `MOTIVATION.md` will need.

- **Consolidate AI agent instructions.** `AGENTS.md`, `.claude/CLAUDE.md`, and `.cursor/rules/*` cover overlapping ground (template detection, security-first, grug-brain). The Justfile already has an `ai-link` recipe using `stow`, but `CLAUDE.md` itself is not in `ai/` and is hand-edited - meaning Claude/Cursor/Codex drift over time. Move the canonical text into `ai/docs/` and symlink from `.claude/` and `.cursor/`; add a CI check that fails if the symlinks are dangling or the canonical files diverge.

## P3 — useful later

- **`/.well-known/security.txt` route.** Trivial, points at the security contact mentioned in `SECURITY.md`, and signals maturity in vendor questionnaires.

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
