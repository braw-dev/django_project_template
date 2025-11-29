# AI Agent Guide

This documentation is intended for AI agents working on this repository. This repository is a **Django Project Template**.

## 1. Context & Architecture

This is NOT a standard Django project. It is a **template** used to generate new Django projects via `django-admin startproject`.

- **Root Directory**: Contains the template structure.
- **`project_name/`**: The source code for the generated Django project.
- **`frontend/project_name/`**: The frontend (React/Vite) source.
- **`dev/`**: Tools for developing and testing *this template* (excluded in generated projects).
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
- **DO NOT** replace `{{ project_name }}` with a real name unless explicitly asked to hardcode a value.
- **DO NOT** fix "syntax errors" that are actually Django template tags (e.g., `{% templatetag openvariable %}`).
- When adding new files, ensure they use the correct directory structure (`project_name/project_name/...`).

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
   - Run migrations and tests to ensure stability.

---

## 3. Working in a Generated Project

If you are reading this file inside a project *generated* from this template (i.e., `project_name` has been replaced by a real name):

### Development Workflow

Always use `just` commands to ensure environment consistency.

- **Setup**: `just install-dev` (sets up venv, installs python/node deps, hooks).
- **Start Server**: `just runserver` (runs Django + Vite).
- **Tests**:
  - Unit: `just test-unit`
  - E2E: `just test-e2e`
  - Fast (watch mode): `just test-fast-watch`
- **Linting**: `just format` (runs Ruff).
- **Database**: `just migrate`, `just reset-db`.

### Project Structure

- `{{ project_name }}/`: Django app code (settings, urls, wsgi).
- `{{ project_name }}/tests/e2e`: Typescript + Playwright end2end tests also for Django logic.
- `frontend/`: React application.
- `templates/`: Django HTML templates (mostly for auth/accounts).
- `static/`: Static assets.

### Frontend Integration

- The frontend is a separate Vite app served by Django in development/production.
- **Location**: `frontend/{{ project_name }}/`.
- **Commands**: managed via `just` (e.g., `install-frontend-dev` is called by `install-dev`).

---

## 4. Rules & Conventions

- **File Editing**: Always read the file first. If it contains template tags (`{% ... %}`), treat it as a template file.
- **Dependency Management**:
  - Python: Edit `pyproject.toml`, then run `uv sync`.
  - Node: Edit `package.json`, then run `pnpm install`.
- **Code Style**: Run `just format` before finishing tasks.
- **Documentation**: Update `README.md` or `MOTIVATION.md` if architectural changes are made.
