# tests/test_login.py

from playwright.sync_api import Page
from lib.config import VALID_USERNAME, VALID_PASSWORD
from lib.pages.login_page import LoginPage


def test_login_correcto_redirige_a_inventory(page: Page) -> None:
    login_page = LoginPage(page)

    login_page.goto()
    login_page.login(VALID_USERNAME, VALID_PASSWORD)

    # Comprobamos que hemos ido a la página de inventario
    page.wait_for_load_state("domcontentloaded")
    assert "inventory.html" in page.url
    assert page.get_by_text("Products").is_visible()


def test_login_incorrecto_muestra_mensaje_error(page: Page) -> None:
    login_page = LoginPage(page)

    login_page.goto()
    login_page.login("usuario_incorrecto", "password_incorrecto")

    error_text = login_page.get_error_text()
    assert "Epic sadface" in error_text
