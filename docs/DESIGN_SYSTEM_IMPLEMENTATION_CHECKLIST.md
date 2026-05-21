# Design System Implementation Checklist

This checklist captures the agreed first-pass implementation plan for the template's new UI system.
It is intentionally concrete and biased toward shipping a coherent generated project rather than a
theoretical component library.

## Goal

Ship a production-ready, Django-first design system for the template with:

- semantic `ui-*` classes as the public UI contract
- CSS-variable themes with light/dark support
- stable primitives plus replaceable starter patterns
- production-ready marketing, auth, and app shells
- downstream-friendly branding and override points
- generated-project verification and critical E2E coverage

## Non-goals for v1

- full React component parity
- command palette
- wizard/stepper system
- chart library integration
- full notification framework
- long-lived parallel DaisyUI/Cotton-era component systems

## Acceptance criteria

The first pass is done when:

- a freshly generated project uses the new design system coherently out of the box
- the public template contract is semantic `ui-*` classes plus documented tokens/themes
- marketing, auth, and app shells are production-ready
- key existing shipped pages are migrated to the new system
- theme overrides, brand assets, and customization docs are in place
- critical shell/system behaviors have Playwright coverage
- relevant docs and agent instructions are updated
- the design-system direction is recorded in an ADR

---

## Phase 1: establish the foundation

### 1. Create the CSS architecture

- [ ] Add a layered stylesheet structure for the frontend design system
- [ ] Separate files by concern, not by individual component explosion
- [ ] Prefer a structure like:
    - [ ] `tokens.css`
    - [ ] `base.css`
    - [ ] `layout.css`
    - [ ] `components.css`
    - [ ] `patterns.css`
    - [ ] optional tiny `utilities.css` only if truly needed
- [ ] Ensure the final import path from the existing Vite entrypoint is clear and documented

### 2. Define the token system

- [ ] Create raw palette tokens
- [ ] Create semantic tokens consumed by components directly
- [ ] Add tokens for at least:
    - [ ] primary/secondary surfaces
    - [ ] text/default/muted
    - [ ] border
    - [ ] info/success/warning/error
    - [ ] destructive action styling needs
    - [ ] focus ring
    - [ ] radius
    - [ ] shadow
    - [ ] typography roles
    - [ ] content widths
    - [ ] spacing rhythm
    - [ ] density scale
- [ ] Keep the token model to two layers by default: raw palette + semantic tokens

### 3. Implement theme selection

- [ ] Drive theme selection through HTML attributes and CSS variables
- [ ] Follow system light/dark preference by default
- [ ] Persist explicit user choice when set
- [ ] Avoid frontend boot dependency for initial theme render
- [ ] Respect `prefers-reduced-motion`

### 4. Create starter theme presets

- [ ] Ship one canonical default theme
- [ ] Ship a very small number of additional starter presets
- [ ] Keep downstream token overrides as the main customization path
- [ ] Do not build a theme gallery

### 5. Establish brand asset conventions

- [ ] Define a canonical brand asset structure for generated projects
- [ ] Include at least:
    - [ ] primary logo/wordmark asset
    - [ ] square mark/icon asset
    - [ ] favicon/app icon asset
- [ ] Optionally support light/dark asset variants
- [ ] Document override locations clearly

### 6. Replace Cotton as a foundation

- [ ] Remove `django-cotton` as a foundational UI dependency if its remaining usage can be replaced
      cleanly
- [ ] Replace `<c-consent />` usage with native template composition
- [ ] Remove Cotton-oriented docs/instructions once no longer needed
- [ ] Do not leave Cotton described as the primary component model in agent docs

### Phase 1 verification

- [ ] Fresh generated project builds successfully
- [ ] Theme switching works without flash on first render
- [ ] Token overrides can visibly restyle the generated project
- [ ] Brand asset override points are discoverable and functional

---

## Phase 2: build the stable UI API

### 7. Build layout primitives

- [ ] Canonical containers for narrow/default/wide/full widths
- [ ] Stack/cluster/section/page spacing primitives
- [ ] Responsive width conventions exposed through both classes and shells
- [ ] Logical start/end naming where appropriate

### 8. Build typography and prose layer

- [ ] Body/UI typography role
- [ ] Heading/emphasis typography role
- [ ] Marketing and major structural heading treatment
- [ ] Canonical prose styling for long-form content
- [ ] Inline code and code block styling
- [ ] Embedded prose callout/notice pattern

### 9. Build feedback primitives

- [ ] Alerts using canonical status hierarchy
- [ ] Badges/tags using canonical status hierarchy
- [ ] Toast presentation pattern
- [ ] Spinner and linear progress bar
- [ ] Skeleton primitives
- [ ] Empty state structure
- [ ] Error state structure
- [ ] Retry/reload affordance pattern

