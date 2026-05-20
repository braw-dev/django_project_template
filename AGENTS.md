# AI Agent Guide

This documentation is intended for AI agents working on this repository. This repository is a
**Django Project Template**.

## 1. Context & Architecture

This is NOT a standard Django project. It is a **template** used to generate new Django projects via
`django-admin startproject`.

- **Root Directory**: Contains the template structure.
- **`project_name/`**: The source code for the generated Django project.
- **`frontend/project_name/`**: The frontend (React/Vite) source.
- **`dev/`**: Tools for developing and testing _this template_ (excluded in generated projects).
- **`Justfile`**: The command runner for both the template and the generated project.

### Core Technologies

- **Backend**: Django 5+, Python 3.13+ (managed by `uv`).
- **Frontend**: React, Vite, Tailwind CSS, Daisy UI (managed by `pnpm`).
- **Database**: SQLite (default), adaptable for PostgreSQL.
- **Task Runner**: `just`.
- **Linting/Formatting**: `ruff` (Python), `biome` (Frontend).
- **Testing**: `pytest` (Django), `playwright` (E2E).

---

## 2. Working on the Template (This Repo)

If you are modifying the template itself (fixing bugs, adding features to the base):

### ⚠️ Critical: Template Variables

- The string `{{ project_name }}` is a Django template variable.
- **DO NOT** replace `{{ project_name }}` with a real name unless explicitly asked to hardcode a
  value.
- **DO NOT** fix "syntax errors" that are actually Django template tags (e.g.,
  `{% templatetag openvariable %}`).
- When adding new files, ensure they use the correct directory structure
  (`project_name/project_name/...`).

### Testing the Template

To verify that the template generates a valid project:

1. **Install Dependencies**: `just install-dev`
2. **Run Test Generation**:

   ```bash
   uv run ansible-playbook ./dev/01-test-project-template.yaml
   ```

   This will:
   - Generate a new project in a temporary directory.
   - Install dependencies in that new project.
   - Run migrations and basic validation to ensure stability.

3. **Verify generated-project tests explicitly**:

   ```bash
   cd /path/to/generated/project
   just test-unit
   ```

   Notes:
   - `just test-unit` uses `pytest`/`pytest-django` for backend tests only.
   - Plain `pytest` is also supported and excludes browser-marked tests by default.
   - Browser/Playwright tests are separate from unit tests.

### Generated-project verification workflow

When changing the template, do not stop after editing template files. Always verify a freshly
generated project.

#### Preferred verification order

1. Generate a fresh project from the template
2. Install the generated project's dependencies
3. Run generated-project linting
4. Run generated-project formatting checks
5. Run generated-project backend tests

Use this exact sequence whenever practical:

```bash
tmpdir=$(mktemp -d /tmp/django-template-XXXXXX)
uv run django-admin startproject \
    --template=. \
    --extension 'py,yaml,md,template,dist,toml,json,css,js,dev,prod' \
    --name Justfile \
    --exclude '.env' \
    --exclude '.env.local' \
    --exclude '.ruff_cache' \
    --exclude '.rumdl_cache' \
    --exclude '.venv' \
    --exclude 'dev' \
    --exclude 'db.sqlite3' \
    --exclude 'node_modules' \
    --exclude 'tmp' \
    TEST_PROJECT_NAME "$tmpdir"
cp "$tmpdir/TEST_PROJECT_NAME/.env.dist" "$tmpdir/TEST_PROJECT_NAME/.env"
python3 - <<'PY' "$tmpdir/TEST_PROJECT_NAME/.env"
from pathlib import Path
import sys
path = Path(sys.argv[1])
text = path.read_text()
replacements = {
    'DEBUG=False': 'DEBUG=True',
    'ENVIRONMENT=production': 'ENVIRONMENT=development',
    'SEND_EMAILS=True': 'SEND_EMAILS=False',
    'LOG_LEVEL=ERROR': 'LOG_LEVEL=DEBUG',
    'DB_DEFAULT_URL=postgis://{{ project_name }}:{{ project_name }}@localhost:5432/{{ project_name }}?pool=True&server_side_binding=True': 'DB_DEFAULT_URL=sqlite:///db.sqlite3',
}
for old, new in replacements.items():
    text = text.replace(old, new)
path.write_text(text)
PY
cd "$tmpdir"
git init
just install-dev
uv run ruff check
uv run ruff format --check
just test-unit
```

#### Why verify this way

- The template repository itself is not the generated project.
- `.py-tpl` and template-tag syntax can hide problems that only appear after generation.
- Ruff and pytest results on the generated project are the source of truth for whether template
  output is actually usable.

#### If the Ansible smoke test is broken

If `uv run ansible-playbook ./dev/01-test-project-template.yaml` fails for unrelated reasons, do not
stop there. Generate a project manually with the workflow above and verify the generated project
directly.

### Backporting generated-project lint/format fixes

If `uv run ruff check` or `uv run ruff format --check` fails in the generated project:

1. **Treat the generated project output as the truth**.
2. Identify the generated file that Ruff is complaining about.
3. Map that file back to the template source file (usually the matching `*.py-tpl`, template, or
   migration file in this repo).
4. Apply the smallest equivalent edit to the template file, not the generated project.
5. Generate a fresh project again and rerun:
   - `uv run ruff check`
   - `uv run ruff format --check`
   - `just test-unit`

#### Practical tips

- Use `uv run ruff format --diff /path/to/generated/file.py` to see Ruff's exact desired rewrite.
- Mirror that diff back into the template file as literally as possible.
- If Ruff's formatter produces invalid Python for generated code, prefer a tiny local `# fmt: off` /
  `# fmt: on` block around the affected code instead of broad formatting suppression.
