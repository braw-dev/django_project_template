# Design System Customisation Guide

This guide explains how to customise the shipped template design system without fighting its
architecture. It is written for teams who want to brand a freshly generated project quickly.

---

## Architecture recap

The design system has three intentional layers:

1. **CSS tokens** — raw palette colours, semantic tokens, spacing, radius, shadows, typography.
   Every visual decision starts here. (`frontend/.../src/styles/tokens.css`)
2. **Stable UI API** — semantic `ui-*` classes that should always work and always be themeable
   (e.g. `ui-button`, `ui-card`, `ui-alert`, `ui-dialog`).
3. **Starter patterns** — higher-level composed patterns that ship as production-ready defaults
   but are explicitly replaceable (e.g. `ui-hero`, `ui-pricing-grid`, `ui-faq-item`).

The contract: **anything with a `ui-*` class is intended for public use.** Downstream teams should
override tokens, not rewrite class semantics.

---

## Stable API vs starter patterns

| Category         | Examples                                                  | Replaceable? | How to customise        |
| ---------------- | --------------------------------------------------------- | ------------ | ----------------------- |
| Stable API       | `ui-button`, `ui-card`, `ui-dialog`, `ui-badge`           | No           | Token overrides only    |
| Starter patterns | `ui-hero`, `ui-pricing-card`, `ui-faq-item`               | Yes          | Replace template files  |
| Shells           | marketing header/footer, auth panel, app sidebar          | Yes          | Replace template files  |

---

## Theme overrides

Themes are driven by CSS custom properties on `:root` and are selected via the
`data-theme` attribute on `<html>`.

### Changing colours

Open `frontend/.../src/styles/tokens.css` in the generated project. The semantic tokens are under
`:root` and `:root[data-theme="dark"]`.

```css
/* Example: change the primary accent colour */
:root {
    --ui-accent: oklch(56% 0.19 295);
    --ui-accent-hover: oklch(50% 0.18 295);
    --ui-accent-contrast: var(--ui-color-white);
    --ui-focus-ring: rgb(168 85 247 / 0.42);
}
```

Use any colour format CSS custom properties accept. The existing palette tokens use `oklch()` but
you are not forced to.

### Changing typography

```css
:root {
    --ui-font-body: "Your Sans", ui-sans-serif, system-ui, sans-serif;
    --ui-font-heading: "Your Serif", ui-serif, Georgia, serif;
}
```

The template ships matching body and heading fonts. Changing only the heading font produces a
noticeable brand difference with one line.

### Density

```css
:root {
    --ui-density-scale: 1;       /* default comfortable */
}

:root[data-density="compact"] {
    --ui-density-scale: 0.9;     /* tighter for data-heavy views */
}
```

There is no runtime density toggle in the default shell, but the token is wired into all stack
and spacing primitives.

### Dark theme

```css
:root[data-theme="dark"] {
    --ui-surface-page: oklch(20% 0.01 257);
    --ui-surface-panel: oklch(24% 0.012 257);
    --ui-text-default: oklch(97% 0.004 255);
    --ui-text-muted: oklch(81% 0.01 255);
}
```

Override individual tokens in the dark block. You do not need a separate palette for dark mode.

### Theme presets

Two optional presets ship in tokens.css: `:root[data-theme-preset="forest"]` and
`:root[data-theme-preset="violet"]`. They override only accent tokens and can be removed, renamed,
or extended.

---

## Brand asset replacement

### Logo assets

The generated project looks for these files:

| Usage            | Path                                     | Type |
| ---------------- | ---------------------------------------- | ---- |
| Horizontal logo  | `static/brand/img/logo--horizontal.svg`  | SVG  |
| Square mark      | `static/brand/img/logo--square.svg`      | SVG  |

Replace those files with your own assets, keeping the same filenames. The brand partial
(`templates/partials/brand.html`) picks them up automatically.

For optional light/dark variants, override the `brand.html` partial to switch based on the
current theme.

### Favicon and app icons

Add your own favicon files to `static/` and update the `<head>` block in
`templates/base.html`. Use Django's built-in block and static tags.

### Text-only fallback

When brand images are unavailable, the brand partial falls back to the `PROJECT_DISPLAY_NAME`
Django setting plus a text node. Set this in your `.env`:

```text
PROJECT_DISPLAY_NAME=Your Project Name
```

---

## Common override recipes

### Change the primary colour

