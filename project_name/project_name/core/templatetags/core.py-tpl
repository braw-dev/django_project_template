from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag
def project_display_name():
    return getattr(settings, "PROJECT_DISPLAY_NAME", "")


@register.inclusion_tag("partials/plausible.html")
def plausible_analytics():
    return {
        "domain": getattr(settings, "PLAUSIBLE_DOMAIN", ""),
        "script_host": getattr(settings, "PLAUSIBLE_SCRIPT_HOST", ""),
    }


@register.inclusion_tag("partials/chatwoot.html")
def chatwoot_widget():
    return {
        "website_token": getattr(settings, "CHATWOOT_WEBSITE_TOKEN", ""),
        "base_url": getattr(settings, "CHATWOOT_BASE_URL", "https://app.chatwoot.com"),
    }
