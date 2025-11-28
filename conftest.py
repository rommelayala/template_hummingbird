# conftest.py
from typing import Generator
import os

import pytest
import allure
from playwright.sync_api import Playwright, sync_playwright, Browser, BrowserContext, Page


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
