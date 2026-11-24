"""End-to-End Flow Tests - ShopEase E-Commerce UI Automation."""

import pytest

pytestmark = pytest.mark.critical


class TestEndToEndFlows:
    """Complete user journey test scenarios."""

    def test_complete_guest_purchase_flow(self, page, home_page, login_page, cart_page, checkout_page, order_confirmation_page):
        """TC-E2E-001: Complete guest purchase from home to order confirmation."""
        home_page.navigate()
        product_names = home_page.page.locator(".product-name").all_inner_texts()
        assert len(product_names) > 0
        home_page.click_add_to_cart(product_names[0])
        home_page.page.wait_for_timeout(1500)
        home_page.click_cart()
        cart_page.assert_item_in_cart(product_names[0])
        cart_page.proceed_to_checkout()
        checkout_page.assert_checkout_loaded()
        checkout_page.fill_customer_details(
            "E2E Test User",
            "e2e@example.com",
            "123 E2E Street, Test City"
        )
        checkout_page.place_order()
        checkout_page.page.wait_for_timeout(1000)
        order_confirmation_page.assert_order_confirmed()

    def test_register_then_purchase_flow(self, page, home_page, register_page, test_user, cart_page, checkout_page, order_confirmation_page):
        """TC-E2E-002: Register user then complete purchase flow."""
        register_page.navigate()
        register_page.register(test_user["name"], test_user["email"], test_user["password"])
        register_page.page.wait_for_timeout(1000)
        home_page.navigate()
        product_names = home_page.page.locator(".product-name").all_inner_texts()
        assert len(product_names) > 0
        home_page.click_add_to_cart(product_names[0])
        home_page.page.wait_for_timeout(1500)
        home_page.click_cart()
        cart_page.proceed_to_checkout()
        checkout_page.assert_checkout_loaded()
        checkout_page.fill_customer_details(
            test_user["name"],
            test_user["email"],
            "123 Registered User Street, Test City"
        )
        checkout_page.place_order()
        checkout_page.page.wait_for_timeout(1000)
        order_confirmation_page.assert_order_confirmed()

    def test_login_then_view_orders_flow(self, page, home_page, login_page, orders_page, test_user):
        """TC-E2E-003: Login then navigate to orders page."""
        home_page.navigate()
        home_page.click_login()
        login_page.login(test_user["email"], test_user["password"])
        login_page.page.wait_for_timeout(1000)
        assert "/login" not in login_page.page.url
        home_page.click_cart()  # navigate somewhere first
        orders_page.navigate()
        orders_page.assert_orders_loaded()

    def test_add_multiple_items_to_cart(self, page, home_page, cart_page):
        """TC-E2E-004: Add multiple different items to cart."""
        home_page.navigate()
        product_names = home_page.page.locator(".product-name").all_inner_texts()
        assert len(product_names) >= 2
        home_page.click_add_to_cart(product_names[0])
        home_page.page.wait_for_timeout(1000)
        home_page.click_add_to_cart(product_names[1])
        home_page.page.wait_for_timeout(1000)
        home_page.click_cart()
        cart_page.assert_item_in_cart(product_names[0])
        cart_page.assert_item_in_cart(product_names[1])

    def test_logout_flow(self, page, home_page, login_page, test_user):
        """TC-E2E-005: Login then logout should return to guest state."""
        home_page.navigate()
        home_page.click_login()
        login_page.login(test_user["email"], test_user["password"])
        login_page.page.wait_for_timeout(1000)
        assert home_page.is_logged_in()
        home_page.click_logout()
        home_page.page.wait_for_timeout(500)
        assert not home_page.is_logged_in()

    def test_search_then_add_to_cart_flow(self, page, home_page, cart_page):
        """TC-E2E-006: Search for product then add to cart."""
        home_page.navigate()
        home_page.search("Headphones")
        home_page.assert_search_results_contain("Headphones")
        home_page.page.wait_for_timeout(1000)
        product_names = home_page.page.locator(".product-name").all_inner_texts()
        if product_names:
            home_page.click_add_to_cart(product_names[0])
            home_page.page.wait_for_timeout(1000)
            assert home_page.get_cart_count() >= 1
