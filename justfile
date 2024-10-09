#!/usr/bin/env just --justfile

# Default recipe to display help information (in order of this file)
_default:
  @just --list --unsorted

# Variables
SAAS_DIR := "{{project_name}}"
# SAAS_DIR := "."
PIPENV_RUN := "pipenv run"

###############################################
## Testing related targets
###############################################

test_command := PIPENV_RUN + " python -Wa manage.py test"
test_options := " --shuffle --parallel=auto"

# Run fast tests (excludes browser tests)
test-fast:
	@cd {% templatetag openvariable %}SAAS_DIR{% templatetag closevariable %}; {% templatetag openvariable %}test_command{% templatetag closevariable %} {% templatetag openvariable %}test_options{% templatetag closevariable %} --exclude-tag=browser

# Run fast tests in watch mode
test-fast-watch:
	@cd {% templatetag openvariable %}SAAS_DIR{% templatetag closevariable %}; rg --files -t python,html | entr {% templatetag openvariable %}test_command{% templatetag closevariable %} {% templatetag openvariable %}test_options{% templatetag closevariable %} --exclude-tag=browser

# Run browser tests (uses Playwright)
test-browser:
	@cd {% templatetag openvariable %}SAAS_DIR{% templatetag closevariable %}; {% templatetag openvariable %}test_command{% templatetag closevariable %} {% templatetag openvariable %}test_options{% templatetag closevariable %} --tag=browser

# Run all tests
test:
	@cd {% templatetag openvariable %}SAAS_DIR{% templatetag closevariable %}; {% templatetag openvariable %}test_command{% templatetag closevariable %} {% templatetag openvariable %}test_options{% templatetag closevariable %}

# Run all tests in watch mode
test-watch:
	@cd {% templatetag openvariable %}SAAS_DIR{% templatetag closevariable %}; rg --files -t python -t html | entr {% templatetag openvariable %}test_command{% templatetag closevariable %} {% templatetag openvariable %}test_options{% templatetag closevariable %}

###############################################
## Django management
###############################################

# Run the development server
runserver:
	@cd {% templatetag openvariable %}SAAS_DIR{% templatetag closevariable %}; {% templatetag openvariable %}PIPENV_RUN{% templatetag closevariable %} python manage.py runserver

# Run Django migrations
migrate:
	@cd {% templatetag openvariable %}SAAS_DIR{% templatetag closevariable %}; {% templatetag openvariable %}PIPENV_RUN{% templatetag closevariable %} python manage.py migrate

# Collect static files
collectstatic:
	@cd {% templatetag openvariable %}SAAS_DIR{% templatetag closevariable %}; {% templatetag openvariable %}PIPENV_RUN{% templatetag closevariable %} python manage.py collectstatic --noinput

###############################################
## Development
###############################################

# Install python dependencies
install:
	@pipenv install --dev
	{% templatetag openvariable %}PIPENV_RUN{% templatetag closevariable %} pre-commit install

# Use Ansible to setup the development environment and install dependencies
setup-dev-environment: install
    {% templatetag openvariable %}PIPENV_RUN{% templatetag closevariable %} ansible-playbook ansible/00-dev-env-setup.yaml

# Install Playwright dependencies
playwright-install:
	@{% templatetag openvariable %}PIPENV_RUN{% templatetag closevariable %} playwright install

# Create Django migrations
makemigrations:
	@cd {% templatetag openvariable %}SAAS_DIR{% templatetag closevariable %}; {% templatetag openvariable %}PIPENV_RUN{% templatetag closevariable %} python manage.py makemigrations

# Run the linter and formatter
format:
	@{% templatetag openvariable %}PIPENV_RUN{% templatetag closevariable %} ruff check --fix
	@{% templatetag openvariable %}PIPENV_RUN{% templatetag closevariable %} ruff format

# Create a Django superuser
createsuperuser:
	@cd {% templatetag openvariable %}SAAS_DIR{% templatetag closevariable %}; {% templatetag openvariable %}PIPENV_RUN{% templatetag closevariable %} python manage.py createsuperuser

# Remove all Django migrations
rm-migrations:
	@cd {% templatetag openvariable %}SAAS_DIR{% templatetag closevariable %}; find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
	@cd {% templatetag openvariable %}SAAS_DIR{% templatetag closevariable %}; find . -path "*/migrations/*.pyc"  -delete

# Reset the database
reset-db:
	@cd {% templatetag openvariable %}SAAS_DIR{% templatetag closevariable %}; {% templatetag openvariable %}PIPENV_RUN{% templatetag closevariable %} python manage.py reset_db --noinput

# Run type checking with mypy
typecheck: 
	@{% templatetag openvariable %}PIPENV_RUN{% templatetag closevariable %} mypy {% templatetag openvariable %}SAAS_DIR{% templatetag closevariable %}