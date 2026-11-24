"""Login Page Object."""

from tests.pages.base_page import BasePage


class LoginPage(BasePage):
    """Login page of the e-commerce application."""

    # Selectors
    EMAIL_INPUT = 'input[name="email"]'
    PASSWORD_INPUT = 'input[name="password"]'
    SUBMIT_BUTTON = 'button[type="submit"]'
    REGISTER_LINK = 'a[href="/register"]'
    HOME_LINK = 'a[href="/"]'
    ERROR_MESSAGE = ".error-message"
    FLASH_MESSAGE = ".flash"

    def assert_login_loaded(self) -> None:
        """Assert the login page is loaded."""
        self.assert_url_contains("/login")

    def fill_email(self, email: str) -> None:
        """Fill the email input."""
        self.fill(self.EMAIL_INPUT, email)

    def fill_password(self, password: str) -> None:
        """Fill the password input."""
        self.fill(self.PASSWORD_INPUT, password)

    def submit(self) -> None:
        """Click the login submit button."""
        self.click(self.SUBMIT_BUTTON)

    def login(self, email: str, password: str) -> None:
        """Perform full login flow."""
        self.fill_email(email)
        self.fill_password(password)
        self.submit()

    def click_register(self) -> None:
        """Click the register link."""
        self.click(self.REGISTER_LINK)

    def click_home(self) -> None:
        """Click the home link."""
        self.click(self.HOME_LINK)

    def get_error_message(self) -> str:
        """Get error message if displayed."""
        if self.is_visible(self.ERROR_MESSAGE):
            return self.get_text(self.ERROR_MESSAGE)
        return ""

    def get_flash_message(self) -> str:
        """Get flash message if displayed."""
        if self.is_visible(self.FLASH_MESSAGE):
            return self.get_text(self.FLASH_MESSAGE)
        return ""

    def assert_login_success(self) -> None:
        """Assert login was successful (redirects away from login page)."""
        self.page.wait_for_url("**/login", timeout=1000)
        # If still on login page, login failed
        current_url = self.page.url
        assert "/login" not in current_url, "Login did not succeed - still on login page"

    def assert_invalid_credentials(self) -> None:
        """Assert invalid credentials error is shown."""
        error = self.get_error_message() or self.get_flash_message()
        assert error, "Expected error message for invalid credentials"
