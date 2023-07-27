import logging
import logging
import sys
import time

from lib.master_test import run_type
from lib.utilities import configure_criticality_error_link_dead

sys.path.append("../../tests")
from lib.config_variables import ConfigVariables
from playwright.sync_api import Page, Playwright, TimeoutError as PlaywrightTimeoutError
from playwright._impl._api_types import Error as PlaywrightError

logging.basicConfig(level=logging.DEBUG)
variables = ConfigVariables()

def test_login_preprod(page: Page):
    # ----------------------------------------------------------------
    # Login
    page.goto(variables.vp_sites_map["DEBUG"]["vp_site_root_url"])
    time.sleep(2)
    page.get_by_role("button", name="Autoriser tous les cookies").click()
    page.get_by_role("button", name="S'identifier").click()
    page.get_by_role("button", name="Se connecter").nth(1).click()
    page.locator("input[id='username']").is_visible()
    page.locator("input[id='username']").click()
    page.locator("input[id='username']").fill("automation.software.20@gmail.com")
    page.locator("input[id='current-password']").is_visible()
    page.locator("input[id='current-password']").click()
    page.locator("input[id='current-password']").fill("VQRw7G9Zk6ZTas9!")
    page.locator("button[id='loginBt']").click()
    # End Login
    time.sleep(1)
    page.get_by_role("button", name="Voir toutes les ventes").click()
    page.keyboard.down('End')
    time.sleep(1)
    page.keyboard.press('Control+Home')
    page.locator("section[id^='bannermodule']").click()
    page.keyboard.down('End')
    time.sleep(1)
    page.keyboard.press('Control+Home')
    page.locator("section[id^='all-new']").click()
    page.keyboard.down('End')
    time.sleep(1)
    page.keyboard.press('Control+Home')
    page.locator("section[id^='highlight-event']").click()
    page.keyboard.down('End')
    time.sleep(1)
    page.keyboard.press('Control+Home')
    page.locator("section[id^='all-sales']").click()
    page.keyboard.down('End')
    time.sleep(1)
    page.keyboard.press('Control+Home')
    page.locator("section[id^='soon']").click()
    page.keyboard.down('End')
    time.sleep(1)
    page.keyboard.press('Control+Home')
    page.get_by_text("InstagramFacebookYoutubeNos applicationsiOSAndroid").click()
    # ----------------------------------------------------------------


def login_accept_cookies(context, key_country):
    logging.debug("# Login # ")
    pages = len(context.pages)

    if pages == 0:
        page = context.new_page()
        page.goto(variables.vp_sites_map[key_country]["vp_site_root_url"])
        page.set_viewport_size({"width": 1654, "height": 1079})
        # ----------------------------------------------------------------
        time.sleep(2)
        logging.debug("# Go to https://www.veepee.fr")
        logging.debug("Authorise cookies")
        # Click text=Autoriser tous les cookies
        if page.locator("text=Autoriser tous les cookies").is_visible():
            page.locator("text=Autoriser tous les cookies").click()
        # page.locator("#onetrust-banner-sdk").click()
        time.sleep(2)
        logging.debug("# Login Process")
        page.locator("button:has-text(\"S'identifier\")").click()
        with page.expect_navigation():
            page.locator("button:has-text(\"Se connecter\")").nth(1).click()
        # Click input[name="email"]
        page.locator("input[name=\"email\"]").click()
        # Fill input[name="email"]
        page.locator("input[name=\"email\"]").fill(
            variables.vp_sites_map[key_country]['user']
        )
        # Click input[name="password"]
        page.locator("input[name=\"password\"]").click()
        # Fill input[name="password"]
        page.locator("input[name=\"password\"]").fill(
            variables.vp_sites_map[key_country]['pass']
        )
        with page.expect_navigation():
            page.locator("button:has-text(\"Se connecter\")").click()
        logging.debug("End Login Process")
        # ----------------------------------------------------------------
    elif pages == 1 and ('gr/portal' in getattr(context.pages[0], "url")):
        page = context.pages[0]
        # Click input[name="email"]
        page.locator("input[name=\"email\"]").click()
        # Fill input[name="email"]
        page.locator("input[name=\"email\"]").fill(
            variables.vp_sites_map[key_country]['user']
        )
        # Click input[name="password"]
        page.locator("input[name=\"password\"]").click()
        # Fill input[name="password"]
        page.locator("input[name=\"password\"]").fill(
            variables.vp_sites_map[key_country]['pass']
        )
        page.locator("button:has-text(\"Se connecter\")").click()
        logging.debug("End Login Process in gr/portal")
        time.sleep(2)
    else:
        raise Exception(f"Too many pages are open in the browser {pages}")

    logged_in = True
    return page


