from django.contrib import admin

from . import models


@admin.register(models.Example)
class ExampleAdmin(admin.ModelAdmin):
    """Register the `Example` model with the Django admin.

    Args:
        admin (admin.ModelAdmin): The Django admin.ModelAdmin class to inherit from
    """

    pass
