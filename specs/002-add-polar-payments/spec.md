# Feature Specification: Polar.sh Payment Boilerplate

**Feature Branch**: `002-add-polar-payments`
**Created**: 2026-01-04
**Status**: Draft
**Input**: User description: "Add boilerplate functionality for payment handling to the template"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Developer Payment Infrastructure (Priority: P1)

As a developer using the template, I want the core Polar.sh integration (models, webhooks, and services) pre-configured so that I can focus on my specific business logic (pricing plans and gated features).

**Why this priority**: This is the core "boilerplate" value proposition. Without this, the developer has to write the integration from scratch.

**Independent Test**: Can be tested by simulating Polar.sh webhooks and verifying that local `Subscription` models are created/updated without writing any new code.

**Acceptance Scenarios**:

1. **Given** a new project generated from the template and configured Polar credentials, **When** a `subscription.created` webhook is received, **Then** a local `Subscription` record is created for the correct Organization.
2. **Given** an active subscription, **When** a `subscription.revoked` webhook is received, **Then** the local `Subscription` status is updated to `revoked`.
3. **Given** the codebase, **When** I look for payment logic, **Then** I find a dedicated structure (e.g., `billing` app) with clean separation of concerns.

---

### User Story 2 - Subscription Entitlement Checks (Priority: P2)

As a developer, I want a simple, standardized way to check if an organization has an active subscription so that I can gate premium features with a single line of code.

**Why this priority**: This is the most common action a developer will take—checking "can they do this?".

**Independent Test**: Can be tested by creating unit tests that set up various subscription states and assert the return value of the entitlement check function.

**Acceptance Scenarios**:

1. **Given** an organization with an `active` subscription, **When** `organization.has_active_subscription()` (or equivalent) is called, **Then** it returns `True`.
2. **Given** an organization with a `revoked` or `past_due` subscription, **When** the check is called, **Then** it returns `False`.
3. **Given** an organization with no subscription history, **When** the check is called, **Then** it returns `False`.

---

### User Story 3 - Checkout and Portal Redirects (Priority: P3)

As an end-user, I want to be able to subscribe to a plan or manage my existing subscription via the provider's secure portal.

**Why this priority**: Essential for the actual transaction to happen.

**Independent Test**: Can be tested by calling the service functions and verifying they return valid URLs (mocking the Polar SDK response).

**Acceptance Scenarios**:

1. **Given** an authenticated user and a product ID, **When** they request to subscribe, **Then** the system generates a valid Polar Checkout URL.
2. **Given** an organization with an existing subscription, **When** they request to manage billing, **Then** the system generates a valid Polar Customer Portal URL.

### Edge Cases

- **Webhook Signature Failure**: If a webhook signature is invalid, the system must return a 400 error and NOT update any data.
- **Missing Organization**: If a webhook refers to an Organization ID (or metadata) that doesn't exist locally, the system should log an error/warning but return 200 to Polar (to prevent retries of unfixable errors).
- **API Downtime**: If Polar API is down when generating a checkout link, the system should handle the exception gracefully and show a user-friendly error message.
- **Race Conditions**: If a `subscription.created` and `subscription.updated` arrive out of order, the system relies on the `current_period_end` or status to determine the most "active" state, or simply processes them as they come (eventual consistency).

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST provide a `Subscription` model that links a Polar Subscription ID to an internal `Organization`.
- **FR-002**: System MUST provide a Webhook endpoint that verifies signatures using `standardwebhooks` and processes `subscription.*` events.
- **FR-003**: System MUST provide a Service layer to interact with the Polar SDK for creating Checkout and Customer Portal sessions.
- **FR-004**: System MUST provide a clear, easy-to-use method (Selector or Property) to check if an Organization has a valid, active subscription.
- **FR-005**: System MUST allow retrieving the list of available products/prices, optionally caching the result to avoid API rate limits.
- **FR-006**: The integration MUST rely on `django-environ` for configuration (`POLAR_ACCESS_TOKEN`, `POLAR_WEBHOOK_SECRET`, etc.).

### Key Entities

- **Subscription**: Represents the link between a local Organization and a remote Polar subscription.
  - Fields: `organization` (FK), `polar_id` (str), `status` (str), `current_period_end` (datetime), `cancel_at_period_end` (bool).
- **BillingService**: A stateless service class/module for interacting with the Polar API.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A developer can enable full payment processing by defining 4 environment variables and creating products in the Polar dashboard.
- **SC-002**: Webhook processing handles standard subscription lifecycle events (created, updated, revoked) with correct database state updates.
- **SC-003**: Entitlement checks (`has_active_subscription`) return instantly (e.g. < 10ms) without external API calls during the check.
