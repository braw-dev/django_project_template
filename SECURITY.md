# Security Model

This template defaults to a **Team-first multi-tenancy** model.

## Core invariants

- Every tenant-owned row must have a non-null `team_id`.
- Users may only access data for teams they belong to.
- Roles are per-team, never global.
- `TenantScopedManager` is a convenience helper, **not** the security boundary.
- Security-critical code must use explicit membership checks and explicit team filters.
- Invitation links are signed, expiring, email-bound, and single-use.
- API token auth is the one explicit unscoped lookup path and must remain tightly bounded.
- Optional Postgres RLS is defence in depth, not the only isolation layer.

## Default tenant model

- `Team`: the tenant/workspace/account boundary
- `TeamMembership(user, team, role)`
- roles: `owner`, `admin`, `member`
- active team resolved from `/t/{team_slug}/`

## Authorization layers

### 1. Data model boundary

Tenant-owned models must inherit from `TenantScopedModel`.

```python
from {{ project_name }}.tenancy.models import TenantScopedModel


class Project(TenantScopedModel):
    name = models.CharField(max_length=255)
```

That guarantees a required `team_id` on the model.

### 2. Request team context

`ActiveTeamMiddleware` inspects `/t/{team_slug}/...` and `/api/v1/teams/{team_slug}/...` routes and sets:

- `request.team`
- `request.team_membership`

For authenticated users, non-members are denied with `404` to reduce tenant enumeration.

For bearer-token API requests, the auth class sets `request.team` directly after token verification. That is deliberate: Django middleware runs before Django Ninja auth handlers, so token-auth team resolution cannot live only in middleware.

### 3. Explicit permission checks

Use `user_has_team_perm(user, perm_name, team, obj=None)` for authorization.

Examples:

- `billing.view_subscription`
- `billing.change_subscription`
- `tenancy.manage_team_members`
- `tenancy.manage_team_billing`

Role defaults:

- `owner`: all team permissions
- `admin`: standard CRUD permissions plus team member/settings/API token management
- `member`: read/view permissions only

### 4. Explicit service-layer enforcement

Mutations should happen through services that accept `actor` and `team`.

```python
def create_project(*, actor, team, name):
    if not user_has_team_perm(actor, "projects.add_project", team):
        raise ValueError("Not allowed")

    return Project.all_objects.create(team=team, name=name)
```

Use `all_objects` for security-critical code so ambient request context does not change what the query means.

## TenantScopedManager gotchas

`TenantScopedManager` automatically filters by the active request team **when a team context exists**.

That helps reduce accidental leaks, but it is **not sufficient for security** because Django ORM code can bypass it:

- `all_objects`
- reverse relations
- raw SQL
- custom managers
- admin queryset overrides
- management commands
- Celery/background tasks
- migrations/data backfills

Treat the scoped manager as a convenience default, not a permission system.

## API tokens

API token authentication is the one place where tenant scoping must be bypassed on purpose.

Flow:

1. parse the bearer token strictly
2. look up the candidate token via `ApiToken.objects.unscoped().for_token_auth()`
3. run a dummy hash check when no candidate exists to reduce timing leakage
4. verify the secret hash
5. set `request.team` and the current team context for the rest of the request

Rules:

- never store plaintext token secrets
- only show plaintext once at creation time
- do not add new unscoped auth lookups casually
- treat every `unscoped()` use as security-sensitive code review territory

## Invitations

Team invitations are backed by database rows plus signed tokens.

Validation checks at acceptance time:

- token signature is valid
- token has not expired
- invitation row still exists
- invitation was not revoked
- invitation was not already accepted
- authenticated user email matches invitation email

The token payload includes a stored `token_key`, so rotating or replacing the invitation invalidates older links.

## Postgres Row Level Security (optional)

If `ENABLE_POSTGRES_RLS=True` and the database vendor is PostgreSQL, the middleware also sets:

```sql
set_config('app.current_team_id', '<team-uuid>', false)
```

This allows Postgres RLS policies to enforce `team_id` at the database layer.

### Recommended policy shape

Use `nullif(..., '')` so cleared request context does not cast an empty string to UUID.

```sql
ALTER TABLE billing_subscription ENABLE ROW LEVEL SECURITY;

CREATE POLICY billing_subscription_team_isolation
ON billing_subscription
USING (
  team_id = nullif(current_setting('app.current_team_id', true), '')::uuid
)
WITH CHECK (
  team_id = nullif(current_setting('app.current_team_id', true), '')::uuid
);
```

Apply equivalent policies to every tenant-owned table.

### RLS limitations

RLS is strong, but only if you set team context correctly everywhere.
Pay attention to:

- management commands
- Celery/background jobs
- scripts
- data migrations
- superuser/database-owner connections
- PgBouncer transaction pooling

If using PgBouncer transaction pooling, prefer explicit transaction scoping with `SET LOCAL` or do not assume session state survives across statements.

## Support access

`django-hijack` is enabled in the template and currently uses `hijack.permissions.superusers_and_staff`.

That means staff users and superusers can impersonate other users if you keep the feature enabled in a generated project.

The template now records append-only `AuditEvent` rows for:

- `support.hijack_started`
- `support.hijack_ended`

Each event stores the actor, target user, timestamp, and available request metadata such as IP address and user agent.

The same audit trail also records the built-in privacy operations:

- `privacy.user_data_exported`
- `privacy.user_data_deleted`
- `privacy.user_data_delete_blocked`

And the template now uses the same pattern for other security-sensitive service-layer actions:

- `tokens.api_token_created`
- `tokens.api_token_revoked`
- `tenancy.team_created`
- `tenancy.membership_added`
- `tenancy.invitation_created`
- `tenancy.invitation_accepted`

The audit log is intentionally read-only in Django admin. The preferred pattern is to write audit rows inside the service-layer functions that own the change, so future security-sensitive mutations follow the same shape.

## Reverse proxy trust contract

In production, the template only trusts `X-Forwarded-Proto` and `X-Forwarded-For` when **both** of these are true:

- `TRUSTED_PROXY_IPS` is set to one or more explicit proxy IPs or CIDR ranges
- the immediate peer (`REMOTE_ADDR`) is in that trusted list

Default behavior is safer: `TRUSTED_PROXY_IPS` is empty, so forwarded headers are ignored and audit IPs fall back to `REMOTE_ADDR`.

This means a generated project must not rely on spoofable client-supplied forwarding headers unless you have put a real reverse proxy in front of Django and documented its source addresses.

Recommended contract:

- bind the app only to localhost or a private interface
- put Caddy in front of it as the only public ingress
- set `TRUSTED_PROXY_IPS` to the exact Caddy source IPs or private-network CIDRs that will reach Django
- do not expose Gunicorn directly to the public internet
- if the proxy path changes, update `TRUSTED_PROXY_IPS` before enabling HTTPS redirect assumptions

## Billing security

Billing in the template is team-owned. Billing API endpoints require:

- authenticated user
- team membership
- `tenancy.manage_team_billing`

By default that permission is owner-only.

Billing webhooks use provider signature verification and persist provider event IDs so duplicate deliveries are ignored safely.

## When adding new tenant-owned code

Checklist:

1. Inherit from `TenantScopedModel`
2. Require `actor` and `team` in service methods
3. Check `user_has_team_perm(...)`
4. Use `all_objects` with explicit `team=...` in security-critical queries
5. Add tests for cross-team denial paths
6. If using Postgres RLS, add a matching RLS policy for the table
