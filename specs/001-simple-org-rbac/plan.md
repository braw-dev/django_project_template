# Implementation Plan: Simple Organisation RBAC

**Branch**: `001-simple-org-rbac` | **Date**: 2026-01-03 | **Spec**: [specs/001-simple-org-rbac/spec.md](spec.md)
**Input**: Feature specification from `/specs/001-simple-org-rbac/spec.md`

## Summary

Replace `django-guardian` with a custom `Organisation -> Team -> User` RBAC system. This involves creating a new `organizations` app, defining `Organisation`, `Team`, `Role` (with JSON permissions), and Membership models. We will use `django-rules` for permission logic, implementing predicates and rules to handle cascading permissions (Org Admin -> Team access). Includes middleware for access control and template tags for UI logic.

## Technical Context

**Language/Version**: Python 3.13+ (Django 5+)
**Primary Dependencies**: `django-rules` (to be added), `django-guardian` (to be removed).
**Storage**: SQLite/PostgreSQL (Standard Django ORM).
**Testing**: `pytest` for unit tests.
**Target Platform**: Web application (Django Template + React Hybrid).
**Project Type**: Django Project Template.
**Performance Goals**: Efficient permission checks (minimize DB queries via caching or efficient queries).
**Constraints**: Must support "Grug Brain" simplicity. JSON permissions allow flexibility without schema changes.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Grug Brain**: Yes. `django-rules` is simpler than `guardian` for this specific hierarchical use case. JSON permissions avoid complex M2M tables for granular permissions.
- **Security First**: Yes. Explicit rules and middleware/decorators to enforce access.
- **Boring Technology**: Yes. Standard Django models + `django-rules` (established package).
- **One Stack**: Yes. Python/Django.

## Project Structure

### Documentation (this feature)

```text
specs/001-simple-org-rbac/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output (Empty, internal feature)
└── tasks.md             # Phase 2 output
```

### Source Code (repository root)

```text
project_name/
├── project_name/
│   ├── organizations/         # NEW APP
│   │   ├── __init__.py-tpl
│   │   ├── admin.py-tpl
│   │   ├── apps.py-tpl
│   │   ├── decorators.py-tpl  # Custom decorators
│   │   ├── migrations/
│   │   ├── models.py-tpl      # Org, Team, Role, Members
│   │   ├── predicates.py-tpl  # django-rules predicates
│   │   ├── rules.py-tpl       # django-rules configuration
│   │   ├── services.py-tpl    # Logic for adding members, etc.
│   │   ├── templatetags/
│   │   │   ├── __init__.py-tpl
│   │   │   └── org_permissions.py-tpl # Template tags
│   │   └── tests.py-tpl
│   ├── settings.py-tpl        # Remove guardian, add rules, add organizations
│   └── ...
pyproject.toml                 # Update dependencies
```

**Structure Decision**: Create a new `organizations` app to encapsulate all RBAC logic, keeping it separate from `users` and `core`.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| None | | |
