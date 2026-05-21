# Service / Selector Refactor Plan

## Why this exists

The template already uses service-layer ideas in several places, but it does not yet apply the
HackSoft-style services/selectors pattern consistently.

The main inconsistencies today are:

1. public service and selector functions do not always use explicit keyword-only parameters
2. some public domain functions are only partially typed
3. read logic and write logic are sometimes mixed in the same module
4. some query logic still lives in managers/querysets instead of selectors
5. a small amount of mutation logic still lives on models

The goal of this plan is to make the template's architecture more consistent without adding
ceremony for its own sake.

---

## Target conventions

These are the conventions this refactor should enforce.

### 1. Services own write operations and side effects

A service should:

- create, update, or delete data
- perform permission checks for writes
- call external systems
- send email
- write audit events
- return model instances or simple result objects

Preferred style:

```python
def create_team(*, actor: User, name: str, slug: str) -> Team:
    ...
```

### 2. Selectors own read operations

A selector should:

- query the database
- compose read-only data structures
- return model instances, querysets, or simple DTO-like dictionaries
- not modify state

Preferred style:

```python
def get_active_subscription(*, team: Team) -> Subscription | None:
    ...
```

### 3. Public domain functions should prefer explicit keyword-only arguments

For public service/selector APIs, use keyword-only arguments when practical.

Preferred style:

```python
def has_entitlement(*, team: Team, key: str) -> bool:
    ...
```

This applies especially to:

- functions in `services.py`, `selectors.py`, or equivalent explicit domain modules
- security-sensitive operations
- functions taking multiple parameters of similar shape
- APIs likely to be called from views, admin actions, commands, or other services

This does **not** need to be forced onto:

- Django-required method signatures (`save`, `delete`, admin hooks, middleware hooks, form hooks)
- signal handlers and framework callbacks
- very small private helpers unless doing so materially improves clarity
- QuerySet methods that are meant to preserve normal queryset chaining ergonomics

### 4. Type public service/selector parameters and return values

When stable types are available, annotate them explicitly.

Examples:

- `actor: User`
- `user: User`
- `team: Team`
- `request: HttpRequest | None`
- `-> QuerySet[ApiToken]`
- `-> dict[str, Any]`

Where Django or `ty` limitations make exact typing awkward, use the smallest practical type rather
than leaving parameters untyped.

### 5. Models stay lean

Models may keep:

- field definitions
- constraints
- `__str__`
- simple derived properties
- invariants that must always hold on the model itself

Models should avoid accumulating:

- orchestration logic
- permission checks
- external API calls
- email sending
- audit logging
- non-trivial persistence workflows

---

## Non-goals

This plan should **not** introduce:

- a large new abstraction layer
- generic service base classes
- repository objects
- DTO frameworks
- a deep `services/` and `selectors/` package tree for every app
- speculative refactors unrelated to the current audit

The template should stay boring and obvious.

---

## Refactor strategy

Use the smallest structure that makes the separation clear.

### Recommended module strategy

Use this default rule:

- keep small apps on `services.py` and `selectors.py`
- allow clearer, explicitly named modules when that improves readability
- do not create deep package trees unless a file is genuinely too large

Recommended examples:

- `tenancy/services.py`
- `tenancy/selectors.py`
- `billing/services.py`
- `billing/selectors.py`
- `users/privacy_services.py`
- `users/privacy_selectors.py`
- `core/newsletter_services.py`
- `pages/faq_selectors.py`

This keeps names explicit without overengineering a package hierarchy.

### Compatibility stance

This is a template repository, not a stable importable library. Prefer direct cleanup over
long-lived backwards-compatibility shims.

If an implementation phase renames a module, update all internal imports and tests in the same
change set. Only add a temporary compatibility re-export if the change would otherwise become noisy
or risky within the template itself.

---

## Current audit summary

## High-confidence mismatches

### Existing selector/service modules with signature drift

#### `project_name/project_name/billing/selectors.py-tpl`

Current public functions still using positional args:

- `has_active_subscription(team: Team) -> bool`
- `get_active_subscription(team: Team) -> Subscription | None`
- `has_entitlement(team: Team, key: str) -> bool`

Target shape:

```python
def has_active_subscription(*, team: Team) -> bool:
def get_active_subscription(*, team: Team) -> Subscription | None:
def has_entitlement(*, team: Team, key: str) -> bool:
```

#### `project_name/project_name/flags/services.py-tpl`

Current public function:

- `is_flag_enabled(flag_key: str, default: bool = False) -> bool`

Target shape:

```python
def is_flag_enabled(*, flag_key: str, default: bool = False) -> bool:
```

#### `project_name/project_name/tenancy/services.py-tpl`

Problems:

- several public params are untyped
- some public functions still take positional args
- one selector is mixed into a service module

Current mismatches:

- `create_team(*, name: str, slug: str, owner) -> Team`
- `validate_team_vat_number(*, actor, team: Team, billing_country: str, vat_number: str, request=None) -> Team` <!-- rumdl-disable-line MD013 -->
- `add_user_to_team(*, actor, team: Team, user, role: str) -> TeamMembership`
- `get_user_teams(user)`
- `create_invitation(*, actor, team: Team, email: str, role: str) -> TeamInvitation`
- `get_invitation_token(invitation: TeamInvitation) -> str`
- `build_invitation_accept_url(invitation: TeamInvitation, request) -> str`
- `send_invitation_email(invitation: TeamInvitation, request) -> None`
- `accept_invitation_from_token(*, token: str, user) -> TeamMembership`

#### `project_name/project_name/tokens/services.py-tpl`

Current issues:

- already keyword-only, but some params are untyped

Current mismatches:

- `create_api_token(*, team, user, name: str, ...) -> TokenCreationResult`
- `revoke_api_token(*, token: ApiToken, user) -> None`

#### `project_name/project_name/tokens/selectors.py-tpl`

Current issue:

- missing return type on `list_tokens_for_team`

#### `project_name/project_name/selectors.py-tpl`

Public functions are mostly fine. Internal helper typing could be tightened for consistency:

- `_get_price_label(...)` missing return type
- `_format_billing_interval(...)` missing return type

These are lower priority than public API cleanup.

---

## Service/selectors pattern currently spread across non-standard modules

These are not necessarily wrong, but they are inconsistent with the target architecture.

### `project_name/project_name/core/newsletter.py-tpl`

This is effectively a service module. It contains:

- signup creation
- token generation
- URL building
- email sending
- confirmation flow
- analytics side effects

Current public signature drift:

- `get_newsletter_confirmation_token(signup: NewsletterSignup) -> str`
- `build_newsletter_confirmation_url(signup: NewsletterSignup, request) -> str`
- `send_newsletter_confirmation_email(signup: NewsletterSignup, request) -> bool`
- `confirm_newsletter_signup(*, token: str, request=None) -> NewsletterSignup`

### `project_name/project_name/users/privacy.py-tpl`

This module currently mixes reads and writes.

Selector-like functions:

- `get_user_by_identifier(identifier: str)`
- `get_users_pending_deletion(*, now=None)`

Service-like functions:

- `export_user_data(...)`
- `delete_user_data(...)`
- `finalize_user_data_deletion(...)`

This is one of the clearest split candidates.

### `project_name/project_name/pages/faq.py-tpl`

This is effectively selector logic:

- `get_faq_entries`
- `get_categorized_faqs`
- `get_featured_faqs`

The signatures are already mostly fine. The question here is naming and consistency, not behavior.

### `project_name/project_name/billing/webhooks.py-tpl`

This module is service/orchestration code.

Current public functions still take positional args:

- `verify_webhook_signature(body: bytes, headers: Mapping[str, str]) -> VerifiedWebhookEvent`
- `process_webhook(body: bytes, headers: Mapping[str, str]) -> str`

### `project_name/project_name/tenancy/permissions.py-tpl`

This is not a selector module, but it is part of the domain read/authorization surface.

Current function:

- `user_has_team_perm(user, permission_name, team, obj=None) -> bool`

This should be evaluated for keyword-only conversion because it is public, security-sensitive, and
frequently called.

---

## Fat model audit

## Overall conclusion

There are **not many truly fat models** in the template today.

Most models are acceptably lean and mostly contain:

- `__str__`
- simple derived properties
- constraints and invariant enforcement

The main borderline cases are in API token handling and some manager/queryset query helpers.

## High-priority borderline cases

### `project_name/project_name/tokens/models.py-tpl`