### 10. Build form primitives

- [ ] Buttons and button variants
- [ ] Destructive action variant naming
- [ ] Field wrapper pattern
- [ ] Input, textarea, select, checkbox, radio
- [ ] Help text, error text, required/optional affordances
- [ ] Disabled/read-only styling
- [ ] Form error summary pattern
- [ ] Search/input-with-actions structural pattern

### 11. Build overlay and menu primitives

- [ ] Accessible dropdown/menu button pattern
- [ ] Dialog primitive
- [ ] Drawer/sheet primitive
- [ ] Destructive confirmation dialog pattern
- [ ] Keyboard/focus handling expectations documented

### 12. Build list/detail primitives

- [ ] Table with honest mobile horizontal scroll default
- [ ] Pagination pattern
- [ ] Resource List pattern
- [ ] Metadata Row pattern
- [ ] Identity Row pattern
- [ ] File Row pattern
- [ ] Detail summary pattern using `dl` semantics where appropriate
- [ ] Inline metadata/status row guidance
- [ ] Optional list selection support where appropriate

### 13. Build supporting stable subpatterns

- [ ] Page header/toolbar
- [ ] Optional breadcrumb slot
- [ ] Settings section pattern
- [ ] Danger zone section
- [ ] Copy action primitive
- [ ] Keyboard shortcut hint style
- [ ] Icon slot contract
- [ ] Upload surface pattern
- [ ] Accessibility helpers including skip-link expectations and screen-reader-only helpers

### 14. Accessibility and internationalization pass

- [ ] Visible focus treatment is explicit and themeable
- [ ] Stable patterns use semantic landmarks and semantics by default
- [ ] RTL is considered in layout, separators, icon slots, and directional icon behavior
- [ ] Directional icons flip/adapt logically where meaning depends on direction
- [ ] Avoid left/right language in the stable API where leading/trailing or start/end is better

### Phase 2 verification

- [ ] Stable primitives work in Django templates without Tailwind utility soup
- [ ] Stable primitives can be restyled through tokens
- [ ] Basic responsive behavior is correct on narrow screens
- [ ] Accessibility review on core primitives passes manual inspection
- [ ] Generated project lint/format/tests still pass

---

## Phase 3: build production-ready shells

### 15. Marketing shell

- [ ] Production-ready header/nav
- [ ] Brand slot with logo/text fallback
- [ ] Production-ready footer
- [ ] Trust/legal link cluster
- [ ] Support/contact/help CTA support
- [ ] Responsive mobile-first navigation behavior

### 16. Auth shell

- [ ] Production-ready auth layout using new brand asset conventions
- [ ] Message/toast rendering consistent with system feedback patterns
- [ ] Narrow content width and strong task focus
- [ ] Replace hardcoded logo path conventions with new brand slot/asset model

### 17. App shell

- [ ] Sidebar-first desktop navigation
- [ ] Drawer/mobile nav on small screens
- [ ] Top bar for context/actions
- [ ] Skip link
- [ ] Semantic landmarks (`header`, `nav`, `main`, etc.)
- [ ] Production-ready account menu
- [ ] Production-ready language switcher if shipped
- [ ] Production-ready theme switcher if shipped
- [ ] Canonical team-context area
- [ ] Active Team switcher control
- [ ] Discoverable team settings/member-management/billing access points
- [ ] Do not ship fake notifications entry UI

### Phase 3 verification

- [ ] Shells are coherent across marketing/auth/app contexts
- [ ] Mobile nav/drawer works accessibly
- [ ] Account menu and team switcher work coherently
- [ ] Skip link and landmarks are present and useful

---

## Phase 4: migrate existing shipped pages

### 18. Migrate template-owned pages first

Prioritize real shipped pages over a component showcase.

- [ ] `base.html`
- [ ] `app_base.html`
- [ ] shared header/footer areas
- [ ] allauth/auth layouts
- [ ] homepage
- [ ] pricing page
- [ ] support/help pages
- [ ] page detail / long-form content pages
- [ ] at least one app/dashboard/settings-style page

### 19. Remove visible legacy public contract

- [ ] Remove DaisyUI-style class conventions from shipped template markup where the new `ui-*`
      system should be authoritative
- [ ] Do not leave mixed public markup conventions in default templates
- [ ] Tailwind may remain as internal tooling only

### Phase 4 verification

- [ ] Generated project looks coherent without custom downstream work
- [ ] Existing core pages visibly use the new system
- [ ] No obvious public contract confusion between legacy DaisyUI classes and new `ui-*` classes

