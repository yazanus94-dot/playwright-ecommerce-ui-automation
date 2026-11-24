"""Order History Page Object."""

from tests.pages.base_page import BasePage


class OrdersPage(BasePage):
    """Order history page of the e-commerce application."""

    # Selectors
    ORDER_ROWS = ".order-row"
    ORDER_IDS = ".order-id"
    ORDER_STATUSES = ".order-status"
    ORDER_TOTALS = ".order-total"
    ORDER_DATES = ".order-date"
    EMPTY_ORDERS_MESSAGE = ".empty-orders"
    NO_ORDERS_LINK = '.btn-primary[href="/"]'

    def assert_orders_loaded(self) -> None:
        """Assert the orders page is loaded."""
        self.assert_url_contains("/orders")

    def get_order_count(self) -> int:
        """Get the number of orders listed."""
        return self.count(self.ORDER_ROWS)

    def get_order_ids(self) -> list:
        """Get all order IDs listed."""
        return self.page.locator(self.ORDER_IDS).all_inner_texts()

    def get_order_statuses(self) -> list:
        """Get all order statuses."""
        return self.page.locator(self.ORDER_STATUSES).all_inner_texts()

    def click_order(self, order_id: str) -> None:
        """Click on an order to view its details."""
        selector = f'.order-row:has-text("{order_id}") a'
        self.click(selector)

    def assert_order_in_history(self, order_id: str) -> None:
        """Assert an order ID appears in order history."""
        self.assert_text_contains(self.ORDER_ROWS, order_id)

    def assert_orders_empty(self) -> None:
        """Assert there are no orders in history."""
        self.assert_element_visible(self.EMPTY_ORDERS_MESSAGE)
