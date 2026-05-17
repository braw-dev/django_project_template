# {{ project_name }}

Opinionated Django template for SaaS MVPs. Start from a production-oriented baseline with auth, tenancy, billing, marketing pages, and frontend scaffolding.

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

- [ ] Init a new git repository `git init .`
- [ ] Install dev dependencies & lefthook git hooks `just install-dev`
- [ ] Configure environment variables by copying `.env.dist` to `.env` and customizing
- [ ] Search for `REPLACE_ME:` and update accordingly.
- [ ] Delete `specs` directory and `.specify/memory`.
- [ ] Establish the [SpecKit project principals](https://github.com/github/spec-kit?tab=readme-ov-file#2-establish-project-principles) in AI agent of choice (Cursor and Claude support included).
- [ ] Run `just ai-link` to link `ai/` directory to claude and cursor.
- [ ] Review `settings.py` settings
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
- [ ] Review and replace the seeded Privacy, Terms, Security, and Subprocessors placeholder pages before launch
- [ ] Review the built-in privacy export/delete hooks and decide what billing, finance, and statutory-retention data must be kept or deleted for your product before using delete workflows in production

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
- **SEO**: `django-meta` integration.
- **Legal**: Editable placeholder Privacy, Terms, Security, and Subprocessors pages are seeded via the pages app and should be replaced with project-specific content before launch.
- **Analytics**: Optional Plausible analytics include.
- **Growth**: Newsletter sign-up with explicit consent, double opt-in email confirmation, resend cooldown protection, and optional Chatwoot widget.

Marketing pages are intended to live in the same project as the app by default. Public pages stay public; app routes opt into protection explicitly with decorators such as `login_required` and `mfa_required`.

### Business

- **Payments**: Polar-first billing foundation behind a lightweight provider interface, with hosted checkout/portal flows, local customer/product/subscription/entitlement models, verified idempotent webhooks, a thin provider-backed pricing-page helper, locale-aware pricing display for EUR/CHF/GBP/USD, and a default European stance of showing prices excluding VAT with final tax calculated at checkout.
- **i18n**: Django gettext workflow plus an AI-assisted helper for filling untranslated `.po` entries.
- **Deployment**: Production-oriented container scaffolding via Dockerfiles and Compose manifests; final deployment wiring is still project-specific.

## Creating apps

A `startapp` template is available under `/app_name` to bootstrap new apps with consistent structure:

```bash
just startapp my_app
```

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

The audit log is stored in the database, visible in Django admin, and intentionally read-only there. Extend it for other sensitive actions such as billing changes, token lifecycle events, or team membership changes as your product needs them.

## Development Setup

### Prerequisites

- [`uv`](https://docs.astral.sh/uv/) (Python) & [`pnpm`](https://github.com/pnpm/pnpm) (Frontend)
- [`mkcert`](https://github.com/FiloSottile/mkcert) for `just runserver`
- [`entr`](https://github.com/eradman/entr) & [`rg`](https://github.com/BurntSushi/ripgrep) for watch-mode commands
- [Playwright](https://playwright.dev/) for browser/E2E tests
- [`stow`](https://www.gnu.org/software/stow/) if you want to use `just ai-link`

### Installation

1. `just install-dev` (Creates venv, installs dependencies, sets up hooks)
2. `cp .env.dist .env` (Setup environment)
3. `just runserver` (Start dev server)

### Workflow

- **Code Quality**: Ruff enforces style via `lefthook` on commit.
- **Testing**:
  - Use `just test-unit` for backend/unit tests.
  - Plain `pytest` is supported and excludes browser-marked tests by default.
  - Use `just test-browser` for Django tests marked `browser`.
  - Use `just playwright-install` then `just test-e2e` for frontend Playwright tests.
- **Debugging**: `django-debug-toolbar` is included outside test runs.

## Internationalisation workflow

This template supports Django's built-in gettext workflow for Python and template strings, plus an AI-assisted helper for filling untranslated `.po` entries.

### What it covers

- Python strings marked with `gettext_lazy` / `_()`
- Template strings marked with `{% templatetag openblock %} trans {% templatetag closeblock %}` / `{% templatetag openblock %} blocktrans {% templatetag closeblock %}`
- Django's built-in language switching via the `set_language` view under `/i18n/`
- Base templates set `<html lang>` and `dir` from the active language
- Locale-prefixed URLs for the `pages` catch-all routes via `i18n_patterns`

### What it does not cover

- Translated database content stored with `django-parler` such as `Page` model content. That content needs a separate export/import workflow.
- Custom date/number/currency presentation still needs explicit template-level decisions where those values are shown.

### Prerequisites

- GNU gettext installed locally so Django can run `makemessages` / `compilemessages`
- `AI_TRANSLATION_API_KEY` set if you want the AI helper to write translations for you

### Extract strings

Create or update locale catalogs with Django:

```bash
just makemessages -l de -l fr -l es -l pt
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

### Checklist for new template pages

- add `{% templatetag openblock %} load i18n {% templatetag closeblock %}` to templates with user-facing copy
- wrap visible text with `{% templatetag openblock %} trans {% templatetag closeblock %}` or `{% templatetag openblock %} blocktrans {% templatetag closeblock %}`
- wrap Python-side user-facing strings in views, forms, and messages with `_()` / `gettext_lazy()`
- prefer `{% templatetag openblock %} blocktrans {% templatetag closeblock %}` or named interpolation for strings with variables
- when rendering dates or numbers, use Django's locale-aware template tools rather than manual string formatting
- run `just makemessages -l de` and confirm new strings were extracted
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
- [ ] Finish implementing [logging and metrics capturing](https://rafed.github.io/devra/posts/cloud/django-mlt-observability-with-opentelemetry/) to Grafana
- [ ] Example application demonstrating what it can do and how to use the installed Django apps
