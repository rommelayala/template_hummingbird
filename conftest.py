# conftest.py
from typing import Generator
import os

import pytest
import allure
from playwright.sync_api import Playwright, sync_playwright, Browser, BrowserContext, Page


# ============================================================================
# COMMAND LINE OPTIONS (Maven-like)
# ============================================================================

def pytest_addoption(parser):
    """Add custom command line options."""
    parser.addoption(
        "--env",
        action="store",
        default="DEV",
        help="Environment to run tests against: DEV, QA, STAG, PP"
    )


@pytest.fixture(scope="session")
def environment(request):
    """Get environment from command line."""
    return request.config.getoption("--env")


# ============================================================================
# BDD TAG TO MARKER CONVERSION
# ============================================================================

def pytest_bdd_apply_tag(tag, function):
    """
    Convert Gherkin tags to pytest markers automatically.
    
    This hook is called by pytest-bdd for each @tag in .feature files.
    It applies the tag as a pytest marker so you can filter with -m.
    
    Example:
        Feature file has: @smoke @critical
        You can run: pytest -m smoke
    """
    # Remove @ if present
    marker_name = tag.lstrip('@')
    
    # Apply marker to the test function
    if hasattr(function, 'pytestmark'):
        function.pytestmark.append(pytest.mark.__getattr__(marker_name))
    else:
        function.pytestmark = [pytest.mark.__getattr__(marker_name)]
    
    return True


# ============================================================================
# PLAYWRIGHT FIXTURES
# ============================================================================

@pytest.fixture(scope="session")
def playwright_instance() -> Generator[Playwright, None, None]:
    """Inicia Playwright una vez por sesión de tests."""
    with sync_playwright() as p:
        yield p


@pytest.fixture(scope="session")
def browser(playwright_instance: Playwright) -> Generator[Browser, None, None]:
    headless_env = os.getenv("HEADLESS", "true").lower() == "true"
    browser = playwright_instance.chromium.launch(headless=headless_env)
    yield browser
    browser.close()


@pytest.fixture
def context(browser: Browser) -> Generator[BrowserContext, None, None]:
    """Crea un contexto nuevo por test (aislamiento de cookies, storage, etc.)."""
    context = browser.new_context(
        user_agent="template-hummingbird-playwright-tests"
    )
    yield context
    context.close()


@pytest.fixture
def page(context: BrowserContext) -> Generator[Page, None, None]:
    """Crea una nueva pestaña (Page) por test."""
    page = context.new_page()
    yield page
    page.close()


# ============================================================================
# ALLURE SCREENSHOT ON FAILURE
# ============================================================================

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook para capturar screenshots en caso de fallo y adjuntarlos a Allure."""
    outcome = yield
    report = outcome.get_result()
    
    if report.when == "call" and report.failed:
        # Intentar capturar screenshot si hay una página disponible
        page = None
        for fixture_name in item.funcargs:
            if fixture_name == "page":
                page = item.funcargs[fixture_name]
                break
        
        if page:
            # Crear directorio para screenshots si no existe
            screenshot_dir = "allure-results/screenshots"
            os.makedirs(screenshot_dir, exist_ok=True)
            
            # Capturar screenshot
            screenshot_path = os.path.join(screenshot_dir, f"{item.name}.png")
            page.screenshot(path=screenshot_path, full_page=True)
            
            # Adjuntar screenshot a Allure
            allure.attach.file(
                screenshot_path,
                name=f"Screenshot - {item.name}",
                attachment_type=allure.attachment_type.PNG
            )
