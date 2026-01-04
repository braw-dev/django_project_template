# Billing App

Billing and subscription management integration with Polar.sh.

## Overview

This app provides boilerplate functionality for handling Polar.sh subscriptions:

- **Subscription Model**: Links Polar subscriptions to local Organizations
- **Webhook Handlers**: Processes subscription lifecycle events from Polar
- **Entitlement Checks**: Simple functions to check if an organization has active access
- **Checkout URLs**: Generate Polar checkout sessions for new subscriptions
- **Service Layer**: Wrapper around Polar SDK for API interactions

## Configuration

Add these environment variables to your `.env`:

```bash
POLAR_ACCESS_TOKEN=polar_at_xxx        # From Polar Dashboard > Settings > Access Tokens
POLAR_ORGANIZATION_ID=org_xxx          # Your Polar organization ID
POLAR_WEBHOOK_SECRET=whsec_xxx         # From Polar Dashboard > Settings > Webhooks
POLAR_API_BASE_URL=https://api.polar.sh  # Optional, defaults to production
```

## Usage

### Check if Organization Has Active Subscription

```python
from {{ project_name }}.billing.selectors import has_active_subscription

if has_active_subscription(organisation):
    # Show premium features
    pass
```

### Get Current Subscription

```python
from {{ project_name }}.billing.selectors import get_active_subscription

subscription = get_active_subscription(organisation)
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
    organisation=organisation,
    success_url="https://your-app.com/billing/success",
    user_email=request.user.email,
)
# Redirect user to checkout_url
```

## Webhooks

Webhooks are automatically handled at `/api/webhooks/polar/`.

Configure this URL in Polar Dashboard > Settings > Webhooks.

Supported events:

- `subscription.created` - Creates local Subscription record
- `subscription.updated` - Updates subscription status and period
- `subscription.revoked` - Sets status to 'revoked'
- `subscription.canceled` - Sets status to 'canceled'

## Customization Hooks

Override these functions in your project to add business logic:

### Subscription Hooks

```python
from {{ project_name }}.billing import webhooks

def my_subscription_created_hook(subscription):
    """Send welcome email, provision resources, etc."""
    send_welcome_email(subscription.organisation.owner)
    provision_premium_features(subscription.organisation)

# Monkey-patch the hook
webhooks.on_subscription_created = my_subscription_created_hook
```

Available hooks:

- `on_subscription_created(subscription)` - Called after subscription created
- `on_subscription_updated(subscription)` - Called after subscription updated
- `on_subscription_revoked(subscription)` - Called after subscription revoked
- `on_subscription_canceled(subscription)` - Called after subscription canceled

### Checkout Metadata

Override `BillingService._get_checkout_metadata()` to add custom metadata:

```python
from {{ project_name }}.billing.services import BillingService

class MyBillingService(BillingService):
    def _get_checkout_metadata(self, organisation):
        metadata = super()._get_checkout_metadata(organisation)
        metadata["custom_field"] = "value"
        return metadata
```

## API Endpoints

### GET /api/v1/billing/subscription/

Get current subscription for an organisation.

Query params:

- `organisation_id` (UUID, required)

Response:

```json
{
  "subscription": {
    "id": "...",
    "status": "active",
    "product_id": "prod_xxx",
    "current_period_end": "2026-02-01T00:00:00Z",
    "cancel_at_period_end": false
  }
}
```

### POST /api/v1/billing/checkout/

Generate checkout URL for a product.

Request:

```json
{
  "product_id": "prod_xxx",
  "organisation_id": "..."
}
```

Response:

```json
{
  "checkout_url": "https://checkout.polar.sh/xxx"
}
```

## Testing

Run billing tests:

```bash
just test-unit billing
```

## Security

- Webhook signatures are verified using Standard Webhooks spec
- Invalid signatures return 400 Bad Request
- Webhook endpoint is CSRF exempt (signature verification provides authenticity)
- All secrets stored in environment variables