- Do not assume a template file is correct just because the repository copy looks formatted. Only
  the generated file matters.
- After every fix, regenerate from scratch. Do not keep patching an old generated directory and
  assume the template is now correct.

---

## 3. Working in a Generated Project

Understand the purpose of the project in [`/docs/PRODUCT_OVERVIEW.md`](/docs/PRODUCT_OVERVIEW.md).

Clean up any code or documents that reference working on the template itself.

If you are reading this file inside a project _generated_ from this template (i.e., `project_name`
has been replaced by a real name):

### Development Workflow

Always use `just` commands to ensure environment consistency.

If you are helping set up a freshly generated project, read and follow
`docs/NEW_PROJECT_CHECKLIST.md` early. Treat it as the canonical short checklist for first-run,
pre-deploy, and pre-customer setup work.

- **Setup**: `just install-dev` (sets up venv, installs python/node deps, hooks).
- **Start Server**: `just runserver` (runs Django + Vite).
- **Tests**:
    - Unit/backend: `just test-unit`
    - E2E/browser: `just playwright-install` then `just test-e2e`
    - Fast (watch mode): `just test-fast-watch`
- **Linting**: `just format` (runs Ruff).
- **Database**: `just migrate`, `just reset-db`.

### Project Structure

- `{{ project_name }}/`: Django app code (settings, urls, wsgi).
- `{{ project_name }}/tests/e2e`: Typescript + Playwright end-to-end tests.
- `{{ project_name }}/tests/`: browser-style Django/Playwright tests, excluded from plain `pytest`
  by default via the `browser` marker.
- `frontend/`: React application.
- `templates/`: Django HTML templates (mostly for auth/accounts).
- `static/`: Static assets.

### Transactional email convention

- Use `{{ project_name }}.users.emails.send_transactional_email(...)` for new product emails.
- Create matching `*.txt` and `*.html` templates and keep them small.
- Reuse the shared wrappers in `templates/email/base.txt` and `templates/email/base.html`.
- See `docs/transactional-email.md` in generated projects before adding new invitation, billing, or
  security emails.

### Public vs Protected Routes

This template includes both public marketing pages and protected app pages in the same Django
project.

- Public pages should remain public by default.
- Protected app routes should opt into `login_required`, `mfa_required`, or similar
  decorators/mixins explicitly.
- Use middleware for request context such as active team resolution, not for blanket access
  enforcement with exception lists.

### Frontend Integration

- The frontend is a separate Vite app served by Django in development/production.
- **Location**: `frontend/{{ project_name }}/`.
- **Commands**: managed via `just` (e.g., `install-frontend-dev` is called by `install-dev`).
- The frontend is intended for **React islands**, not a separate SPA replacing Django templates.
- Django remains the source of truth for the active language; React islands must derive locale from
  the rendered document (`<html lang>` / `dir`), not `navigator.language`.
- For React-island UI strings, use the shared frontend i18n shim under
  `frontend/{{ project_name }}/src/i18n/` and register mountable islands in
  `frontend/{{ project_name }}/src/islands/registry.ts`.

---

## 4. Rules & Conventions

- **File Editing**: Always read the file first. If it contains template tags
  (`{% templatetag openblock %} ... {% templatetag closeblock %}`), treat it as a template file.
- **Dependency Management**:
    - Python: Edit `pyproject.toml`, then run `uv sync`.
    - Node: Edit `package.json`, then run `pnpm install`.
- **Code Style**: Run `just format` before finishing tasks.
- **Documentation**: Update `README.md` or `MOTIVATION.md` if architectural changes are made.
- **Route protection**: When adding a new app route, decide explicitly whether it is public or
  protected. Do not extend global middleware allowlists for public-page exceptions.

---

## 5. AI Agent-Specific Instructions

This repository includes detailed instructions for different AI coding assistants.

The canonical shared instruction text lives in `ai/docs/`. `.claude/CLAUDE.md` and `.claude/docs/`
are symlinked to that source, while `.cursor/rules/` keeps tool-specific rule wrappers that point
back to the same canonical docs.

### For Claude Code

Comprehensive instructions are in the `.claude/` directory:

- **`.claude/CLAUDE.md`**: Main instructions file (start here)
- **`.claude/docs/`**: Detailed documentation:
    - `template-development.md`: Template-specific development rules
    - `django-stack.md`: Django architecture and conventions
    - `security-simplicity.md`: Security principles and simplicity philosophy
    - `grug-brain.md`: Grug brain developer philosophy
    - `internationalisation-first.md`: Guidance on supporting translations from the start

**Quick Start for Claude Code:**

1. Read `.claude/CLAUDE.md` for context detection (template vs generated project)
2. Follow security-first principles (never compromise on auth, validation, secrets)
3. Apply Grug brain philosophy (say no to complexity, features, dependencies)
4. Use established Django patterns (services/selectors, ORM, built-in features)
5. Test template changes with: `uv run ansible-playbook ./dev/01-test-project-template.yaml`

### For Cursor

Instructions are in the `.cursor/rules/` directory. Key files:

- `grug-brain.mdc`: Simplicity philosophy
- `security-simplicity.mdc`: Security and simplicity principles  
- `django-stack.mdc`: Django conventions
- `template-development.mdc`: Template development rules

### Cross-Agent Principles

All AI agents should follow these universal principles:

1. **Context Detection**: Determine if working on template or generated project
2. **Security First**: Never compromise on authentication, validation, or data handling
3. **Grug Brain Philosophy**: Complexity is the enemy, say no to most things
4. **Boring Technology**: Don't introduce new languages/frameworks without strong justification
5. **Minimal Changes**: Don't refactor unrelated code or add unrequested features
6. **Test First**: Test template changes before committing

See individual agent directories for detailed, agent-specific instructions.
