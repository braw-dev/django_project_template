# Billing App

Billing and subscription management integration with Polar.sh.

## Overview

This app provides boilerplate functionality for handling Polar.sh subscriptions:

- **Subscription Model**: Links Polar subscriptions to local Teams
- **Webhook Handlers**: Processes subscription lifecycle events from Polar
- **Entitlement Checks**: Simple functions to check if a team has active access
- **Checkout URLs**: Generate Polar checkout sessions for new subscriptions
- **Service Layer**: Wrapper around Polar SDK for API interactions

## Configuration

Add these environment variables to your `.env`:

```bash
POLAR_ACCESS_TOKEN=polar_at_xxx        # From Polar Dashboard > Settings > Access Tokens
POLAR_ORGANIZATION_ID=org_xxx          # Your Polar organization ID inside Polar
POLAR_WEBHOOK_SECRET=whsec_xxx         # From Polar Dashboard > Settings > Webhooks
POLAR_API_BASE_URL=https://api.polar.sh  # Optional, defaults to production
```

## Usage

### Check if Team Has Active Subscription

```python
from {{ project_name }}.billing.selectors import has_active_subscription

if has_active_subscription(team):
    # Show premium features
    pass
```

### Get Current Subscription

```python
from {{ project_name }}.billing.selectors import get_active_subscription

subscription = get_active_subscription(team)
if subscription:
    print(f"Plan: {subscription.polar_product_id}")
    print(f"Expires: {subscription.current_period_end}")
```

### Generate Checkout URL

```python
from {{ project_name }}.billing.services import get_billing_service

billing_service = get_billing_service()
checkout_url = billing_service.create_checkout_url(
    product_id="prod_xxx",
    team=team,
    success_url="https://your-app.com/billing/success",
    user_email=request.user.email,
)
```

Polar checkout metadata includes `team_id` by default.

## Security

- subscriptions are team-owned via `TenantScopedModel`
- billing API endpoints require authenticated users with `tenancy.manage_team_billing`
- webhook signatures are verified using Standard Webhooks spec
- invalid signatures return `400 Bad Request`
- webhook endpoints are CSRF exempt because signature verification provides authenticity
- all secrets are stored in environment variables

See `SECURITY.md` for the full multi-tenancy security model.
