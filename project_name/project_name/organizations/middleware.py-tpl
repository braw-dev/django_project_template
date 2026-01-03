"""Middleware for permission enforcement."""

from django.http import Http404


class OrganizationPermissionMiddleware:
    """Middleware to catch permission errors and convert to 404.

    This prevents data leakage by not revealing whether a resource exists
    when the user doesn't have permission.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            response = self.get_response(request)
        except PermissionError:
            raise Http404("Not found") from None

        return response
