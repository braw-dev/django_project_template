---
description: Create a test project from the template, run Django's `check` and `migrate` commands, and surface any errors. Use when modifying template code that affects Django's configuration or database schema.
name: template-django-check
---

## Usage

Use this skill when modifying the template files to ensure that the generated project is
a valid Django project and its migrations are correct.

1. Run the Django check script:

   ```bash
   python3 .agents/skills/template-django-check/scripts/django_check.py
   ```

2. The script will:
   - Generate a project in a temporary directory.
   - Run `python manage.py check` to find configuration errors.
   - Run `python manage.py migrate` to verify the initial schema and migration files.
3. **Analyze the output**: If errors are reported, map the generated file paths to their source
   template files.
4. **Apply changes**: Manually apply the minimal equivalent changes to the template files.
5. **Verify**: Run the script again until it passes.

## Core Principles

- **Template Integrity**: Never hardcode the test project name into template files.
- **Minimal Edits**: Apply only what is necessary to fix the Django errors.
- **Verification**: Always regenerate and re-check.
- **Django is Truth**: The generated project's `manage.py check` and `migrate` output are the
  source of truth for template correctness.
