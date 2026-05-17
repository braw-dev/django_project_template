# Template feedback tasks

Aim: Make this a stronger foundation for a solo, EU-focused B2B micro-SaaS business.

Principles:

- keep the stack boring
- prefer Django built-ins
- security before convenience
- minimal, repeatable changes that pay rent across many products
- EU-first where it affects privacy, billing, localisation, and deployment

Perspectives - take these into account when making changes:

1. As a solopreneur/company-of-one using the template to build B2B micro-SaaS products as part of a SaaS factory;
2. A technical expert performing a Technical Due Diligence for a VC/investor or potential acquirer;
3. A customer of one of the micro-SaaS products built with this template focused on data privacy, security, performance, end-user experience and customer satisfaction.

## P0 — fix first

None.

## P1 — important for EU B2B readiness

None.

## P2 — important for product quality and repeatability

None.

## P3 — useful later

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
