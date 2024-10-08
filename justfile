#!/usr/bin/env just --justfile

# Default recipe to display help information (in order of this file)
_default:
  @just --list --unsorted

# Variables
SAAS_DIR := {{project_name}}
# SAAS_DIR := "."
PIPENV_RUN := "pipenv run"

###############################################
## Testing related targets
###############################################

test_command := PIPENV_RUN + "python -Wa manage.py test"
test_options := "--shuffle --parallel=auto"

# Run fast tests (excludes browser tests)
test-fast:
	@cd {{SAAS_DIR}}; {{test_command}} {{test_options}} --exclude-tag=browser

# Run fast tests in watch mode
test-fast-watch:
	@cd {{SAAS_DIR}}; rg --files -t python,html | entr {{test_command}} {{test_options}} --exclude-tag=browser

# Run browser tests (uses Playwright)
test-browser:
	@cd {{SAAS_DIR}}; {{test_command}} {{test_options}} --tag=browser

# Run all tests
test:
	@cd {{SAAS_DIR}}; {{test_command}} {{test_options}}

# Run all tests in watch mode
test-watch:
	@cd {{SAAS_DIR}}; rg --files -t python -t html | entr {{test_command}} {{test_options}}

###############################################
## Django management
###############################################

# Run the development server
runserver:
	@cd {{SAAS_DIR}}; {{PIPENV_RUN}} python manage.py runserver

# Run Django migrations
migrate:
	@cd {{SAAS_DIR}}; {{PIPENV_RUN}} python manage.py migrate

# Collect static files
collectstatic:
	@cd {{SAAS_DIR}}; {{PIPENV_RUN}} python manage.py collectstatic --noinput

###############################################
## Development
###############################################

# Install python dependencies
install:
	@pipenv install --dev
	{{PIPENV_RUN}} pre-commit install

# Use Ansible to setup the development environment and install dependencies
setup-dev-environment: install
    {{PIPENV_RUN}} ansible-playbook ansible/00-dev-env-setup.yaml

# Install Playwright dependencies
playwright-install:
	@{{PIPENV_RUN}} playwright install

# Create Django migrations
makemigrations:
	@cd {{SAAS_DIR}}; {{PIPENV_RUN}} python manage.py makemigrations

# Run the linter and formatter
format:
	@{{PIPENV_RUN}} ruff check --fix
	@{{PIPENV_RUN}} ruff format

# Create a Django superuser
createsuperuser:
	@cd {{SAAS_DIR}}; {{PIPENV_RUN}} python manage.py createsuperuser

# Remove all Django migrations
rm-migrations:
	@cd {{SAAS_DIR}}; find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
	@cd {{SAAS_DIR}}; find . -path "*/migrations/*.pyc"  -delete

# Reset the database
reset-db:
	@cd {{SAAS_DIR}}; {{PIPENV_RUN}} python manage.py reset_db --noinput

# Run type checking with mypy
typecheck: 
	@{{PIPENV_RUN}} mypy {{SAAS_DIR}}