#### `ApiToken.touch_last_used(self) -> None`

Why it is borderline:

- writes to persistence state
- contains update throttling logic
- is more than a plain convenience getter/setter

Recommendation:

- move the persistence workflow into a token service during the implementation phase
- keep the model method only if the team deliberately prefers this as a tiny, entity-local mutation

#### `ApiToken.revoke(self, *, actor) -> None`

Why it is borderline:

- mutates business state
- is part of a larger revocation workflow
- overlaps with service responsibilities

Recommendation:

- prefer revocation through `tokens/services.py`
- decide whether to remove the model method entirely or keep it as a very thin internal helper only

## Query logic living in managers/querysets

These are not classic fat models, but they are adjacent to the same architectural concern.

### `project_name/project_name/tokens/models.py-tpl`

- `ApiTokenQuerySet.active()`
- `ApiTokenQuerySet.for_token_auth()`

Recommendation:

- leave simple queryset helpers alone if they are internal convenience only
- if these become public app-facing query APIs, mirror them as selectors and keep usage consistent

### `project_name/project_name/pages/models.py-tpl`

- `PageManager.published()`

Recommendation:

- acceptable to keep for now
- if the refactor aims for stricter selector purity, move page visibility queries into selectors

## Acceptable to leave on models

### `project_name/project_name/tenancy/models.py-tpl`

These are simple derived properties, not fat-model concerns:

- `TeamMembership.is_owner`
- `TeamMembership.is_admin`
- `TeamMembership.can_manage_members`
- `TeamInvitation.is_expired`
- `TeamInvitation.is_active`

### `project_name/project_name/pages/models.py-tpl`

- `Page.is_visible()` is slightly more than trivial but still acceptable as entity-local derived
  state

### `project_name/project_name/users/models.py-tpl`

- `get_preference()` is fine
- `set_preference()` is mildly service-like because it saves, but it is still small and local

### `project_name/project_name/core/models.py-tpl`

- `AuditEvent.save()` / `delete()` / queryset `delete()` are invariant enforcement, not fat-model
  logic

---

## Proposed phased implementation plan

## Phase 0: agree the boundary rules

Before touching code, lock in the architectural rules to avoid inconsistent cleanup.

Decision points to confirm:

1. keyword-only applies to all public service/selector functions by default
2. private helpers may remain positional unless clarity demands otherwise
3. specialized files with explicit names are allowed when clearer than generic `services.py`
4. queryset helpers may remain for chaining convenience, but app-facing read APIs should prefer
   selectors
5. small derived model properties stay on models

Deliverable:

- this plan accepted as the implementation guide

---

## Phase 1: mechanical signature cleanup in existing service/selector modules

This phase should be behavior-preserving and low risk.

### Files in scope

- `project_name/project_name/billing/selectors.py-tpl`
- `project_name/project_name/flags/services.py-tpl`
- `project_name/project_name/tenancy/services.py-tpl`
- `project_name/project_name/tokens/services.py-tpl`
- `project_name/project_name/tokens/selectors.py-tpl`
- `project_name/project_name/selectors.py-tpl`
- `project_name/project_name/tenancy/permissions.py-tpl` (if included in boundary rule)

### Actions

- convert public functions to keyword-only arguments where practical
- add missing parameter annotations
- add missing return types
- update all internal call sites to keyword form
- update tests to call these APIs using keyword arguments

### Example changes

#### Billing selectors

```python
def has_active_subscription(*, team: Team) -> bool:
def get_active_subscription(*, team: Team) -> Subscription | None:
def has_entitlement(*, team: Team, key: str) -> bool:
```

#### Flags service

```python
def is_flag_enabled(*, flag_key: str, default: bool = False) -> bool:
```

#### Tenancy services

```python
def create_team(*, name: str, slug: str, owner: User) -> Team:
def validate_team_vat_number(*, actor: User, team: Team, billing_country: str, vat_number: str, request: HttpRequest | None = None) -> Team:
def add_user_to_team(*, actor: User, team: Team, user: User, role: str) -> TeamMembership:
def create_invitation(*, actor: User, team: Team, email: str, role: str) -> TeamInvitation:
def get_invitation_token(*, invitation: TeamInvitation) -> str:
def build_invitation_accept_url(*, invitation: TeamInvitation, request: HttpRequest) -> str:
def send_invitation_email(*, invitation: TeamInvitation, request: HttpRequest) -> None:
def accept_invitation_from_token(*, token: str, user: User) -> TeamMembership:
```

