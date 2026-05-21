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
ordinary collaborators, but cannot manage Team administration by default. Member-management starter
screens should present **Owner**, **Admin**, and **Member** roles consistently and distinctly.

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
from request context, not from the **Account** alone. In this template, the app shell should
provide a canonical control pattern for representing and switching **Active Team** context.

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

### Design System

The reusable visual language shipped with the template, including design tokens, component
primitives, and default presentation rules for generated projects. The **Design System** is a
template-level foundation intended to be usable out of the box and replaceable by downstream
projects.

_Avoid_: React library, Tailwind kit, theme pack

### UI Primitive

A low-level reusable interface building block such as a button, field, card, alert, or dialog.
**UI Primitives** are the stable foundation of the **Design System** and are intended to compose
into larger screens and flows.

_Avoid_: Full page, feature module, marketing section

### Application Shell

A reusable page-level frame such as an auth shell, app shell, or marketing shell that provides
consistent layout and presentation structure around content. An **Application Shell** uses **UI
Primitives** but is more opinionated and less fundamental. In this template, marketing, auth, and
app experiences should share one **Design System** while using distinct shell families, and the app
shell should use a responsive hybrid navigation model with sidebar-first desktop navigation.

_Avoid_: Primitive, widget, one-off page

### Brand Slot

The shared shell-level presentation for a project's identity, used in places such as navigation,
auth pages, and footers. A **Brand Slot** should support an optional logo or mark alongside brand
text, while falling back cleanly to text-only presentation when no custom asset is provided.

_Avoid_: Hardcoded one-off logo usage, image-only brand assumption

### Icon Slot

The defined place within a **UI Primitive**, **Application Shell**, or **Starter Pattern** where an
icon may appear with consistent sizing, alignment, and accessibility behavior. In this template,
**Icon Slots** should be part of the **Stable UI API** while the exact icon family remains
replaceable.

_Avoid_: Ad hoc SVG placement, icon-font-only assumption

### Theme

A project's visual identity expressed through **Design System** tokens such as color, typography,
radius, and surface treatment. In this template, a **Theme** should support light and dark
variants by default, and the template may ship a very small number of starter presets while
keeping downstream token overrides as the main customization path.

_Avoid_: Color mode only, skin pack

### Design Token

A named visual value within the **Design System** used to keep presentation consistent across
**UI Primitives** and **Application Shells**. In this template, **Design Tokens** should use a
two-layer model: raw palette tokens plus semantic tokens consumed directly by components.

_Avoid_: One-off CSS value, component config object

### Typography Role

A named text style role within the **Design System**, such as body text or heading text, used to
keep hierarchy and brand tone consistent. In this template, the default system should distinguish
between body/UI typography and heading/emphasis typography, with heading typography used
selectively for marketing and major structural headings rather than dense operational UI.

_Avoid_: One-font-for-everything assumption, decorative one-off type choice

### UI Class

A semantic CSS class exposed as the public styling contract of the **Design System**, such as
`.ui-button` or `.ui-card`. **UI Classes** should be stable, human-readable, and preferable to
utility-heavy template markup for default template components.

_Avoid_: Utility soup, framework-private selector

### Starter Pattern

A higher-level reusable UI composition shipped with the template, such as a pricing section,
sidebar, or dashboard widget, intended to give generated projects a functional starting point.
**Starter Patterns** are more opinionated and more replaceable than **UI Primitives**.

_Avoid_: Core primitive, permanent product architecture

### Stable UI API

The subset of the **Design System** that downstream projects should be able to rely on as a durable
public contract, primarily covering **UI Primitives**, layout helpers, and core **Application
Shells**. The **Stable UI API** should exclude highly product-specific marketing or dashboard
compositions and should treat accessibility, internationalization, and RTL compatibility as
required properties rather than optional enhancements.

_Avoid_: Every shipped template snippet, one-off section library

### Default UI Style

The template's out-of-the-box visual stance for generated projects. In this template, the **Default
UI Style** should be opinionated, polished, and B2B-focused while remaining restrained enough to be
easily rebranded by downstream projects.

_Avoid_: Bare scaffold, novelty aesthetic

### Theme Override

A downstream project change to **Theme** and **Design Token** values that rebrands the generated UI
without rewriting component structure. In this template, **Theme Overrides** should cover color,
typography, radius, shadow, and limited density choices, but not page composition or component
anatomy.

_Avoid_: Full redesign system, layout rewrite via variables alone

### Theme Selection

The mechanism that chooses which **Theme** variant is active for a rendered interface. In this
template, **Theme Selection** should be driven by CSS variables and HTML attributes, with minimal
JavaScript used only when needed for preference persistence.

_Avoid_: Frontend-only boot requirement, framework-owned runtime theme state

### Component Variant

A stable semantic variation of a **UI Primitive** such as primary, secondary, destructive, ghost,
or success. A **Component Variant** expresses the role of a component, while the active **Theme**
determines how that variant looks. In this template, negative action intent should prefer
**destructive** naming, while negative feedback should prefer **error** naming.

_Avoid_: Theme alias, one-off utility class

### UI State

The interactive or semantic condition of a rendered interface element, such as disabled, expanded,
selected, open, or invalid. In this template, **UI State** should prefer native HTML, ARIA, and
`data-*` attributes as styling hooks where appropriate rather than inventing class-only state
markers. Motion used to express **UI State** should respect reduced-motion user preferences.

_Avoid_: Class-only transient state when semantic attributes exist

### Empty State

A structured interface state shown when relevant content, records, or results do not yet exist.
An **Empty State** should support optional iconography, explanatory text, and clear next actions
without becoming a product-specific onboarding flow by default.

_Avoid_: Blank screen, onboarding flow by default

### Toast

A transient status message shown briefly without replacing page content, typically for success,
information, warning, or error feedback. In this template, **Toasts** should remain lightweight and
should not imply a full notification framework.

_Avoid_: Permanent alert, full inbox or notification center

### Resource List

A structured collection view for app entities that sits between a full data table and a generic
card grid, typically showing title, metadata, status, and actions in a mobile-friendly layout. A
**Resource List** should be part of the **Stable UI API** and may optionally support selection.

_Avoid_: Full table replacement for every case, unstructured card soup

### Identity Row

A compact presentation of a person, team, or similar entity using avatar or mark, primary label,
and supporting metadata. An **Identity Row** should be part of the **Stable UI API** as a common
building block for navigation, lists, and management screens.

_Avoid_: Rich profile card by default, ad hoc avatar-and-text markup

### Metadata Row

A compact inline presentation of supporting facts such as status, plan, timestamp, or secondary
labels associated with a primary entity or record. A **Metadata Row** should be part of the stable
structural design language for lists, summaries, and management views.

_Avoid_: Free-form separator soup, ad hoc muted text strings

### File Row

A structured presentation of a file or attachment showing its primary label, supporting metadata,
and available actions in a mobile-friendly layout. A **File Row** should be a named stable pattern
built on the **Resource List** and **Metadata Row** foundations.

_Avoid_: Full document-management workflow by default, ad hoc attachment markup

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
