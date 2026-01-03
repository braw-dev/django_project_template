"""Business logic for organizations and teams."""

from django.contrib.auth import get_user_model
from django.db import transaction
from django.utils.translation import gettext_lazy as _

from . import models

User = get_user_model()


def create_organisation(name, slug, owner=None):
    """Create a new organization.

    Args:
        name: Organization name
        slug: URL-friendly slug
        owner: Optional User instance

    Returns:
        Organisation instance
    """
    return models.Organisation.objects.create(
        name=name,
        slug=slug,
        owner=owner,
    )


def add_user_to_organisation(user, organisation, role):
    """Add a user to an organization with a specific role.

    Args:
        user: User instance
        organisation: Organisation instance
        role: Role instance

    Returns:
        OrganisationMember instance

    Raises:
        ValueError: If user is already a member
    """
    if models.OrganisationMember.objects.filter(user=user, organisation=organisation).exists():
        raise ValueError(_("User is already a member of this organisation"))

    return models.OrganisationMember.objects.create(
        user=user,
        organisation=organisation,
        role=role,
    )


def remove_user_from_organisation(user, organisation):
    """Remove a user from an organization and all its teams.

    Args:
        user: User instance
        organisation: Organisation instance
    """
    with transaction.atomic():
        # Remove from all teams in this organisation
        models.TeamMember.objects.filter(
            user=user,
            team__organisation=organisation,
        ).delete()

        # Remove from organisation
        models.OrganisationMember.objects.filter(
            user=user,
            organisation=organisation,
        ).delete()


def update_organisation_member_role(user, organisation, role):
    """Update a user's role in an organization.

    Args:
        user: User instance
        organisation: Organisation instance
        role: Role instance
    """
    membership = models.OrganisationMember.objects.get(user=user, organisation=organisation)
    membership.role = role
    membership.save()


def create_team(organisation, name, slug):
    """Create a new team within an organization.

    Args:
        organisation: Organisation instance
        name: Team name
        slug: URL-friendly slug

    Returns:
        Team instance
    """
    return models.Team.objects.create(
        organisation=organisation,
        name=name,
        slug=slug,
    )


def add_user_to_team(user, team, role):
    """Add a user to a team with a specific role.

    Args:
        user: User instance
        team: Team instance
        role: Role instance

    Returns:
        TeamMember instance

    Raises:
        ValueError: If user is not an organisation member or already a team member
    """
    # Ensure user is a member of the organisation
    if not models.OrganisationMember.objects.filter(
        user=user, organisation=team.organisation
    ).exists():
        raise ValueError(_("User must be a member of the organisation first"))

    if models.TeamMember.objects.filter(user=user, team=team).exists():
        raise ValueError(_("User is already a member of this team"))

    return models.TeamMember.objects.create(
        user=user,
        team=team,
        role=role,
    )


def remove_user_from_team(user, team):
    """Remove a user from a team.

    Args:
        user: User instance
        team: Team instance
    """
    models.TeamMember.objects.filter(user=user, team=team).delete()


def update_team_member_role(user, team, role):
    """Update a user's role in a team.

    Args:
        user: User instance
        team: Team instance
        role: Role instance
    """
    membership = models.TeamMember.objects.get(user=user, team=team)
    membership.role = role
    membership.save()


def get_user_organisations(user):
    """Get all organisations a user is a member of.

    Args:
        user: User instance

    Returns:
        QuerySet of Organisation instances
    """
    return models.Organisation.objects.filter(members__user=user).distinct()


def get_user_teams(user):
    """Get all teams a user is a member of.

    Args:
        user: User instance

    Returns:
        QuerySet of Team instances
    """
    return models.Team.objects.filter(members__user=user).distinct()


def get_user_teams_in_organisation(user, organisation):
    """Get all teams in an organisation that a user is a member of.

    Args:
        user: User instance
        organisation: Organisation instance

    Returns:
        QuerySet of Team instances
    """
    return models.Team.objects.filter(
        organisation=organisation,
        members__user=user,
    ).distinct()
