"""Configuration settings for the Playwright automation framework."""

import os
from dotenv import load_dotenv

load_dotenv()

# Base URL of the application under test
BASE_URL = os.getenv("BASE_URL", "http://localhost:5000")

# Default timeout in milliseconds
TIMEOUT = int(os.getenv("TIMEOUT", "30000"))

# Default browser
BROWSER = os.getenv("BROWSER", "chromium")

# Headless mode
HEADLESS = os.getenv("HEADLESS", "true").lower() == "true"

# Screenshot and video settings
SCREENSHOT_ON_FAILURE = True
VIDEO_ON_FAILURE = True

# Test credentials
TEST_USER_EMAIL = os.getenv("TEST_USER_EMAIL", "test@example.com")
TEST_USER_PASSWORD = os.getenv("TEST_USER_PASSWORD", "TestPass123!")
TEST_USER_NAME = os.getenv("TEST_USER_NAME", "Test User")

# Allure results directory
ALLURE_RESULTS_DIR = os.getenv("ALLURE_RESULTS_DIR", "tests/reports/allure-results")
