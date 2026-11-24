"""Authentication Tests - ShopEase E-Commerce UI Automation."""

import pytest
from tests.pages.login_page import LoginPage
from tests.pages.register_page import RegisterPage

pytestmark = pytest.mark.critical


class TestLoginPage:
    """Login page test scenarios."""

    def test_login_page_loads(self, login_page):
        """TC-AUTH-001: Login page should load with email and password fields."""
        login_page.navigate()
        login_page.assert_login_loaded()
        login_page.assert_element_visible('input[name="email"]')
        login_page.assert_element_visible('input[name="password"]')

    def test_successful_login(self, login_page, home_page, test_user):
        """TC-AUTH-002: Valid credentials should log user in successfully."""
        login_page.navigate()
        login_page.login(test_user["email"], test_user["password"])
        login_page.page.wait_for_timeout(1000)
        # Should redirect to home on success
        assert "/login" not in login_page.page.url

    def test_invalid_login_shows_error(self, login_page):
        """TC-AUTH-003: Invalid credentials should show error message."""
        login_page.navigate()
        login_page.login("wrong@example.com", "wrongpassword")
        login_page.page.wait_for_timeout(1000)
        login_page.assert_invalid_credentials()

    def test_empty_login_fields_shows_validation(self, login_page):
        """TC-AUTH-004: Empty required fields should show HTML5 validation."""
        login_page.navigate()
        login_page.page.click('button[type="submit"]')
        login_page.page.wait_for_timeout(500)
        email_input = login_page.page.locator('input[name="email"]')
        assert email_input.evaluate("(el) => el.willValidate")

    def test_login_link_from_nav(self, login_page, home_page):
        """TC-AUTH-005: Login link in nav should navigate to login page."""
        home_page.navigate()
        home_page.click_login()
        login_page.assert_login_loaded()


class TestRegisterPage:
    """Registration page test scenarios."""

    def test_register_page_loads(self, register_page):
        """TC-AUTH-006: Register page should load with all required fields."""
        register_page.navigate()
        register_page.assert_register_loaded()

    def test_successful_registration(self, register_page, home_page, test_user):
        """TC-AUTH-007: Valid registration should create account and log in."""
        register_page.navigate()
        register_page.register(test_user["name"], test_user["email"], test_user["password"])
        register_page.page.wait_for_timeout(1000)
        assert "/register" not in register_page.page.url

    def test_duplicate_email_shows_error(self, register_page, test_user):
        """TC-AUTH-008: Registering with existing email should show error."""
        # First register
        register_page.navigate()
        register_page.register(test_user["name"], test_user["email"], test_user["password"])
        register_page.page.wait_for_timeout(1000)
        # Try again with same email
        register_page.navigate()
        register_page.register(test_user["name"], test_user["email"], test_user["password"])
        register_page.page.wait_for_timeout(1000)
        register_page.assert_duplicate_email_error()

    def test_register_link_to_login(self, register_page, login_page):
        """TC-AUTH-009: Register page login link should navigate to login."""
        register_page.navigate()
        register_page.click_login()
        login_page.assert_login_loaded()
