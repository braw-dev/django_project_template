#!/usr/bin/env just --justfile

# Default recipe to display help information (in order of this file)
_default:
    @just --list --unsorted

# Variables

export PIPENV_VENV_IN_PROJECT := ""
SAAS_DIR := "{{project_name}}"
PROJECT_DIR := SAAS_DIR + "/" + SAAS_DIR
PIPENV_RUN := "pipenv run"

###############################################
## Testing related targets
###############################################

test_command := PIPENV_RUN + " python manage.py test"
test_options := " --shuffle --parallel=auto"

# Run fast tests (excludes browser tests)
test-fast:
    @cd {% templatetag openvariable %} SAAS_DIR {% templatetag closevariable %}; {% templatetag openvariable %} test_command {% templatetag closevariable %} {% templatetag openvariable %} test_options {% templatetag closevariable %} --exclude-tag=browser

# Run fast tests in watch mode
test-fast-watch:
    @cd {% templatetag openvariable %} SAAS_DIR {% templatetag closevariable %}; rg --files -t python,html | entr {% templatetag openvariable %} test_command {% templatetag closevariable %} {% templatetag openvariable %} test_options {% templatetag closevariable %} --exclude-tag=browser

# Run browser tests (uses Playwright)
test-browser:
    @cd {% templatetag openvariable %} SAAS_DIR {% templatetag closevariable %}; {% templatetag openvariable %} test_command {% templatetag closevariable %} {% templatetag openvariable %} test_options {% templatetag closevariable %} --tag=browser

# Run all tests
test:
    @cd {% templatetag openvariable %} SAAS_DIR {% templatetag closevariable %}; {% templatetag openvariable %} test_command {% templatetag closevariable %} {% templatetag openvariable %} test_options {% templatetag closevariable %}

# Run all tests in watch mode
test-watch:
    @cd {% templatetag openvariable %} SAAS_DIR {% templatetag closevariable %}; rg --files -t python -t html | entr {% templatetag openvariable %} test_command {% templatetag closevariable %} {% templatetag openvariable %} test_options {% templatetag closevariable %}

###############################################
## Django management
###############################################

manage := "cd " + SAAS_DIR + ";" + PIPENV_RUN + " python manage.py"

# Shortcut to run Django management commands
manage *ARGS:
    @{% templatetag openvariable %} manage {% templatetag closevariable %} {% templatetag openvariable %} ARGS {% templatetag closevariable %}

# Run the development server
runserver:
    @{% templatetag openvariable %} manage {% templatetag closevariable %} runserver

# Run Django migrations
migrate:
    @{% templatetag openvariable %} manage {% templatetag closevariable %} migrate

# Collect static files
collectstatic:
    @{% templatetag openvariable %} manage {% templatetag closevariable %} collectstatic --noinput

# Create a new Django app in the correct directory
startapp APP_NAME:
    @cd {% templatetag openvariable %} PROJECT_DIR {% templatetag closevariable %} && mkdir -p {% templatetag openvariable %} APP_NAME {% templatetag closevariable %}
    @{% templatetag openvariable %} manage {% templatetag closevariable %} startapp {% templatetag openvariable %} APP_NAME {% templatetag closevariable %} {% templatetag openvariable %} SAAS_DIR {% templatetag closevariable %}/{% templatetag openvariable %} APP_NAME {% templatetag closevariable %}
    @cd {% templatetag openvariable %} PROJECT_DIR {% templatetag closevariable %} && sed -i '' 's/{% templatetag openvariable %} APP_NAME {% templatetag closevariable %}/{% templatetag openvariable %} SAAS_DIR {% templatetag closevariable %}\.{% templatetag openvariable %} APP_NAME {% templatetag closevariable %}/g' {% templatetag openvariable %} APP_NAME {% templatetag closevariable %}/apps.py

###############################################
## Development
###############################################

# Install python dependencies
install:
    @pipenv install --dev
    {% templatetag openvariable %} PIPENV_RUN {% templatetag closevariable %} pre-commit install

# Use Ansible to setup the development environment and install dependencies
setup-dev-environment: install
    {% templatetag openvariable %} PIPENV_RUN {% templatetag closevariable %} ansible-playbook ansible/00-dev-env-setup.yaml

# Install Playwright dependencies
playwright-install:
    @{% templatetag openvariable %} PIPENV_RUN {% templatetag closevariable %} playwright install

# Create Django migrations
makemigrations:
    @{% templatetag openvariable %} manage {% templatetag closevariable %} makemigrations

# Run the linter and formatter
format:
    @{% templatetag openvariable %} PIPENV_RUN {% templatetag closevariable %} ruff check --fix
    @{% templatetag openvariable %} PIPENV_RUN {% templatetag closevariable %} ruff format

# Create a Django superuser
createsuperuser *FLAGS:
    @{% templatetag openvariable %} manage {% templatetag closevariable %} createsuperuser {% templatetag openvariable %} FLAGS {% templatetag closevariable %}

# Remove all Django migrations
rm-migrations:
    @cd {% templatetag openvariable %} SAAS_DIR {% templatetag closevariable %}; find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
    @cd {% templatetag openvariable %} SAAS_DIR {% templatetag closevariable %}; find . -path "*/migrations/*.pyc"  -delete

# Reset the database
reset-db:
    @{% templatetag openvariable %} manage {% templatetag closevariable %} reset_db --noinput

# Run type checking with mypy
typecheck:
    @{% templatetag openvariable %} PIPENV_RUN {% templatetag closevariable %} mypy {% templatetag openvariable %} SAAS_DIR {% templatetag closevariable %}

# Translate any i18n strings with DeepL (requires a DeepL API key)
translate:
    @{% templatetag openvariable %} manage {% templatetag closevariable %} django-polyglot translate