---

## Phase 5: add starter patterns

### 20. Marketing starter patterns

- [ ] Hero
- [ ] Feature grid
- [ ] Pricing presentation
- [ ] FAQ presentation
- [ ] CTA band
- [ ] Support/contact starter pattern

### 21. App starter patterns

- [ ] KPI/stat cards
- [ ] Dashboard widgets
- [ ] First-run/onboarding starter screen if useful
- [ ] Billing/plan summary starter pattern
- [ ] Invitation/member-management screen pattern
- [ ] Team/domain-specific state examples built on canonical status hierarchy
- [ ] Billing-state examples built on canonical status hierarchy

### 22. Domain-native starter screens

- [ ] Member-management starter screen presents Owner/Admin/Member roles clearly
- [ ] Invitation lifecycle states are presented consistently
- [ ] Billing/subscription starter surfaces are production-ready defaults but replaceable

### Phase 5 verification

- [ ] Starter patterns clearly compose from stable primitives
- [ ] Domain-native starter screens reinforce the glossary language already defined in `CONTEXT.md`
- [ ] Replaceable patterns are visually useful but not mistaken for immovable primitives

---

## Phase 6: docs, ADR, and agent guidance

### 23. Add customization docs

- [ ] Write a dedicated customization guide
- [ ] Document the stable API vs starter pattern split
- [ ] Document theme override flow
- [ ] Document brand asset replacement flow
- [ ] Document common override recipes:
    - [ ] change primary color
    - [ ] swap heading font
    - [ ] replace logo asset
    - [ ] change density feel
    - [ ] disable shadows
    - [ ] replace a starter pattern
    - [ ] add a new component variant

### 24. Add targeted inline comments

- [ ] Add comments only at key extension points
- [ ] Keep comments focused and non-noisy
- [ ] Cover token/theme entrypoints and intentional replacement points

### 25. Update agent docs

- [ ] Update relevant `AGENTS.md`
- [ ] Update relevant `ai/` docs
- [ ] Remove outdated guidance that still presents Cotton or utility-heavy template markup as the
      preferred default
- [ ] Document Django 6 template partials as preferred where appropriate

### 26. Record the ADR

- [ ] Add an ADR for the design-system direction
- [ ] Capture at least:
    - [ ] semantic `ui-*` public API
    - [ ] CSS-token theme model
    - [ ] Django-first composition model
    - [ ] stable API vs starter patterns split
    - [ ] Tailwind retained only as tooling
    - [ ] Cotton no longer foundational

### Phase 6 verification

- [ ] A downstream team can understand how to customize the generated project quickly
- [ ] Future agents will not be steered back toward the old design-system assumptions
- [ ] The design direction is documented in one durable place, not only in commit history

---

## Phase 7: testing and verification

### 27. Generated project verification

Always verify a freshly generated project, not just the template source.

- [ ] Generate a fresh project from the template
- [ ] Install dependencies
- [ ] Run generated-project lint checks
- [ ] Run generated-project formatting checks
- [ ] Run generated-project backend tests

### 28. Add critical Playwright coverage

Prefer critical-path shell/system coverage over exhaustive component browser testing.

- [ ] theme selection / persistence
- [ ] mobile nav drawer behavior
- [ ] account menu behavior
- [ ] Active Team switcher behavior if implemented in browser flows
- [ ] dialog/menu accessibility-critical behavior
- [ ] copy action feedback
- [ ] brand slot/logo fallback rendering where practical
- [ ] auth shell renders correctly

### 29. Keep lower-level testing pragmatic

- [ ] Do not attempt exhaustive E2E for every primitive in v1
- [ ] Use smaller-scope tests/manual verification for lower-level visual patterns where appropriate

### Final verification checklist

- [ ] Fresh generated project passes lint
- [ ] Fresh generated project passes format checks
- [ ] Fresh generated project passes backend tests
- [ ] Critical Playwright tests pass
- [ ] Core pages and shells look coherent in both light and dark themes
- [ ] Mobile-first behavior is acceptable across shells and key pages
- [ ] Accessibility basics are intact after migration

---

## Nice-to-have after v1

These are intentionally not required for the first pass:

- [ ] broader React wrappers
- [ ] richer chart integrations
- [ ] command palette
- [ ] wizard/stepper system
- [ ] master-detail shell pattern
- [ ] richer timeline/activity feed patterns
- [ ] secret/token display starter patterns beyond narrow cases
- [ ] broader component showcase beyond a small reference page

---

## Summary rule

If a decision conflicts with this checklist, prefer the version that makes the **generated project**
more coherent, more accessible, more mobile-friendly, and easier for downstream teams to customize
without fighting the template.
