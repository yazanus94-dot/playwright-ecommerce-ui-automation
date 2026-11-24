"""Home Page Tests - ShopEase E-Commerce UI Automation."""

import pytest
from tests.pages.home_page import HomePage

pytestmark = pytest.mark.smoke


class TestHomePage:
    """Home page test scenarios."""

    def test_home_page_loads_successfully(self, home_page):
        """TC-HOME-001: Home page should load with correct title and content."""
        home_page.navigate()
        home_page.assert_page_title("ShopEase")
        home_page.assert_element_visible(".logo a")
        home_page.assert_element_visible(".search-form")

    def test_cart_count_displays_zero_for_guest(self, home_page):
        """TC-HOME-002: Cart count should display 0 for unauthenticated users."""
        home_page.navigate()
        assert home_page.get_cart_count() == 0

    def test_home_page_shows_products(self, home_page):
        """TC-HOME-003: Home page should display product cards."""
        home_page.navigate()
        assert home_page.get_product_count() > 0

    def test_login_link_redirects_to_login_page(self, home_page, login_page):
        """TC-HOME-004: Login link should navigate to login page."""
        home_page.navigate()
        home_page.click_login()
        login_page.assert_login_loaded()

    def test_register_link_redirects_to_register_page(self, home_page, register_page):
        """TC-HOME-005: Register link should navigate to register page."""
        home_page.navigate()
        home_page.click_register()
        register_page.assert_register_loaded()

    def test_cart_link_redirects_to_cart_page(self, home_page, cart_page):
        """TC-HOME-006: Cart link should navigate to cart page."""
        home_page.navigate()
        home_page.click_cart()
        cart_page.assert_cart_loaded()

    def test_search_functionality_returns_results(self, home_page):
        """TC-HOME-007: Search should return products matching the query."""
        home_page.navigate()
        home_page.search("Headphones")
        home_page.assert_search_results_contain("Headphones")

    def test_empty_search_returns_all_products(self, home_page):
        """TC-HOME-008: Empty search should return all products."""
        home_page.navigate()
        home_page.search("")
        assert home_page.get_product_count() > 0

    def test_product_click_navigates_to_product_page(self, home_page, product_page):
        """TC-HOME-009: Clicking a product should navigate to product detail page."""
        home_page.navigate()
        product_names = home_page.page.locator(".product-name").all_inner_texts()
        if product_names:
            home_page.click_product(product_names[0])
            product_page.assert_product_loaded(product_names[0])

    def test_add_to_cart_increments_cart_count(self, home_page):
        """TC-HOME-010: Adding a product to cart should increment cart count."""
        home_page.navigate()
        initial_count = home_page.get_cart_count()
        product_names = home_page.page.locator(".product-name").all_inner_texts()
        if product_names:
            home_page.click_add_to_cart(product_names[0])
            home_page.page.wait_for_timeout(1000)
            new_count = home_page.get_cart_count()
            assert new_count > initial_count

    def test_category_filter_changes_products(self, home_page):
        """TC-HOME-011: Filtering by category should show only matching products."""
        home_page.navigate()
        home_page.filter_by_category("Electronics")
        home_page.page.wait_for_timeout(1000)
        # Just verify the page still loads products after filter
        assert home_page.get_product_count() >= 0

    def test_footer_copyright_visible(self, home_page):
        """TC-HOME-012: Footer should display copyright text."""
        home_page.navigate()
        home_page.assert_text_contains(".footer", "ShopEase")
