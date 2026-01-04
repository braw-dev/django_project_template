# API Contract: Polar Webhooks

**Feature**: 002-add-polar-payments
**Date**: 2026-01-04

## Endpoint

### POST /api/webhooks/polar/

Receives and processes webhook events from Polar.sh.

#### Security

- **Authentication**: Webhook signature verification (Standard Webhooks spec)
- **CSRF**: Exempt (signature verification provides authenticity)
- **Rate Limiting**: Rely on Polar's rate limiting

#### Request

**Headers** (Required for signature verification):

| Header | Description |
|--------|-------------|
| `webhook-id` | Unique webhook delivery ID |
| `webhook-timestamp` | Unix timestamp of delivery |
| `webhook-signature` | HMAC signature |

**Body**: JSON payload from Polar (varies by event type)

```json
{
  "type": "subscription.created",
  "timestamp": "2026-01-04T12:00:00Z",
  "data": {
    "id": "sub_xxx",
    "customer_id": "cust_xxx",
    "product_id": "prod_xxx",
    "status": "active",
    "current_period_start": "2026-01-04T12:00:00Z",
    "current_period_end": "2026-02-04T12:00:00Z",
    "cancel_at_period_end": false,
    "metadata": {
      "organization_id": "550e8400-e29b-41d4-a716-446655440000"
    }
  }
}
```

#### Responses

| Status | Condition | Body |
|--------|-----------|------|
| `200 OK` | Event processed successfully | `{"status": "ok"}` |
| `200 OK` | Event ignored (unknown type) | `{"status": "ignored"}` |
| `200 OK` | Organisation not found (logged) | `{"status": "ok"}` |
| `400 Bad Request` | Invalid signature | `{"error": "Invalid signature"}` |
| `400 Bad Request` | Missing required headers | `{"error": "Missing headers"}` |

**Note**: We return 200 even for "unfixable" errors (like missing organization) to prevent Polar from retrying indefinitely.

#### Supported Event Types

| Event | Action |
|-------|--------|
| `subscription.created` | Create local Subscription |
| `subscription.updated` | Update Subscription fields |
| `subscription.revoked` | Set status to "revoked" |
| `subscription.canceled` | Set status to "canceled" |

---

## Internal Endpoints (Authenticated)

### POST /api/v1/billing/checkout/

Generate a Polar checkout URL for a product.

#### Security

- **Authentication**: Session (logged-in user)
- **Authorization**: User must be member of organisation

#### Request

```json
{
  "product_id": "prod_xxx",
  "organisation_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

#### Response

**200 OK**:

```json
{
  "checkout_url": "https://checkout.polar.sh/xxx"
}
```

**403 Forbidden** (not org member):

```json
{
  "error": "Not authorized"
}
```

**503 Service Unavailable** (Polar API down):

```json
{
  "error": "Payment service temporarily unavailable"
}
```

---

### GET /api/v1/billing/subscription/

Get the current subscription for an organisation.

#### Security

- **Authentication**: Session (logged-in user)
- **Authorization**: User must be member of organisation

#### Request

Query parameters:

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `organisation_id` | UUID | Yes | Organisation to check |

#### Response

**200 OK** (has subscription):

```json
{
  "subscription": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "status": "active",
    "product_id": "prod_xxx",
    "current_period_end": "2026-02-04T12:00:00Z",
    "cancel_at_period_end": false
  }
}
```

**200 OK** (no subscription):

```json
{
  "subscription": null
}
```

---

## Pydantic Schemas

```python
from pydantic import BaseModel
from datetime import datetime
from uuid import UUID


class CheckoutRequest(BaseModel):
    """Request to create a checkout session."""
    product_id: str
    organisation_id: UUID


class CheckoutResponse(BaseModel):
    """Response with checkout URL."""
    checkout_url: str


class SubscriptionResponse(BaseModel):
    """Current subscription details."""
    id: UUID
    status: str
    product_id: str
    current_period_end: datetime | None
    cancel_at_period_end: bool


class SubscriptionDetailResponse(BaseModel):
    """Wrapper for subscription response."""
    subscription: SubscriptionResponse | None


class WebhookResponse(BaseModel):
    """Standard webhook response."""
    status: str


class ErrorResponse(BaseModel):
    """Error response."""
    error: str
```
