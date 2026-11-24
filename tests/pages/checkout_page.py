"""Checkout Page Object."""

from tests.pages.base_page import BasePage


class CheckoutPage(BasePage):
    """Checkout page of the e-commerce application."""

    # Selectors
    NAME_INPUT = 'input[name="customer_name"]'
    EMAIL_INPUT = 'input[name="customer_email"]'
    ADDRESS_INPUT = 'textarea[name="customer_address"]'
    PLACE_ORDER_BUTTON = ".place-order-btn"
    BACK_BUTTON = '.btn-secondary[href="/cart"]'
    ORDER_SUMMARY_ITEMS = ".summary-item"
    ORDER_TOTAL = ".summary-total span:last-child"

    def assert_checkout_loaded(self) -> None:
        """Assert the checkout page is loaded."""
        self.assert_url_contains("/checkout")

    def fill_customer_details(self, name: str, email: str, address: str) -> None:
        """Fill in customer checkout details."""
        self.fill(self.NAME_INPUT, name)
        self.fill(self.EMAIL_INPUT, email)
        self.fill(self.ADDRESS_INPUT, address)

    def place_order(self) -> None:
        """Click Place Order button."""
        self.click(self.PLACE_ORDER_BUTTON)

    def click_back(self) -> None:
        """Click Back to Cart button."""
        self.click(self.BACK_BUTTON)

    def get_order_total(self) -> str:
        """Get the order total displayed."""
        return self.get_text(self.ORDER_TOTAL)

    def assert_required_fields_present(self) -> None:
        """Assert all required checkout fields are present."""
        self.assert_element_visible(self.NAME_INPUT)
        self.assert_element_visible(self.EMAIL_INPUT)
        self.assert_element_visible(self.ADDRESS_INPUT)
