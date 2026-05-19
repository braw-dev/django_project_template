# Template feedback tasks

Aim: Make this a stronger foundation for a solo, EU-focused B2B micro-SaaS business.

Principles:

- keep the stack boring
- prefer Django built-ins
- security before convenience
- minimal, repeatable changes that pay rent across many products
- EU-first where it affects privacy, billing, localisation, and deployment

Perspectives - take these into account as key stakeholders:

1. As a solopreneur/company-of-one using the template to build B2B micro-SaaS products as part of a SaaS factory;
2. A technical expert performing a Technical Due Diligence for a VC/investor or potential acquirer;
3. A customer of one of the micro-SaaS products built with this template focused on data privacy, security, performance, end-user experience and customer satisfaction.

## Overall assessment

The template is already in unusually good shape for a one-person SaaS factory: team-first multi-tenancy with explicit permission checks, audit events for security-sensitive mutations, allauth + MFA + axes, structlog with a request-performance middleware, seeded trust pages (`terms`, `subprocessors`), a privacy module for GDPR export/erasure, a webhook-deduplicating billing app, an i18n-ready URL layout, and a single CI workflow that generates a fresh project and runs lint/format/type/pytest/Playwright/Docker build. That foundation is sound.

The gaps below are the deltas that, in my view, would meaningfully raise the EU B2B-readiness and TDD-pass-rate of every product spun out of this template. I have **not** invented priorities to fill buckets - if a bucket has no entry, that is intentional.

## P0 — fix first

None

## P1 — important for EU B2B readiness

None

## P2 — important for product quality and repeatability

None

## P3 — useful later

- **Per-project cost telemetry.** `MOTIVATION.md` describes a BI dashboard with revenue/expenses/profit per project. Today nothing in the template emits cost-side data. A small `core/costs.py` module that consumes Hetzner + Bunny + Scaleway billing APIs and writes a daily `CostSnapshot` row is enough to start; the dashboard itself can live outside the template.

## Definition of done for each task

Prefer each task to be considered done only when:

- the generated project contains the change
- at least one test covers the core behaviour if practical
- docs reflect the final behaviour
- no new abstraction was added unless it clearly pays rent across multiple SaaS products