def test_links_execption_travel_check_campaign_link_is_not_dead(playwright: Playwright):
    error = 0
    success = 0
    country = variables.vp_sites_map['FR']['country']
    url_page_before_click = "https://www.veepee.fr/gr/home/travel"
    is_banner_dark = False
    is_logged = False
    browser = playwright.chromium.launch(
        headless=False,
        # slow_mo = 1000
    )
    context = browser.new_context()
    page = context.new_page()
    page.set_viewport_size({"width": 1654, "height": 1079})
    page.goto(url_page_before_click)

    urls_browser = [
        "https://www.veepee.fr/experiences/crb-monabanq6/?vpas=vpCkhkZmFiM2VkYzI0OTdjM2QwY2ZiYmMyOGYyOGYxODg3MzRkNWRiODg1OTdiZTYwOGZkMDViYmI4MDkyZmM4MzhiMGQ1MjEzNzMSGDY0NjM5YWQxNTY1MDg2MDAxZTlhMTE5MRoYNjQ2MzlhZDE1NjUwODYwMDFlOWExMTk0Ihg2NDYzOWFkMTU2NTA4NjAwMWU5YTExOTMo7_SE5YQxMgg2MDUwMTg2NTgBQAJIAFABWgMxMTFgAHIHNDQyeDE4MoIBDUNSQl9NT05BQkFOUTY",
        "https://www.veepee.fr/gr/catalog/845280",
        "https://www.veepee.fr/gr/catalog/rec36",
        "https://www.veepee.fr/gr/catalog/bpt4273",
        "https://www.veepee.fr/web/catalog/v1/sale/851913/redirect",
        "https://privalia.perfectstay.com/it-IT?source=VPV_SDP8",
        "https://tinyurl.com/26chvc6x?vpas=vpCkhlOTM5OTg1NGJkYThkYTUwNTc1ZjAyODY4ODlhM2E0MDkzOGQ4MDczYThiOTM0ODBkNDIzN2I2ZjRhZGQ1NjA1MWQwOGMxODYSGDY0NjIyNGYyZTU0YzA1MDAxZDFiYTkwMhoYNjQ2MjI0ZjJlNTRjMDUwMDFkMWJhOTA1Ihg2NDYyMjRmMmU1NGMwNTAwMWQxYmE5MDQo7tu2zIQxMgItMTgBQAJIAFABWgMxMTBgAHIHNDQyeDE4MoIBC0NSQl9PVUlHTzI1",
        "https://www.ouigo.com/content/ouigo-train-classique?utm_source=veepee&utm_medium=display&utm_campaign=1_an_train_classique&utm_term=&utm_content=carte_rose_hp&utm_date=05_2023&utm_od=&utm_axe=&utm_phase=reveal",
        "https://it.soshape.com/discount/VP20?redirect=/pages/partnership/?&utm_source=veepee&utm_medium=paid&utm_campaign=display-052023",
        "https://coccinelle.com/it/hellospring/?src=veepee20&vpas=vpCkg4MGRhYTdkZDIxZTViZWNlZmU4YTUxNjQxZDE1M2NjZTZhZGYyNzQ5NjA3NGQzMDhhOGUxNTMyN2E3OTNlN2UxOTJlYmVjM2USGDY0NGI4Zjg3ZTU0YzA1MDAxZDFiYTcxNhoYNjQ0YjhmODdlNTRjMDUwMDFkMWJhNzE5Ihg2NDRiOGY4N2U1NGMwNTAwMWQxYmE3MTgo8oSNwv0wMgg4ODM1NzMxOTgFQAJIAFABWgMxMTJgAHIHNDQyeDE4MoIBDVBCX0NPQ0NJTkVMMzU",
        "https://tinyurl.com/yck3v52c?vpas=vpCkg2ZmNhODQzNDAxYTQzMjRmNWVkOTZjZWU1MzFhZGI0NGI0ZjA3ZjMxYWZkMGQwYzFiY2I2YzM0MDk2ZTYxZWE5NjUxZmExMWUSGDY0MmU3ZWE0NTY1MDg2MDAxZTlhMGNkZBoYNjQyZTdlYTQ1NjUwODYwMDFlOWEwY2UwIhg2NDJlN2VhNDU2NTA4NjAwMWU5YTBjZGYo9ejV0_kwMggxMjY5Mzg1MDgBQAJIAFABWgMxMTBgAHIHNDQyeDE4MoIBCUNSQl9KRUVQMw",
        "https://clarins.commander1.com/c3/?tcs=835&chn=partnerships&src=veepee&ctry=bnl&type=ue_ecom&cmp=beauty-days&med=fr&perf_pub=veepee&perf_c=&perf_v=&perf_f=fr&url=https%3A%2F%2Fbnl.clarins.com%2Ffr%2Fveepee%2F%3Futm_source%3Dveepee&utm_medium=partnerships&utm_campaign=beauty-days&utm_term=fr&vpas=vpCkg3N2IzNGRjMTAyMDAzM2JiZTU0MjY1NTUyN2U5Njg3YWY5MTA2Zjg5M2UyM2YxYjcxYWMwNjcyZjA4ZGNhNzdiZDhmMmRjODcSGDY0MzY5ZTYwZTU0YzA1MDAxZDFiYTUwYRoYNjQzNjllNjBlNTRjMDUwMDFkMWJhNTBkIhg2NDM2OWU2MGU1NGMwNTAwMWQxYmE1MGMo-ufC3PcwMgItMTgRQAJIAFABWgMxMTFgAHIHNDQyeDE4MoIBDFBCX0NMQVJJTlM1OA",
        "https://www.veepee.fr/gr/home/travel",
        "https://www.veepee.fr/gr/home/default",
        "/web/catalog/v1/sale/851126/redirect",
        "may_tu_may",
        ""
    ]
    for url in urls_browser:
        try:
            href_url = ""
            url_browser = ""
            href_url = url
            operation_code = '123'
            operation_id = 'lolo'
            if is_banner_dark:
                logging.debug(
                    f'SKIPPING Url "{href_url}" operation-code "{operation_code}"  operation-id "{operation_id}"')
            else:
                url_page_after_click = href_url
                logging.debug('----------------------------------------------------------------------------')
                logging.debug(f"values pages must be 1 at this point {len(context.pages)}")
                # Return the main page travel
                context.pages[0].goto(url_page_before_click)
                # Open a new page with banner url
                with context.new_page() as page_camp:
                    page_camp.goto(
                        url_page_after_click
                    )
                    page_camp.wait_for_selector("body")
                    url_browser = getattr(page_camp, "url")
                    logging.debug(f'Url in the browser is --------> {url_browser}')
                    logging.debug('----------------------------------XXX--------------------------------------')
                    # ----------------------------------------------------------------
                    assert 'gr/home/default' not in url_browser
                    success += 1
                    # ----------------------------------------------------------------
        except AssertionError as e:
            logging.error(f"Redirection to homepage the url in web component is '{href_url}'")
            # Possible values
            # "run_type": "manual"/"scheduled"
            data = {
                "run_type": run_type,
                "status": "FAILED",
                "fail_level": "high",
                "country": country,
                "debug": f"Redirection to homepage the url in web component is '{href_url}'",
                "reason": "Url Redirection to Home page",
                "operation_id": operation_id,
                "operation_code": operation_code,
                "url_campaign_configured_in_href_banner": href_url,
                "url_campaign_result": url_browser,
                "tags": ["FAILED", "travel_check_campaign_link_is_not_dead"],
            }
            logging.debug("--------------------------------")
            data_configured = configure_criticality_error_link_dead(data, href_url, url_browser)
            logging.debug(data_configured)
            logging.exception(e)
            error += 1
        except PlaywrightTimeoutError as e:
            logging.error("PLAYWRIGHT TIMEOUT ERROR")
            # Possible values
            # "run_type": "manual"/"scheduled"
            data = {
                "run_type": run_type,
                "status": "FAILED",
                "fail_level": "high",
                "country": country,
                "debug": f"PLAYWRIGHT TIMEOUT ERROR, opening campaign in url '{href_url}' take more that 30 seconds",
                "reason": "Timeout 30s",
                "operation_id": operation_id,
                "operation_code": operation_code,
                "url_campaign_configured_in_href_banner": href_url,
                "url_campaign_result": url_browser,
                "tags": ["FAILED", "travel_check_campaign_link_is_not_dead"]
            }
            logging.debug("--------------------------------")
            data_configured = configure_criticality_error_link_dead(data, href_url, url_browser)
            logging.debug(data_configured)
            logging.exception(e)
            error += 1
        except TimeoutError as e:
            logging.error("TIMEOUT ERROR")
            # Possible values
            # "run_type": "manual"/"scheduled"
            data = {
                "run_type": run_type,
                "status": "FAILED",
                "fail_level": "high",
                "country": country,
                "debug": f"TIMEOUT ERROR, opening campaign in url '{href_url}' take more that 30 seconds",
                "reason": "Timeout 30s",
                "operation_id": operation_id,
                "operation_code": operation_code,
                "url_campaign_configured_in_href_banner": href_url,
                "url_campaign_result": url_browser,
                "tags": ["FAILED", "travel_check_campaign_link_is_not_dead"]
            }
            logging.debug("--------------------------------")
            data_configured = configure_criticality_error_link_dead(data, href_url, url_browser)
            logging.debug(data_configured)
            logging.exception(e)
            error += 1
        except Exception as e:
            # Possible values
            # "run_type": "manual"/"scheduled"
            data = {
                "run_type": run_type,
                "status": "FAILED",
                "fail_level": "high",
                "country": country,
                "debug": f"there were problem Opening campaign in url '{href_url}'",
                "reason": "Invalid url",
                "operation_id": operation_id,
                "operation_code": operation_code,
                "url_campaign_configured_in_href_banner": href_url,
                "url_campaign_result": url_browser,
                "tags": ["FAILED", "travel_check_campaign_link_is_not_dead"]
            }
            data_configured = configure_criticality_error_link_dead(data, href_url, url_browser)
            logging.debug(data_configured)
            logging.exception(e)
            error += 1


