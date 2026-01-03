"""django-rules configuration for organizations app."""

import rules

from . import predicates  # noqa: F401

# Organization rules
rules.add_rule(
    "organizations.view_organisation",
    predicates.is_org_member | rules.is_superuser,
)

rules.add_rule(
    "organizations.change_organisation",
    predicates.is_org_admin | rules.is_superuser,
)

rules.add_rule(
    "organizations.delete_organisation",
    predicates.is_org_admin | rules.is_superuser,
)

# Team rules
rules.add_rule(
    "organizations.view_team",
    predicates.is_team_member | predicates.is_org_admin_for_team | rules.is_superuser,
)

rules.add_rule(
    "organizations.change_team",
    predicates.is_team_admin | predicates.is_org_admin_for_team | rules.is_superuser,
)

rules.add_rule(
    "organizations.delete_team",
    predicates.is_team_admin | predicates.is_org_admin_for_team | rules.is_superuser,
)
