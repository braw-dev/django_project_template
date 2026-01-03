"""Organization models for multi-tenant RBAC system."""

import uuid

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class Organisation(models.Model):
    """Top-level organization entity."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(_("Name"), max_length=255)
    slug = models.SlugField(_("Slug"), unique=True)
    owner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="owned_organisations",
        help_text=_("Optional primary owner"),
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Organisation")
        verbose_name_plural = _("Organisations")
        ordering = ["-created_at"]

    def __str__(self):
        return self.name


class Team(models.Model):
    """Sub-group within an Organization."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE, related_name="teams")
    name = models.CharField(_("Name"), max_length=255)
    slug = models.SlugField(_("Slug"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Team")
        verbose_name_plural = _("Teams")
        unique_together = [("organisation", "slug")]
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.organisation.name} / {self.name}"


class Role(models.Model):
    """Defines a set of permissions. Can be global or org-specific."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(_("Name"), max_length=100)
    organisation = models.ForeignKey(
        Organisation,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="roles",
        help_text=_("Null = Global Role available to all orgs"),
    )
    permissions = models.JSONField(
        _("Permissions"),
        default=dict,
        help_text=_("e.g., {'can_edit': true, 'can_create': true}"),
    )

    class Meta:
        verbose_name = _("Role")
        verbose_name_plural = _("Roles")
        unique_together = [("organisation", "name")]
        ordering = ["name"]

    def __str__(self):
        scope = self.organisation.name if self.organisation else "Global"
        return f"{self.name} ({scope})"


class OrganisationMember(models.Model):
    """Links a User to an Organization with a Role."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="organisation_memberships"
    )
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE, related_name="members")
    role = models.ForeignKey(Role, on_delete=models.PROTECT)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Organisation Member")
        verbose_name_plural = _("Organisation Members")
        unique_together = [("user", "organisation")]
        ordering = ["-joined_at"]

    def __str__(self):
        return f"{self.user} in {self.organisation.name} as {self.role.name}"


class TeamMember(models.Model):
    """Links a User to a Team with a Role."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="team_memberships")
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="members")
    role = models.ForeignKey(Role, on_delete=models.PROTECT)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Team Member")
        verbose_name_plural = _("Team Members")
        unique_together = [("user", "team")]
        ordering = ["-joined_at"]

    def __str__(self):
        return f"{self.user} in {self.team.name} as {self.role.name}"
