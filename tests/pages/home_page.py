"""Home Page Object."""

from tests.pages.base_page import BasePage


class HomePage(BasePage):
    """Home page of the e-commerce application."""

    # Selectors
    LOGO = ".logo a"
    SEARCH_INPUT = 'input[name="q"]'
    CATEGORY_SELECT = 'select[name="category"]'
    SEARCH_BUTTON = 'button[type="submit"]'
    PRODUCT_CARDS = ".product-card"
    PRODUCT_NAME = ".product-name"
    PRODUCT_PRICE = ".product-price"
    ADD_TO_CART_BUTTON = ".add-to-cart"
    CART_COUNT = "#cart-count"
    LOGIN_LINK = 'a[href="/login"]'
    REGISTER_LINK = 'a[href="/register"]'
    LOGOUT_LINK = 'a[href="/logout"]'
    ORDERS_LINK = 'a[href="/orders"]'
    CART_LINK = 'a[href="/cart"]'

    def navigate(self) -> None:
        """Navigate to the homepage."""
        super().navigate("/")

    def search(self, query: str) -> None:
        """Search for a product."""
        self.fill(self.SEARCH_INPUT, query)
        self.click(self.SEARCH_BUTTON)

    def filter_by_category(self, category: str) -> None:
        """Filter products by category."""
        self.page.select_option(self.CATEGORY_SELECT, category)
        self.click(self.SEARCH_BUTTON)

    def click_product(self, product_name: str) -> None:
        """Click on a product card by name."""
        selector = f'.product-card:has-text("{product_name}") .product-name'
        self.click(selector)

    def click_add_to_cart(self, product_name: str) -> None:
        """Click Add to Cart for a specific product."""
        selector = f'.product-card:has-text("{product_name}") .add-to-cart'
        self.click(selector)

    def get_cart_count(self) -> int:
        """Get the current cart item count."""
        return int(self.get_text(self.CART_COUNT) or 0)

    def is_logged_in(self) -> bool:
        """Check if user is logged in."""
        return self.is_visible(self.LOGOUT_LINK)

    def click_login(self) -> None:
        """Click the login link."""
        self.click(self.LOGIN_LINK)

    def click_register(self) -> None:
        """Click the register link."""
        self.click(self.REGISTER_LINK)

    def click_logout(self) -> None:
        """Click the logout link."""
        self.click(self.LOGOUT_LINK)

    def click_cart(self) -> None:
        """Click the cart link."""
        self.click(self.CART_LINK)

    def get_product_count(self) -> int:
        """Get the number of products displayed."""
        return self.count(self.PRODUCT_CARDS)

    def assert_product_visible(self, product_name: str) -> None:
        """Assert a product is visible on the page."""
        self.assert_text_contains(".product-card", product_name)

    def assert_search_results_contain(self, query: str) -> None:
        """Assert search results contain the query term."""
        self.assert_text_contains(".product-card", query)
