"""Billing models for Polar.sh subscription management."""

import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


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
