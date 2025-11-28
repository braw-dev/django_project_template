#!/usr/bin/env just --justfile

# Default recipe to display help information (in order of this file)
_default:
    @just --list --unsorted

# Variables

UV_RUN := "uv run"
PNPM := "pnpm"

# Install dev dependencies
install-dev: install-python-dev install-frontend-dev

# Generates a self-signed certificate for the development server
mkcert:
    @if [ ! -f /tmp/{{project_name}}.crt ]; then \
        mkcert -cert-file=/tmp/{{project_name}}.crt -key-file=/tmp/{{project_name}}.key localhost 127.0.0.1; \
    fi

###############################################
## Testing related targets
###############################################

test_command := UV_RUN + " python manage.py test"
test_options := " --shuffle --parallel=auto"

# Run fast tests (excludes browser tests)
[working-directory: '{{ project_name }}']
test-fast:
    @{% templatetag openvariable %} test_command {% templatetag closevariable %} {% templatetag openvariable %} test_options {% templatetag closevariable %} --exclude-tag=browser

# Run fast tests in watch mode
[working-directory: '{{ project_name }}']
test-fast-watch:
    @rg --files -t python,html | entr {% templatetag openvariable %} test_command {% templatetag closevariable %} {% templatetag openvariable %} test_options {% templatetag closevariable %} --exclude-tag=browser

# Run browser tests (uses Playwright)
[working-directory: '{{ project_name }}']
test-browser:
    @{% templatetag openvariable %} test_command {% templatetag closevariable %} {% templatetag openvariable %} test_options {% templatetag closevariable %} --tag=browser

# Run all tests
[working-directory: '{{ project_name }}']
test:
    @{% templatetag openvariable %} test_command {% templatetag closevariable %} {% templatetag openvariable %} test_options {% templatetag closevariable %}

# Run all tests in watch mode
[working-directory: '{{ project_name }}']
test-watch:
    @rg --files -t python -t html | entr {% templatetag openvariable %} test_command {% templatetag closevariable %} {% templatetag openvariable %} test_options {% templatetag closevariable %}

[working-directory: '{{ project_name }}']
test-unit:
    @{% templatetag openvariable %} UV_RUN {% templatetag closevariable %} pytest

[working-directory: 'project_name/tests/e2e']
test-e2e:
    @{% templatetag openvariable %} PNPM {% templatetag closevariable %} test

###############################################
## Django management
###############################################

manage := UV_RUN + " python manage.py"

# Shortcut to run Django management commands
[working-directory: '{{ project_name }}']
manage +ARGS:
    @{% templatetag openvariable %} manage {% templatetag closevariable %} {% templatetag openvariable %} ARGS {% templatetag closevariable %}

# Run the development server with HTTPS
[working-directory: '{{ project_name }}']
runserver: mkcert
    @{% templatetag openvariable %} manage {% templatetag closevariable %} runserver_plus --cert-file=/tmp/{{project_name}}.crt --key-file=/tmp/{{project_name}}.key

# Runs the development server without HTTPS
runserver-no-https:
    @{% templatetag openvariable %} manage {% templatetag closevariable %} runserver

# Run Django migrations
[working-directory: '{{ project_name }}']
migrate:
    @{% templatetag openvariable %} manage {% templatetag closevariable %} migrate

# Collect static files
[working-directory: '{{ project_name }}']
collectstatic:
    @{% templatetag openvariable %} manage {% templatetag closevariable %} collectstatic --noinput

# Create a new Django app in the correct directory
[working-directory: '{{ project_name }}']
startapp APP_NAME:
    @mkdir -p {{ project_name }}/{% templatetag openvariable %} APP_NAME {% templatetag closevariable %}
    @{% templatetag openvariable %} manage {% templatetag closevariable %} startapp --template ../app_name {% templatetag openvariable %} APP_NAME {% templatetag closevariable %} {{ project_name }}/{% templatetag openvariable %} APP_NAME {% templatetag closevariable %}
    @sed -i '' 's/{% templatetag openvariable %} APP_NAME {% templatetag closevariable %}/{{ project_name }}\.{% templatetag openvariable %} APP_NAME {% templatetag closevariable %}/g' {{ project_name }}/{% templatetag openvariable %} APP_NAME {% templatetag closevariable %}/apps.py

###############################################
## Development
###############################################

# Install python dependencies
install-python-dev:
    @uv sync
    {% templatetag openvariable %} UV_RUN {% templatetag closevariable %} lefthook install

# Use Ansible to setup the development environment and install dependencies
setup-dev-environment: install-dev
    {% templatetag openvariable %} UV_RUN {% templatetag closevariable %} ansible-playbook ansible/00-dev-env-setup.yaml

# Install Playwright dependencies
playwright-install:
    @{% templatetag openvariable %} UV_RUN {% templatetag closevariable %} playwright install

# Create Django migrations
makemigrations:
    @{% templatetag openvariable %} manage {% templatetag closevariable %} makemigrations

# Run the linter and formatter
format:
    @{% templatetag openvariable %} UV_RUN {% templatetag closevariable %} ruff check --fix
    @{% templatetag openvariable %} UV_RUN {% templatetag closevariable %} ruff format

# Create a Django superuser
createsuperuser *FLAGS:
    @{% templatetag openvariable %} manage {% templatetag closevariable %} createsuperuser {% templatetag openvariable %} FLAGS {% templatetag closevariable %}

# Remove all Django migrations
[working-directory: '{{ project_name }}']
clean-migrations:
    @find . -path "*/migrations/*.py" -not -name "__init__.py" -not -path "./.venv/*" -type f -delete

# Reset the database
reset-db:
    @{% templatetag openvariable %} manage {% templatetag closevariable %} reset_db --noinput

# Run type checking with mypy
typecheck:
    @{% templatetag openvariable %} UV_RUN {% templatetag closevariable %} mypy {{ project_name }}

###############################################
## Frontend
###############################################

# Install frontend dependencies
[working-directory: 'frontend/{{ project_name }}']
install-frontend-dev:
    @{% templatetag openvariable %} PNPM {% templatetag closevariable %} install

# Build the frontend
[working-directory: 'frontend/{{ project_name }}']
build-frontend:
    @{% templatetag openvariable %} PNPM {% templatetag closevariable %} build

# Run the frontend development server
[working-directory: 'frontend/{{ project_name }}']
dev-frontend:
    @{% templatetag openvariable %} PNPM {% templatetag closevariable %} dev