Edit `tokens.css`, replacing `--ui-accent` and `--ui-accent-hover` under both `:root` and
`:root[data-theme="dark"]`. Update `--ui-focus-ring` to match. That single change propagates to
buttons, links, badges, stat cards, alert borders, and the hero eyebrow.

### Swap the heading font

Change `--ui-font-heading` in `tokens.css`. Optionally scope headings to marketing pages by
keeping the variable default and adding a second variable for the app shell.

### Replace the logo

Drop a new `logo--horizontal.svg` and `logo--square.svg` into `static/brand/img/`.

### Change the density feel

Set `--ui-density-scale` to `0.85` for a tighter feel, or `1.1` for airier. All `ui-stack`
gaps and spacing primitives scale with this value.

### Disable shadows

```css
:root {
    --ui-shadow-sm: none;
    --ui-shadow-md: none;
    --ui-shadow-lg: none;
}
```

### Disable border radius

```css
:root {
    --ui-radius-xs: 0;
    --ui-radius-sm: 0;
    --ui-radius-md: 0;
    --ui-radius-lg: 0;
    --ui-radius-xl: 0;
    --ui-radius-pill: 0;
}
```

### Replace a starter pattern

Example: replace the pricing grid with your own layout.

1. Create `templates/custom/pricing-grid.html` with your markup.
2. In `core/templates/core/pages/pricing.html`, replace the `ui-pricing-grid` block with
   use the standard `include` tag pointing to your custom partial.
3. The stable `ui-button`, `ui-card`, and `ui-badge` classes continue to work inside your custom
   markup.

### Add a new button variant

```css
.ui-button--soft {
    background: rgb(from var(--ui-accent) r g b / 0.12);
    color: var(--ui-accent);
    border-color: rgb(from var(--ui-accent) r g b / 0.18);
}

.ui-button--soft:hover {
    background: rgb(from var(--ui-accent) r g b / 0.2);
}
```

Then use `class="ui-button ui-button--soft"` in your templates. The variant inherits the base
button dimensions, font, and focus ring from `.ui-button`.

---

## Customising shells

### Marketing shell

The marketing header and footer are `core/templates/core/partials/header.html` and
`…/footer.html`. Override them in your project without touching the core templates.

### Auth shell

The auth layout is `templates/allauth/layouts/base.html`. It uses the shared brand partial
and message/toast surface. Replace the brand asset by updating the static files; replace the
shell by overriding this template.

### App shell

The app shell is `templates/app_base.html` which includes `partials/app-shell-navigation.html`.
Team context, switcher, and navigation links are all in the navigation partial. Override it to
add or remove app-specific links.

The account menu and toolbar controls (theme, language) are rendered in the topbar of
`app_base.html`. They are replaceable by overriding the template.

---

## Adding a new page

1. Create a view in the appropriate app (`core/views.py` for public pages,
   `tenancy/views.py` for team-scoped pages).
2. Create a template extending `base.html` (public) or `app_base.html` (authenticated).
3. Use `ui-*` classes for layout and components.
4. Add the URL to `urls.py` in the generated project.

Example template for a team-scoped page (extends `app_base.html`):

```html
<div class="ui-stack ui-stack--xl">
    <header class="ui-page-header">
        <h2>{{ team.name }}</h2>
    </header>
    <div class="ui-card">
        <div class="ui-card__body">
            <!-- your content using ui-* classes -->
        </div>
    </div>
</div>
```

The view sets `team` in the template context so `{{ team.name }}` resolves.

---

## CSS architecture (for advanced overrides)

If you need to replace the entire CSS layer:

1. Copy `frontend/.../src/styles/` into your project override path.
2. Update `frontend/.../src/tailwind.css` to import your files instead.
3. Rebuild the frontend: `cd frontend/... && pnpm build`.

The import order matters:

```
tokens.css → base.css → layout.css → components.css → patterns.css
```

Each file depends on the one before it. You can replace individual files while keeping the
token contract intact.

---

## Where to look next

- **ADR**: records why this architecture was chosen and when to reconsider.
  (`docs/adr/0001-adopt-a-django-first-css-token-design-system.md`)
- **Implementation checklist**: what is done and what remains.
  (`docs/DESIGN_SYSTEM_IMPLEMENTATION_CHECKLIST.md`)
- **Token source file**: the single file that controls every visual decision.
  (`frontend/.../src/styles/tokens.css`)