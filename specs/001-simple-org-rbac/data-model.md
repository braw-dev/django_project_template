# Data Model: Simple Organisation RBAC

## App: `organizations`

### Model: `Organisation`

Represents a tenant or top-level grouping.

| Field | Type | Attributes | Description |
|-------|------|------------|-------------|
| `id` | UUID | PK | |
| `name` | CharField | max_length=255 | Display name |
| `slug` | SlugField | unique=True | URL-friendly identifier |
| `owner` | FK(User) | null=True, on_delete=SET_NULL | Optional primary owner |
| `created_at`| DateTime | auto_now_add=True | |
| `updated_at`| DateTime | auto_now=True | |

### Model: `Team`

Represents a sub-group within an Organisation.

| Field | Type | Attributes | Description |
|-------|------|------------|-------------|
| `id` | UUID | PK | |
| `organisation` | FK(Organisation) | on_delete=CASCADE, related_name="teams" | Parent Org |
| `name` | CharField | max_length=255 | |
| `slug` | SlugField | | Unique within Org |
| `created_at`| DateTime | auto_now_add=True | |
| `updated_at`| DateTime | auto_now=True | |

**Meta**: `unique_together = [('organisation', 'slug')]`

### Model: `Role`

Defines a set of permissions.

| Field | Type | Attributes | Description |
|-------|------|------------|-------------|
| `id` | UUID | PK | |
| `name` | CharField | max_length=100 | e.g. "Admin", "Editor" |
| `organization` | FK(Organisation) | null=True, blank=True, on_delete=CASCADE | Null = Global Role |
| `permissions` | JSONField | default=dict | e.g. `{"can_edit": true}` |

**Meta**: `unique_together = [('organization', 'name')]`

### Model: `OrganisationMember`

Links a User to an Organisation with a Role.

| Field | Type | Attributes | Description |
|-------|------|------------|-------------|
| `id` | UUID | PK | |
| `user` | FK(User) | on_delete=CASCADE | |
| `organisation` | FK(Organisation) | on_delete=CASCADE | |
| `role` | FK(Role) | on_delete=PROTECT | |
| `joined_at` | DateTime | auto_now_add=True | |

**Meta**: `unique_together = [('user', 'organisation')]`

### Model: `TeamMember`

Links a User to a Team with a Role.

| Field | Type | Attributes | Description |
|-------|------|------------|-------------|
| `id` | UUID | PK | |
| `user` | FK(User) | on_delete=CASCADE | |
| `team` | FK(Team) | on_delete=CASCADE | |
| `role` | FK(Role) | on_delete=PROTECT | |
| `joined_at` | DateTime | auto_now_add=True | |

**Meta**: `unique_together = [('user', 'team')]`

## Default Roles (Global)

1. **Admin**: `{"*": true}`
2. **Editor**: `{"can_edit": true, "can_create": true, ...}`
3. **Viewer**: `{}` (Read only)

## Logic

- **Cascading Permissions**:
  - `OrganisationMember` with Admin role implies full access to all Teams in that Org.
  - `TeamMember` permissions apply only to that Team.
