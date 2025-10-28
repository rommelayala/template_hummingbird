import re
import sys
from playwright.sync_api import Page, expect, Playwright, sync_playwright
sys.path.append("..")
from lib.config_variables import ConfigVariables
variables = ConfigVariables()

def test_homepage_contains_veepee_accueil_text(page: Page):
    # go to the homepage
    page.goto(variables.vp_fr_url)
    # expect the title has Veepee -Accueil text
    expect(page).to_have_title(re.compile("Veepee - Accueil"))


def test_homepage_check_homepage_main_banner(page: Page):
    # go to the homepage
    page.goto(variables.vp_fr_url)
    # expect the title has Veepee -Accueil text
    main_banner = page.locator('#default')
    expect(main_banner).to_be_visible()


def run(playwright):
    browser = playwright.chromium.launch(
         headless=False,
        # slow_mo = 1000
    )
    with browser.new_context() as context:
        page = context.new_page()
        page.mouse.move(100, 100)
        test_homepage_contains_veepee_accueil_text(page=page)
        test_homepage_check_homepage_main_banner(page=page)

    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
