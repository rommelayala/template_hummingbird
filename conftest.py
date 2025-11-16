# conftest.py
from typing import Generator

import pytest
from playwright.sync_api import Playwright, sync_playwright, Browser, BrowserContext, Page


@pytest.fixture(scope="session")
def playwright_instance() -> Generator[Playwright, None, None]:
    """Inicia Playwright una vez por sesión de tests."""
    with sync_playwright() as p:
        yield p# conftest.py
from typing import Generator

import pytest
from playwright.sync_api import Playwright, sync_playwright, Browser, BrowserContext, Page


@pytest.fixture(scope="session")
def playwright_instance() -> Generator[Playwright, None, None]:
    """Inicia Playwright una vez por sesión de tests."""
    with sync_playwright() as p:
        yield p


@pytest.fixture(scope="session")
def browser(playwright_instance: Playwright) -> Generator[Browser, None, None]:
    """Lanza un navegador Chromium una vez por sesión."""
    browser = playwright_instance.chromium.launch(headless=False)
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



@pytest.fixture(scope="session")
def browser(playwright_instance: Playwright) -> Generator[Browser, None, None]:
    """Lanza un navegador Chromium una vez por sesión."""
    browser = playwright_instance.chromium.launch(headless=False)
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
