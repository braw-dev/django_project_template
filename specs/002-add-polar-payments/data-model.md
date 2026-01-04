# Data Model: Polar.sh Payment Integration

**Feature**: 002-add-polar-payments
**Date**: 2026-01-04

## Entities

### Subscription

Links a Polar subscription to a local Organization.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | UUID | PK, auto | Primary key |
| `organisation` | FK(Organisation) | NOT NULL, CASCADE | The organization this subscription belongs to |
| `polar_subscription_id` | CharField(255) | UNIQUE, NOT NULL | Polar's subscription ID |
| `polar_customer_id` | CharField(255) | NOT NULL | Polar's customer ID |
| `polar_product_id` | CharField(255) | NOT NULL | Polar's product ID |
| `status` | CharField(50) | NOT NULL | Subscription status (see enum below) |
| `current_period_start` | DateTimeField | NULL | Start of current billing period |
| `current_period_end` | DateTimeField | NULL | End of current billing period |
| `cancel_at_period_end` | BooleanField | DEFAULT False | Will cancel at period end |
| `canceled_at` | DateTimeField | NULL | When the subscription was canceled |
| `created_at` | DateTimeField | auto_now_add | Record creation timestamp |
| `updated_at` | DateTimeField | auto_now | Record update timestamp |

#### Status Enum

```python
class SubscriptionStatus(models.TextChoices):
    INCOMPLETE = "incomplete", _("Incomplete")
    INCOMPLETE_EXPIRED = "incomplete_expired", _("Incomplete Expired")
    TRIALING = "trialing", _("Trialing")
    ACTIVE = "active", _("Active")
    PAST_DUE = "past_due", _("Past Due")
    CANCELED = "canceled", _("Canceled")
    UNPAID = "unpaid", _("Unpaid")
    REVOKED = "revoked", _("Revoked")
```

### Relationships

```text
┌─────────────────┐         ┌──────────────┐
│  Organisation   │ 1 ─── * │ Subscription │
│  (existing)     │         │   (new)      │
└─────────────────┘         └──────────────┘
```

- One Organisation can have multiple Subscriptions (e.g., past subscriptions, multiple products)
- Latest active subscription is the "current" subscription

## Indexes

| Index | Fields | Purpose |
|-------|--------|---------|
| `subscription_org_status` | `organisation_id`, `status` | Fast entitlement checks |
| `subscription_polar_id` | `polar_subscription_id` | Webhook lookups |

## Validation Rules

1. `polar_subscription_id` must be unique
2. `status` must be a valid `SubscriptionStatus` choice
3. `organisation` must reference an existing Organisation

## State Transitions

```text
                    ┌─────────────────────────────────────┐
                    │                                     │
                    ▼                                     │
┌──────────┐   ┌────────┐   ┌────────┐   ┌──────────┐   │
│incomplete│ → │trialing│ → │ active │ → │ canceled │   │
└──────────┘   └────────┘   └────────┘   └──────────┘   │
     │              │            │            │          │
     │              │            ▼            ▼          │
     │              │       ┌─────────┐  ┌────────┐     │
     │              └─────→ │past_due │  │revoked │     │
     │                      └─────────┘  └────────┘     │
     │                           │                       │
     ▼                           ▼                       │
┌─────────────────┐         ┌────────┐                  │
│incomplete_expired│         │ unpaid │ ─────────────────┘
└─────────────────┘         └────────┘
```

## Model Code (Preview)

```python
class Subscription(models.Model):
    """Links a Polar subscription to a local Organization."""

    class SubscriptionStatus(models.TextChoices):
        INCOMPLETE = "incomplete", _("Incomplete")
        INCOMPLETE_EXPIRED = "incomplete_expired", _("Incomplete Expired")
        TRIALING = "trialing", _("Trialing")
        ACTIVE = "active", _("Active")
        PAST_DUE = "past_due", _("Past Due")
        CANCELED = "canceled", _("Canceled")
        UNPAID = "unpaid", _("Unpaid")
        REVOKED = "revoked", _("Revoked")

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organisation = models.ForeignKey(
        "organizations.Organisation",
        on_delete=models.CASCADE,
        related_name="subscriptions",
    )
    polar_subscription_id = models.CharField(
        max_length=255,
        unique=True,
        db_index=True,
    )
    polar_customer_id = models.CharField(max_length=255)
    polar_product_id = models.CharField(max_length=255)
    status = models.CharField(
        max_length=50,
        choices=SubscriptionStatus.choices,
        default=SubscriptionStatus.INCOMPLETE,
    )
    current_period_start = models.DateTimeField(null=True, blank=True)
    current_period_end = models.DateTimeField(null=True, blank=True)
    cancel_at_period_end = models.BooleanField(default=False)
    canceled_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Subscription")
        verbose_name_plural = _("Subscriptions")
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["organisation", "status"]),
        ]

    def __str__(self):
        return f"{self.organisation.name} - {self.status}"
```
