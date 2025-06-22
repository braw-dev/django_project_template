from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

User = get_user_model()


###############################################
## Test cases
###############################################
class AuthTestCase(TestCase):
    username = "jane"
    email = "jane@example.com"
    password = "iKDt6EFwyQEjkgqSzCdvFdC7imS5JN0H"

    def test_register_view_uses_template(self):
        response = self.client.get(reverse("account_signup"))

        self.assertTemplateUsed(response, "account/signup.html")

    def test_register_successfully_registers_user(self):
        form_data = {"username": self.username, "password1": self.password}

        self.client.post(
            reverse("account_signup"),
            data=form_data,
        )

        users = User.objects.filter(username=self.username)
        self.assertEqual(users.count(), 1)

    def test_register_redirects_on_valid_data(self):
        form_data = {"username": self.username, "password1": self.password}

        response = self.client.post(
            reverse("account_signup"),
            data=form_data,
        )

        self.assertRedirects(response, reverse("account:dashboard"))

    def test_register_shows_error_on_invalid_password(self):
        form_data = {"username": self.username, "password1": ""}

        response = self.client.post(
            reverse("account_signup"),
            data=form_data,
        )

        self.assertTemplateUsed(response, "account/signup.html")
        self.assertContains(response, "This field is required")

    def test_register_shows_error_on_invalid_username(self):
        form_data = {"username": "d", "password1": self.password}

        response = self.client.post(
            reverse("account_signup"),
            data=form_data,
        )

        self.assertTemplateUsed(response, "account/signup.html")
        self.assertContains(response, "Ensure this value has at least 3 characters (it has 1)")

    def test_dashboard_view(self):
        response = self.client.get(reverse("account:dashboard"))

        self.assertTemplateUsed(response, "core/pages/dashboard.html")
