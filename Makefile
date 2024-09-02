.DEFAULT_GOAL := help

SAAS_DIR := {{ project_name }}
PIPENV_RUN := pipenv run

.PHONY: help

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

###############################################
## Testing related targets
###############################################

test_command := ${PIPENV_RUN} python -Wa manage.py test
test_options := --shuffle --parallel=auto

.PHONY: test-fast
test-fast: ## Run fast tests (excludes browser tests)
	@cd ${SAAS_DIR}; ${test_command} ${test_options} --exclude-tag=browser

.PHONY: test-fast-watch
test-fast-watch: ## Run all tests in watch mode
	@cd ${SAAS_DIR}; rg --files -t python -t html | entr ${test_command} ${test_options} --exclude-tag=browser

.PHONY: test-browser
test-browser: ## Run browser tests (uses Playwright)
	@cd ${SAAS_DIR}; ${test_command} ${test_options} --tag=browser

.PHONY: test
test:  ## Run all tests
	@cd ${SAAS_DIR}; ${test_command} ${test_options}

.PHONY: test-watch
test-watch: ## Run all tests in watch mode
	@cd ${SAAS_DIR}; rg --files -t python -t html | entr ${test_command} ${test_options}

###############################################
## Django management
###############################################

.PHONY: runserver
runserver: ## Run the development server
	@cd ${SAAS_DIR}; ${PIPENV_RUN} python manage.py runserver

.PHONY: migrate
migrate: ## Run Django migrations
	@cd ${SAAS_DIR}; ${PIPENV_RUN} python manage.py migrate

.PHONY: collectstatic
collectstatic: ## Collect static files
	@cd ${SAAS_DIR}; ${PIPENV_RUN} python manage.py collectstatic --noinput

###############################################
## Development
###############################################

.PHONY: install
install: ## Install python dependencies
	@pipenv install --dev
	${PIPENV_RUN} pre-commit install

.PHONY: playwright-install
playwright-install: ## Install Playwright dependencies
	@${PIPENV_RUN} playwright install

.PHONY: makemigrations
makemigrations: ## Create Django migrations
	@cd ${SAAS_DIR}; ${PIPENV_RUN} python manage.py makemigrations

.PHONY: format
format: ## Run the linter and formatter
	@${PIPENV_RUN} ruff check --fix
	@${PIPENV_RUN} ruff format

.PHONY: createsuperuser
createsuperuser: ## Create a Django superuser
	@cd ${SAAS_DIR}; ${PIPENV_RUN} python manage.py createsuperuser

.PHONY: rm-migrations
rm-migrations: ## Remove all Django migrations
	@cd ${SAAS_DIR}; find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
	@cd ${SAAS_DIR}; find . -path "*/migrations/*.pyc"  -delete

.PHONY: reset-db
reset-db: ## Reset the database
	@cd ${SAAS_DIR}; ${PIPENV_RUN} python manage.py reset_db --noinput

.PHONY: typecheck
typecheck: ## Run type checking with mypy
	@${PIPENV_RUN} mypy ${SAAS_DIR}