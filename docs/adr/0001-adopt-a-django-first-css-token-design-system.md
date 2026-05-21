# 0001. Adopt a Django-first CSS token design system

**Date:** 2026-05-21

**Status:** accepted

## Context

The template currently mixes several UI approaches: Tailwind and DaisyUI utility-heavy markup in
Django templates, ad hoc inline SVG/icon usage, a small amount of React-island infrastructure, and
`django-cotton` still described in docs as a primary component model despite barely being used in
practice. This makes the default UI contract unclear for downstream projects and for future agents
working on the template.

We want the template to ship with a production-ready, opinionated B2B-focused UI foundation that:

- looks coherent out of the box
- can be customized quickly by downstream micro-SaaS projects
- works primarily in server-rendered Django templates
- supports light/dark theming, branding overrides, accessibility, i18n, and RTL
- avoids locking the public contract to utility-class soup, React-first assumptions, or Cotton as a
  component DSL

Because this repository is a project template rather than a mature application with many external UI
consumers, we can make a deliberate breaking refresh rather than preserving a long-lived mixed UI
system.

## Decision

We will adopt a Django-first design system with semantic `ui-*` classes and CSS-variable themes as
its public contract.

The design system will follow these rules:

- Django templates are the primary consumption surface.
- The public API is semantic `ui-*` classes plus documented design tokens.
- Themes are implemented with CSS variables and HTML attributes, not frontend-owned runtime state.
- The token model uses two layers: raw palette tokens plus semantic tokens consumed directly by
  components.
- The template ships one canonical default theme, light/dark variants, and a very small number of
  starter presets; downstream token overrides remain the main customization path.
- The system distinguishes clearly between:
    - stable UI API
    - replaceable starter patterns
    - theme/brand overrides
    - project-specific UI added later
- Marketing, auth, and app experiences share one design system while using distinct shell families.
- Accessibility, internationalization, and RTL compatibility are required properties of the stable
  system.
- Mobile-first behavior applies to primitives, shells, and starter patterns.
- The icon system is SVG-based and replaceable, with a stable contract for icon slots, sizing,
  alignment, and accessibility.
- Brand presentation uses a shared brand slot with optional logo/mark plus text fallback.
- Tailwind may remain in the toolchain as internal authoring/build tooling, but it is not part of
  the visible public UI contract.
- `django-cotton` will no longer be treated as a foundational UI architecture choice.
- React wrappers, if added, will be minimal and secondary to the Django/CSS contract.

We will implement this as a layer-first internal redesign followed by a broad breaking refresh of
shipped templates, rather than maintaining a parallel legacy system indefinitely.

## Consequences

- Existing shipped template markup will be migrated toward the new semantic `ui-*` system.
- Visible DaisyUI-style conventions will be removed from the default template contract, even if
  Tailwind remains available internally.
- `django-cotton` usage and documentation will be reduced or removed where it no longer adds value.
- Marketing, auth, and app shells will be rewritten to be production-ready defaults using the new
  system.
- Stable primitives and structural patterns will be documented separately from replaceable starter
  patterns.
- Downstream projects will get clearer override points for:
    - theme tokens
    - brand assets
    - shell controls
    - starter pattern replacement
- The generated project will require fresh-project verification and critical Playwright coverage for
  shell/system behavior as part of acceptance.
- Relevant docs and agent instructions must be updated so future work follows the new contract
  instead of the old mixed assumptions.

## Reversal Conditions

We should revisit this decision if one or more of the following becomes true:

- downstream projects consistently need a React-first component model rather than Django-first UI
  composition
- maintaining semantic class-based templates alongside retained Tailwind tooling proves more complex
  than expected and offers too little benefit
- the stable API vs starter-pattern split fails in practice and downstream teams cannot customize
  the template without invasive rewrites
- a future template direction, such as a substantial Wagtail- or frontend-driven architecture,
  changes the primary UI composition model enough that this contract no longer fits
