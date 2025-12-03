from celery import shared_task
from django.contrib.auth import get_user_model

User = get_user_model()


@shared_task
def delete_user(user_id: int):
    """Delete a user by their ID."""
    User.objects.get(id=user_id).delete()
