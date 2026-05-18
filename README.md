# {{ project_name }}

Opinionated Django template for SaaS MVPs. Start from a production-oriented baseline with auth, tenancy, billing, marketing pages, and frontend scaffolding.

If you are starting a real product from this template, read `{{ project_name }}/docs/NEW_PROJECT_CHECKLIST.md` early. That is the short operator-facing checklist for "what do I need to do before I forget?".

To get started, make sure you have Django installed (5.1+) and run:

```bash
uv run django-admin startproject \
    --template=https://github.com/braw-dev/django_project_template/archive/main.zip \
    --extension 'py,yaml,md,template,dist,toml,json,css,js,dev,prod' \
    --name Justfile \
    --exclude '.ruff_cache' \
    --exclude '.rumdl_cache' \
    --exclude '.venv' \
    --exclude 'node_modules' \
    --exclude 'db.sqlite3' \
    --exclude 'dev' \
    --exclude 'tmp' \
    project_name [project_dir]
```

## Post-setup checklist

For the fuller "before deploy / before customers / before launch" list, use `{{ project_name }}/docs/NEW_PROJECT_CHECKLIST.md`.

- [ ] Init a new git repository `git init .`
- [ ] Install dev dependencies & lefthook git hooks `just install-dev`
- [ ] Configure environment variables by copying `{{ project_name }}/.env.dist` to `{{ project_name }}/.env` and customizing
- [ ] Search for `REPLACE_ME:` and update accordingly.
- [ ] Delete `specs` directory and `.specify/memory`.
- [ ] Establish the [SpecKit project principals](https://github.com/github/spec-kit?tab=readme-ov-file#2-establish-project-principles) in AI agent of choice (Cursor and Claude support included).
- [ ] Run `just ai-link` to link `ai/` directory to claude and cursor.
- [ ] Review `settings.py` settings
- [ ] Run database migrations `just migrate`
- [ ] Create a superuser with `just createsuperuser` if you want admin access straight away
- [ ] Collect staticfiles `just collectstatic`
- [ ] Run backend tests: `just test-unit`
- [ ] Run Django browser tests if needed: `just test-browser`
- [ ] Run Playwright E2E tests separately: `just playwright-install` then `just test-e2e`

## Billing bootstrap checklist

If you plan to use the built-in billing foundation in a new project, do this before exposing pricing or paid features:

- [ ] Set `BILLING_PROVIDER=polar` in `.env`
- [ ] Create a Polar access token and set `POLAR_ACCESS_TOKEN`
- [ ] Copy your Polar organization ID into `POLAR_ORGANIZATION_ID`
- [ ] Create at least one recurring product in Polar for your app
- [ ] Create a webhook endpoint in Polar pointing to `https://your-domain.com/api/webhooks/polar`
- [ ] Copy the Polar webhook secret into `POLAR_WEBHOOK_SECRET`
- [ ] Trigger a test checkout and confirm a local `Customer`, `Product`, `Subscription`, and `WebhookEvent` are created
- [ ] Trigger the customer portal flow and confirm it redirects back to your dashboard
- [ ] Keep billing-gated feature checks on local subscription/entitlement state, not direct provider API calls
- [ ] Confirm your public pricing copy states that prices exclude VAT and final tax is calculated at checkout (the template default)
- [ ] If using the newsletter, verify the double opt-in email flow, consent wording, and resend cooldown before sending marketing emails
- [ ] Review and replace the seeded Privacy, Terms, Security, Subprocessors, Contact, and FAQ placeholder pages before launch
- [ ] Review the seeded support FAQs for hosting, encryption, backups, MFA, support access, and uptime/performance expectations before sharing the app with customers
- [ ] Fill in the Subprocessors page with your real providers, hosting regions, data locations, and customer-notification process before customer review or launch
- [ ] Review the built-in privacy export/delete hooks and decide what billing, finance, and statutory-retention data must be kept or deleted for your product before using delete workflows in production
- [ ] Decide how bookkeeping will work: treat Polar as the source of truth for invoices, receipts, refunds, and tax documents; treat your bank or payout account as the source of truth for cash received; do not treat the local Django billing tables as your accounting ledger

For the full step-by-step setup, see `{{ project_name }}/billing/README.md`.

## What's included?

### Development

- **Security**: Custom User with MFA, Argon2id hashing, SRI, team-scoped API tokens, and an append-only audit trail for sensitive operator actions.
- **Privacy ops**: Operator-run user data export/delete hooks exposed through Django admin actions and management commands.
- **Configuration**: Typed `pydantic-settings` setup with fast failure on missing required config.
- **Structure**: Team-first multi-tenancy with memberships, invitations, and tenant-scoped models.
- **Stack**: Django + Django Ninja API, PostgreSQL/PostGIS via `DB_DEFAULT_URL`, SQLite in tests, and a Redis-compatible cache via `CACHE_DEFAULT_URL`.
- **Testing**: `pytest` + `pytest-django` for backend tests, Django browser tests, and Playwright for frontend E2E tests.
- **Typing**: `ty` static analysis.
- **Frontend**: WhiteNoise static file serving, Vite + React, Tailwind CSS + Daisy UI, and `django-cotton` components.
- **Tooling**: `Justfile` command runner, Ruff linting/formatting via `lefthook`.

### Marketing

- **Content**: Markdown `Page` model for FAQs and landing pages, sanitised with `nh3` at render time.
- **Support**: Public help-center pattern with a `/support/` index, simple FAQ search, categorized FAQ sections, seeded customer-facing FAQ starter pages, a reusable featured-FAQ partial for landing pages, and a seeded contact page.
- **SEO**: `django-meta` integration.
- **Legal**: Editable placeholder Privacy, Terms, Security, and Subprocessors pages are seeded via the pages app; the Subprocessors page includes starter tables for subprocessors and hosting inventory, and all of them should be replaced with project-specific content before launch.
- **Analytics**: Optional Plausible analytics include.
- **Growth**: Newsletter sign-up with explicit consent, double opt-in email confirmation, resend cooldown protection, and optional Chatwoot widget.

Marketing pages are intended to live in the same project as the app by default. Public pages stay public; app routes opt into protection explicitly with decorators such as `login_required` and `mfa_required`.

The template now separates layouts more clearly:

- `base.html` is the default marketing/public layout and includes the footer plus optional Plausible and Chatwoot snippets
- `app_base.html` is for authenticated app pages and omits those marketing/support snippets by default

When adding new authenticated product UI, prefer extending `app_base.html` unless the page genuinely needs marketing-site footer or third-party scripts.

### Business

- **Payments**: Polar-first billing foundation behind a lightweight provider interface, with hosted checkout/portal flows, local customer/product/subscription/entitlement models, verified idempotent webhooks, a thin provider-backed pricing-page helper, locale-aware pricing display for EUR/CHF/GBP/USD, and a default European stance of showing prices excluding VAT with final tax calculated at checkout. The local billing tables are for product access and support workflows, not a substitute for provider-issued billing documents or accounting records.
- **i18n**: Django gettext workflow plus an AI-assisted helper for filling untranslated `.po` entries, and a React-island bridge that reads the active Django-selected locale from `<html lang>`.
- **Deployment**: Production-oriented container scaffolding via Dockerfiles and Compose manifests, with an opinionated docs default of Hetzner VPS + rootless Podman + `systemd --user` + root-managed Caddy + Bunny.net; final deployment wiring is still project-specific.
- **Observability**: Sentry for exceptions, health checks, and structured request-performance logs that work well with Grafana Alloy + Grafana Cloud.

## Built-in Features

### Team-First Multi-Tenancy

This project includes a built-in multi-tenancy foundation for B2B SaaS products:

- **Teams**: Top-level tenants/workspaces/accounts
- **TeamMembership**: Fixed roles (`owner`, `admin`, `member`)
- **TenantScopedModel**: Abstract base for team-owned models
- **Active Team Middleware**: Resolves `/t/{team_slug}/` requests
- **Signed Invitations**: Email-delivered invitation links with expiry and replay protection
- **API Tokens**: Team-scoped bearer tokens with hashed secrets and one-time plaintext display
- **Optional Postgres RLS**: Defence-in-depth row-level isolation for production Postgres deployments

See `{{ project_name }}/tenancy/README.md`, `{{ project_name }}/tokens/README.md`, and `SECURITY.md` for the security model.

### Route Protection Policy

Use middleware for request-wide context such as active team resolution. Use decorators or mixins for access policy such as login, MFA, or onboarding requirements. Avoid global middleware with growing exception lists for public marketing pages.

### Support FAQ pattern

This template includes a small customer-facing support/help-center convention built on the existing `pages` app.

What gets generated by default:

- a public `/support/` page
- a seeded `contact` page
- seeded FAQ `Page` records for account, billing, security, and performance/reliability questions
- a reusable featured FAQ partial for marketing pages such as the homepage

How it works:

- FAQ entries are ordinary published `Page` records whose slugs start with `faq-`
- the support page searches FAQ titles and content with a simple database query; there is no separate search service
- FAQ categories are derived from the slug naming convention:
  - `faq-account-*` → Account and access
  - `faq-billing-*` → Billing
  - `faq-security-*` → Security
  - `faq-performance-*` → Performance and reliability
- featured FAQs are selected in `{{ project_name }}/pages/faq.py` via the `FEATURED_FAQ_SLUGS` constant

Files to know about:

- `{{ project_name }}/pages/faq.py` — FAQ grouping and featured-FAQ selection
- `templates/pages/support_index.html` — full help-center page
- `templates/partials/featured_faqs.html` — embeddable featured FAQ block
- `{{ project_name }}/pages/migrations/0004_seed_support_pages.py`
- `{{ project_name }}/pages/migrations/0005_seed_customer_faq_starters.py`

How to customize it in a generated project:

- edit the seeded FAQ and contact pages in Django admin under Pages
- replace all `REPLACE_ME` placeholder content before launch
- add more FAQs by creating more published pages with `faq-<category>-<slug>` slugs
- if you need a new category, add its label in `{{ project_name }}/pages/faq.py`
- change the featured FAQ set by editing `FEATURED_FAQ_SLUGS` in `{{ project_name }}/pages/faq.py`

To embed featured FAQs on another template, pass `featured_faqs` from the view context and include:

```django
{% templatetag openblock %} include "partials/featured_faqs.html" with faqs=featured_faqs {% templatetag closeblock %}
```

The template intentionally keeps this simple: no FAQ model, no tags, no docs CMS, and no separate search index by default.

### Billing and bookkeeping stance

The template takes a deliberately boring stance for solo-operator bookkeeping:

- **Polar is the source of truth** for invoices, receipts, credit notes, refunds, subscription charges, and tax documents
- **your bank account or payout statement is the source of truth** for cash actually received and fees actually paid
- **your Django database is the source of truth** for product access state such as which team has an active subscription or entitlement

That means the local `billing.Customer`, `billing.Product`, `billing.Subscription`, `billing.Entitlement`, and `billing.WebhookEvent` records are primarily operational. They exist so your app can gate features, show billing status, and help with support/debugging. They are not intended to be a full accounting ledger.

Minimum operator workflow for bookkeeping:

1. export invoices, refunds, and tax documents from Polar
2. reconcile payouts and fees against your bank account or payout statements
3. use the local Django billing records only to answer support questions and verify access state
4. if your accountant or bookkeeping tool needs structured imports, build that as a project-level extension from Polar exports rather than making Django the billing source of truth

### Privacy operations

This template includes boring operator-run hooks for basic user privacy requests:

- Django admin actions on the Users admin changelist to export or delete selected users' personal data
- `uv run python manage.py export_user_data user@example.com`
- `uv run python manage.py delete_user_data user@example.com --yes`

The default scope is intentionally narrow:

- exports direct user-linked data such as the user profile, verified email addresses, MFA authenticator types, newsletter signup state, team memberships/invitations, and API tokens created by that user
- deletes the user plus a minimal set of directly linked records needed for a basic privacy workflow
- refuses to delete users who still own teams
- does **not** automatically delete billing, finance, or other records that may be subject to statutory retention or business record requirements

Downstream projects should extend `{{ project_name }}/users/privacy.py` as they add app-specific personal data and should document their own retention rules before using deletion in production.

### Audit trail

This template includes an append-only `AuditEvent` model for sensitive operator actions.

Default events wired by the template:

- `support.hijack_started`
- `support.hijack_ended`
- `privacy.user_data_exported`
- `privacy.user_data_deleted`
- `privacy.user_data_delete_blocked`
- `tokens.api_token_created`
- `tokens.api_token_revoked`
- `tenancy.team_created`
- `tenancy.membership_added`
- `tenancy.invitation_created`
- `tenancy.invitation_accepted`

The audit log is stored in the database, visible in Django admin, and intentionally read-only there. The intended pattern is to record security-sensitive changes at the service-layer entry points that own the mutation. Extend it for other sensitive actions such as billing changes as your product needs them.

## Deployment default

If you want one boring default for a generated project, the docs now recommend:

- Hetzner VPS in the EU
- one Unix user per app
- rootless Podman managed by `systemd --user`
- one root-managed Caddy on the host for TLS and reverse proxying
- Bunny.net as the CDN in front of Caddy
- PostgreSQL managed separately in-region
- Dragonfly on the same VPS or a small sister instance on the same private network

This repo does not generate the host-level Caddy, Podman unit, or PostgreSQL setup for you. See `DEPLOYMENT.md` for the intended shape and tradeoffs.

## Development Setup

### Prerequisites

- [`uv`](https://docs.astral.sh/uv/) (Python) & [`pnpm`](https://github.com/pnpm/pnpm) (Frontend)
- [`gitleaks`](https://github.com/gitleaks/gitleaks) for pre-commit secret scanning
- [`mkcert`](https://github.com/FiloSottile/mkcert) for `just runserver`
- [`entr`](https://github.com/eradman/entr) & [`rg`](https://github.com/BurntSushi/ripgrep) for watch-mode commands
- [Playwright](https://playwright.dev/) for browser/E2E tests
- [`stow`](https://www.gnu.org/software/stow/) if you want to use `just ai-link`

### Installation

1. `git init .` from the generated project root if you have not already done so
2. `just install-dev` (Creates the Python virtualenv, installs Python and frontend dependencies, and sets up hooks; expects `gitleaks` to already be installed locally)
3. `cp {{ project_name }}/.env.dist {{ project_name }}/.env`
4. For a zero-friction local setup, edit `{{ project_name }}/.env` and change these defaults:
   - `DEBUG=True`
   - `ENVIRONMENT=development`
   - `SEND_EMAILS=False`
   - `LOG_LEVEL=INFO`
   - `DB_DEFAULT_URL=sqlite:///db.sqlite3`
   - `CACHE_DEFAULT_URL=locmemcache://`
5. `just migrate`
6. `just runserver` (Start dev server)

Most commands are run from the generated project root through `just`, but the Django app, `manage.py`, and `.env` live under `{{ project_name }}/`.

### Workflow

- **Code Quality**: Ruff enforces style via `lefthook` on commit.
- **Testing**:
  - Use `just test-unit` for backend/unit tests.
  - Plain `pytest` is supported and excludes browser-marked tests by default.
  - Use `just test-browser` for Django tests marked `browser`.
  - Use `just playwright-install` then `just test-e2e` for frontend Playwright tests.
- **Debugging**: `django-debug-toolbar` is included outside test runs.
- **Expected first-run warning**: `manage.py check` may warn that `frontend/{{ project_name }}/dist` does not exist yet. That is expected before your first frontend build and does not block local development with the Vite dev server.

## Template release review checklist

Before calling a template change "done", sanity-check it against a freshly generated project.

Recommended review loop:

1. generate a fresh project using the README command
2. confirm the README paths still match the generated layout, especially `{{ project_name }}/.env.dist`, `manage.py`, and root-level `just` commands
3. initialize git in the generated project root and run `just install-dev`
4. copy `{{ project_name }}/.env.dist` to `{{ project_name }}/.env` and switch to the documented local SQLite + locmem settings
5. run `just manage check`, `just migrate`, and `just test-unit`
6. if helper commands are documented, verify them in the generated project rather than only in the template repo
7. spot-check seeded pages, support/help links, pricing page behaviour, and footer links in the generated project
8. update the README if any manual step, path, or prerequisite changed

Treat the generated project as the source of truth. If the README and generated output disagree, fix the docs or the template before release.

## Internationalisation workflow

This template supports Django's built-in gettext workflow for Python and template strings, plus an AI-assisted helper for filling untranslated `.po` entries.

### What it covers

- Python strings marked with `gettext_lazy` / `_()`
- Template strings marked with `{% templatetag openblock %} trans {% templatetag closeblock %}` / `{% templatetag openblock %} blocktrans {% templatetag closeblock %}`
- Django's built-in language switching via the `set_language` view under `/i18n/`
- Base templates set `<html lang>` and `dir` from the active language
- React islands read the active document language from `<html lang>` and `dir` via the shared frontend i18n bridge
- Locale-prefixed URLs for the `pages` catch-all routes via `i18n_patterns`

### What it does not cover

- Translated database content stored with `django-parler` such as `Page` model content. That content needs a separate export/import workflow.
- Django gettext catalogs and React JSON locale catalogs are separate; the template does not auto-sync strings between them.
- Custom date/number/currency presentation still needs explicit template-level decisions where those values are shown.

### Prerequisites

- GNU gettext installed locally so Django can run `makemessages` / `compilemessages`
- `AI_TRANSLATION_API_KEY` set if you want the AI helper to write translations for you

### Extract strings

Create or update locale catalogs with Django:

```bash
just makemessages -l de -l fr -l es -l pt -l it
```

This writes `.po` files under `locale/<lang>/LC_MESSAGES/django.po`.

### Fill untranslated entries with AI

Use the built-in management command through `just`:

```bash
export AI_TRANSLATION_API_KEY=your-api-key
just translate-locale de
```

Optional flags are passed through to the management command:

```bash
just translate-locale de --model gpt-4.1-mini --base-url https://api.openai.com/v1 --batch-size 10
```

The helper uses an OpenAI-compatible chat completions API and only updates untranslated entries in `locale/<lang>/LC_MESSAGES/django.po`.

### Compile translations

After reviewing the generated `.po` changes, compile them:

```bash
just compilemessages
```

### Recommended flow

```bash
just makemessages -l de
just translate-locale de
just compilemessages
```

### React islands

The template includes a small React-island i18n bridge for frontend code loaded with `django-vite`.

Rules:

- Django remains the source of truth for the active language
- React islands must read locale from the document, not from `navigator.language`
- use the shared frontend i18n helpers under `frontend/{{ project_name }}/src/i18n/`
- register islands in `frontend/{{ project_name }}/src/islands/registry.ts`
- render island roots from Django templates with `{% templatetag openblock %} react_island "ComponentName" props {% templatetag closeblock %}`

See `{{ project_name }}/docs/frontend-i18n.md` for the concrete workflow.

### Checklist for new template pages

- add `{% templatetag openblock %} load i18n {% templatetag closeblock %}` to templates with user-facing copy
- wrap visible text with `{% templatetag openblock %} trans {% templatetag closeblock %}` or `{% templatetag openblock %} blocktrans {% templatetag closeblock %}`
- wrap Python-side user-facing strings in views, forms, and messages with `_()` / `gettext_lazy()`
- for React islands, put user-facing strings in the frontend locale JSON catalogs and use the shared `useAppTranslation()` helper
- prefer `{% templatetag openblock %} blocktrans {% templatetag closeblock %}` or named interpolation for strings with variables
- when rendering dates or numbers, use Django's locale-aware template tools rather than manual string formatting
- run `just makemessages -l de` and confirm new Django strings were extracted
- test the page with the built-in language switcher before shipping

## Developing on the template

If contributing to this template, use the provided Ansible playbook to test changes:

```bash
uv run ansible-playbook ./dev/01-test-project-template.yaml
```

This creates a test project in a temporary directory. Note: `rg` can help find hardcoded `project_name` instances that need variable replacement.

### Find `project_name` that is not a variable

Django will automatically replace `{{ project_name }}` with the actual name of the project when rendering the templates/files.
However when developing on the template we need to find `project_name` that **is not** a variable (so we can fix it). One
approach is to render the template and use `rg` to find `project_name`. However we can also use `rg` to find non-variable
`project_name` in just the template:

```bash
rg 'project_name' | rg -v '\{\{\s*project_name\s*\}\}'
```

---

If in doubt, check [awesome django](https://github.com/wsvincent/awesome-django) for libraries.

Always remember the [grug developer](https://grugbrain.dev/).

## Documentation

- [Motivation & Philosophy](MOTIVATION.md)
- [Production Architecture & Deployment](DEPLOYMENT.md)
- [Security Model](SECURITY.md)

## Todo

- [ ] Development in a dev container that's suitable for Mac and Linux
- [ ] Example application demonstrating what it can do and how to use the installed Django apps
