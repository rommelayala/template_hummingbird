# lib/pages/login_page.py

from playwright.sync_api import Page
from lib.config import BASE_URL


class LoginPage:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.username_input = page.locator("#user-name")
        self.password_input = page.locator("#password")
        self.login_button = page.locator("#login-button")
        self.error_message = page.locator("h3[data-test='error']")

    def goto(self) -> None:
        self.page.goto(BASE_URL)
        # Asegurarnos de que el DOM está listo
        self.page.wait_for_load_state("domcontentloaded")

    def login(self, username: str, password: str) -> None:
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()

    def get_error_text(self) -> str:
        return self.error_message.inner_text()
