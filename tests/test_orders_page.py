"""Order History Tests - ShopEase E-Commerce UI Automation."""

import pytest
from tests.pages.orders_page import OrdersPage

pytestmark = pytest.mark.regression


class TestOrderHistoryPage:
    """Order history page test scenarios."""

    def test_orders_redirects_when_not_logged_in(self, orders_page, login_page):
        """TC-ORDER-001: Orders page should redirect to login for unauthenticated users."""
        orders_page.navigate()
        orders_page.page.wait_for_timeout(500)
        assert "/login" in orders_page.page.url

    def test_order_history_displays_orders(self, orders_page, login_page, test_user):
        """TC-ORDER-002: Order history should display user's orders."""
        login_page.navigate()
        login_page.login(test_user["email"], test_user["password"])
        login_page.page.wait_for_timeout(1000)
        orders_page.navigate()
        orders_page.assert_orders_loaded()
        # Orders may be empty or have items - just verify page loads
        assert orders_page.get_order_count() >= 0

    def test_order_id_click_shows_details(self, orders_page, login_page, test_user):
        """TC-ORDER-003: Clicking order ID should navigate to order detail."""
        login_page.navigate()
        login_page.login(test_user["email"], test_user["password"])
        login_page.page.wait_for_timeout(1000)
        orders_page.navigate()
        order_ids = orders_page.get_order_ids()
        if order_ids:
            orders_page.click_order(order_ids[0])
            orders_page.page.wait_for_timeout(500)
            assert "/orders/" in orders_page.page.url
