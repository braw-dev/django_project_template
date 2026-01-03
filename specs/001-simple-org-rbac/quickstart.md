# Quickstart: Simple Organisation RBAC

## Overview

This feature replaces `django-guardian` with a custom `Organisation -> Team -> User` RBAC system powered by `django-rules`.

## Checking Permissions

### In Python Code (Views/Services)

```python
import rules

# Check if user can edit an organization
if rules.has_perm('organizations.change_organisation', user, org):
    # do something
    pass

# Check if user can edit a team
if rules.has_perm('organizations.change_team', user, team):
    # do something
    pass
```

### In Templates

```django
{% load rules %}

{% has_perm 'organizations.change_organisation' user org as can_edit_org %}
{% if can_edit_org %}
    <a href="...">Edit Org</a>
{% endif %}
```

### Decorators

```python
from project_name.organizations.decorators import require_org_perm

@require_org_perm('organizations.change_organisation')
def my_view(request, org_slug):
    # ...
```

## Creating Roles

Global roles are created via data migration.

```python
from project_name.organizations.models import Role

# Create a custom Org-specific role
custom_role = Role.objects.create(
    name="Project Manager",
    organization=my_org,
    permissions={
        "can_create_projects": True,
        "can_view_reports": True
    }
)
```

## Assigning Members

```python
from project_name.organizations.services import add_user_to_org

add_user_to_org(user, org, role=admin_role)
```
