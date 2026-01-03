"""Tests for organizations app."""

import rules
from django.contrib.auth import get_user_model
from django.test import TestCase

from . import models, services

User = get_user_model()


class OrganisationTestCase(TestCase):
    """Tests for Organisation model and related logic."""

    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123",
        )
        self.other_user = User.objects.create_user(
            username="otheruser",
            email="other@example.com",
            password="testpass123",
        )

        # Create global roles
        self.admin_role = models.Role.objects.create(
            name="Admin",
            organisation=None,
            permissions={"*": True},
        )
        self.editor_role = models.Role.objects.create(
            name="Editor",
            organisation=None,
            permissions={"can_edit": True, "can_create": True},
        )
        self.viewer_role = models.Role.objects.create(
            name="Viewer",
            organisation=None,
            permissions={},
        )

    def test_create_organisation(self):
        """Test creating an organization."""
        org = services.create_organisation(
            name="Test Org",
            slug="test-org",
            owner=self.user,
        )
        self.assertEqual(org.name, "Test Org")
        self.assertEqual(org.slug, "test-org")
        self.assertEqual(org.owner, self.user)

    def test_add_user_to_organisation(self):
        """Test adding a user to an organization."""
        org = services.create_organisation(
            name="Test Org",
            slug="test-org",
            owner=self.user,
        )
        member = services.add_user_to_organisation(self.user, org, self.admin_role)
        self.assertEqual(member.user, self.user)
        self.assertEqual(member.organisation, org)
        self.assertEqual(member.role, self.admin_role)

    def test_cannot_add_user_twice(self):
        """Test that a user cannot be added twice to the same org."""
        org = services.create_organisation(
            name="Test Org",
            slug="test-org",
        )
        services.add_user_to_organisation(self.user, org, self.admin_role)
        with self.assertRaises(ValueError):
            services.add_user_to_organisation(self.user, org, self.viewer_role)

    def test_remove_user_from_organisation(self):
        """Test removing a user from an organization."""
        org = services.create_organisation(
            name="Test Org",
            slug="test-org",
        )
        services.add_user_to_organisation(self.user, org, self.admin_role)
        services.remove_user_from_organisation(self.user, org)

        self.assertFalse(
            models.OrganisationMember.objects.filter(user=self.user, organisation=org).exists()
        )

    def test_org_admin_permission(self):
        """Test org admin permission check."""
        org = services.create_organisation(
            name="Test Org",
            slug="test-org",
        )
        services.add_user_to_organisation(self.user, org, self.admin_role)

        self.assertTrue(rules.has_perm("organizations.view_organisation", self.user, org))
        self.assertTrue(rules.has_perm("organizations.change_organisation", self.user, org))

    def test_org_viewer_no_edit_permission(self):
        """Test that org viewer cannot edit."""
        org = services.create_organisation(
            name="Test Org",
            slug="test-org",
        )
        services.add_user_to_organisation(self.user, org, self.viewer_role)

        self.assertTrue(rules.has_perm("organizations.view_organisation", self.user, org))
        self.assertFalse(rules.has_perm("organizations.change_organisation", self.user, org))

    def test_non_member_no_permission(self):
        """Test that non-members have no permission."""
        org = services.create_organisation(
            name="Test Org",
            slug="test-org",
        )

        self.assertFalse(rules.has_perm("organizations.view_organisation", self.user, org))


class TeamTestCase(TestCase):
    """Tests for Team model and related logic."""

    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123",
        )
        self.other_user = User.objects.create_user(
            username="otheruser",
            email="other@example.com",
            password="testpass123",
        )

        # Create global roles
        self.admin_role = models.Role.objects.create(
            name="Admin",
            organisation=None,
            permissions={"*": True},
        )
        self.editor_role = models.Role.objects.create(
            name="Editor",
            organisation=None,
            permissions={"can_edit": True},
        )
        self.viewer_role = models.Role.objects.create(
            name="Viewer",
            organisation=None,
            permissions={},
        )

        self.org = services.create_organisation(
            name="Test Org",
            slug="test-org",
        )

    def test_create_team(self):
        """Test creating a team."""
        team = services.create_team(self.org, name="Test Team", slug="test-team")
        self.assertEqual(team.name, "Test Team")
        self.assertEqual(team.organisation, self.org)

    def test_add_user_to_team(self):
        """Test adding a user to a team."""
        services.add_user_to_organisation(self.user, self.org, self.admin_role)
        team = services.create_team(self.org, name="Test Team", slug="test-team")
        member = services.add_user_to_team(self.user, team, self.editor_role)
        self.assertEqual(member.user, self.user)
        self.assertEqual(member.team, team)

    def test_cannot_add_non_member_to_team(self):
        """Test that a non-org member cannot be added to a team."""
        team = services.create_team(self.org, name="Test Team", slug="test-team")
        with self.assertRaises(ValueError):
            services.add_user_to_team(self.user, team, self.editor_role)

    def test_team_permission_by_membership(self):
        """Test team permissions based on team membership."""
        services.add_user_to_organisation(self.user, self.org, self.viewer_role)
        team = services.create_team(self.org, name="Test Team", slug="test-team")
        services.add_user_to_team(self.user, team, self.editor_role)

        self.assertTrue(rules.has_perm("organizations.view_team", self.user, team))
        self.assertTrue(rules.has_perm("organizations.change_team", self.user, team))

    def test_cascading_org_admin_permission(self):
        """Test that org admin has access to all teams."""
        services.add_user_to_organisation(self.user, self.org, self.admin_role)
        team = services.create_team(self.org, name="Test Team", slug="test-team")

        # Org admin should have team access without being a team member
        self.assertTrue(rules.has_perm("organizations.view_team", self.user, team))
        self.assertTrue(rules.has_perm("organizations.change_team", self.user, team))

    def test_remove_user_from_org_removes_from_teams(self):
        """Test that removing user from org removes them from all teams."""
        services.add_user_to_organisation(self.user, self.org, self.admin_role)
        team = services.create_team(self.org, name="Test Team", slug="test-team")
        services.add_user_to_team(self.user, team, self.editor_role)

        services.remove_user_from_organisation(self.user, self.org)

        self.assertFalse(models.TeamMember.objects.filter(user=self.user, team=team).exists())
