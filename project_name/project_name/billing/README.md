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

## Billing vs accounting source of truth

The template treats billing and accounting as related but different concerns.

Use these sources of truth by default:

- **Polar** for invoices, receipts, credit notes, refunds, subscription charges, tax handling, and provider-issued billing documents
- **your bank account or payout statements** for cash actually received, provider fees, and reconciliation
- **your Django database** for operational product state such as which team has an active subscription, which entitlements are active, and which provider IDs are linked to a local team

This means the local billing models in this app are intentionally **not** an accounting ledger. They are for app behaviour and support workflows:

- gating paid features from local subscription state
- rendering billing status in the product UI
- linking teams to provider-side customer and subscription IDs
- helping debug webhook processing and support issues

If you later need bookkeeping exports into a specific accounting tool, prefer exporting from Polar first and only add local project-specific reconciliation helpers if they clearly solve a real workflow.

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

### 9. Decide your bookkeeping workflow

Before launch, decide how you will reconcile money for this product.

The boring default is:

1. export invoices, refunds, and tax documents from Polar
2. use Polar as the financial source of truth for what was billed
3. use bank or payout statements as the source of truth for what cash actually arrived and what fees were deducted
4. use local Django billing rows only for access control, support, and troubleshooting

Do not assume that `Subscription` or `WebhookEvent` rows are enough to satisfy accounting, tax filing, or end-of-year bookkeeping requirements.

## European tax and billing display default

The template takes a conservative default stance for EU-friendly B2B billing:

- public pricing pages show prices **excluding VAT**
- final tax is calculated at checkout by the billing provider
- VAT number collection, reverse-charge handling, and tax calculation should stay with the billing provider where possible
- invoices, receipts, and tax documents should be issued by the billing provider, not from Django admin
- the default happy path is provider-hosted checkout and provider-managed billing records

### What this means in practice

- if a business buyer is VAT-exempt or reverse charge applies, rely on Polar to handle that during checkout
- do not try to hardcode country-specific VAT rules into templates or selectors
- do not scaffold manual invoice issuance or local invoice reconciliation by default
- do not treat the local billing tables as a finance ledger for bookkeeping or statutory reporting
- if a generated project later needs offline invoicing, purchase-order workflows, or accounting-tool exports, add that as an explicit project-level extension rather than changing the default template flow

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

### Pricing page helper

The public pricing page uses `{{ project_name }}.selectors.product_list()` as a thin mapping layer from provider products to template cards.

It includes a small locale-aware currency formatter for EUR, CHF, GBP, and USD using the active request locale.

That helper is the intended override point for generated projects when you want to:

- change plan ordering
- hide internal products
- tune marketing copy per plan
- choose which product benefits to surface publicly
- replace the default price display in task-specific ways

It is intentionally smaller than a full pricing abstraction.

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
