from django.conf import settings
from django.db import migrations


TRUST_PAGES = [
    {
        "slug": "privacy",
        "title": "Privacy",
        "meta_description": "Placeholder privacy notice for {{ project_name }}.",
        "content": """# Privacy

> REPLACE_ME: This is a starter privacy page and is **not** legal advice.

## Who we are

REPLACE_ME: Add your company or operator name, contact email, and registered address if applicable.

## What data we collect

REPLACE_ME: Describe the personal data your product collects, why you collect it, and the legal basis.

## Processors and infrastructure

REPLACE_ME: Link to your subprocessors page and explain where customer data is stored and processed.

## Retention

REPLACE_ME: State how long you keep account, billing, support, and analytics data.

## Your rights

REPLACE_ME: Explain how users can request access, correction, deletion, export, or restriction.
""",
    },
    {
        "slug": "terms",
        "title": "Terms",
        "meta_description": "Placeholder terms for {{ project_name }}.",
        "content": """# Terms

> REPLACE_ME: This is a starter terms page and is **not** legal advice.

## Agreement

REPLACE_ME: Explain who the service is for and what customers agree to by using it.

## Acceptable use

REPLACE_ME: List prohibited behavior, abuse, scraping, or unlawful use.

## Billing and cancellation

REPLACE_ME: State that billing, tax calculation, invoices, and cancellations are handled by your billing provider unless you add a project-specific exception.

## Liability

REPLACE_ME: Add your limitation of liability, warranty disclaimer, and governing law language.
""",
    },
    {
        "slug": "security",
        "title": "Security",
        "meta_description": "Placeholder security overview for {{ project_name }}.",
        "content": """# Security

> REPLACE_ME: Update this page before sharing with customers.

## Authentication

REPLACE_ME: Describe MFA support, password policy, and account protection defaults.

## Data protection

REPLACE_ME: Describe encryption in transit, storage protections, backups, and access controls.

## Support access

REPLACE_ME: State whether staff can access customer accounts, whether impersonation exists, and how it is audited.

## Incident reporting

REPLACE_ME: Add a security contact address and your reporting expectations.
""",
    },
    {
        "slug": "subprocessors",
        "title": "Subprocessors",
        "meta_description": "Placeholder subprocessor inventory for {{ project_name }}.",
        "content": """# Subprocessors

> REPLACE_ME: Keep this list current for customers and procurement reviews.

| Service | Purpose | Region | Notes |
| --- | --- | --- | --- |
| REPLACE_ME | REPLACE_ME | REPLACE_ME | REPLACE_ME |

## Updates

REPLACE_ME: Explain how customers are informed when subprocessors change.
""",
    },
]


def seed_trust_pages(apps, schema_editor):
    Page = apps.get_model("pages", "Page")
    PageTranslation = apps.get_model("pages", "PageTranslation")
    language_code = settings.LANGUAGE_CODE
    db_alias = schema_editor.connection.alias

    for page_data in TRUST_PAGES:
        page, _ = Page.objects.using(db_alias).get_or_create(
            slug=page_data["slug"],
            defaults={
                "is_published": True,
            },
        )
        if not page.is_published:
            page.is_published = True
            page.save(update_fields=["is_published"])

        PageTranslation.objects.using(db_alias).update_or_create(
            master_id=page.id,
            language_code=language_code,
            defaults={
                "title": page_data["title"],
                "content": page_data["content"],
                "meta_description": page_data["meta_description"],
            },
        )


def unseed_trust_pages(apps, schema_editor):
    Page = apps.get_model("pages", "Page")
    db_alias = schema_editor.connection.alias
    Page.objects.using(db_alias).filter(slug__in=[page["slug"] for page in TRUST_PAGES]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("pages", "0002_alter_pagetranslation_unique_together_and_more"),
    ]

    operations = [
        migrations.RunPython(seed_trust_pages, unseed_trust_pages),
    ]
