"""Cart Page Object."""

from tests.pages.base_page import BasePage


class CartPage(BasePage):
    """Shopping cart page of the e-commerce application."""

    # Selectors
    CART_ITEMS = ".cart-item"
    CART_ITEM_NAME = ".cart-item-name"
    CART_ITEM_PRICE = ".cart-item-price"
    CART_ITEM_SUBTOTAL = ".cart-item-subtotal"
    CART_ITEM_QUANTITY = 'input[name="quantity"]'
    REMOVE_BUTTON = ".remove-item"
    UPDATE_BUTTON = ".update-qty"
    CHECKOUT_BUTTON = ".checkout-btn"
    CONTINUE_SHOPPING_BUTTON = '.btn-secondary[href="/"]'
    CART_COUNT = "#cart-count"
    EMPTY_CART_MESSAGE = ".empty-cart"
    TOTAL = ".summary-row.total span:last-child"

    def assert_cart_loaded(self) -> None:
        """Assert the cart page is loaded."""
        self.assert_url_contains("/cart")

    def get_cart_item_count(self) -> int:
        """Get the number of items in the cart."""
        return self.count(self.CART_ITEMS)

    def get_cart_item_names(self) -> list:
        """Get names of all items in the cart."""
        return self.page.locator(self.CART_ITEM_NAME).all_inner_texts()

    def get_cart_total(self) -> str:
        """Get the cart total amount."""
        return self.get_text(self.TOTAL)

    def remove_item(self, item_name: str) -> None:
        """Remove an item from the cart by name."""
        selector = f'.cart-item:has-text("{item_name}") .remove-item'
        self.click(selector)

    def update_quantity(self, item_name: str, quantity: int) -> None:
        """Update the quantity of a cart item."""
        selector = f'.cart-item:has-text("{item_name}") input[name="quantity"]'
        self.fill(selector, str(quantity))
        update_selector = f'.cart-item:has-text("{item_name}") .update-qty'
        self.click(update_selector)

    def proceed_to_checkout(self) -> None:
        """Click Proceed to Checkout button."""
        self.click(self.CHECKOUT_BUTTON)

    def click_continue_shopping(self) -> None:
        """Click Continue Shopping button."""
        self.click(self.CONTINUE_SHOPPING_BUTTON)

    def assert_item_in_cart(self, item_name: str) -> None:
        """Assert an item is present in the cart."""
        self.assert_text_contains(self.CART_ITEMS, item_name)

    def assert_item_not_in_cart(self, item_name: str) -> None:
        """Assert an item is NOT present in the cart."""
        selector = f'.cart-item:has-text("{item_name}")'
        assert not self.is_visible(selector), f"Item '{item_name}' should not be in cart"

    def assert_cart_empty(self) -> None:
        """Assert the cart is empty."""
        self.assert_element_visible(self.EMPTY_CART_MESSAGE)
