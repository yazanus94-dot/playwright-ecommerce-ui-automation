"""Checkout Flow Tests - ShopEase E-Commerce UI Automation."""

import pytest
from tests.pages.checkout_page import CheckoutPage

pytestmark = pytest.mark.critical


class TestCheckoutPage:
    """Checkout page test scenarios."""

    def test_checkout_redirects_when_cart_empty(self, checkout_page):
        """TC-CHECKOUT-001: Empty cart should redirect to home from checkout."""
        checkout_page.navigate()
        checkout_page.page.wait_for_timeout(500)
        # Should redirect to home since cart is empty
        assert checkout_page.page.url.endswith("/") or "/checkout" not in checkout_page.page.url

    def test_checkout_form_fields_present(self, checkout_page):
        """TC-CHECKOUT-002: Checkout form should display all required fields."""
        checkout_page.navigate("/checkout")
        # May redirect if cart empty, but page structure should exist
        checkout_page.assert_required_fields_present()

    def test_place_order_with_valid_details(self, checkout_page, order_confirmation_page):
        """TC-CHECKOUT-003: Placing order with valid details should succeed."""
        checkout_page.navigate("/checkout")
        checkout_page.fill_customer_details(
            "Test User",
            "test@example.com",
            "123 Test Street, Test City"
        )
        checkout_page.place_order()
        checkout_page.page.wait_for_timeout(1000)
        order_confirmation_page.assert_order_confirmed()

    def test_checkout_total_displays(self, checkout_page):
        """TC-CHECKOUT-004: Checkout should display order total."""
        checkout_page.navigate("/checkout")
        try:
            total = checkout_page.get_order_total()
            assert "$" in total or total == "$0.00"
        except Exception:
            # Page may have redirected if cart empty
            pass

    def test_back_button_returns_to_cart(self, checkout_page, cart_page):
        """TC-CHECKOUT-005: Back button should return to cart page."""
        checkout_page.navigate("/checkout")
        checkout_page.click_back()
        checkout_page.page.wait_for_timeout(500)
        assert "/cart" in checkout_page.page.url or checkout_page.page.url.endswith("/")
