# Research: Polar.sh Payment Integration

**Feature**: 002-add-polar-payments
**Date**: 2026-01-04

## 1. Polar SDK Python Usage

### Decision

Use the official `polar-sdk` Python package for all Polar API interactions.

### Rationale

- Already installed in `pyproject.toml`
- High-quality SDK with 96.7 benchmark score on Context7
- Provides typed models, async support, and proper error handling
- Includes `standardwebhooks` for signature verification

### Alternatives Considered

| Alternative | Rejected Because |
|-------------|------------------|
| Raw `httpx` calls | More code, no type safety, must handle auth manually |
| Third-party wrapper | Unnecessary layer, polar-sdk is official and maintained |

### Usage Pattern

```python
from polar_sdk import Polar

with Polar(access_token="<token>") as polar:
    # API calls here
    pass
```

## 2. Webhook Signature Verification

### Decision

Use `standardwebhooks` library (bundled with polar-sdk) for webhook signature verification.

### Rationale

- Polar uses Standard Webhooks spec (<https://www.standardwebhooks.com/>)
- Library handles timing-safe comparison, timestamp validation
- Already a dependency via polar-sdk

### Implementation Pattern

```python
from standardwebhooks import Webhook

wh = Webhook(secret)
try:
    payload = wh.verify(body, headers)
except WebhookVerificationError:
    return HttpResponse(status=400)
```

### Security Considerations

1. **Always verify before processing** - Never trust unverified payloads
2. **Return 400 on failure** - Don't reveal verification details
3. **Return 200 on success** - Even if business logic fails (prevents retries of unfixable errors)
4. **Log failures** - For security monitoring

## 3. Webhook Events to Handle

### Decision

Handle the core subscription lifecycle events only. Additional events can be added per-project.

### Core Events

| Event | Action |
|-------|--------|
| `subscription.created` | Create local Subscription record |
| `subscription.updated` | Update status, period_end, cancel_at_period_end |
| `subscription.revoked` | Set status to 'revoked' |
| `subscription.canceled` | Set status to 'canceled' |

### Extensibility Pattern

Project-specific handlers are added via hook functions that raise `NotImplementedError`:

```python
def on_subscription_created(subscription: Subscription) -> None:
    """Called after a subscription is created locally.

    Override this function to add project-specific logic:
    - Send welcome email
    - Provision resources
    - Update user permissions

    Args:
        subscription: The newly created Subscription instance

    Raises:
        NotImplementedError: Implement this in your project
    """
    raise NotImplementedError(
        "Implement on_subscription_created() for project-specific logic"
    )
```

## 4. Checkout and Customer Portal URLs

### Decision

Provide service functions that wrap Polar SDK checkout/portal creation.

### Rationale

- Checkout happens on Polar's hosted page (security: no card data touches our server)
- Customer Portal also hosted by Polar (manage subscriptions, payment methods)
- We just need to generate redirect URLs

### API Pattern

```python
# Generate checkout URL
url = polar.checkouts.custom_create(
    product_id="prod_xxx",
    success_url="https://example.com/success",
    customer_email="user@example.com",
    metadata={"organization_id": str(org.id)},
)

# Customer portal (Polar doesn't have a dedicated portal endpoint - 
# customers manage via the product dashboard or email links)
```

### Note on Customer Portal

Polar.sh handles subscription management differently than Stripe. Customers receive email links for managing their subscriptions. The SDK doesn't expose a "customer portal URL" endpoint. For template purposes, we'll stub this as `NotImplementedError` with documentation.

## 5. Linking Subscriptions to Organizations

### Decision

Link subscriptions to `Organization` (not `User`) to support B2B/team billing.

### Rationale

- Template already has Organization model with team support
- B2B SaaS typically bills organizations, not individuals
- Organization ID passed via checkout `metadata`

### Pattern

1. Checkout includes `metadata={"organization_id": str(org.id)}`
2. Webhook receives `subscription.created` with metadata
3. Local `Subscription` created with FK to Organization

## 6. Entitlement Checks

### Decision

Provide a simple selector function and Organization method for checking subscription status.

### Rationale

- Most common operation: "Does this org have access?"
- Must be fast (database query, no API calls)
- Simple boolean return for easy use

### Implementation

```python
# In selectors.py
def has_active_subscription(organisation: Organisation) -> bool:
    """Check if organisation has an active subscription."""
    return Subscription.objects.filter(
        organisation=organisation,
        status="active",
        current_period_end__gt=timezone.now(),
    ).exists()
```

## 7. Django-Ninja API Design

### Decision

Create dedicated webhook endpoint outside the versioned API namespace.

### Rationale

- Webhooks are machine-to-machine, not user-facing
- Don't need versioning (Polar controls the format)
- CSRF exemption required (Polar can't send CSRF tokens)

### Implementation

```python
# Separate NinjaAPI for webhooks (CSRF exempt)
webhooks_api = NinjaAPI(
    urls_namespace="webhooks",
)

@webhooks_api.post("/polar")
def polar_webhook(request):
    # Verify signature first
    # Then process event
    pass
```

## 8. Configuration via django-environ

### Decision

All Polar configuration via environment variables using existing `django-environ` pattern.

### Rationale

- Settings.py already uses `env.str()` pattern
- Polar settings already defined: `POLAR_ACCESS_TOKEN`, `POLAR_ORGANIZATION_ID`, `POLAR_WEBHOOK_SECRET`, `POLAR_API_BASE_URL`
- Secrets never in code

### Existing Configuration (no changes needed)

```python
POLAR_ACCESS_TOKEN = env.str("POLAR_ACCESS_TOKEN", default="")
POLAR_ORGANIZATION_ID = env.str("POLAR_ORGANIZATION_ID", default="")
POLAR_WEBHOOK_SECRET = env.str("POLAR_WEBHOOK_SECRET", default="")
POLAR_API_BASE_URL = env.str("POLAR_API_BASE_URL", default="https://api.polar.sh")
```
