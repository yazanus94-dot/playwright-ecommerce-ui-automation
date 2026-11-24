# ShopEase - Professional Python + Playwright UI Automation Framework

A professional, production-ready UI automation framework for e-commerce web applications, built with Python, Playwright, pytest, and Allure reporting. Designed as a portfolio project for QA Automation Engineers / SDETs.

## 🚀 Features

- **Page Object Model (POM)** - Clean separation of test logic and page selectors
- **40+ Test Scenarios** - Comprehensive coverage across home, product, cart, checkout, auth, order history, and end-to-end flows
- **Multi-Browser Support** - Chromium, Firefox, and WebKit
- **Test Reports** - pytest-html + Allure reports with screenshots, videos, and traces
- **Parallel Execution** - pytest-xdist support for faster test runs
- **Docker & Docker Compose** - Containerized test execution
- **GitHub Actions CI** - Matrix browser testing on every push/PR
- **Failure Artifacts** - Automatic screenshots, videos, and traces on test failure

## 📁 Project Structure

```
playwright-ecommerce-ui-automation/
├── app/                          # Flask demo e-commerce application
│   ├── main.py                   # Flask application entry point
│   ├── static/
│   │   ├── css/style.css
│   │   └── js/app.js
│   └── templates/                # HTML templates (12 pages)
├── config/                       # Framework configuration
│   └── settings.py
├── tests/
│   ├── pages/                    # Page Object Model classes
│   │   ├── base_page.py
│   │   ├── home_page.py
│   │   ├── product_page.py
│   │   ├── cart_page.py
│   │   ├── checkout_page.py
│   │   ├── order_confirmation_page.py
│   │   ├── login_page.py
│   │   ├── register_page.py
│   │   ├── orders_page.py
│   │   └── __init__.py
│   ├── conftest.py               # Pytest fixtures
│   ├── test_home_page.py         # Home page tests (12 scenarios)
│   ├── test_product_page.py      # Product page tests (8 scenarios)
│   ├── test_cart_page.py         # Cart page tests (7 scenarios)
│   ├── test_checkout_page.py     # Checkout tests (5 scenarios)
│   ├── test_auth_page.py         # Authentication tests (9 scenarios)
│   ├── test_orders_page.py       # Order history tests (3 scenarios)
│   ├── test_e2e_flow.py          # End-to-end flow tests (6 scenarios)
│   ├── data/                     # Test data
│   ├── fixtures/                 # Test fixtures
│   └── reports/                  # Test reports (pytest-html, Allure, screenshots, videos)
├── .github/workflows/
│   └── ci.yml                    # GitHub Actions CI pipeline
├── requirements.txt              # Python dependencies
├── Dockerfile                    # Docker image definition
├── docker-compose.yml            # Docker Compose configuration
├── pytest.ini                    # Pytest configuration
├── .env.example                  # Environment variables template
├── .gitignore                    # Git ignore rules
└── README.md                     # This file
```

## 🧪 Test Coverage

| Test File | Scenarios | Marker |
|-----------|-----------|--------|
| `test_home_page.py` | 12 | smoke |
| `test_product_page.py` | 8 | regression |
| `test_cart_page.py` | 7 | regression |
| `test_checkout_page.py` | 5 | critical |
| `test_auth_page.py` | 9 | critical |
| `test_orders_page.py` | 3 | regression |
| `test_e2e_flow.py` | 6 | critical |
| **Total** | **50+** | |

## 🛠️ Prerequisites

- Python 3.11+
- Chrome/Chromium, Firefox, or WebKit browsers (managed by Playwright)
- Docker and Docker Compose (optional, for containerized execution)

## 📦 Installation

### Local Development

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/playwright-ecommerce-ui-automation.git
cd playwright-ecommerce-ui-automation

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
python -m playwright install chromium firefox webkit

# Copy environment variables
cp .env.example .env
# Edit .env with your configuration
```

### Docker

```bash
# Build and run with Docker Compose
docker-compose up --build

# Run tests in Docker
docker-compose run tests pytest tests/ --browser=chromium --headless
```

## ▶️ Running Tests

### Local Execution

```bash
# Start the Flask application (in a separate terminal)
python app/main.py

# Run all tests with Chromium
pytest tests/ --browser=chromium --headless

# Run specific test file
pytest tests/test_home_page.py --browser=chromium --headless

# Run smoke tests only
pytest tests/ -m smoke --browser=chromium --headless

# Run critical tests only
pytest tests/ -m critical --browser=chromium --headless

# Run with Allure reporting
pytest tests/ --browser=chromium --headless --alluredir=tests/reports/allure-results
allure serve tests/reports/allure-results

# Run in parallel (requires pytest-xdist)
pytest tests/ -n auto --browser=chromium --headless
```

### Docker Execution

```bash
# Run tests in Docker container
docker-compose run --rm tests pytest tests/ --browser=chromium --headless

# Run specific browser matrix
docker-compose run --rm tests pytest tests/ --browser=firefox --headless
docker-compose run --rm tests pytest tests/ --browser=webkit --headless
```

## 📊 Reporting

### pytest-html
Reports are generated at `tests/reports/pytest-report.html` with `--self-contained-html`.

### Allure
```bash
# Generate Allure report
allure generate tests/reports/allure-results -o tests/reports/allure-report --clean

# Serve Allure report
allure serve tests/reports/allure-results
```

### Screenshots & Videos
On test failure, screenshots are saved to `tests/reports/screenshots/` and videos to `tests/reports/videos/`. Both are attached to Allure reports.

## 🔄 CI/CD (GitHub Actions)

The `.github/workflows/ci.yml` runs tests on every push and pull request across three browsers:

- **Chromium**
- **Firefox**
- **WebKit**

The workflow:
1. Checks out code
2. Sets up Python 3.11
3. Installs system dependencies for browser automation
4. Installs Python dependencies
5. Installs Playwright browsers
6. Starts the Flask application
7. Runs Playwright tests
8. Uploads test reports, screenshots, and videos as artifacts

## 🔧 Configuration

Edit `.env` or set environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `BASE_URL` | `http://localhost:5000` | Application under test URL |
| `TIMEOUT` | `30000` | Default timeout in milliseconds |
| `BROWSER` | `chromium` | Default browser |
| `HEADLESS` | `true` | Run browser in headless mode |
| `TEST_USER_EMAIL` | `test@example.com` | Test user email |
| `TEST_USER_PASSWORD` | `TestPass123!` | Test user password |
| `TEST_USER_NAME` | `Test User` | Test user name |

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👤 Author

**Ali Essam** - [https://github.com/dragonked2/alphacode](https://github.com/dragonked2/alphacode)

## 🙏 Acknowledgments

- [Playwright](https://playwright.dev/) - Browser automation
- [pytest](https://docs.pytest.org/) - Test framework
- [Allure](https://allure.qatools.ru/) - Test reporting
- [Flask](https://flask.palletsprojects.com/) - Demo application backend
