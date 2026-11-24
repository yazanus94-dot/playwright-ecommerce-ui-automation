"""Base Page Object - Foundation for all page objects in the framework."""

from typing import Optional
from playwright.sync_api import Page, expect

from config.settings import BASE_URL, TIMEOUT


class BasePage:
    """Base page class providing common actions and helpers."""

    def __init__(self, page: Page, base_url: str = BASE_URL):
        self.page = page
        self.base_url = base_url
        self.timeout = TIMEOUT

    # ------------------------------------------------------------------
    # Navigation helpers
    # ------------------------------------------------------------------
    def navigate(self, path: str = "/") -> None:
        """Navigate to a path relative to the base URL."""
        url = f"{self.base_url.rstrip('/')}{path}"
        self.page.goto(url, wait_until="networkidle")
        self.page.wait_for_load_state("networkidle", timeout=self.timeout)

    def go_home(self) -> None:
        """Navigate to the homepage."""
        self.navigate("/")

    # ------------------------------------------------------------------
    # Common element actions
    # ------------------------------------------------------------------
    def click(self, selector: str, timeout: Optional[int] = None) -> None:
        """Click an element identified by selector."""
        self.page.click(selector, timeout=timeout or self.timeout)

    def fill(self, selector: str, value: str, timeout: Optional[int] = None) -> None:
        """Fill an input field with value."""
        self.page.fill(selector, value, timeout=timeout or self.timeout)

    def get_text(self, selector: str, timeout: Optional[int] = None) -> str:
        """Get the text content of an element."""
        return self.page.inner_text(selector, timeout=timeout or self.timeout)

    def get_attribute(self, selector: str, attribute: str, timeout: Optional[int] = None) -> Optional[str]:
        """Get an attribute value from an element."""
        return self.page.get_attribute(selector, attribute, timeout=timeout or self.timeout)

    def is_visible(self, selector: str, timeout: Optional[int] = None) -> bool:
        """Check if an element is visible."""
        try:
            return self.page.is_visible(selector, timeout=timeout or self.timeout)
        except Exception:
            return False

    def wait_for_selector(self, selector: str, timeout: Optional[int] = None) -> None:
        """Wait for an element to appear in the DOM."""
        self.page.wait_for_selector(selector, timeout=timeout or self.timeout)

    def count(self, selector: str) -> int:
        """Count elements matching a selector."""
        return self.page.locator(selector).count()

    # ------------------------------------------------------------------
    # Assertions
    # ------------------------------------------------------------------
    def assert_url_contains(self, fragment: str) -> None:
        """Assert the current URL contains the given fragment."""
        expect(self.page).to_have_url(f"*{fragment}*")

    def assert_page_title(self, expected: str) -> None:
        """Assert the page title contains the expected text."""
        title = self.page.title()
        assert expected in title, f"Expected title to contain '{expected}', got '{title}'"

    def assert_element_visible(self, selector: str) -> None:
        """Assert an element is visible on the page."""
        expect(self.page.locator(selector)).to_be_visible()

    def assert_element_hidden(self, selector: str) -> None:
        """Assert an element is hidden from the page."""
        expect(self.page.locator(selector)).to_be_hidden()

    def assert_text_contains(self, selector: str, fragment: str) -> None:
        """Assert an element's text contains the given fragment."""
        expect(self.page.locator(selector)).to_contain_text(fragment)

    def assert_text_equals(self, selector: str, expected: str) -> None:
        """Assert an element's text equals the expected value."""
        expect(self.page.locator(selector)).to_have_text(expected)