def login_accept_cookies_retry(page, key_country, retry_count=variables.retry):
    try:
        logging.debug(f"# Login {key_country} #")
        if retry_count >= 0:
            logging.debug(f"# Login {key_country} #")
            page.set_viewport_size({"width": 1654, "height": 1079})
            logging.debug(f"# Going to {variables.vp_sites_map[key_country]['vp_site_root_url']}")
            page.goto(
                variables.vp_sites_map[key_country]['vp_site_root_url']
            )
            logging.debug("Authorise cookies")
            if page.locator("button[id^='onetrust-accept']").is_visible():
                page.locator("button[id^='onetrust-accept']").click()
            time.sleep(5)
            page.wait_for_load_state("domcontentloaded")
            logging.debug("# Login Process")
            page.locator("button[class*='styles__Button-groot']").is_visible()
            page.locator("button[class*='styles__Button-groot']").click()
            with page.expect_navigation():
                page.locator("button:has-text(\"Einloggen\")").nth(1).click()
            # Click input[name="email"]
            page.locator("input[name=\"email\"]").click()
            # Fill input[name="email"]
            page.locator("input[name=\"email\"]").fill(
                variables.vp_sites_map[key_country]['user'])
            # Click input[name="password"]
            page.locator("input[name=\"password\"]").click()
            # Fill input[name="password"]
            page.locator("input[name=\"password\"]").fill(variables.vp_sites_map[key_country]['pass'])
            with page.expect_navigation():
                page.locator("button:has-text(\"Einloggen\")").click()
            logging.debug("End Login Process")
            # ----------------------------------------------------------------
        else:
            raise Exception(f"Not possible to Log in retry {variables.retry} times")

    except PlaywrightTimeoutError as e:
        retry_count -= 1
        logging.error(f"PLAYWRIGHT TIMEOUT ERROR countdown retry {retry_count}")
        # testing purposes use only running in local --------------------
        # take_screenshot(page, "login_playwright_timeout")
        login_accept_cookies_retry(page, key_country, retry_count)
    except PlaywrightError as e:
        retry_count -= 1
        logging.error(
            f"PLAYWRIGHT ERROR: Target page, context or browser has been closed countdown retry {retry_count}")
        # testing purposes use only running in local --------------------
        # take_screenshot(page, "login_playwright_timeout")
        login_accept_cookies_retry(page, key_country, retry_count)
    except TimeoutError as e:
        retry_count -= 1
        logging.error(f"TIMEOUT ERROR countdown retry {retry_count}")
        # testing purposes use only running in local --------------------
        # take_screenshot(page, "login_timeout")
        login_accept_cookies_retry(page, key_country, retry_count)
    except Exception as e:
        retry_count -= 1
        logging.error(f"OTHER ERROR countdown retry {retry_count}")
        # testing purposes use only running in local --------------------
        # take_screenshot(page, "login_other_exception")
        logging.error(f"Failed to login XX {e}")

    return page

# def run(playwright: Playwright) -> None:
#     variables = ConfigVariables()
#     browser = playwright.chromium.launch()
#     context = browser.new_context()
#
#     # Open new page
#     page = context.new_page()
#     # Go to https://www.veepee.fr/gr/home/default
#     page.goto(variables.vp_fr_url)
#     # ---------------------
#     test_login(page=page)
#     # ---------------------
#     context.close()
#     browser.close()
#
#
# with sync_playwright() as playwright:
#     run(playwright)
