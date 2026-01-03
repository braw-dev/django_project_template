# Feature Specification: Simple Organisation RBAC

**Feature Branch**: `001-simple-org-rbac`  
**Created**: 2026-01-03  
**Status**: Draft  
**Input**: User description: "remove django guardian and instead replace with a simple Organisation -> Team -> User approach. Each level can have 3 roles: 1) Admin 2) Editor 3) Viewer."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Organisation Management (Priority: P1)

As a User, I need to create and manage Organisations so that I can group resources and teams.

**Why this priority**: Foundation of the hierarchy.

**Independent Test**: Can be tested by creating an Org and assigning members without Teams existing yet.

**Acceptance Scenarios**:

1. **Given** a User, **When** they create a new Organisation, **Then** they are automatically assigned the 'Admin' role for that Organisation.
2. **Given** an Organisation Admin, **When** they invite another User, **Then** they can assign 'Admin', 'Editor', or 'Viewer' role.
3. **Given** an Organisation Viewer, **When** they try to change Organisation settings, **Then** access is denied.

---

### User Story 2 - Team Management (Priority: P1)

As an Organisation Admin or Editor, I need to create Teams and assign users to them so that I can organize work subsets.

**Why this priority**: Second level of the hierarchy.

**Independent Test**: Requires Organisation existence.

**Acceptance Scenarios**:

1. **Given** an Organisation, **When** an Admin creates a Team, **Then** the Team is linked to that Organisation.
2. **Given** a Team, **When** a User is added to the Team, **Then** a role ('Admin', 'Editor', 'Viewer') must be specified.
3. **Given** a User who is NOT in the Organisation, **When** trying to add them to a Team, **Then** the system should either fail or auto-add them to the Org (Assume fail/require Org membership first for simplicity/explicit behavior).

---

### User Story 3 - Role-Based Access Enforcement (Priority: P1)

As a Developer, I need to ensure permissions are checked against these custom roles instead of Django Guardian.

**Why this priority**: Core security requirement replacing the old system.

**Independent Test**: Unit tests checking permission checks.

**Acceptance Scenarios**:

1. **Given** a Resource belonging to an Organisation, **When** an Org Viewer tries to edit it, **Then** permission is denied.
2. **Given** a Resource belonging to a Team, **When** a Team Editor tries to edit it, **Then** permission is granted.
3. **Given** a Resource belonging to a Team, **When** an Org Admin (who is NOT explicitly in the Team) tries to edit it, **Then** permission is granted (cascading permissions).

---

### Edge Cases

- What happens when a User is removed from an Organisation?
  - They should be removed from all Teams in that Organisation.
- What happens if an Organisation is deleted?
  - All Teams and Memberships should be deleted (Cascade).
- Can a User have different roles in different Teams of the same Org?
  - Yes.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST define an `Organisation` model.
- **FR-002**: System MUST define a `Team` model with a relationship to `Organisation`.
- **FR-003**: System MUST support `OrganisationMembership` linking User and Organisation with a Role.
- **FR-004**: System MUST support `TeamMembership` linking User and Team with a Role.
- **FR-005**: Supported Roles at both levels MUST be: `Admin`, `Editor`, `Viewer`.
- **FR-006**: System MUST remove `django-guardian` dependency and configuration.
- **FR-007**: System MUST provide a mechanism to query permissions based on these models.
- **FR-008**: Organisation Admin role MUST imply full access to all Teams within that Organisation (Cascading Admin).

### Key Entities

- **Organisation**: Name, Slug, Owner (optional).
- **Team**: Name, Slug, Organisation (FK).
- **OrganisationMember**: User (FK), Organisation (FK), Role (Choice).
- **TeamMember**: User (FK), Team (FK), Role (Choice).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Application functions without `django-guardian` installed.
- **SC-002**: Users can be assigned to Organisations and Teams with distinct roles.
- **SC-003**: Permission checks return correct results for all 3 roles at both Org and Team levels.
- **SC-004**: Organisation creation assigns the creator as Admin.
