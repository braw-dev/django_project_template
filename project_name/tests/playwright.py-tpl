import os
from abc import ABC

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import tag
from playwright.sync_api import expect, sync_playwright


@tag("browser")
class PlaywrightTestCase(ABC, StaticLiveServerTestCase):
    """A base test case class for Playwright tests.
    It provides a Playwright browser instance and a browser context
    and launches the Django static live server."""

    expect = expect  # helper for assertions

    @classmethod
    def setUpClass(cls) -> None:
        # Allow running async code in Django tests
        # https://docs.djangoproject.com/en/5.1/topics/async/#envvar-DJANGO_ALLOW_ASYNC_UNSAFE
        os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
        super().setUpClass()
        cls.playwright = sync_playwright().start()
        cls.browser = cls.playwright.chromium.launch()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.browser.close()
        cls.playwright.stop()
        super().tearDownClass()

    @property
    def server_url(self) -> str:
        return self.live_server_url
