# Claude Code Instructions

This file provides core instructions for Claude Code when working on this Django Project Template and projects generated from it.

## Overview

You are working with a **Django Project Template** designed for a company of one building a portfolio of SaaS projects. The primary goals are:

1. **Security by default** - Never compromise on security
2. **Simplicity above all** - Grug brain philosophy (see docs/grug-brain.md)
3. **Boring technology** - Proven, stable, maintainable
4. **Cost-effective** - Optimized for solo developers and small teams

## Critical Context Detection

Before making ANY changes, determine the context:

### Are you working on the TEMPLATE itself?

**Indicators:**

- File paths contain `{{ project_name }}` template variables
- Files end in `.py-tpl` extension
- Working in `dev/` directory
- `AGENTS.md` mentions "Django Project Template"

**Rules:**

- **NEVER** replace `{{ project_name }}` with a real name
- **NEVER** "fix" Django template tags like `{% templatetag openvariable %}`
- **ALWAYS** test changes with: `uv run ansible-playbook ./dev/01-test-project-template.yaml`
- See `docs/template-development.md` for details

### Are you working on a GENERATED project?

**Indicators:**

- `{{ project_name }}` has been replaced with actual project name
- No `.py-tpl` files
- No `dev/` directory

**Rules:**

- Follow standard Django development practices
- Use `just` commands for all operations
- See `docs/django-stack.md` and `docs/development-workflow.md`

## Core Principles

### 1. Security First

- **Authentication**: Use `django-allauth`. Never write custom auth.
- **Validation**: Validate at boundaries (forms, API inputs)
- **Data Minimization**: Only collect necessary data
- **Secrets**: Environment variables only, never in code
- **Sanitization**: Use `nh3` for HTML, use ORM to prevent SQL injection

**Human review required for:**

- Authentication/authorization changes
- Payment/billing logic
- PII handling
- Database migrations that modify existing data

See `docs/security-simplicity.md`

### 2. Grug Brain Philosophy

- **Complexity is the enemy** - Fight it always
- **Say no** to features, abstractions, dependencies, "what if" scenarios
- **Code is liability** - Delete code whenever possible
- **One stack** - Don't introduce new languages/frameworks lightly
- **Ship it** - Working software beats perfect plans
- **Boring beats clever** - Explicit, readable, debuggable

See `docs/grug-brain.md`

### 3. Avoid Over-Engineering

**Don't:**

- Add features beyond what was asked
- Refactor unrelated code "while you're there"
- Add docstrings/comments to code you didn't change
- Create helpers/utilities for one-time operations
- Add error handling for scenarios that can't happen
- Use backwards-compatibility shims (delete unused code completely)
- Add "improvements" like feature flags or abstractions for hypothetical future needs

**Do:**

- Make minimal changes to accomplish the task
- Trust internal code and framework guarantees
- Only validate at system boundaries
- Keep solutions simple and focused

### 4. Django Stack Conventions

**Architecture:**

- MVT Pattern with services layer
- Hybrid rendering (Django templates + optional React)
- Django Ninja for REST APIs

**Key Patterns:**

- Business logic in `services.py`
- Data retrieval in `selectors.py`
- Use built-in Django features first
- Use the ORM (avoid raw SQL)
- Use provided User model in `users/models.py`

See `docs/django-stack.md`

## Development Workflow

### Before Making Changes

1. **Read files first** - Never propose changes to code you haven't read
2. **Check context** - Template vs generated project?
3. **Understand existing patterns** - Follow established conventions
4. **Consider security** - Security-critical changes require human review

### Making Changes

1. Use `just` commands for all operations:
   - `just install-dev` - Setup environment
   - `just runserver` - Start server
   - `just test-unit` - Run pytest tests
   - `just test-e2e` - Run Playwright tests
   - `just format` - Format code with Ruff
   - `just migrate` - Run migrations

2. **Edit existing files** - Don't create new files unless necessary
3. **Follow existing patterns** - Consistency is key
4. **Run `just format`** before finishing tasks

