# Implementation Complete: Simple Organisation RBAC

**Status**: ✅ COMPLETE  
**Branch**: `001-simple-org-rbac`  
**Date**: 2026-01-03  
**Tasks Completed**: 26/26

## Summary

Successfully replaced `django-guardian` with a custom, lightweight Organization -> Team -> User RBAC system powered by `django-rules`. The implementation follows Grug Brain simplicity principles and provides a clean, extensible permission model.

## What Was Built

### 1. New `organizations` App

Created a complete Django app at `project_name/project_name/organizations/` with:

- **Models**:
  - `Organisation`: Top-level tenant
  - `Team`: Sub-group within org
  - `Role`: Permission container (JSONField for flexibility)
  - `OrganisationMember`: User-Org-Role linkage
  - `TeamMember`: User-Team-Role linkage

- **Business Logic** (`services.py`):
  - Organization management (create, add/remove members, update roles)
  - Team management (create, add/remove members, update roles)
  - User queries (get orgs, teams, teams in org)
  - Cascading removal (removing org member removes from all teams)

- **Permission System** (`predicates.py` + `rules.py`):
  - Org-level predicates: `is_org_member`, `is_org_admin`, `has_org_permission`
  - Team-level predicates: `is_team_member`, `is_team_admin`, `is_org_admin_for_team`, `has_team_permission`
  - Rules registered with django-rules for `view_organisation`, `change_organisation`, `delete_organisation`, `view_team`, `change_team`, `delete_team`
  - Cascading: Org Admins automatically access all teams

- **Access Control**:
  - `decorators.py`: `@require_permission`, `@require_org_permission`, `@require_team_permission`
  - Raises `Http404` on denied access (prevents data leakage)
  - `middleware.py`: Catches `PermissionError` and converts to `Http404`

- **UI Integration** (`templatetags/org_permissions.py`):
  - `{% has_org_perm %}` template tag
  - `{% has_team_perm %}` template tag
  - `{{ org|user_org_role:user }}` filter
  - `{{ team|user_team_role:user }}` filter

- **Testing** (`tests.py`):
  - 20+ unit tests covering:
    - Organization creation and membership
    - Team creation and management
    - Permission checks (all roles)
    - Cascading admin permissions
    - Cascading member removal
    - Error cases

### 2. Data Migrations

Created initial migration with global roles:

- **Admin**: `{"*": true}` - Wildcard access
- **Editor**: `{"can_create": true, "can_edit": true}`
- **Viewer**: `{}` - Read-only

### 3. Dependencies Updated

**Removed**:

- `django-guardian` from `pyproject.toml`
- `guardian` from `INSTALLED_APPS` in settings
- `guardian.backends.ObjectPermissionBackend` from `AUTHENTICATION_BACKENDS`

**Added**:

- `django-rules` to `pyproject.toml`
- `rules.permissions.ObjectPermissionBackend` to `AUTHENTICATION_BACKENDS`
- `{{ project_name }}.organizations` to `INSTALLED_APPS`

### 4. Documentation

- **Developer Guide**: `project_name/project_name/organizations/README.md`
  - Architecture overview
  - Usage examples (Python, templates, services)
  - Permission model
  - Security features
  - Middleware info

- **Product Overview**: Updated `docs/PRODUCT_OVERVIEW.md`
  - Added section describing RBAC system
  - Referenced developer guide for details

## Design Principles Applied

✅ **Grug Brain (Simplicity)**

- JSON permissions instead of complex M2M permission tables
- Simple boolean checks: `role.permissions.get("permission") is True`
- Clear predicate-based rules with django-rules
- No unnecessary abstractions

✅ **Security First**

- 404 responses on unauthorized access (no enumeration)
- Cascading admin permissions prevent orphaned access
- Role deletion protected when in use (on_delete=PROTECT)
- User removal cascades through all related teams

✅ **One Stack (Django)**

- Uses standard Django models and ORM
- Integrates with django-allauth for authentication
- Built on django-rules (lightweight, established package)
- Uses Django's translation system (gettext_lazy)

✅ **Documentation First**

- Clear README in app
- Usage examples in quickstart
- Test cases serve as documentation
- Updated product docs

## File Structure Created

```text
project_name/project_name/organizations/
├── __init__.py-tpl
├── admin.py-tpl
├── apps.py-tpl
├── decorators.py-tpl         # Permission decorators
├── middleware.py-tpl          # Permission verification middleware
├── models.py-tpl              # Core models (Org, Team, Role, Members)
├── predicates.py-tpl          # django-rules predicates
├── rules.py-tpl               # django-rules configuration
├── services.py-tpl            # Business logic
├── tests.py-tpl               # 20+ unit tests
├── README.md                  # Developer guide
├── migrations/
│   ├── __init__.py-tpl
│   ├── 0001_initial.py-tpl    # (auto-generated)
│   └── 0002_create_global_roles.py-tpl  # Global roles
└── templatetags/
    ├── __init__.py-tpl
    └── org_permissions.py-tpl # Template tags
```

## Integration Points

Developers using this template can now:

```python
# In views
from organizations.decorators import require_org_permission
import rules

@require_org_permission('organizations.change_organisation')
def edit_org(request, org_slug):
    org = Organisation.objects.get(slug=org_slug)
    # User has been verified to have permission

# In services/logic
if rules.has_perm('organizations.change_team', user, team):
    # Update team
    pass

# In templates
{% load org_permissions %}
{% has_org_perm user 'organizations.change_organisation' org as can_edit %}
{% if can_edit %}<a href="...">Edit</a>{% endif %}
```

## What Replaces django-guardian

| Old (django-guardian) | New (organizations) |
|----------------------|-------------------|
| `guardian.assign_perm()` | `services.add_user_to_organisation()` / `services.add_user_to_team()` |
| `guardian.remove_perm()` | `services.remove_user_from_organisation()` / `services.remove_user_from_team()` |
| Per-object permissions | Org/Team role-based permissions |
| Complex M2M tables | Simple Role with JSONField |
| `guardian.shortcuts` | `organizations.services` functions |

## Testing

All 26 tasks completed and validated:

- ✅ Setup (T001-T004): App structure, dependencies, settings
- ✅ Foundation (T005-T008): Models, migrations, global roles
- ✅ User Story 1 (T009-T014): Org management, predicates, rules, tests
- ✅ User Story 2 (T015-T019): Team management, cascading permissions
- ✅ User Story 3 (T020-T023): Middleware, decorators, template tags, tests
- ✅ Documentation (T024-T026): Product docs, developer guide, linting

## Next Steps for Users of This Template

1. Run migrations: `python manage.py migrate organizations`
2. Create your first organization via admin or services
3. Add users to organizations with roles
4. Use `@require_org_permission` decorator for views
5. Use template tags to conditionally show actions in UI
6. Create custom roles with specific permissions as needed

## Success Criteria Met

✅ **SC-001**: Application functions without `django-guardian` installed  
✅ **SC-002**: Users can be assigned to Organisations and Teams with distinct roles  
✅ **SC-003**: Permission checks return correct results for all 3 roles at both Org and Team levels  
✅ **SC-004**: Organisation creation assigns the creator as Admin  

---

**Implementation complete. Feature ready for integration.**
