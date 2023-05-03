import sys
sys.path.append(".")
from lib.config_variables import ConfigVariables
from playwright.sync_api import Page, Playwright, sync_playwright


def test_login(page: Page):
    # Click text=Autoriser tous les cookies
    page.locator("text=Autoriser tous les cookies").click()

    # Click button:has-text("S'identifier")
    page.locator("button:has-text(\"S'identifier\")").click()

    # Click button:has-text("Se connecter") >> nth=1
    # with page.expect_navigation(url="https://www.veepee.fr/gr/authentication?opendoor=true"):
    with page.expect_navigation():
        page.locator("button:has-text(\"Se connecter\")").nth(1).click()
    # assert page.url == "https://www.veepee.fr/gr/authentication?opendoor=true"

    # Click input[name="email"]
    page.locator("input[name=\"email\"]").click()

    # Fill input[name="email"]
    page.locator("input[name=\"email\"]").fill(
        "automation.software.20@gmail.com")

    # Click input[name="password"]
    page.locator("input[name=\"password\"]").click()

    # Fill input[name="password"]
    page.locator("input[name=\"password\"]").fill("VQRw7G9Zk6ZTas9!")

    # Click button:has-text("Se connecter")
    # with page.expect_navigation(url="https://www.veepee.fr/gr/home"):
    with page.expect_navigation():
        page.locator("button:has-text(\"Se connecter\")").click()

    # Click section:has-text("ÇA VA VOUS PLAIRECoup de foudre inévitable")
    page.locator(
        "section:has-text(\"ÇA VA VOUS PLAIRECoup de foudre inévitable\")").click()

    # Click text=ÇA VA VOUS PLAIRE
    page.locator("text=ÇA VA VOUS PLAIRE").click()

    # Click text=C'EST TOUT NOUVEAU
    page.locator("text=C'EST TOUT NOUVEAU").click()

    # Click h2:has-text("THE PLACE")
    page.locator("h2:has-text(\"THE PLACE\")").click()

    # Click text=De quoi sauter sur l'occasion
    page.locator("text=De quoi sauter sur l'occasion").click()

    # Click text=UN PEU DE PATIENCE..
    page.locator("text=UN PEU DE PATIENCE..").click()

    # Click .sc-ynJRL
    page.locator(".sc-ynJRL").click()

    # Click div:has-text("Aide & ContactQui sommes-nous ? Nos engagements RSEMentions légalesLivraisonLes ") >> nth=3
    page.locator(
        "div:has-text(\"Aide & ContactQui sommes-nous ? Nos engagements RSEMentions légalesLivraisonLes \")").nth(3).click()


def run(playwright: Playwright) -> None:
    variables = ConfigVariables()
    browser = playwright.chromium.launch()
    context = browser.new_context()

    # Open new page
    page = context.new_page()
    # Go to https://www.veepee.fr/gr/home/default
    page.goto(variables.vp_fr_url)
    # ---------------------
    test_login(page=page)
    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
