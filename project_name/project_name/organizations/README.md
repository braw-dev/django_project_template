# Organizations RBAC System

This app provides a simple, flexible role-based access control (RBAC) system
organized around Organizations and Teams.

## Architecture

- **Organisation**: Top-level tenant/workspace
- **Team**: Sub-group within an Organisation
- **Role**: Defines permissions (can be Global or org-specific)
- **OrganisationMember**: Links User -> Organisation -> Role
- **TeamMember**: Links User -> Team -> Role

## Key Features

1. **Multi-tenant**: Users can be members of multiple organizations
2. **Hierarchical**: Organizations contain Teams
3. **Cascading Permissions**: Org Admins automatically have access to all Teams
4. **Flexible Permissions**: JSON-based permission storage allows easy extension
5. **django-rules Integration**: Clear predicate-based permission checking

## Usage

### In Python Code

```python
import rules
from organizations.decorators import require_org_permission

# Check permission directly
if rules.has_perm('organizations.change_organisation', user, org):
    # do something
    pass

# Use decorators for views
@require_org_permission('organizations.change_organisation')
def edit_org(request, org_slug):
    org = Organisation.objects.get(slug=org_slug)
    # ...
```

### In Templates

```django
{% templatetag openblock %} load org_permissions {% templatetag closeblock %}

{% templatetag openblock %} has_org_perm user 'organizations.change_organisation' org as can_edit {% templatetag closeblock %}
{% templatetag openblock %} if can_edit {% templatetag closeblock %}
    <a href="...">Edit Organization</a>
{% templatetag openblock %} endif {% templatetag closeblock %}

{% templatetag opencomment %} Get user's role {% templatetag closecomment %}
{% templatetag openvariable %} org|user_org_role:user {% templatetag closevariable %}
```

### Services

```python
from organizations import services

# Create organization (creator becomes admin)
org = services.create_organisation(
    name="Acme Corp",
    slug="acme",
    owner=request.user
)

# Add user to organization
admin_role = Role.objects.get(name="Admin", organisation=None)
services.add_user_to_organisation(user, org, admin_role)

# Create team
team = services.create_team(org, "Engineering", "engineering")

# Add user to team
editor_role = Role.objects.get(name="Editor", organisation=None)
services.add_user_to_team(user, team, editor_role)
```

## Permission Model

### Global Roles (organisation=None)

- **Admin**: `{"*": true}` - Full access
- **Editor**: `{"can_create": true, "can_edit": true}` - Create and edit
- **Viewer**: `{}` - Read-only access

### Custom Roles

Create org-specific or team-specific roles with custom permissions:

```python
custom_role = Role.objects.create(
    name="Project Manager",
    organisation=org,
    permissions={
        "can_manage_team": True,
        "can_view_reports": True,
        "can_edit_budget": True,
    }
)
```

## Security Features

1. **Permission Checks**: Always verify permissions before allowing access
2. **404 on Denied Access**: Middleware converts permission errors to 404 to prevent data leakage
3. **Cascading Admin**: Org admins automatically access all teams (no team membership needed)
4. **PROTECT on Delete**: Roles cannot be deleted if users are assigned to them

## Queryset Helpers

```python
# Get all organizations user is in
organisations = services.get_user_organisations(user)

# Get all teams user is in
teams = services.get_user_teams(user)

# Get teams in specific org
teams_in_org = services.get_user_teams_in_organisation(user, org)
```

## Middleware

The `OrganisationPermissionMiddleware` is optional but recommended:

```python
MIDDLEWARE = [
    # ... other middleware
    "organizations.middleware.OrganisationPermissionMiddleware",
]
```

This middleware catches `PermissionError` exceptions and converts them to
`Http404` responses to prevent accidental information leakage.
