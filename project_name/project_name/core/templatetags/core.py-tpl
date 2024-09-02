from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag
def project_display_name():
    return getattr(settings, "PROJECT_DISPLAY_NAME", "")
