# tests/test_login.py

import allure
from playwright.sync_api import Page
from lib.config import VALID_USERNAME, VALID_PASSWORD
from lib.pages.login_page import LoginPage


@allure.feature("Autenticación")
@allure.story("Login exitoso")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("Verificar que un login correcto redirige a la página de inventario")
@allure.description("""
Este test verifica que cuando un usuario se autentica con credenciales válidas,
el sistema lo redirige correctamente a la página de inventario de productos.
""")
def test_login_correcto_redirige_a_inventory(page: Page) -> None:
    with allure.step("Inicializar la página de login"):
        login_page = LoginPage(page)

    with allure.step("Navegar a la URL de login"):
        login_page.goto()
        
    with allure.step(f"Ingresar credenciales válidas (usuario: {VALID_USERNAME})"):
        login_page.login(VALID_USERNAME, VALID_PASSWORD)

    with allure.step("Verificar redirección a página de inventario"):
        # Comprobamos que hemos ido a la página de inventario
        page.wait_for_load_state("domcontentloaded")
        assert "inventory.html" in page.url, f"Expected 'inventory.html' in URL, got: {page.url}"
        
    with allure.step("Verificar que el título 'Products' es visible"):
        assert page.get_by_text("Products").is_visible(), "Products header not visible"


@allure.feature("Autenticación")
@allure.story("Login con credenciales inválidas")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("Verificar que credenciales incorrectas muestran mensaje de error")
@allure.description("""
Este test verifica que cuando un usuario intenta autenticarse con credenciales incorrectas,
el sistema muestra un mensaje de error apropiado sin permitir el acceso.
""")
def test_login_incorrecto_muestra_mensaje_error(page: Page) -> None:
    with allure.step("Inicializar la página de login"):
        login_page = LoginPage(page)

    with allure.step("Navegar a la URL de login"):
        login_page.goto()
        
    with allure.step("Ingresar credenciales inválidas"):
        login_page.login("usuario_incorrecto", "password_incorrecto")

    with allure.step("Verificar que aparece mensaje de error"):
        error_text = login_page.get_error_text()
        assert "Epic sadface" in error_text, f"Expected error message with 'Epic sadface', got: {error_text}"
        allure.attach(error_text, name="Error message", attachment_type=allure.attachment_type.TEXT)
