# Reusable UI patterns

The default shipped UI contract is the `ui-*` CSS class system plus reusable partials under
`templates/partials/`. For a complete overview and customisation guidance, read
`docs/DESIGN_SYSTEM_CUSTOMIZATION_GUIDE.md` in a generated project.

The `components/` directory is kept available for downstream teams who want to add their own
reusable partials, but the template no longer ships `django-cotton` as a default dependency.

## Quick links

- **Customisation guide**: `docs/DESIGN_SYSTEM_CUSTOMIZATION_GUIDE.md`
- **Implementation checklist**: `docs/DESIGN_SYSTEM_IMPLEMENTATION_CHECKLIST.md`
- **ADR**: `docs/adr/0001-adopt-a-django-first-css-token-design-system.md`