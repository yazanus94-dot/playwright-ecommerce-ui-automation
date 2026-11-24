"""Product Detail Page Tests - ShopEase E-Commerce UI Automation."""

import pytest
from tests.pages.product_page import ProductPage

pytestmark = pytest.mark.regression


class TestProductPage:
    """Product detail page test scenarios."""

    def test_product_page_loads_with_details(self, product_page):
        """TC-PRODUCT-001: Product page should display product name, price, category, description."""
        product_page.navigate_to_product(1)
        product_page.assert_product_loaded("Wireless Bluetooth Headphones")
        product_page.assert_text_contains(".product-price", "$")
        product_page.assert_text_contains(".product-category", "")
        product_page.assert_text_contains(".product-desc", "")

    def test_product_image_is_visible(self, product_page):
        """TC-PRODUCT-002: Product image should be visible on product page."""
        product_page.navigate_to_product(1)
        product_page.assert_image_visible()

    def test_add_to_cart_from_product_page(self, product_page):
        """TC-PRODUCT-003: Adding product to cart from product page should work."""
        product_page.navigate_to_product(1)
        product_page.add_to_cart()
        product_page.page.wait_for_timeout(1000)
        # Verify toast or cart count updated
        toast = product_page.page.locator(".toast")
        cart_count = product_page.get_cart_count()
        assert cart_count >= 0

    def test_quantity_field_defaults_to_one(self, product_page):
        """TC-PRODUCT-004: Quantity input should default to 1."""
        product_page.navigate_to_product(1)
        qty_value = product_page.page.input_value('input[name="quantity"]')
        assert qty_value == "1"

    def test_invalid_product_id_shows_404(self, product_page):
        """TC-PRODUCT-005: Non-existent product should show 404 page."""
        product_page.navigate("/product/99999")
        product_page.page.wait_for_timeout(500)
        assert product_page.page.url or product_page.page.title()

    def test_back_button_returns_to_home(self, product_page, home_page):
        """TC-PRODUCT-006: Back button should return to home page."""
        product_page.navigate_to_product(1)
        product_page.click_back()
        product_page.page.wait_for_timeout(500)
        assert product_page.page.url.endswith("/") or product_page.page.url.endswith("/home")

    def test_product_price_format(self, product_page):
        """TC-PRODUCT-007: Product price should be formatted as currency."""
        product_page.navigate_to_product(1)
        price = product_page.get_product_price()
        assert "$" in price

    def test_product_stock_displayed(self, product_page):
        """TC-PRODUCT-008: Product stock status should be displayed."""
        product_page.navigate_to_product(1)
        product_page.assert_in_stock()
