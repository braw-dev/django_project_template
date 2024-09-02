from django.urls import reverse
from playwright.sync_api import expect

from .playwright import PlaywrightTestCase

# Persona:
# Jackie wants to know the pricing of the product


class PricingTestCase(PlaywrightTestCase):
    def test_pricing_page(self):
        # Jackie visits the pricing page
        context = self.browser.new_context()
        context.set_default_timeout(3000)
        page = context.new_page()
        page.goto(self.server_url + reverse("pricing"))

        # Jackie sees the pricing table
        pricing_table = page.get_by_test_id("pricing-table")
        self.assertTrue(pricing_table.is_visible())

        # Jackie sees the available pricing plans
        pricing_plans = pricing_table.get_by_test_id("pricing-plan")
        expect(pricing_plans).to_have_count(2)

        # For each pricing plan, Jackie sees the name, price, features and a button to sign up
        for plan in pricing_plans.all():
            plan_name = plan.get_by_test_id("plan-name")
            plan_price = plan.get_by_test_id("plan-price")
            plan_features = plan.get_by_test_id("plan-features")
            plan_button = plan.get_by_test_id("plan-button")
            self.assertTrue(plan_name.is_visible())
            self.assertTrue(plan_price.is_visible())
            self.assertTrue(plan_features.is_visible())
            self.assertTrue(plan_button.is_visible())

        # Jackie closes the browser
        page.close()
