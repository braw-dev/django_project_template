# Internationalization First (i18n)

You are a Python/Django coding agent. Your paramount instruction is 'i18n First'.

**No Hardcoded Strings:** Absolutely NO user-facing strings (labels, messages, titles, error text) shall be hardcoded in Python or Django template files.

**Use Translation Functions:** All translatable content in Python code MUST be wrapped using `gettext_lazy` `(_('...'))` or `gettext`.

**Use Template Tags:** All translatable content in Django templates MUST use the `{% load i18n %}` and the `{% translate '...' %}` (or `{% trans '...' %}`) tag.

**Date/Number Formatting:** When displaying dynamic data, utilize Django's localization tools (e.g., `{% load l10n %}`, `{% localize %}`).

**Context Preparation:** Ensure all context variables passed to templates are ready for localization.

**Model translations:** If model translations are needed, use `django-parler`
