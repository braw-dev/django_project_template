# {{ project_name }}

Opinionated Django template for SaaS MVPs. Start writing business logic immediately with a production-ready, cost-effective setup. Includes tools for support, payments, marketing, translations, and monitoring.

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
    --exclude 'dev' \
    --exclude 'tmp' \
    project_name
```

## Post-setup checklist

- [ ] Init a new git repository `git init .`
- [ ] Install dev dependencies & lefthook git hooks `just install-dev`
- [ ] Configure environment variables by copying `.env.dist` to `.env` and customizing
- [ ] Search for `REPLACE_ME:` and update accordingly
- [ ] Establish the [SpecKit project principals](https://github.com/github/spec-kit?tab=readme-ov-file#2-establish-project-principles) in AI agent of choice (Cursor and Claude support included)
- [ ] Review `settings.py` settings
- [ ] Collect staticfiles `just collectstatic`
- [ ] Run tests: `just test-unit` and `just test-e2e`

## What's included?

### Development

- **Security**: Custom User with MFA, Argon2id hashing, SRI, `nh3` sanitization.
- **Configuration**: Simple `django-environ` setup.
- **Structure**: Users in Teams (Django Groups) with permission levels.
- **Stack**: PostgreSQL (production), SQLite (test), Dragonfly (Redis-compatible cache), Django Ninja API.
- **Testing**: `pytest-django` coverage, Playwright e2e tests.
- **Typing**: `mypy` static analysis.
- **Frontend**: Whitenoise serving, Vite + React (optional), Tailwind CSS + Daisy UI, `django-cotton` components.
- **Tooling**: `Justfile` command runner, Ruff linting/formatting via `lefthook`.

### Marketing

- **Content**: Markdown `Page` model for FAQs/Landing pages.
- **SEO**: `django-meta` integration.
- **Legal**: Privacy policy and Terms & Conditions pages.
- **Analytics**: Plausible analytics.
- **Growth**: Newsletter sign-up, embedded Chatwoot support.

### Business

- **Payments**: Polar.sh integration.
- **i18n**: Django i18n with Google Gemini auto-translation.
- **Deployment**: VPS ready (Podman + Ansible), multi-site support.

## Creating apps

A `startapp` template is available under `/app_name` to bootstrap new apps with consistent structure:

```bash
just startapp {{ app_name }}
```

## Built-in Features

### Organizations & Teams (RBAC)

This project includes a built-in role-based access control (RBAC) system for managing
multi-tenant organizational hierarchies:

- **Organizations**: Top-level tenants/workspaces
- **Teams**: Sub-groups within organizations
- **Roles**: Define permissions (Admin, Editor, Viewer)
- **Cascading Permissions**: Organization admins automatically access all teams

See `{{ project_name }}/organizations/README.md` for usage details.

## Development Setup

### Prerequisites

- [`uv`](https://docs.astral.sh/uv/) (Python) & [`pnpm`](https://github.com/pnpm/pnpm) (Frontend)
- [`entr`](https://github.com/eradman/entr) & [`rg`](https://github.com/BurntSushi/ripgrep) (Hot reloading)
- [Playwright](https://playwright.dev/) (E2E tests)

### Installation

1. `just install-dev` (Creates venv, installs dependencies, sets up hooks)
2. `cp .env.dist .env` (Setup environment)
3. `just runserver` (Start dev server)

### Workflow

- **Code Quality**: Ruff enforces style via `lefthook` on commit.
- **Testing**: TDD encouraged. Write `pytest` in `tests/` or Playwright specs in `tests/e2e/tests`.
- **Debugging**: `django-debug-toolbar` included for SQL analysis.

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

## Todo

- [ ] Development in a dev container that's suitable for Mac and Linux
- [ ] Finish implementing [logging and metrics capturing](https://rafed.github.io/devra/posts/cloud/django-mlt-observability-with-opentelemetry/) to Grafana
- [ ] Example application demonstrating what it can do and how to use the installed Django apps