#### Token services/selectors

```python
def create_api_token(*, team: Team, user: User, name: str, ...) -> TokenCreationResult:
def revoke_api_token(*, token: ApiToken, user: User) -> None:
def list_tokens_for_team(*, team: Team) -> QuerySet[ApiToken]:
```

### Risk level

Low.

This phase is mostly signature tightening and import updates.

---

## Phase 2: move obvious read logic into selectors

This phase improves architectural clarity without broad behavior changes.

### 2.1 Create `tenancy/selectors.py-tpl`

Move the read-only function out of `tenancy/services.py-tpl`:

- `get_user_teams(user)`

Target:

```python
def get_user_teams(*, user: User) -> QuerySet[Team]:
    ...
```

Then update call sites and tests.

### 2.2 Split `users/privacy.py-tpl`

Recommended split:

- `project_name/project_name/users/privacy_services.py-tpl`
- `project_name/project_name/users/privacy_selectors.py-tpl`

Move to selectors:

- `get_user_by_identifier`
- `get_users_pending_deletion`

Keep in services:

- `export_user_data`
- `_validate_user_deletion_request`
- `delete_user_data`
- `finalize_user_data_deletion`

Recommended target shapes:

```python
def get_user_by_identifier(*, identifier: str) -> User:
def get_users_pending_deletion(*, now: datetime | None = None) -> QuerySet[User]:
```

Notes:

- `get_user_by_identifier` currently may raise `DoesNotExist`; that behavior can remain
- this split is structural, not semantic

### 2.3 Decide whether `pages/faq.py-tpl` should become an explicit selector module

Recommended minimal option:

- rename to `pages/faq_selectors.py-tpl`

Alternative minimal-churn option:

- keep the filename as-is
- document that it is selector logic
- only tighten any signatures/types if needed

Recommendation:

- prefer `faq_selectors.py-tpl` for clarity if the rename is not noisy
- otherwise defer the rename

### Risk level

Low to medium.

The main risk is import churn, not behavior.

---

## Phase 3: normalize service-like modules with explicit names

This phase is about consistency, not mandatory flattening.

### 3.1 Normalize newsletter service naming

Current file:

- `project_name/project_name/core/newsletter.py-tpl`

Recommended target:

- `project_name/project_name/core/newsletter_services.py-tpl`

Reason:

- the module is service logic, not a model or generic utility
- the explicit name is clearer than a bare domain noun

Target signature improvements:

```python
def get_newsletter_confirmation_token(*, signup: NewsletterSignup) -> str:
def build_newsletter_confirmation_url(*, signup: NewsletterSignup, request: HttpRequest) -> str:
def send_newsletter_confirmation_email(*, signup: NewsletterSignup, request: HttpRequest) -> bool:
def confirm_newsletter_signup(*, token: str, request: HttpRequest | None = None) -> NewsletterSignup:
```

### 3.2 Normalize billing webhook orchestration naming or signatures

Current file:

- `project_name/project_name/billing/webhooks.py-tpl`

Two acceptable options:

#### Option A: keep `webhooks.py-tpl`

Do this if naming by integration concern feels clearer.

Still tighten signatures:

```python
def verify_webhook_signature(*, body: bytes, headers: Mapping[str, str]) -> VerifiedWebhookEvent:
def process_webhook(*, body: bytes, headers: Mapping[str, str]) -> str:
```

#### Option B: rename to `webhook_services.py-tpl`

Do this only if the team wants stricter naming consistency over shorter imports.

Recommendation:

- choose Option A
- keep the integration-oriented filename, but enforce service-style signatures

### Risk level

Medium.

The behavior should not change, but import churn grows once modules are renamed.

---

## Phase 4: decide what to do with model/queryset borderline cases

This phase should be small and deliberate. Do not turn it into a purity crusade.

### 4.1 `ApiToken.revoke()` and `ApiToken.touch_last_used()`

Recommended approach:

- keep public mutation entry points in `tokens/services.py`
- avoid calling these model methods directly from views or APIs
- optionally demote model methods to thin internal helpers or remove them if the service fully owns
  the workflow

