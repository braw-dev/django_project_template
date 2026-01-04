# Tasks: Polar.sh Payment Boilerplate

**Input**: Design documents from `/specs/002-add-polar-payments/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

**Tests**: Not explicitly requested in specification. Included minimal tests for webhook security verification.

**Organization**: Tasks grouped by user story (US1, US2, US3) to enable independent implementation.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1, US2, US3)
- All file paths use `.py-tpl` extension (Django template project)

## Path Conventions

- **App location**: `project_name/project_name/billing/`
- **API location**: `project_name/project_name/core/api/`
- **Settings**: `project_name/project_name/settings.py-tpl`

---

## Phase 1: Setup (Billing App Structure)

**Purpose**: Create the billing app directory structure and boilerplate files

- [ ] T001 Create billing app directory at `project_name/project_name/billing/`
- [ ] T002 [P] Create `project_name/project_name/billing/__init__.py-tpl` (empty file)
- [ ] T003 [P] Create `project_name/project_name/billing/apps.py-tpl` with BillingConfig class
- [ ] T004 [P] Create `project_name/project_name/billing/migrations/__init__.py-tpl` (empty file)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T005 Add `{{ project_name }}.billing` to INSTALLED_APPS in `project_name/project_name/settings.py-tpl`
- [ ] T006 Create Subscription model in `project_name/project_name/billing/models.py-tpl` with all fields from data-model.md
- [ ] T007 Create initial migration for Subscription model in `project_name/project_name/billing/migrations/0001_initial.py-tpl`
- [ ] T008 [P] Register Subscription in admin at `project_name/project_name/billing/admin.py-tpl`

**Checkpoint**: Foundation ready - Subscription model exists and is registered

---

## Phase 3: User Story 1 - Developer Payment Infrastructure (Priority: P1) 🎯 MVP

**Goal**: Core Polar.sh integration with models, webhooks, and services pre-configured

**Independent Test**: Simulate Polar.sh webhooks and verify local Subscription records are created/updated

### Implementation for User Story 1

- [ ] T009 [US1] Create webhook signature verification helper in `project_name/project_name/billing/webhooks.py-tpl`
- [ ] T010 [US1] Implement `handle_subscription_created()` handler in `project_name/project_name/billing/webhooks.py-tpl`
- [ ] T011 [US1] Implement `handle_subscription_updated()` handler in `project_name/project_name/billing/webhooks.py-tpl`
- [ ] T012 [US1] Implement `handle_subscription_revoked()` handler in `project_name/project_name/billing/webhooks.py-tpl`
- [ ] T013 [US1] Implement `handle_subscription_canceled()` handler in `project_name/project_name/billing/webhooks.py-tpl`
- [ ] T014 [US1] Add stub hooks (`on_subscription_created`, etc.) with NotImplementedError in `project_name/project_name/billing/webhooks.py-tpl`
- [ ] T015 [US1] Create webhook API endpoint in `project_name/project_name/core/api/billing_v1.py-tpl` using django-ninja
- [ ] T016 [US1] Export billing API in `project_name/project_name/core/api/__init__.py-tpl`
- [ ] T017 [US1] Add webhook URL route to `project_name/project_name/urls.py-tpl`
- [ ] T018 [US1] Create unit tests for webhook handlers in `project_name/project_name/billing/tests.py-tpl`

**Checkpoint**: Webhooks receive events, verify signatures, and update Subscription records

---

## Phase 4: User Story 2 - Subscription Entitlement Checks (Priority: P2)

**Goal**: Simple, standardized way to check if an organization has an active subscription

**Independent Test**: Unit tests that set up various subscription states and assert entitlement check return values

### Implementation for User Story 2

- [ ] T019 [P] [US2] Implement `has_active_subscription(organisation)` selector in `project_name/project_name/billing/selectors.py-tpl`
- [ ] T020 [P] [US2] Implement `get_active_subscription(organisation)` selector in `project_name/project_name/billing/selectors.py-tpl`
- [ ] T021 [P] [US2] Implement `get_subscription_by_polar_id(polar_id)` selector in `project_name/project_name/billing/selectors.py-tpl`
- [ ] T022 [US2] Add GET `/api/v1/billing/subscription/` endpoint in `project_name/project_name/core/api/billing_v1.py-tpl`
- [ ] T023 [US2] Add unit tests for selectors in `project_name/project_name/billing/tests.py-tpl`

**Checkpoint**: Entitlement checks return correct boolean values for all subscription states

---

## Phase 5: User Story 3 - Checkout and Portal Redirects (Priority: P3)

**Goal**: Generate Polar checkout URLs and customer portal URLs

**Independent Test**: Call service functions and verify they return valid URLs (mocking Polar SDK)

### Implementation for User Story 3

- [ ] T024 [US3] Create BillingService class in `project_name/project_name/billing/services.py-tpl` with Polar SDK initialization
- [ ] T025 [US3] Implement `create_checkout_url()` in `project_name/project_name/billing/services.py-tpl`
- [ ] T026 [US3] Implement stub `get_customer_portal_url()` with NotImplementedError in `project_name/project_name/billing/services.py-tpl`
- [ ] T027 [US3] Implement `get_products()` with optional caching in `project_name/project_name/billing/services.py-tpl`
- [ ] T028 [US3] Add POST `/api/v1/billing/checkout/` endpoint in `project_name/project_name/core/api/billing_v1.py-tpl`
- [ ] T029 [US3] Update existing `product_list()` in `project_name/project_name/selectors.py-tpl` to use BillingService
- [ ] T030 [US3] Add Pydantic schemas for billing endpoints in `project_name/project_name/core/api/billing_v1.py-tpl`

**Checkpoint**: Checkout URLs are generated and returned via API

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Documentation, cleanup, and validation

- [ ] T031 [P] Create `project_name/project_name/billing/README.md` with usage documentation
- [ ] T032 [P] Update main `README.md` to mention billing/payments feature
- [ ] T033 Validate all strings use `gettext_lazy` in billing app
- [ ] T034 Run `just format` and fix any linting issues
- [ ] T035 Test template generation with `uv run ansible-playbook ./dev/01-test-project-template.yaml`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-5)**: All depend on Foundational phase completion
- **Polish (Phase 6)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Core infrastructure - webhook handling
- **User Story 2 (P2)**: Uses Subscription model from US1, but independently testable
- **User Story 3 (P3)**: Uses Subscription model, can run parallel with US2

### Within Each User Story

- Services/handlers before API endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

**Setup Phase (T002-T004)**:

```text
T002: billing/__init__.py-tpl
T003: billing/apps.py-tpl
T004: billing/migrations/__init__.py-tpl
```

**Foundational Phase (T006, T008)**:

```text
T006: billing/models.py-tpl (after T005)
T008: billing/admin.py-tpl (after T006)
```

**User Story 2 (T019-T021)**:

```text
T019: has_active_subscription selector
T020: get_active_subscription selector
T021: get_subscription_by_polar_id selector
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1 (Webhook infrastructure)
4. **STOP and VALIDATE**: Test webhook processing independently
5. Deploy/demo if ready

### Incremental Delivery

1. Setup + Foundational → Subscription model exists
2. Add User Story 1 → Webhooks work → MVP!
3. Add User Story 2 → Entitlement checks work
4. Add User Story 3 → Checkout URLs work
5. Each story adds value without breaking previous stories

---

## Notes

- All files use `.py-tpl` extension for Django template project
- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story
- Each user story is independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Stub functions use `NotImplementedError` with docstrings explaining required implementation
