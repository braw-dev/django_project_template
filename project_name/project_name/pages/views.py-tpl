import markdown
from django.http import Http404
from django.utils.safestring import mark_safe
from django.views.generic import DetailView

from .models import Page


class PageDetailView(DetailView):
    """
    Display a single published page.

    Features:
    - Respects publish/unpublish scheduling
    - Renders markdown content to HTML
    - Supports custom template override per page
    """

    model = Page
    context_object_name = "page"
    template_name = "pages/page_detail.html"

    def get_queryset(self):
        """Only return published pages within their publish window."""
        return Page.objects.published()

    def get_object(self, queryset=None):
        """Get the page or raise 404 if not found/not visible."""
        obj = super().get_object(queryset)
        if not obj.is_visible():
            raise Http404("Page not found")
        return obj

    def get_template_names(self):
        """Use custom template if specified, otherwise use default."""
        if self.object.template_name:
            return [self.object.template_name, self.template_name]
        return [self.template_name]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Render markdown to HTML
        md = markdown.Markdown(
            extensions=[
                "extra",  # Tables, fenced code, etc.
                "smarty",  # Smart quotes
                "toc",  # Table of contents
            ]
        )
        context["content_html"] = mark_safe(md.convert(self.object.content))
        # Pass meta object for django-meta template
        context["meta"] = self.object.as_meta()
        return context

