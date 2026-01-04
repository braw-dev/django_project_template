# Quickstart: Polar.sh Payment Integration

**Feature**: 002-add-polar-payments
**Date**: 2026-01-04

## Prerequisites

1. A Polar.sh account with an organization
2. At least one product created in Polar dashboard
3. A webhook endpoint configured in Polar dashboard

## Configuration

Add the following to your `.env` file:

```bash
# Polar.sh Configuration
POLAR_ACCESS_TOKEN=polar_at_xxx        # From Polar Dashboard > Settings > Access Tokens
POLAR_ORGANIZATION_ID=org_xxx          # Your Polar organization ID
POLAR_WEBHOOK_SECRET=whsec_xxx         # From Polar Dashboard > Settings > Webhooks
POLAR_API_BASE_URL=https://api.polar.sh  # Optional, defaults to production
```

## Setup Steps

### 1. Run Migrations

```bash
just migrate
```

### 2. Configure Polar Webhook

In Polar Dashboard > Settings > Webhooks:

1. Create a new webhook endpoint
2. URL: `https://your-domain.com/api/webhooks/polar/`
3. Select events:
   - `subscription.created`
   - `subscription.updated`
   - `subscription.revoked`
   - `subscription.canceled`
4. Copy the webhook secret to `POLAR_WEBHOOK_SECRET`

### 3. Create Products in Polar

In Polar Dashboard > Products:

1. Create your subscription products (e.g., "Pro", "Enterprise")
2. Note the product IDs for use in your application

## Usage Examples

### Check if Organisation Has Active Subscription

```python
from {{ project_name }}.billing.selectors import has_active_subscription

if has_active_subscription(organisation):
    # Show premium features
    pass
else:
    # Show upgrade prompt
    pass
```

### Generate Checkout URL

```python
from {{ project_name }}.billing.services import create_checkout_url

checkout_url = create_checkout_url(
    product_id="prod_xxx",
    organisation=organisation,
    success_url="https://your-app.com/billing/success",
    user_email=request.user.email,
)
# Redirect user to checkout_url
```

### Get Current Subscription

```python
from {{ project_name }}.billing.selectors import get_active_subscription

subscription = get_active_subscription(organisation)
if subscription:
    print(f"Plan: {subscription.polar_product_id}")
    print(f"Expires: {subscription.current_period_end}")
```

## Testing Webhooks Locally

### Using ngrok

```bash
# Start ngrok
ngrok http 8000

# Update Polar webhook URL to ngrok URL
# https://abc123.ngrok.io/api/webhooks/polar/
```

### Manual Testing

```bash
# Simulate webhook (requires valid signature)
just test-unit billing
```

## Test Scenarios

### Scenario 1: New Subscription Created

**Given**: An organisation without a subscription
**When**: User completes checkout, Polar sends `subscription.created` webhook
**Then**: Local Subscription record created with status "active"

### Scenario 2: Subscription Canceled

**Given**: An organisation with an active subscription
**When**: User cancels in Polar, `subscription.updated` webhook received with `cancel_at_period_end=true`
**Then**: Local Subscription updated, access continues until period end

### Scenario 3: Subscription Revoked (Payment Failed)

**Given**: An organisation with past_due subscription
**When**: Payment retries exhausted, `subscription.revoked` webhook received
**Then**: Local Subscription status set to "revoked", access blocked

### Scenario 4: Invalid Webhook Signature

**Given**: A webhook request with invalid signature
**When**: POST to `/api/webhooks/polar/`
**Then**: Returns 400, no database changes

## Customizing Business Logic

The billing app includes hook functions that raise `NotImplementedError`. Override these in your project:

```python
# In your app's billing_hooks.py or similar
from {{ project_name }}.billing import webhooks

def my_subscription_created_hook(subscription):
    """Send welcome email, provision resources, etc."""
    send_welcome_email(subscription.organisation.owner)
    provision_premium_features(subscription.organisation)

# Monkey-patch or use signals
webhooks.on_subscription_created = my_subscription_created_hook
```

## Troubleshooting

### Webhook Not Receiving Events

1. Check webhook URL is correct and publicly accessible
2. Verify `POLAR_WEBHOOK_SECRET` matches Polar dashboard
3. Check Django logs for signature verification errors

### Subscription Not Found After Checkout

1. Ensure `organization_id` is passed in checkout metadata
2. Check webhook logs for errors
3. Verify Organisation exists with matching ID

### Entitlement Check Returns False

1. Check subscription status is "active"
2. Verify `current_period_end` is in the future
3. Run `Subscription.objects.filter(organisation=org)` to inspect records
