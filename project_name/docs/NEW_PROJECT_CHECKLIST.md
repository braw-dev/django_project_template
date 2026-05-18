# New Project Checklist

Use this checklist when you generate a new project from this template.

This document is intentionally practical. It is not the full architecture guide. It is the short list of things to do before you forget them.

## 1. Immediately after generation

- [ ] Copy `{{ project_name }}/.env.dist` to `{{ project_name }}/.env`
- [ ] For local development, change these defaults in `{{ project_name }}/.env`:
  - [ ] `DEBUG=True`
  - [ ] `ENVIRONMENT=development`
  - [ ] `SEND_EMAILS=False`
  - [ ] `LOG_LEVEL=INFO`
  - [ ] `DB_DEFAULT_URL=sqlite:///db.sqlite3`
  - [ ] `CACHE_DEFAULT_URL=locmemcache://`
- [ ] Run `just install-dev`
- [ ] Run `just migrate`
- [ ] Run `just test-unit`
- [ ] Fill in `docs/PRODUCT_OVERVIEW.md`
- [ ] Search for `REPLACE_ME:` and replace every placeholder before sharing the app more widely
- [ ] Review `README.md`, `DEPLOYMENT.md`, and `SECURITY.md` once so you know what the template already assumes

## 2. Before the first deploy

- [ ] Set a real `SITE_DOMAIN`
- [ ] Set real `ALLOWED_HOSTS`
- [ ] Set real `EMAIL_DOMAIN`
- [ ] Set real `DJANGO_ADMINS`
- [ ] Confirm `SECRET_KEY` is unique for this project and kept out of the repo
- [ ] Decide on your production database, cache, and hosting layout
- [ ] Set `TRUSTED_PROXY_IPS` if Django will sit behind a real reverse proxy
- [ ] Set `SENTRY_DSN`
- [ ] Build the frontend once with `just build-frontend`
- [ ] Run `just collectstatic`
- [ ] Run a basic health check with `just manage check`, `/api/v1/health`, and `/api/v1/health/live`

## 3. Before sharing with anyone outside development

- [ ] Create a superuser with `just createsuperuser`
- [ ] Verify login, logout, email verification, and MFA setup flows
- [ ] Verify the built-in language switcher and, if you use React islands, confirm they follow the same selected language
- [ ] Confirm security notification emails and reauthentication-sensitive actions behave the way you expect
- [ ] Review whether support hijack should stay enabled in this project

## 4. Before charging money

- [ ] Decide whether the project will actually use the built-in billing foundation
- [ ] If yes, complete the setup in `{{ project_name }}/billing/README.md`
- [ ] Test checkout end to end
- [ ] Test the billing portal flow end to end
- [ ] Test webhook delivery and confirm local billing state updates correctly
- [ ] Review your pricing copy, VAT stance, and customer-facing billing wording before exposing pricing publicly

## 5. Before first customer access

- [ ] Replace the seeded Privacy, Terms, Security, Subprocessors, Contact, and support FAQ placeholder content
- [ ] Verify that your trust pages describe your real providers, regions, subprocessors, backup posture, and support process
- [ ] Decide how backups will work and document the restore process you will actually follow
- [ ] Decide how privacy export/delete should behave for your app-specific data before using those workflows in production
- [ ] Decide whether Plausible and Chatwoot will be enabled, and verify consent behavior if they are
- [ ] Do one end-to-end smoke test as a real user from signup/login through the main product flow

## 6. Useful follow-up docs

- `README.md` - generated project overview and setup
- `DEPLOYMENT.md` - default production shape and operational assumptions
- `SECURITY.md` - security model and invariants
- `docs/frontend-i18n.md` - Django/React island language bridge
- `{{ project_name }}/billing/README.md` - billing setup and operational stance

## Notes for future-you

If you are starting a second or third product from this template later, start here first.

The main failure mode is not missing functionality in the template. It is forgetting to replace placeholders, forgetting to document operational choices, or assuming "I'll do that before launch" and then shipping anyway.