Suggested outcome:

- `revoke_api_token(...)` remains the public entry point
- if needed, add `touch_token_last_used(*, token: ApiToken) -> None` service/helper and move
  throttling logic there

### 4.2 Queryset/manager helpers

Keep these unless they create confusion:

- `ApiTokenQuerySet.active()`
- `ApiTokenQuerySet.for_token_auth()`
- `PageManager.published()`
- `TenantScopedQuerySet.for_team()`
- `TenantScopedQuerySet.for_request()`

Rule:

- queryset helpers may stay as internal convenience
- public app-facing query APIs should use selectors

### Risk level

Medium.

This phase has the highest chance of causing unnecessary churn if done aggressively.

---

## Phase 5: update docs and examples to reinforce the pattern

Once code changes land, update the docs that teach the pattern.

### Files likely needing updates

- `README.md` if it shows examples that should use keyword-only selectors/services
- `SECURITY.md` where service-layer patterns are referenced
- app README files where service/selector examples appear
- any generated-project docs that reference moved modules or old imports

### Documentation goals

- show one consistent example per app
- show keyword-only public service/selector usage
- clarify that `all_objects` is used in security-sensitive service code
- clarify that selectors own read logic, not managers by default

### Risk level

Low.

---

## File-by-file recommended end state

## Tenancy

### `tenancy/services.py-tpl`

Keep here:

- `create_team`
- `validate_team_vat_number`
- `add_user_to_team`
- `create_invitation`
- `get_invitation_token`
- `build_invitation_accept_url`
- `send_invitation_email`
- `accept_invitation_from_token`

Move out:

- `get_user_teams` -> `tenancy/selectors.py-tpl`

Add typing:

- `owner: User`
- `actor: User`
- `user: User`
- `request: HttpRequest | None` or `HttpRequest`

### `tenancy/selectors.py-tpl`

Create with:

- `get_user_teams(*, user: User) -> QuerySet[Team]`

### `tenancy/permissions.py-tpl`

Recommended target:

```python
def user_has_team_perm(*, user: AbstractBaseUser, permission_name: str, team: Team | None, obj: object | None = None) -> bool:
```

If converting this to keyword-only causes too much call-site churn for too little value, it may be
left positional for one implementation pass. If that happens, document it as an exception rather
than letting it drift silently.

## Billing

### `billing/selectors.py-tpl`

Keep file. Convert public selector parameters to keyword-only.

### `billing/services.py-tpl`

Already broadly aligned. Tighten only where a public API lacks typing.

### `billing/webhooks.py-tpl`

Keep file name unless a later pass strongly prefers `webhook_services.py-tpl`.

Apply keyword-only public signatures.

## Tokens

### `tokens/services.py-tpl`

Keep file. Add explicit parameter types.

### `tokens/selectors.py-tpl`

Keep file. Add explicit return types.

### `tokens/models.py-tpl`

Do not rush to strip methods from the model. First make sure public entry points use services.

## Users

### `users/privacy.py-tpl`

Split into:

- `users/privacy_services.py-tpl`
- `users/privacy_selectors.py-tpl`

This is the clearest structural cleanup in the repo.

## Core

### `core/newsletter.py-tpl`

Preferred target:

- rename to `core/newsletter_services.py-tpl`

If a rename feels too noisy for one pass, keep the file name and still enforce typed keyword-only
public signatures.

## Pages

### `pages/faq.py-tpl`

Optional clarity rename:

- `pages/faq_selectors.py-tpl`

### `pages/models.py-tpl`

Leave `is_visible()` and `PageManager.published()` alone unless a later pass finds they are causing
real confusion.

---

## Implementation order recommendation

Use this order to keep the diff understandable.

1. **Phase 1 mechanical cleanup**
   - tighten signatures/types in existing service/selector modules
   - verify tests still pass
2. **Tenancy selector split**
   - create `tenancy/selectors.py-tpl`
   - move `get_user_teams`
3. **Users privacy split**
   - separate selector and service concerns
4. **Newsletter naming/signature cleanup**
5. **Webhook signature cleanup**
6. **Optional clarity renames**
   - `faq.py-tpl` -> `faq_selectors.py-tpl`
   - `newsletter.py-tpl` -> `newsletter_services.py-tpl`
