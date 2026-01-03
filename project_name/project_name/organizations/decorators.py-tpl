"""Decorators for permission-based access control."""

from functools import wraps

import rules
from django.http import Http404
from django.shortcuts import get_object_or_404


def require_permission(permission_name, obj_kwarg="organisation"):
    """Decorator to require permission to access a view.

    Raises Http404 if permission denied to prevent data leakage.

    Args:
        permission_name: Permission string (e.g., 'organizations.change_organisation')
        obj_kwarg: URL kwarg name for the object (default: 'organisation')
    """

    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            # Get the object from kwargs
            obj_id = kwargs.get(obj_kwarg)
            if not obj_id:
                raise ValueError(f"URL must have '{obj_kwarg}' kwarg for permission check")

            # Check permission
            if not rules.has_perm(permission_name, request.user):
                raise Http404("Not found")

            return view_func(request, *args, **kwargs)

        return wrapper

    return decorator


def require_org_permission(permission_name):
    """Decorator to require organization permission.

    Args:
        permission_name: Permission string (e.g., 'organizations.change_organisation')
    """

    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            org_slug = kwargs.get("org_slug")
            if not org_slug:
                raise ValueError("URL must have 'org_slug' kwarg")

            from . import models

            org = get_object_or_404(models.Organisation, slug=org_slug)

            if not rules.has_perm(permission_name, request.user, org):
                raise Http404("Not found")

            return view_func(request, *args, **kwargs)

        return wrapper

    return decorator


def require_team_permission(permission_name):
    """Decorator to require team permission.

    Args:
        permission_name: Permission string (e.g., 'organizations.change_team')
    """

    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            team_slug = kwargs.get("team_slug")
            org_slug = kwargs.get("org_slug")

            if not team_slug or not org_slug:
                raise ValueError("URL must have 'org_slug' and 'team_slug' kwargs")

            from . import models

            org = get_object_or_404(models.Organisation, slug=org_slug)
            team = get_object_or_404(models.Team, organisation=org, slug=team_slug)

            if not rules.has_perm(permission_name, request.user, team):
                raise Http404("Not found")

            return view_func(request, *args, **kwargs)

        return wrapper

    return decorator
