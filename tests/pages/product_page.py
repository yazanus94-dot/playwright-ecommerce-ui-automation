"""Product Detail Page Object."""

from tests.pages.base_page import BasePage


class ProductPage(BasePage):
    """Product detail page of the e-commerce application."""

    # Selectors
    PRODUCT_TITLE = ".product-title"
    PRODUCT_CATEGORY = ".product-category"
    PRODUCT_PRICE = ".product-price"
    PRODUCT_DESC = ".product-desc"
    PRODUCT_IMAGE = ".main-image"
    QUANTITY_INPUT = 'input[name="quantity"]'
    ADD_TO_CART_BUTTON = ".add-to-cart"
    BACK_BUTTON = '.btn-secondary[href="/"]'
    CART_COUNT = "#cart-count"

    def assert_product_loaded(self, product_name: str) -> None:
        """Assert the product detail page is loaded with correct product."""
        self.assert_text_contains(self.PRODUCT_TITLE, product_name)

    def navigate_to_product(self, product_id: int) -> None:
        """Navigate to a product detail page by ID."""
        self.navigate(f"/product/{product_id}")

    def get_product_name(self) -> str:
        """Get the product name displayed."""
        return self.get_text(self.PRODUCT_TITLE)

    def get_product_price(self) -> str:
        """Get the product price displayed."""
        return self.get_text(self.PRODUCT_PRICE)

    def get_product_category(self) -> str:
        """Get the product category displayed."""
        return self.get_text(self.PRODUCT_CATEGORY)

    def set_quantity(self, quantity: int) -> None:
        """Set the product quantity."""
        self.fill(self.QUANTITY_INPUT, str(quantity))

    def add_to_cart(self) -> None:
        """Click Add to Cart button."""
        self.click(self.ADD_TO_CART_BUTTON)

    def get_cart_count(self) -> int:
        """Get the current cart item count."""
        return int(self.get_text(self.CART_COUNT) or 0)

    def click_back(self) -> None:
        """Click Back to Shopping button."""
        self.click(self.BACK_BUTTON)

    def assert_image_visible(self) -> None:
        """Assert the product image is visible."""
        self.assert_element_visible(self.PRODUCT_IMAGE)

    def assert_in_stock(self) -> None:
        """Assert the product is in stock."""
        self.page.wait_for_selector(".stock", timeout=5000)
