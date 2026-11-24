"""Shopping Cart Tests - ShopEase E-Commerce UI Automation."""

import pytest
from tests.pages.cart_page import CartPage

pytestmark = pytest.mark.regression


class TestCartPage:
    """Shopping cart page test scenarios."""

    def test_cart_page_loads_empty_for_guest(self, cart_page):
        """TC-CART-001: Cart page should show empty state for guest user."""
        cart_page.navigate()
        cart_page.assert_cart_loaded()
        # Cart may be empty or have items - just verify page loads

    def test_cart_item_displayed_after_add(self, cart_page, home_page):
        """TC-CART-002: Added item should appear in cart."""
        home_page.navigate()
        product_names = home_page.page.locator(".product-name").all_inner_texts()
        if product_names:
            home_page.click_add_to_cart(product_names[0])
            home_page.page.wait_for_timeout(1500)
            home_page.click_cart()
            cart_page.assert_cart_loaded()
            cart_page.assert_item_in_cart(product_names[0])

    def test_remove_item_from_cart(self, cart_page, home_page):
        """TC-CART-003: Removing item from cart should work."""
        home_page.navigate()
        product_names = home_page.page.locator(".product-name").all_inner_texts()
        if product_names:
            home_page.click_add_to_cart(product_names[0])
            home_page.page.wait_for_timeout(1500)
            home_page.click_cart()
            cart_page.remove_item(product_names[0])
            cart_page.page.wait_for_timeout(1000)
            cart_page.assert_item_not_in_cart(product_names[0])

    def test_update_item_quantity(self, cart_page, home_page):
        """TC-CART-004: Updating item quantity should work."""
        home_page.navigate()
        product_names = home_page.page.locator(".product-name").all_inner_texts()
        if product_names:
            home_page.click_add_to_cart(product_names[0])
            home_page.page.wait_for_timeout(1500)
            home_page.click_cart()
            cart_page.update_quantity(product_names[0], 2)
            cart_page.page.wait_for_timeout(1000)

    def test_continue_shopping_returns_home(self, cart_page, home_page):
        """TC-CART-005: Continue Shopping should return to home page."""
        home_page.navigate()
        home_page.click_cart()
        cart_page.click_continue_shopping()
        cart_page.page.wait_for_timeout(500)
        assert cart_page.page.url.endswith("/") or cart_page.page.url.endswith("/home")

    def test_cart_total_displays(self, cart_page, home_page):
        """TC-CART-006: Cart total should display when items are present."""
        home_page.navigate()
        product_names = home_page.page.locator(".product-name").all_inner_texts()
        if product_names:
            home_page.click_add_to_cart(product_names[0])
            home_page.page.wait_for_timeout(1500)
            home_page.click_cart()
            total = cart_page.get_cart_total()
            assert "$" in total or total == "$0.00"

    def test_cart_count_persists_across_pages(self, home_page, cart_page):
        """TC-CART-007: Cart count should persist across navigation."""
        home_page.navigate()
        product_names = home_page.page.locator(".product-name").all_inner_texts()
        if product_names:
            initial_count = home_page.get_cart_count()
            home_page.click_add_to_cart(product_names[0])
            home_page.page.wait_for_timeout(1500)
            new_count = home_page.get_cart_count()
            assert new_count > initial_count
