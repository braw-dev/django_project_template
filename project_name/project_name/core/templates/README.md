# Templates

This directory contains the templates used by the application to generate the HTML.

As we use HTMX for selective page updates, we separate the templates into categories:

- Pages - Full HTML pages that extend from the base templates.
- Partials - Reusable HTML partials that are included in the pages and fragments.
- Fragments - Small chunks of HTML returned to HTMX to replace/update content in the browser.

## Fragments

These must only include partials and should not include any HTML that would not be present in a partial or a page. The reason for this is that fragments are used to update the page using HTMX and to maintain consistent between pages (which may be shown in case HTMX is not used or on first page load) and HTMX fragments.
