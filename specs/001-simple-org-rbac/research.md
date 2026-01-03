# Research: Simple Organisation RBAC

## Context

We are replacing `django-guardian` with a custom, simpler RBAC system using `Organisation -> Team -> User` hierarchy and `django-rules`.

## Technical Decisions

### 1. Data Model Structure

**Decision**: Create a new app `organizations` to house the RBAC models.
**Rationale**: Keeps auth/org logic separate from `users` (which focuses on authentication and profile) and `core` (business logic).

**Entities**:

- `Organisation`: Root entity.
- `Team`: Child of Organisation.
- `Role`: Defines permissions. Can be Global (org=None) or Contextual (org=FK).
- `OrganisationMember`: Links User <-> Org <-> Role.
- `TeamMember`: Links User <-> Team <-> Role.

**Alternative Considered**: Adding fields to `User` model.
**Reason for Rejection**: Too coupled; doesn't support multiple orgs/teams cleanly.

### 2. Permissions Storage

**Decision**: `JSONField` in `Role` model.
**Rationale**: Flexible, allows "grug brain" simple boolean checks (e.g., `{"can_edit": true}`). Easy to extend without schema migrations.
**Pattern**:

```python
class Role(models.Model):
    permissions = models.JSONField(default=dict) # {"resource:action": true}
```

### 3. Permission Checking Library

**Decision**: `django-rules`.
**Rationale**: Lightweight, logical composition of rules (predicates). Fits the requirement.
**Implementation**:

- Define predicates like `is_org_member`, `has_role_permission`.
- Register rules for models.

### 4. Middleware & Access Control

**Decision**:

- Custom Middleware to catch `PermissionDenied` and render appropriate error (or 404 to prevent enumeration).
- Custom Decorator `@require_permission(perm)` that uses `django-rules`.
**Rationale**: specific requirement to "verify permissions (404 if not authorized)".

### 5. Template Tags

**Decision**: Custom template tag `{% has_perm 'action' obj %}` wrapping `rules.has_perm`.

## Unknowns & Clarifications (Resolved)

- **Clarification**: "Contextual saas roles so don't use django groups".
  - **Resolution**: We will explicitly NOT use `auth.Group`. Our `Role` model effectively replaces it for this context.
- **Clarification**: "Global System Role".
  - **Resolution**: `Role` with `organization=None` is global.

## Dependencies

- Remove: `django-guardian`
- Add: `django-rules`

## Migration Strategy

Since this is a template, we just modify the template files. No runtime migration needed for existing data (as it's a template for new projects).
