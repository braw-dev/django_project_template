# Billing App

Billing and subscription management foundation with Polar.sh as the default provider.

## Overview

This app provides a small billing abstraction so generated projects can start with Polar, while keeping call sites small if you later swap providers.

Included by default:

- **Provider interface**: `get_billing_provider()` returns the configured billing provider
- **Polar implementation**: hosted checkout, hosted customer portal session, product listing, webhook verification
- **Local billing models**: `Customer`, `Product`, `Subscription`, `Entitlement`, and persisted `WebhookEvent`
- **Webhook processing**: signature verification, duplicate-event short-circuiting, and local billing sync
- **Selectors**: helpers for active subscription and entitlement checks

## Configuration

Add these environment variables to your `.env`:

```bash
BILLING_PROVIDER=polar
POLAR_ACCESS_TOKEN=polar_at_xxx          # Polar Dashboard > Settings > Access Tokens
POLAR_ORGANIZATION_ID=org_xxx            # Polar organization ID
POLAR_WEBHOOK_SECRET=whsec_xxx           # Polar Dashboard > Settings > Webhooks
POLAR_API_BASE_URL=https://api.polar.sh  # Optional, defaults to production
```

## Bootstrapping billing in a new project

Use this checklist when turning billing on in a generated project for the first time.

### 1. Configure environment variables

Set these in `.env`:

```bash
BILLING_PROVIDER=polar
POLAR_ACCESS_TOKEN=polar_at_xxx
POLAR_ORGANIZATION_ID=org_xxx
POLAR_WEBHOOK_SECRET=whsec_xxx
POLAR_API_BASE_URL=https://api.polar.sh
```

### 2. Create products in Polar

Create the recurring products you want to sell in Polar first.

The template expects real Polar product IDs when creating checkout sessions. Keep those IDs in your pricing/selectors layer rather than scattering them through templates.

### 3. Create the webhook endpoint in Polar

In Polar, add a webhook endpoint pointing to:

```text
https://your-domain.com/api/webhooks/polar
```

Then copy the webhook secret into `POLAR_WEBHOOK_SECRET`.

### 4. Deploy before testing live webhooks

Make sure the deployed app can:

- receive POST requests at `/api/webhooks/polar`
- access the configured billing environment variables
- write billing records to the database

### 5. Verify the happy path

Run through one real or test checkout and confirm:

- a `WebhookEvent` row is created
- a local `Customer` row is created for the team
- a local `Product` row is synced
- a local `Subscription` row is created or updated
- local `Entitlement` rows are created for active product benefits

### 6. Verify duplicate webhook handling

Replay the same webhook event from Polar and confirm the app records it once and ignores the duplicate delivery.

### 7. Verify the customer portal flow

Call the customer portal endpoint or trigger it from your UI and confirm Polar redirects back to your dashboard return URL.

### 8. Wire your app to local billing state

Use local selectors such as `has_active_subscription(...)`, `get_active_subscription(...)`, and `has_entitlement(...)` in your app logic.

Avoid making live provider API calls during normal feature checks.

## Usage

### Check if a team has active billing access

```python
from {{ project_name }}.billing.selectors import has_active_subscription, has_entitlement

if has_active_subscription(team):
    # Show premium features
    pass

if has_entitlement(team, "analytics"):
    # Enable analytics feature
    pass
```

### Get the current subscription

```python
from {{ project_name }}.billing.selectors import get_active_subscription

subscription = get_active_subscription(team)
if subscription:
    print(f"Plan: {subscription.external_product_id}")
    print(f"Expires: {subscription.current_period_end}")
```

### Generate a hosted checkout URL

```python
from {{ project_name }}.billing.services import get_billing_provider

billing_provider = get_billing_provider()
checkout_url = billing_provider.create_checkout_url(
    product_id="prod_xxx",
    team=team,
    success_url="https://your-app.com/dashboard",
    return_url="https://your-app.com/dashboard",
    user_email=request.user.email,
    locale=getattr(request, "LANGUAGE_CODE", None),
)
```

Polar checkout uses the local team UUID as `external_customer_id` and includes `team_id` in checkout metadata.

### Generate a hosted customer portal URL

```python
from {{ project_name }}.billing.services import get_billing_provider

billing_provider = get_billing_provider()
portal_url = billing_provider.get_customer_portal_url(
    team=team,
    return_url="https://your-app.com/dashboard",
)
```

## Webhooks

The template exposes a Polar webhook endpoint at:

```text
/api/webhooks/polar
```

Processing flow:

1. verify the provider signature
2. extract the provider event ID
3. persist the event in `WebhookEvent`
4. ignore duplicates safely
5. sync local `Customer`, `Product`, `Subscription`, and `Entitlement` records

Invalid signatures return `400`. Internal processing failures return `500` so the provider can retry.

## Security

- billing data is team-owned where appropriate
- billing API endpoints require authenticated users with `tenancy.manage_team_billing`
- webhook endpoints are CSRF exempt because provider signature verification provides authenticity
- duplicate webhook deliveries are ignored using persisted provider event IDs
- all provider secrets are stored in environment variables

See `SECURITY.md` for the wider multi-tenancy security model.
