<!--
Sync Impact Report:
- Version change: New -> 1.0.0
- Modified principles: Initial creation based on project rules and motivation.
- Added sections: Core Principles (Grug Brain, Security First, Boring Technology, Internationalisation First, MVP & Speed), Architecture & Patterns, Development Workflow.
- Templates requiring updates:
  - .specify/templates/plan-template.md: ✅ (Compatible)
  - .specify/templates/spec-template.md: ✅ (Compatible)
  - .specify/templates/tasks-template.md: ✅ (Compatible)
- Follow-up TODOs: None.
-->

# Django Project Template Constitution

## Core Principles

### I. Grug Brain (Simplicity)

Complexity is the enemy. Fight it always. Simple code that works beats clever code that might work. If you can't explain it simply, it's too complex.

- **Say No**: To features unless they serve users; to abstractions until needed 3 times; to new dependencies unless they save significant time.
- **Code is Liability**: Delete code whenever possible. The best code is no code.
- **Debugging > Cleverness**: Explicit beats implicit. Boring beats clever.

### II. Security First

Security by default. This enables a solo developer to maintain a portfolio of SaaS projects securely.

- **Authentication**: Use `django-allauth`. Never write custom authentication code.
- **Data Handling**: Minimize data collection. Sanitize user content with `nh3`. Store secrets in environment variables.
- **Validation**: Validate at boundaries. Trust internal code.
- **Verification**: Human review required for auth, permissions, payment logic, and PII handling.

### III. Boring Technology (One Stack)

Stick to the defined stack: Django, Python, React/Vite (optional), Tailwind CSS, PostgreSQL/SQLite.

- **Consistency**: Consistency across projects beats "best tool for the job".
- **No New Stacks**: Don't introduce new languages or frameworks lightly. Learning and maintenance costs compound.
- **Use Built-ins**: Prefer Django's built-in solutions and the ORM over third-party packages or raw SQL.

### IV. Internationalisation First

Support translations from the start to avoid technical debt later.

- **No Hardcoded Strings**: Absolutely NO user-facing strings shall be hardcoded in Python or templates.
- **Use Translation Tools**: Wrap strings in `gettext_lazy` / `_()` or `{% templatetag openblock %} translate {% templatetag closeblock %}` tags.
- **Localization**: Use Django's localization tools for dates and numbers.

### V. MVP & Speed

Working software beats perfect plans.

- **Ship It**: Ship, measure, iterate. Done is better than perfect.
- **Monolithic First**: Keep business logic in Django apps. Don't extract microservices prematurely.
- **Focus**: Solve today's problems, not "what if" scenarios.

## Architecture & Patterns

Follow the defined Django stack architecture (`django-stack.mdc`).

- **MVT Pattern**: Model-View-Template with a services layer.
- **Services**: Business logic lives in `services.py` (e.g., `user_create`).
- **Selectors**: Data retrieval logic lives in `selectors.py` (e.g., `user_get_by_email`).
- **Components**: Use `django-cotton` for reusable UI components.
- **API**: Use `django-ninja` for REST endpoints.
- **Frontend**: Hybrid rendering (Django templates + React/Vite for interactivity).

## Development Workflow

- **Operational Excellence**: Use `Justfile` for all commands (`just install-dev`, `just test-unit`, `just format`).
- **Testing**: Test-First mentality. Use `pytest` for unit tests and `playwright` for E2E.
- **Quality Gates**: `ruff` for linting/formatting is enforced via `lefthook`.
- **Documentation**: Update `README.md` or `MOTIVATION.md` if architectural changes are made.

## Governance

- **Supremacy**: This Constitution supersedes other documentation practices unless explicitly amended.
- **Amendments**: Changes to principles require a Pull Request, justification, and version bump.
- **Compliance**: All PRs must verify compliance with these principles.
- **Reference**: See `ai/rules/` for detailed runtime guidance.

**Version**: 1.0.0 | **Ratified**: 2026-01-02 | **Last Amended**: 2026-01-02
