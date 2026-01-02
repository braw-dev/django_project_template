from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import FeatureFlag


@admin.register(FeatureFlag)
class FeatureFlagAdmin(admin.ModelAdmin):
    """Admin configuration for FeatureFlag model."""

    list_display = [
        "name",
        "enabled",
        "description",
        "created_at",
        "updated_at",
    ]
    list_filter = [
        "enabled",
        "created_at",
        "updated_at",
    ]
    search_fields = [
        "name",
        "description",
    ]
    list_editable = ["enabled"]
    readonly_fields = ["created_at", "updated_at"]

    fieldsets = [
        (
            None,
            {
                "fields": ["name", "enabled", "description"],
            },
        ),
        (
            _("Metadata"),
            {
                "fields": ["created_at", "updated_at"],
                "classes": ["collapse"],
            },
        ),
    ]