7. **Model/queryset cleanup only if still justified**

This sequence gets the biggest architectural gains early with the least behavioral risk.

---

## Testing and verification plan

Because this repository is a template, the source of truth is a freshly generated project.

### For each implementation phase

Run the smallest relevant local tests first, then verify the generated project.

### Preferred generated-project verification sequence

```bash
tmpdir=$(mktemp -d /tmp/django-template-XXXXXX)
uv run django-admin startproject \
    --template=. \
    --extension 'py,yaml,md,template,dist,toml,json,css,js,dev,prod' \
    --name Justfile \
    --exclude '.env' \
    --exclude '.env.local' \
    --exclude '.ruff_cache' \
    --exclude '.rumdl_cache' \
    --exclude '.venv' \
    --exclude 'dist' \
    --exclude 'dev' \
    --exclude 'db.sqlite3' \
    --exclude 'node_modules' \
    --exclude 'tmp' \
    TEST_PROJECT_NAME "$tmpdir"
cp "$tmpdir/TEST_PROJECT_NAME/.env.dist" "$tmpdir/TEST_PROJECT_NAME/.env"
python3 - <<'PY' "$tmpdir/TEST_PROJECT_NAME/.env"
from pathlib import Path
import sys
path = Path(sys.argv[1])
text = path.read_text()
replacements = {
    'DEBUG=False': 'DEBUG=True',
    'ENVIRONMENT=production': 'ENVIRONMENT=development',
    'SEND_EMAILS=True': 'SEND_EMAILS=False',
    'LOG_LEVEL=ERROR': 'LOG_LEVEL=DEBUG',
    'DB_DEFAULT_URL=postgis://{{ project_name }}:{{ project_name }}@localhost:5432/{{ project_name }}?pool=True&server_side_binding=True': 'DB_DEFAULT_URL=sqlite:///db.sqlite3',
}
for old, new in replacements.items():
    text = text.replace(old, new)
path.write_text(text)
PY
cd "$tmpdir"
git init
just install-dev
uv run ruff check
uv run ruff format --check
just test-unit
```

### Additional useful checks

If a phase touches Django config, models, or migrations in a material way, also run:

```bash
uv run ansible-playbook ./dev/01-test-project-template.yaml
```

If the Ansible smoke test is noisy or broken for unrelated reasons, do not stop there; continue with
manual generated-project verification.

---

## Success criteria

The refactor should be considered complete when all of the following are true.

### Architecture

- public read APIs live in selectors or explicitly named selector-style modules
- public write/side-effect APIs live in services or explicitly named service-style modules
- mixed read/write modules have been split where that improves clarity

### API clarity

- public service/selector functions use keyword-only arguments by default
- public service/selector parameters are typed where practical
- public service/selector return types are explicit where practical

### Model discipline

- no new business workflows have been added to models
- model methods retained after the refactor are clearly entity-local or invariant-oriented

### Template health

- generated project passes `ruff check`
- generated project passes `ruff format --check`
- generated project passes `just test-unit`

---

## Open questions for the implementation phase

These do not block planning, but they should be decided before broad edits start.

1. Should `user_has_team_perm(...)` be converted to keyword-only now, or treated as a temporary
   exception because of call-site churn?
2. Should `core/newsletter.py-tpl` be renamed immediately, or should naming changes be deferred
   until after signature cleanup?
3. Should `pages/faq.py-tpl` be renamed, or is that too much churn for too little benefit?
4. Should `ApiToken.revoke()` remain as a thin model helper, or should token revocation become
   service-only?
5. Do we want a short architecture note in the template docs after implementation, or is updating
   existing examples enough?

---

## Recommended first implementation PR

To keep the first PR small and easy to review, start with this exact scope:

1. keyword-only and typing cleanup in:
   - `billing/selectors.py-tpl`
   - `flags/services.py-tpl`
   - `tenancy/services.py-tpl`
   - `tokens/services.py-tpl`
   - `tokens/selectors.py-tpl`
2. move `get_user_teams` into new `tenancy/selectors.py-tpl`
3. update tests and imports
4. verify on a freshly generated project

That PR should deliver most of the signature consistency wins without taking on large module
renames yet.
