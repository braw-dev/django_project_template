from django.urls import path

from .views import PageDetailView

app_name = "pages"

urlpatterns = [
    # Catch-all pattern for pages - should be placed last in main urls.py
    path("<slug:slug>/", PageDetailView.as_view(), name="page_detail"),
]

