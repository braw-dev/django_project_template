from django.contrib.sitemaps import Sitemap

from .models import Page


class PageSitemap(Sitemap):
    """Sitemap for published pages."""

    changefreq = "weekly"
    priority = 0.7

    def items(self):
        """Return all published pages."""
        return Page.objects.published()

    def lastmod(self, obj):
        """Return the last modification date."""
        return obj.updated_at

