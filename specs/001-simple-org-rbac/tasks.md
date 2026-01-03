# Tasks: Simple Organisation RBAC

**Branch**: `001-simple-org-rbac` | **Spec**: [specs/001-simple-org-rbac/spec.md](spec.md)

## Phases

### Phase 1: Setup

**Goal**: Initialize the new app and manage dependencies.
**Independent Test**: App exists, dependencies are correct, project runs without guardian.

- [x] T001 Create `organizations` app structure in `project_name/project_name/organizations` (apps.py-tpl, **init**.py-tpl, etc)
- [x] T002 Add `django-rules` to `pyproject.toml`
- [x] T003 Remove `django-guardian` from `pyproject.toml` and `project_name/project_name/settings.py-tpl`
- [x] T004 Configure `django-rules` backend in `project_name/project_name/settings.py-tpl`

### Phase 2: Foundation

**Goal**: Establish the core data models and default roles.
**Independent Test**: Models can be migrated, Global Roles exist in DB.

- [x] T005 [P] Create `Organisation` and `Team` models in `project_name/project_name/organizations/models.py-tpl`
- [x] T006 [P] Create `Role` model with JSONField in `project_name/project_name/organizations/models.py-tpl`
- [x] T007 [P] Create `OrganisationMember` and `TeamMember` models in `project_name/project_name/organizations/models.py-tpl`
- [x] T008 Create migration/fixture for Global Roles (Admin, Editor, Viewer) in `project_name/project_name/organizations/migrations/`

### Phase 3: User Story 1 - Organisation Management

**Goal**: Users can create/manage Organisations and Members.
**Independent Test**: Test Org creation, Member assignment, and basic Org permissions.

- [x] T009 [P] [US1] Implement `Organisation` services (create, update) in `project_name/project_name/organizations/services.py-tpl`
- [x] T010 [US1] Implement logic to assign Creator as Admin in `project_name/project_name/organizations/services.py-tpl`
- [x] T011 [US1] Implement `OrganisationMember` management services in `project_name/project_name/organizations/services.py-tpl`
- [x] T012 [US1] Define predicates for Org access (`is_org_member`, `has_org_perm`) in `project_name/project_name/organizations/predicates.py-tpl`
- [x] T013 [US1] Register Org rules in `project_name/project_name/organizations/rules.py-tpl`
- [x] T014 [US1] Add unit tests for Org management in `project_name/project_name/organizations/tests.py-tpl`

### Phase 4: User Story 2 - Team Management

**Goal**: Org Admins/Editors can manage Teams and Team Members.
**Independent Test**: Test Team creation, Team Member assignment, and Cascading Admin access.

- [x] T015 [P] [US2] Implement `Team` services in `project_name/project_name/organizations/services.py-tpl`
- [x] T016 [US2] Implement `TeamMember` services in `project_name/project_name/organizations/services.py-tpl`
- [x] T017 [US2] Define predicates for Team access (`is_team_member`, `org_admin_access`) in `project_name/project_name/organizations/predicates.py-tpl`
- [x] T018 [US2] Register Team rules in `project_name/project_name/organizations/rules.py-tpl`
- [x] T019 [US2] Add unit tests for Team management and cascading permissions in `project_name/project_name/organizations/tests.py-tpl`

### Phase 5: User Story 3 - Role-Based Access Enforcement

**Goal**: Enforce permissions via Middleware, Decorators, and Template Tags.
**Independent Test**: Verify 404/403 on unauthorized access, verify template tag output.

- [x] T020 [US3] Implement custom Middleware for permission verification in `project_name/project_name/organizations/middleware.py-tpl`
- [x] T021 [US3] Implement `@require_permission` decorator in `project_name/project_name/organizations/decorators.py-tpl`
- [x] T022 [US3] Implement template tags in `project_name/project_name/organizations/templatetags/org_permissions.py-tpl`
- [x] T023 [US3] Add unit tests for Middleware, Decorators, and Template Tags in `project_name/project_name/organizations/tests.py-tpl`

### Phase 6: Polish & Documentation

**Goal**: Finalize feature and update documentation.
**Independent Test**: Docs are accurate, linting passes.

- [x] T024 Update project documentation to reflect RBAC changes in `docs/PRODUCT_OVERVIEW.md`
- [x] T025 Create developer usage guide for permissions in `project_name/project_name/organizations/README.md`
- [x] T026 Run `ruff` and ensure all linting checks pass

## Implementation Strategy

- **MVP**: Phases 1-3 provide the core Org capability.
- **Full Feature**: Phases 4-5 add Team granularity and enforcement tools.
- **Docs**: Phase 6 ensures future developers understand the new system.

## Dependencies

- Phase 2 depends on Phase 1
- Phase 3 depends on Phase 2
- Phase 4 depends on Phase 3
- Phase 5 depends on Phase 4
- Phase 6 depends on Phase 5
