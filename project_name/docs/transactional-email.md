# Transactional email foundation

The template includes a small shared foundation for product emails.

## What to use

Use `{{ project_name }}.users.emails.send_transactional_email(...)` for product emails that should
send both plain-text and HTML content.

That helper:

- renders a `*.txt` template for the text body
- renders a `*.html` template for the HTML body
- sends a multipart email with `EmailMultiAlternatives`
- injects `project_display_name` and `email_subject` into the template context

## Template layout

Shared wrappers live in:

- `templates/email/base.txt`
- `templates/email/base.html`

Existing live emails now follow the pattern:

- `templates/tenancy/email/team_invitation.txt`
- `templates/tenancy/email/team_invitation.html`
- `{{ project_name }}/core/templates/core/email/newsletter_confirmation.txt`
- `{{ project_name }}/core/templates/core/email/newsletter_confirmation.html`
- `{{ project_name }}/users/templates/users/email/security_event.txt`
- `{{ project_name }}/users/templates/users/email/security_event.html`

## Adding a new transactional email

1. Create a matching text and HTML template pair
2. Make both extend the shared email base templates
3. Call `send_transactional_email(...)` with the shared template prefix

Example:

```python
from {{ project_name }}.users.emails import send_transactional_email

send_transactional_email(
    subject="Example subject",
    template_prefix="users/email/example",
    recipient_list=[user.email],
    context={"example_value": "hello"},
)
```

That call expects these templates to exist:

- `users/email/example.txt`
- `users/email/example.html`

## Guidance

- keep subjects in Python close to the call site
- keep message content in templates
- prefer a small, explicit context over passing whole model objects unless the template genuinely
  needs them
- for user-facing copy, mark strings for translation in both text and HTML templates
- use this helper for new product emails instead of calling `send_mail(...)` directly unless the
  email is intentionally text-only
