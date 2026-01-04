# Implementation Plan: Polar.sh Payment Boilerplate

**Branch**: `002-add-polar-payments` | **Date**: 2026-01-04 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/002-add-polar-payments/spec.md`

## Summary

Add production-ready Polar.sh payment boilerplate to the Django template. This includes a `billing` app with subscription models, webhook handling, checkout/portal URL generation, and entitlement checks. The integration uses the official `polar-sdk`, `standardwebhooks` for signature verification, and `django-ninja` for API endpoints. Business logic hooks are stubbed with `NotImplementedError` for project-specific customization.

## Technical Context

**Language/Version**: Python 3.13+ (per existing `pyproject.toml`)
**Primary Dependencies**:

- `polar-sdk` (already installed) - Official Polar.sh Python SDK
- `standardwebhooks` (already installed via polar-sdk) - Webhook signature verification
- `django-ninja` (already installed) - REST API endpoints with Pydantic schemas
- `pydantic` (already installed via django-ninja) - Data validation

**Storage**: PostgreSQL (production), SQLite (development/test) - uses existing Django ORM
**Testing**: `pytest-django` (unit), `playwright` (E2E)
**Target Platform**: Django 5.x web application
**Project Type**: Django Template (files use `.py-tpl` extension)
**Performance Goals**: Webhook processing < 500ms, Entitlement checks < 10ms (local DB)
**Constraints**: Security-first (signature verification mandatory), no plaintext secrets
**Scale/Scope**: Single `billing` app, ~8 files, minimal footprint

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| **I. Grug Brain** | ✅ PASS | Single app, minimal abstraction, stubs for customization |
| **II. Security First** | ✅ PASS | Webhook signature verification, CSRF exempt only for verified webhooks, secrets in env vars |
| **III. Boring Technology** | ✅ PASS | Uses existing stack (Django, django-ninja, Pydantic), no new languages/frameworks |
| **IV. Internationalisation** | ✅ PASS | All user-facing strings wrapped in `gettext_lazy` |
| **V. MVP & Speed** | ✅ PASS | Provides working foundation, stubs for project-specific logic |

## Project Structure

### Documentation (this feature)

```text
specs/002-add-polar-payments/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output
│   └── webhooks.md
└── tasks.md             # Phase 2 output (from /speckit.tasks)
```

### Source Code (repository root)

```text
project_name/project_name/
├── billing/                          # NEW: Billing app
│   ├── __init__.py-tpl
│   ├── admin.py-tpl                  # Admin registration for Subscription
│   ├── apps.py-tpl                   # BillingConfig
│   ├── migrations/
│   │   └── __init__.py-tpl
│   ├── models.py-tpl                 # Subscription model
│   ├── selectors.py-tpl              # has_active_subscription, get_subscription
│   ├── services.py-tpl               # BillingService (Polar SDK wrapper)
│   ├── webhooks.py-tpl               # Webhook handlers
│   └── tests.py-tpl                  # Unit tests
├── core/
│   └── api/
│       ├── __init__.py-tpl           # MODIFY: Export billing API
│       └── billing_v1.py-tpl         # NEW: Billing API endpoints
└── settings.py-tpl                   # MODIFY: Add billing to INSTALLED_APPS
```

**Structure Decision**: New `billing` app follows existing app pattern (see `organizations/`). API endpoints added to existing `core/api/` structure using django-ninja.

## Complexity Tracking

> No violations. All choices align with Constitution.

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| *None* | — | — |
