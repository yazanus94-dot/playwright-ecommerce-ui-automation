"""Register Page Object."""

from tests.pages.base_page import BasePage


class RegisterPage(BasePage):
    """Register page of the e-commerce application."""

    # Selectors
    NAME_INPUT = 'input[name="name"]'
    EMAIL_INPUT = 'input[name="email"]'
    PASSWORD_INPUT = 'input[name="password"]'
    CONFIRM_PASSWORD_INPUT = 'input[name="confirm_password"]'
    SUBMIT_BUTTON = 'button[type="submit"]'
    LOGIN_LINK = 'a[href="/login"]'
    HOME_LINK = 'a[href="/"]'
    ERROR_MESSAGE = ".error"
    FLASH_MESSAGE = ".flash"

    def assert_register_loaded(self) -> None:
        """Assert the register page is loaded."""
        self.assert_url_contains("/register")

    def fill_name(self, name: str) -> None:
        """Fill the name input."""
        self.fill(self.NAME_INPUT, name)

    def fill_email(self, email: str) -> None:
        """Fill the email input."""
        self.fill(self.EMAIL_INPUT, email)

    def fill_password(self, password: str) -> None:
        """Fill the password input."""
        self.fill(self.PASSWORD_INPUT, password)

    def fill_confirm_password(self, password: str) -> None:
        """Fill the confirm password input."""
        self.fill(self.CONFIRM_PASSWORD_INPUT, password)

    def submit(self) -> None:
        """Click the register submit button."""
        self.click(self.SUBMIT_BUTTON)

    def register(self, name: str, email: str, password: str) -> None:
        """Perform full registration flow."""
        self.fill_name(name)
        self.fill_email(email)
        self.fill_password(password)
        self.fill_confirm_password(password)
        self.submit()

    def click_login(self) -> None:
        """Click the login link."""
        self.click(self.LOGIN_LINK)

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

    def assert_registration_success(self) -> None:
        """Assert registration was successful (redirects away from register page)."""
        current_url = self.page.url
        assert "/register" not in current_url, "Registration did not succeed - still on register page"

    def assert_duplicate_email_error(self) -> None:
        """Assert duplicate email error is shown."""
        error = self.get_error_message() or self.get_flash_message()
        assert error, "Expected error message for duplicate email registration"
