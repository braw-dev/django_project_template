from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import CharField
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """Custom user model.

    As this can be hard to change mid project then we create a
    custom user model from the start.

    Read more: https://docs.djangoproject.com/en/5.1/topics/auth/customizing/#auth-custom-user"""

    # First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None  # type: ignore[assignment]
    last_name = None  # type: ignore[assignment]

    # Onboarding fields
    onboarding_completed = models.DateField(null=True, blank=True, default=None)
    company = CharField(_("Company"), blank=True, max_length=255)
    role = CharField(_("Role/Title"), blank=True, max_length=255)

    # User preferences stored as JSON
    preferences = models.JSONField(
        _("Preferences"),
        default=dict,
        blank=True,
        help_text=_("User preferences like timezone, language, theme, notifications"),
    )

    REQUIRED_FIELDS = []

    def get_preference(self, key: str, default=None):
        """Get a specific preference value."""
        return self.preferences.get(key, default)

    def set_preference(self, key: str, value) -> None:
        """Set a specific preference value."""
        self.preferences[key] = value
        self.save(update_fields=["preferences"])
