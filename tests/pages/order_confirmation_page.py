"""Order Confirmation Page Object."""

from tests.pages.base_page import BasePage


class OrderConfirmationPage(BasePage):
    """Order confirmation page of the e-commerce application."""

    # Selectors
    SUCCESS_MESSAGE = "h1"
    ORDER_ID = ".order-id"
    ORDER_TOTAL_SELECTOR = ".order-details p:nth-child(3)"
    ORDER_STATUS = ".order-details p:nth-child(4)"
    CUSTOMER_NAME = ".order-details p:nth-child(1)"
    CONTINUE_SHOPPING_BUTTON = '.btn-primary[href="/"]'
    VIEW_ORDERS_BUTTON = '.btn-secondary[href="/orders"]'

    def assert_order_confirmed(self) -> None:
        """Assert the order confirmation page is displayed."""
        self.assert_url_contains("/")  # Confirmation uses root path
        self.assert_text_contains(self.SUCCESS_MESSAGE, "Order Placed Successfully")

    def get_order_id(self) -> str:
        """Get the order confirmation ID."""
        return self.get_text(self.ORDER_ID)

    def get_customer_name(self) -> str:
        """Get the customer name from the confirmation."""
        return self.get_text(self.CUSTOMER_NAME)

    def click_continue_shopping(self) -> None:
        """Click Continue Shopping button."""
        self.click(self.CONTINUE_SHOPPING_BUTTON)

    def click_view_orders(self) -> None:
        """Click View My Orders button."""
        self.click(self.VIEW_ORDERS_BUTTON)

    def assert_thank_you_message(self) -> None:
        """Assert thank you message is displayed."""
        self.assert_text_contains("body", "Thank you")
