# Django SaaS Template

This context captures the reusable product language baked into the template itself. It defines the
business-facing terms for identity, team tenancy, invitations, and billing so generated projects
start from consistent language.

## Language

### Team

The top-level container that owns shared data, memberships, and billing within an app generated from
this template. A **Team** can have many **Team Memberships**, many **Team Invitations**, and zero or
one active subscriptions at a time.

_Avoid_: Workspace, organization, organisation, account, tenant

### Account

A user's personal sign-in identity used for authentication and security settings. An **Account** may
belong to many **Teams** through **Team Memberships**.

_Avoid_: Team, customer, workspace

### Customer

The billing-provider-facing customer record associated with a **Team**. In this template, a
**Customer** is a billing projection of a **Team**, not a separate collaboration container or
sign-in identity.

_Avoid_: Account, user, team owner

### Owner

The single **Account** with ultimate authority over a **Team**. Every **Team** must have exactly one
**Owner**, and ownership may be transferred but not shared. Billing authority belongs to the
**Owner** by default. When ownership is transferred, the previous **Owner** becomes an **Admin** by
default. Outside team creation, the **Owner** role should only be assigned through an explicit
ownership-transfer flow to a different existing **Team Member**, with recent reauthentication by the
current **Owner**.

_Avoid_: Co-owner, primary admin

### Admin

An **Account** with elevated operational authority within a **Team**, but not ownership. An
**Admin** can manage members, settings, and API tokens, but cannot manage billing or transfer
ownership.

_Avoid_: Owner, co-owner

### Member

An **Account** that belongs to a **Team** for normal product use without administrative authority
over the **Team** itself. A **Member** may use Team-owned features that the product exposes to
ordinary collaborators, but cannot manage Team administration by default.

_Avoid_: Guest, admin, owner

### Team Invitation

A pending request for a specific email address to join a **Team** in a specified role. A
**Team Invitation** is not a **Team Membership**; it may be accepted, revoked, or expire. By
default, it may only be accepted by an **Account** using the invited email address, and acceptance
creates a **Team Membership** in the invited role. In the default model, invitations may create
**Admin** or **Member** memberships, but not **Owner** memberships.

_Avoid_: Pending member, provisional membership

### Team Membership

The relationship that links an **Account** to a **Team** with exactly one role at a time. An
**Account** may have many **Team Memberships**, but at most one **Team Membership** per **Team**.

_Avoid_: Seat, participant record

### Active Team

The **Team** currently in scope for a request, route, or API call. The **Active Team** is resolved
from request context, not from the **Account** alone.

_Avoid_: Current workspace, selected account

### Subscription

A provider-backed billing agreement that gives a **Team** paid access over time. A **Team** may have
many historical **Subscriptions**, but at most one active **Subscription** at a time in the default
template model.

_Avoid_: Payment, invoice, plan record

### Entitlement

The right for a **Team** to use a specific paid capability. **Entitlements** are derived from
billing state and used to decide whether Team-owned features are available. Product feature checks
should prefer **Entitlement** when deciding access to a specific paid capability.

_Avoid_: Feature flag, permission, cache row

### Billing

The provider-backed commercial layer that manages checkout, subscription state, customer portal
access, and related tax and customer records for a **Team**. **Billing** determines paid access, but
provider-issued invoices and tax documents remain part of the external provider workflow by default.

_Avoid_: Accounting, ledger, finance system

### Team-owned

Belonging to a specific **Team** rather than to an **Account** personally. Team-owned data and
capabilities follow the Team boundary for access, billing, and request scoping.

_Avoid_: Tenant-scoped, workspace-owned, account-owned

## Flagged ambiguities

- **Account** is reserved for a user's sign-in identity, not the shared container for app data and
  billing.
- **Tenant** may be used informally when discussing architecture, but the canonical domain term is
  **Team**.
- The current code now enforces at most one `owner` membership per **Team**, and member-management
  flows no longer assign the `owner` role. It does not yet guarantee that every **Team** always has
  an **Owner** across every future role-change or removal path. The glossary remains the intended
  model.

## Example dialogue

- **Developer:** If Alice invites Bob, does he join her account?
- **Domain expert:** No — he joins her **Team**. His **Account** is still his personal sign-in
  identity.
- **Developer:** Can one **Account** belong to more than one **Team**?
- **Domain expert:** Yes. An **Account** is personal. **Teams** are shared containers.
- **Developer:** So who is the **Customer** in billing?
- **Domain expert:** The **Customer** is the billing record for the **Team**. It is not a second
  kind of user.
- **Developer:** Can a **Team** have two **Owners**?
- **Domain expert:** No. A **Team** has exactly one **Owner**. **Admin** powers can be shared, but
  ownership cannot.
- **Developer:** What happens to the old **Owner** after a transfer?
- **Domain expert:** They become an **Admin** by default, unless a future product changes that
  policy explicitly.
- **Developer:** Can I transfer ownership to myself?
- **Domain expert:** No. Ownership transfer must target a different existing **Team Member**.
- **Developer:** Does ownership transfer need reauthentication?
- **Domain expert:** Yes. It is a sensitive action, so the current **Owner** must reauthenticate
  recently before transferring ownership.
- **Developer:** What can an **Admin** do?
- **Domain expert:** Run most day-to-day team operations, but not become or replace the **Owner**
  automatically.
- **Developer:** Can an **Admin** start or cancel billing?
- **Domain expert:** Not by default. Billing authority belongs to the **Owner**.
- **Developer:** What is a **Member** then?
- **Domain expert:** A normal collaborator in the **Team**. They use team-owned features but do not
  administer the **Team** itself.
- **Developer:** Is an invited person already a **Member**?
- **Domain expert:** No. They have a **Team Invitation** until they accept. Only then do they get a
  **Team Membership**.
- **Developer:** Can anyone with the invite link accept it?
- **Domain expert:** No. By default, only an **Account** using the invited email address can accept
  that **Team Invitation**.
- **Developer:** Is the role chosen before or after acceptance?
- **Domain expert:** Before. The **Team Invitation** carries the invited role, and acceptance
  creates a **Team Membership** in that role.
- **Developer:** Can I invite someone as **Owner**?
- **Domain expert:** No. In the default model, ownership is special. Invitations create **Admin**
  or **Member** memberships; ownership must be transferred explicitly.
- **Developer:** Can Alice have different roles in different teams?
- **Domain expert:** Yes. Roles belong to the **Team Membership**, not to the **Account** globally.
- **Developer:** Which team does a request act on?
- **Domain expert:** The **Active Team** — the team currently in scope for that request.
- **Developer:** What does a **Subscription** mean here?
- **Domain expert:** A provider-backed billing agreement for the **Team**, not just a database row.
- **Developer:** What is an **Entitlement** then?
- **Domain expert:** The team's right to use a specific paid capability derived from billing state.
- **Developer:** When deciding feature access, should I check **Subscription** or **Entitlement**?
- **Domain expert:** Prefer **Entitlement** for specific paid capabilities. **Subscription** is the
  commercial agreement underneath.
- **Developer:** What do you mean by **Billing** overall?
- **Domain expert:** The provider-backed commercial layer for the **Team**, not a full accounting
  system.
- **Developer:** What does it mean for something to be **Team-owned**?
- **Domain expert:** It belongs to the **Team** boundary, not to one person's **Account**.
- **Developer:** And billing belongs to the **Team**, not to Alice personally?
- **Domain expert:** Correct. The **Team** owns billing, memberships, and shared app data.
