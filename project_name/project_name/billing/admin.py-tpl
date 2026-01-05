from django.contrib import admin

from . import models


@admin.register(models.Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        "organisation",
        "polar_subscription_id",
        "status",
        "current_period_end",
        "cancel_at_period_end",
        "created_at",
    )
    list_filter = ("status", "cancel_at_period_end", "created_at")
    search_fields = (
        "polar_subscription_id",
        "polar_customer_id",
        "organisation__name",
    )
    readonly_fields = ("created_at", "updated_at")
    raw_id_fields = ("organisation",)
