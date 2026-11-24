"""Pytest configuration and fixtures for the Playwright automation framework."""

import os
import pytest

from config.settings import BASE_URL, TIMEOUT


@pytest.fixture
def test_user():
    """Test user credentials fixture."""
    return {
        "email": os.getenv("TEST_USER_EMAIL", "test@example.com"),
        "password": os.getenv("TEST_USER_PASSWORD", "TestPass123!"),
        "name": os.getenv("TEST_USER_NAME", "Test User"),
    }


@pytest.fixture
def home_page(page):
    """Home page object fixture."""
    from tests.pages.home_page import HomePage
    return HomePage(page)


@pytest.fixture
def product_page(page):
    """Product detail page object fixture."""
    from tests.pages.product_page import ProductPage
    return ProductPage(page)


@pytest.fixture
def cart_page(page):
    """Cart page object fixture."""
    from tests.pages.cart_page import CartPage
    return CartPage(page)


@pytest.fixture
def checkout_page(page):
    """Checkout page object fixture."""
    from tests.pages.checkout_page import CheckoutPage
    return CheckoutPage(page)


@pytest.fixture
def order_confirmation_page(page):
    """Order confirmation page object fixture."""
    from tests.pages.order_confirmation_page import OrderConfirmationPage
    return OrderConfirmationPage(page)


@pytest.fixture
def login_page(page):
    """Login page object fixture."""
    from tests.pages.login_page import LoginPage
    return LoginPage(page)


@pytest.fixture
def register_page(page):
    """Register page object fixture."""
    from tests.pages.register_page import RegisterPage
    return RegisterPage(page)


@pytest.fixture
def orders_page(page):
    """Order history page object fixture."""
    from tests.pages.orders_page import OrdersPage
    return OrdersPage(page)
