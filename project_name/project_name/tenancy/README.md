# Team-First Tenancy

This app provides the default multi-tenancy model for generated projects.

## Core concepts

- **Team**: the top-level shared container for memberships, billing, and team-owned data
- **TeamMembership**: links an account to a team as `owner`, `admin`, or `member`
- **TeamInvitation**: email-delivered invitation for a specific email address, redeemed via a signed
  token
- **TenantScopedModel**: abstract base for models that must belong to a team
- **ApiToken**: example team-scoped model showing the explicit auth-time unscoped lookup

## Safe defaults

- team-owned models must inherit from `TenantScopedModel`
- request team context is resolved from `/t/{team_slug}/`
- use `user_has_team_perm(user=user, permission_name=perm, team=team)` for authorization
- scoped managers are convenience only, not a security boundary
- security-critical queries should use `all_objects` with explicit team filters

## Example model

```python
from django.db import models

from {{ project_name }}.tenancy.models import TenantScopedModel


class Project(TenantScopedModel):
    name = models.CharField(max_length=255)
```

## Example service

```python
from {{ project_name }}.tenancy.permissions import user_has_team_perm


def create_project(*, actor, team, name):
    if not user_has_team_perm(
        user=actor,
        permission_name="projects.add_project",
        team=team,
    ):
        raise ValueError("Not allowed")

    return Project.all_objects.create(team=team, name=name)
```

## Queryset gotcha

`Project.objects.all()` will auto-filter when an active team context exists, but Django
ORM APIs can bypass that manager. Treat it as convenience only.

See `{{ project_name }}/tokens/README.md` for the API token example and `SECURITY.md` for the full
security model and Postgres RLS guidance.