### After Making Changes

1. Run tests relevant to your changes
2. Format code with `just format`
3. For template changes: Test generation with Ansible playbook

## File Organization

```text
project_name/              # Template root (or project root if generated)
├── .claude/               # Claude Code instructions (this directory)
│   ├── CLAUDE.md          # Main instructions (this file)
│   └── docs/              # Detailed documentation
├── project_name/          # Django source (becomes actual name in generated)
│   ├── project_name/      # Main app (settings, urls)
│   ├── core/              # Shared models, views, utilities
│   ├── users/             # User management
│   └── <other_apps>/      # Feature apps
├── frontend/              # React/Vite frontend
├── templates/             # Django templates
├── static/                # Static assets
├── dev/                   # Template testing tools (template only)
├── Justfile               # Command runner
└── AGENTS.md              # AI agent guide
```

## Common Tasks

### Adding a New Feature

1. Determine if it fits the Grug philosophy (say no by default)
2. Use existing patterns (check similar features)
3. Put business logic in `services.py`
4. Put data retrieval in `selectors.py`
5. Write tests first (TDD encouraged with red/green refactoring)
6. Keep it simple - minimum code to solve the problem

### Fixing a Bug

1. Read the relevant code first
2. Write a failing test that demonstrates the bug
3. Fix with minimal changes
4. Don't refactor unrelated code
5. Verify the test passes

### Adding a Dependency

1. **Strong justification required** - Does it pay rent?
2. Prefer Django built-ins over third-party
3. Consider maintenance cost
4. Update `pyproject.toml` and run `uv sync`

### Database Changes

1. Create migration: `just makemigrations`
2. Review migration file
3. Test: `just migrate`
4. For data migrations: Request human review

## Code Quality Standards

### Python

- **Formatting**: Ruff (runs automatically via lefthook)
- **Type hints**: Use type hints for function signatures
- **Validation**: Use Django's built-in validators
- **Docstrings**: Only for complex business logic (not every function)

### Frontend

- **Formatting**: Biome
- **Framework**: React + Vite + Tailwind CSS + Daisy UI
- **Components**: django-cotton for reusable HTML components

### Testing

- **Unit tests**: pytest-django in `tests/`
- **E2E tests**: Playwright in `tests/e2e/tests/`
- **Coverage**: Reasonable coverage expected, not 100%

## When to Ask for Clarification

**Always ask:**

- Security-critical changes
- Architectural decisions
- Adding dependencies
- Multiple valid approaches to a problem

**Proceed autonomously:**

- Bug fixes within existing patterns
- Features using established conventions
- Refactoring that doesn't change behavior (if explicitly requested)

## Error Prevention

### Common Pitfalls to Avoid

1. **Template confusion**: Don't replace `{{ project_name }}` in template files
2. **Dependency creep**: Say no to new dependencies unless absolutely necessary
3. **Over-abstraction**: Don't create abstractions until needed 3+ times
4. **Security shortcuts**: Never compromise on auth, validation, or data handling
5. **Scope creep**: Don't add unrequested features

### Security Checklist

Before completing any task, verify:

- [ ] No hardcoded secrets or credentials
- [ ] User input is validated/sanitized
- [ ] SQL injection prevented (using ORM)
- [ ] XSS prevented (using Django's auto-escaping or nh3)
- [ ] Authentication/authorization enforced where needed
- [ ] No OWASP Top 10 vulnerabilities introduced

## Key Documentation Files

- `AGENTS.md` - AI agent guide (high-level overview)
- `MOTIVATION.md` - Project philosophy and goals
- `README.md` - Setup and usage instructions
- `.claude/docs/` - Detailed Claude Code documentation

## References

Always remember:

- [The Grug Brained Developer](https://grugbrain.dev/)
- OWASP Top 10 security risks
- Django documentation (prefer built-in solutions)
- The user's goal: Financial freedom through a portfolio of simple SaaS projects
