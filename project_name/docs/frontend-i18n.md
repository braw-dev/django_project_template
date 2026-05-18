# Frontend i18n for React islands

This template uses Django as the source of truth for the active language.

## How the bridge works

- Django's built-in `set_language` view updates the active language
- `LocaleMiddleware` applies that language on the next request
- base templates render `<html lang="..." dir="...">`
- the React island runtime reads `document.documentElement.lang` and `document.documentElement.dir`
- `i18next` uses that document language when islands mount

This means the server-rendered Django templates and the client-rendered React islands stay on the same language without a separate frontend language selector.

## What ships in the template

- `frontend/{{ project_name }}/src/i18n/` - frontend i18n setup
- `frontend/{{ project_name }}/src/islands/registry.ts` - React island registry
- `frontend/{{ project_name }}/src/main.tsx` - island bootstrap
- `templates/base.html` - loads the Vite entry bundle for islands
- `{% templatetag openblock %} load core {% templatetag closeblock %}` / `{% templatetag openblock %} react_island ... {% templatetag closeblock %}` - helper to render island roots from Django templates

## Adding a new React island

1. Create a React component under `frontend/{{ project_name }}/src/`
2. Register it in `frontend/{{ project_name }}/src/islands/registry.ts`
3. Render it from a Django template using the `react_island` template tag

Example component registration:

```ts
import { PricingCalculator } from '../pricing/PricingCalculator'

export const islandRegistry = {
  PricingCalculator,
}
```

Example template usage:

```django
{% templatetag openblock %} load core {% templatetag closeblock %}
{% templatetag openblock %} react_island "PricingCalculator" pricing_props {% templatetag closeblock %}
```

The `props` value must be JSON-serializable.

## Translating React island strings

Use the frontend i18n helpers for user-facing text inside React islands.

```tsx
import { useAppTranslation } from './i18n/use-app-translation'

export function PricingCalculator() {
  const { t, locale, direction } = useAppTranslation()

  return <div dir={direction}>{t('pricing.title')}</div>
}
```

Add translations to the locale JSON files in `frontend/{{ project_name }}/src/i18n/locales/`.

## Important limits

- Django gettext catalogs and React JSON catalogs are separate; the template does not auto-sync them
- do not use `navigator.language` as the source of truth for islands
- do not add a second independent frontend language switcher unless you also wire it back to Django's language selection flow
