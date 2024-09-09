from django.urls import reverse
from django_stubs_ext.db.models import TypedModelMeta
from model_utils import Choices
from model_utils.models import StatusModel, TimeStampedModel


class Example(TimeStampedModel, StatusModel):
    """By inheriting from `TimeStampedModel`, we get the `created` and `modified` fields.

    `StatusModel` provides a `status` field with choices and a `status_changed` field.

    https://django-model-utils.readthedocs.io/en/latest/models.html#timestampedmodel

    Args:
        TimeStampedModel (TimeStampedModel): The django-model-utils model to inherit from
    """

    """Combined with a `StatusModel`, we get a `status` field with 
    choices and a `status_changed` field.

    ```python
    a = Example()
    a.status = Example.STATUS.published

    # this save will update a.status_changed
    a.save()

    # this query will only return published examples:
    Example.published.all()
    ```
    """
    STATUS = Choices("draft", "published")

    def __str__(self) -> str:
        """String representation of the model."""
        return f"{self.pk} - {self.status} - {self.created}"

    def get_absolute_url(self):
        """Get the absolute URL for the model instance."""
        return reverse("example:detail", kwargs={"pk": self.pk})

    class Meta(TypedModelMeta):
        """When writing model `Meta` classes, make sure to inherit from `TypedModelMeta`.

        This ensures correct types for Meta options and attributes.

        https://github.com/typeddjango/django-stubs?tab=readme-ov-file#type-checking-of-model-meta-attributes

        Args:
            TypedModelMeta (TypedModelMeta): Django stubs data type
        """

        ordering = ["-modified"]  # By default order by modified date, newest first
