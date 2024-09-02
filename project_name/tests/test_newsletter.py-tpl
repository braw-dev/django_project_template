from django.urls import reverse
from playwright.sync_api import expect

from .playwright import PlaywrightTestCase

# Persona:
# Jack wants to learn more about the product and sign up for the newsletter


class NewsletterTestCase(PlaywrightTestCase):
    def test_newsletter_signup(self):
        # Jack visits the newsletter signup page
        email = "jack@example.com"
        context = self.browser.new_context()
        context.set_default_timeout(3000)
        page = context.new_page()
        page.goto(self.server_url + reverse("newsletter:signup"))

        # Jack sees the newsletter signup form and accidentally submits it with an invalid email
        email_input = page.get_by_test_id("newsletter-signup-form")
        email_input.type("invalid-email")
        email_input.press("Enter")

        # Jack sees an error message
        page.wait_for_selector("[data-testid=newsletter-signup-form]:invalid")

        # Jack corrects the email and submits the form
        email_input.fill("")
        email_input.type(email)
        email_input.press("Enter")

        # Jack is redirected to the success page
        page.wait_for_url(self.server_url + reverse("newsletter:signup_success"), timeout=3000)

        # Jack sees a success message
        self.assertIn("Thank you", page.title())
        self.assertIn("You have successfully signed up for the newsletter.", page.content())

        # For some reason Jack decides to sign up again
        page.goto(self.server_url + reverse("newsletter:signup"))
        email_input = page.get_by_test_id("newsletter-signup-form")
        email_input.type(email)
        email_input.press("Enter")

        page.wait_for_url(self.server_url + reverse("newsletter:signup"), timeout=3000)

        # Jack sees an info message that he is already subscribed
        error_list = page.locator("ul.errorlist")
        expect(error_list).to_be_visible()
        expect(error_list).to_contain_text("You are already subscribed.")

        # Jack closes the browser
        page.close()
