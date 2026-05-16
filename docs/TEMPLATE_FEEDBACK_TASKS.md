# Template feedback tasks

Prioritised follow-up list from the template review, aimed at making this a stronger foundation for a solo, EU-focused B2B micro-SaaS business.

Principles used for suggested fixes:

- keep the stack boring
- prefer Django built-ins
- security before convenience
- minimal, repeatable changes that pay rent across many products
- EU-first where it affects privacy, billing, localisation, and deployment

## P0 — fix first

### 3. Make generated templates actually i18n-first

**Problem:** Many user-facing strings in templates and views are still hardcoded in English.

**Potential fix:** Wrap all visible copy with Django i18n tools and add a small regression checklist so new template pages do not ship with hardcoded strings.

### 4. Fix `<html lang>` and locale-aware rendering

**Problem:** `base.html` hardcodes `lang="en"`, which undermines localisation.

**Potential fix:** Set the HTML lang attribute from the active language and use Django localisation tools consistently for dates, numbers, and text direction assumptions.

### 5. Sanitize rendered markdown

**Problem:** Marketing page markdown is rendered with `mark_safe` but is not visibly sanitized first, despite `nh3` being in the project dependencies.

**Potential fix:** Sanitize markdown output with `nh3` at the rendering boundary. Keep the solution small and explicit rather than introducing a CMS abstraction.

### 6. Finish the Polar billing foundation

**Problem:** Billing is structurally present, but parts of the integration are still stubs or SDK-shape placeholders.

**Potential fix:** Tighten the Polar service and webhook flow against the current SDK, remove speculative comments, and provide one boring happy path for checkout, subscription sync, and entitlement checks.

### 7. Add webhook idempotency for billing events

**Problem:** Subscription webhook handlers do not appear to persist processed event IDs or otherwise guard against duplicate delivery.

**Potential fix:** Store webhook event IDs in a simple model and short-circuit duplicates. Keep it local and explicit rather than relying on undocumented provider behaviour.

## P1 — important for EU B2B readiness

### 8. Replace hardcoded pricing page content with real provider-backed data

**Problem:** The pricing page template is still mostly static placeholder copy and USD-style formatting.

**Potential fix:** Render pricing from Polar-backed selectors with a small formatter layer. Prefer a thin mapping function over a large pricing abstraction.

### 9. Add locale-aware currency formatting

**Problem:** Price formatting currently assumes dollars and simple string interpolation.

**Potential fix:** Add a small currency formatting helper that takes amount, currency, and locale. Support EUR-first by default and avoid inventing a full billing engine.

### 10. Clarify tax and billing display strategy for Europe

**Problem:** The template says Polar is preferred for tax handling, but the user-facing tax display and plan presentation strategy is not yet defined.

**Potential fix:** Document the default stance for VAT, reverse charge, invoicing expectations, and tax-inclusive versus tax-exclusive display. Keep the template opinionated and simple.

### 11. Add newsletter consent and double opt-in

**Problem:** Newsletter signup currently captures email addresses but does not show consent language or a double opt-in flow.

**Potential fix:** Extend the newsletter model and flow with explicit consent capture and confirmation email. Use Django forms and email, not a marketing automation system.

### 12. Seed legal and trust pages that B2B buyers expect

**Problem:** The footer references legal links, but the template does not yet provide a strong default set of trust-facing pages.

**Potential fix:** Add starter pages for Privacy, Terms, Security, and Subprocessors using the existing pages app or static templates. Keep them editable and plain.

### 13. Add basic privacy operations hooks

**Problem:** There is no obvious scaffold for user/customer data export, deletion, or retention handling.

**Potential fix:** Add minimal management commands, admin actions, or service-layer hooks for export/delete requests. Start with boring operational workflows before building end-user self-service.

### 14. Audit support access and impersonation

**Problem:** `django-hijack` is enabled, but there is no obvious customer-facing audit trail or internal audit log around support access.

**Potential fix:** Log impersonation start/stop events with actor, target, and timestamp. Keep the trail append-only and simple.

## P2 — important for product quality and repeatability

### 15. Separate marketing and app layouts more clearly

**Problem:** analytics and support scripts are injected globally from `base.html`, which is not ideal for authenticated app pages.

**Potential fix:** Split into a marketing base template and an app base template. Only load third-party scripts where they are needed.

### 16. Tighten sovereign deployment guidance

**Problem:** The repo direction is sovereignty-friendly, but the deployment guidance is still too generic for EU-focused use.

**Potential fix:** Document one opinionated EU deployment path using boring providers and region-local services. Prefer a clear default over many options.

### 17. Add a simple subprocessor and hosting inventory

**Problem:** A business customer will want a clear list of subprocessors and hosting locations.

**Potential fix:** Add a markdown template listing service, purpose, region, and optional replacement. Keep it manual and easy to update.

### 18. Add a basic audit log pattern for security-sensitive actions

**Problem:** The template has good auth and tenancy primitives, but not a reusable audit trail pattern.

**Potential fix:** Add a minimal app or model pattern for recording security-sensitive events such as billing changes, token creation, team membership changes, and impersonation.

### 19. Finish observability story or reduce the claim

**Problem:** The docs talk about monitoring and metrics more strongly than the implementation supports.

**Potential fix:** Either implement one small supported path for logs/errors/metrics or reduce the docs to what is actually included today.

### 20. Ensure the template’s helper commands and scaffolds are complete

**Problem:** Some scaffolding references appear incomplete or inconsistent, such as `startapp` expectations and container/deployment files.

**Potential fix:** Verify every documented command and referenced file exists in a generated project. Prefer fewer commands that definitely work.

## P3 — useful later

### 21. Add a small docs/help-center pattern

**Problem:** The template covers marketing pages, but not a clear documentation or help-center structure.

**Potential fix:** Reuse the pages app with a constrained convention for docs content before introducing a separate docs stack.

### 22. Add customer-facing security/performance FAQ starters

**Problem:** Prospective B2B customers often ask the same trust and performance questions, but there is no standard answer scaffold.

**Potential fix:** Add editable FAQ starter content for hosting, encryption, backups, MFA, support access, and uptime expectations.

### 23. Add a simple billing/accounting export stance

**Problem:** A solo operator running several SaaS products will need consistent exports for bookkeeping and support.

**Potential fix:** Document where source-of-truth billing data lives and add a minimal export path rather than building finance features into the product.

### 24. Add a template review checklist for future releases

**Problem:** Some of the current gaps are consistency problems rather than architecture problems.

**Potential fix:** Add a short pre-release checklist covering docs accuracy, i18n checks, billing flow, legal links, and generated-project smoke tests.

## Suggested order of attack

If you want to address these one at a time, this is the cleanest sequence:

1. Make docs match reality
2. Wire language switching properly
3. Make generated templates actually i18n-first
4. Fix `<html lang>` and locale-aware rendering
5. Sanitize rendered markdown
6. Finish the Polar billing foundation
7. Add webhook idempotency for billing events
8. Replace hardcoded pricing page content with real provider-backed data
9. Add locale-aware currency formatting
10. Add newsletter consent and double opt-in
11. Seed legal and trust pages
12. Add privacy operations hooks
13. Audit support access and impersonation
14. Separate marketing and app layouts
15. Tighten sovereign deployment guidance

## Definition of done for each task

Prefer each task to be considered done only when:

- the generated project contains the change
- at least one test covers the core behaviour if practical
- docs reflect the final behaviour
- no new abstraction was added unless it clearly pays rent across multiple SaaS products
