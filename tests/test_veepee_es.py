import logging
import time
import sys
import traceback
from playwright.async_api import expect
from playwright.sync_api import Page, Playwright, sync_playwright, BrowserContext
from datetime import datetime, timezone
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

sys.path.append(".")
from lib.config_variables import ConfigVariables
from lib.utilities import *
from integrations.elastic import log_json_to_foundatoin_elastic

logging.basicConfig(level=logging.DEBUG)
variables = ConfigVariables()


def test_homepage_check_campaigns_es(context: BrowserContext):
    logging.debug("# Open new page")
    page = context.new_page()
    page.set_viewport_size({"width": 1654, "height": 1079})
    logging.debug("# Go to https://www.veepee.es")
    page.goto(variables.vp_es_url)
    logging.debug("# ------Authorise cookies")
    page.locator("text=Aceptar todo").click()
    # page.locator("#onetrust-banner-sdk").click()
    time.sleep(2)
    logging.debug("# Login Process")
    print("Login process..")
    page.locator("button:has-text(\"Identificarme\")").click()

    with page.expect_navigation():
        page.locator("button:has-text(\"Conectarme\")").nth(1).click()
    # Click input[name="email"]
    page.locator("input[name=\"email\"]").click()

    # Fill input[name="email"]
    page.locator("input[name=\"email\"]").fill(
        "automation.vp.es@gmail.com")

    # Click input[name="password"]
    page.locator("input[name=\"password\"]").click()

    # Fill input[name="password"]
    page.locator("input[name=\"password\"]").fill("@Ut0mati0n.es")

    with page.expect_navigation():
        page.locator("button:has-text(\"Conectarme\")").click()
    logging.debug("# End Login Process")
    logging.debug("Scrolling page to get all banners")

    page.locator(
        "section:has-text(\"MARCAS TOP\")").click()
    page.keyboard.down('End')
    time.sleep(1)

    page.locator("text=NOVEDADES").click()
    page.keyboard.down('End')
    time.sleep(1)

    page.locator("text=MÁS ARTÍCULOS").click()
    page.keyboard.down('End')
    time.sleep(1)

    page.locator("h2:has-text(\"AHORA\")").click()
    page.keyboard.down('End')
    time.sleep(1)

    page.locator("text=ÚLTIMAS HORAS").click()
    page.keyboard.down('End')
    time.sleep(1)

    page.locator("text=PRÓXIMAMENTE").click()
    page.keyboard.down('End')
    time.sleep(1)
    logging.debug("End Scrolling page")
    logging.debug("Getting all WebElements...")
    pictures = page.query_selector_all("picture[class*='navigation']")
    logging.debug("Getting all Webelements banners")
    campaigns_catalogs = [
        page.get_by_role('article').all(),
    ]

    # ------ Launching tests
    logging.debug("Launching check_campaign_link_is_not_dead_es")
    check_campaign_link_is_not_dead_es(context, campaigns_catalogs)
    logging.debug("Launching check_picture_images_in_campaigns_es")
    # todo: comment/uncomment to work
    check_picture_images_in_campaigns_es(context, pictures)


def check_campaign_link_is_not_dead_es(context, campaigns_catalogs):
    error = 0
    success = 0
    vp_root_link = variables.vp_sites_map['ES']['vp_site_root_url']
    start_time_before_all_checks = datetime.now()
    for campaigns_catalog in campaigns_catalogs:
        for campaign in campaigns_catalog:
            try:
                href_url = ""
                url_browser = ""
                web_element_a = campaign.locator('..')
                href_url = ger_attributr_href_webelement(web_element_a)
                # pass href_url from bew element to complete the url if url do not start with
                # href_url_completed = complete_href_url_with_vp_root_url(href_url, vp_root_link)
                operation_code = get_operation_code(campaign)
                operation_id = get_operation_id(campaign)
                # logging.debug(f"href: {href_url} ,operation_code: {operation_code} , operation_id: {operation_id}")
                if (
                        href_url == ""
                        or "/web/catalog/v1/sale/" in href_url
                        or "bit.ly" in href_url
                        or "club.veepee.es" in href_url
                        or "ad.doubleclick.net" in href_url
                        or "clarins.commander" in href_url
                        or "experiences" in href_url

                ):
                    logging.debug(f'SKIPPING Url "{href_url}"')
                    # you are able to check web element that is skipped
                    # logging.debug(f'SKIPPING Url {href_url} in component {web_element_a.inner_html()}')

                else:
                    with context.new_page() as page_camp:
                        start_time_check_campaign = datetime.now(timezone.utc).isoformat()
                        logging.debug(f"going to ----> {href_url}")
                        page_camp.goto(
                            href_url
                            #    ,timeout=5000
                        )
                        page_camp.wait_for_selector("body")
                        url_browser = getattr(page_camp, "url")
                        logging.debug('----------------------------------------------------------------------------')
                        logging.debug(f'Url in the browser is --------> {url_browser}')
                        logging.debug(f'Url the href_url is ----------> {href_url}')
                        logging.debug('----------------------------------XXX--------------------------------------')
                        # ----------------------------------------------------------------
                        assert url_browser == href_url
                        # ----------------------------------------------------------------
                        # print_report_execution_error_success_in_console(start_time_check_campaign)
                        success += 1
            except PlaywrightTimeoutError as e:
                logging.error("PLAYWRIGHT TIMEOUT ERROR")
                timestamp = datetime.now(timezone.utc).isoformat()
                data = {
                    "status": "FAILED",
                    "fail_level": "high",
                    "timestamp": timestamp,
                    "country": variables.vp_sites_map['ES']['country'],
                    "reason": "PLAYWRIGHT TIMEOUT ERROR",
                    "operation_id": operation_id,
                    "url_campaign_configured in href banner": href_url,
                    "url_campaign_expected": href_url,
                    "url_campaign_result": url_browser,
                    "tags": ["FAILED", "check_campaign_link_is_not_dead"],
                    "component": web_element_a.inner_html()
                }
                logging.debug("--------------------------------")
                data_configured = configure_criticality_error_link_dead(data, href_url, url_browser)
                logging.debug(data_configured)
                # Inject into Elastic
                # todo: comment/uncomment to work
                log_json_to_foundatoin_elastic(data_configured=data_configured)
                # page_camp.screenshot(path=timestamp)
                logging.exception(e)
            except TimeoutError as e:
                logging.error("TIMEOUT ERROR")
                timestamp = datetime.now(timezone.utc).isoformat()
                data = {
                    "status": "FAILED",
                    "fail_level": "high",
                    "timestamp": timestamp,
                    "country": variables.vp_sites_map['ES']['country'],
                    "reason": "TIMEOUT ERROR",
                    "operation_id": operation_id,
                    "url_campaign_configured in href banner": href_url,
                    "url_campaign_expected": href_url,
                    "url_campaign_result": url_browser,
                    "tags": ["FAILED", "check_campaign_link_is_not_dead"],
                    "component": web_element_a.inner_html()
                }
                logging.debug("--------------------------------")
                data_configured = configure_criticality_error_link_dead(data, href_url, url_browser)
                logging.debug(data_configured)
                # Inject into Elastic
                # todo: comment/uncomment to work
                log_json_to_foundatoin_elastic(data_configured=data_configured)
                # page_camp.screenshot(path=timestamp)
                logging.exception(e)

            except Exception as e:
                timestamp = datetime.now(timezone.utc).isoformat()
                data = {
                    "status": "FAILED",
                    "fail_level": "default",
                    "timestamp": timestamp,
                    "country": variables.vp_sites_map['ES']['country'],
                    "reason": "Campaign URL mismatch",
                    "operation_id": operation_id,
                    "url_campaign_configured in href banner": href_url,
                    "url_campaign_expected": href_url,
                    "url_campaign_result": url_browser,
                    "tags": ["FAILED", "check_campaign_link_is_not_dead"],
                    "component": web_element_a.inner_html()
                }
                # print("")
                # print("configuring FAILED...")
                data_configured = configure_criticality_error_link_dead(data, href_url, url_browser)
                # print(data_configured)
                # Inject into Elastic
                # todo: comment/uncomment to work
                log_json_to_foundatoin_elastic(data_configured=data_configured)
                logging.exception(e)
                error += 1
            finally:
                if 'page_camp' in locals():
                    page_camp.close()

    print_report_execution_error_success_in_console("check_campaign_link_is_not_dead_es", start_time_before_all_checks,
                                                    error, success)


def check_picture_images_in_campaigns_es(context, pictures):
    error = 0
    success = 0
    start_time = datetime.now()

    for picture in pictures:
        sources = picture.query_selector_all('source')
        for source in sources:
            try:
                srcset = source.get_attribute('srcset')
                url_img_srcset = srcset.split()[0]
                with context.new_page() as page_camp:
                    page_camp.goto(url_img_srcset)
                    page_camp.wait_for_selector("img")
                    page_camp.wait_for_selector("img").is_visible()
                    timestamp = datetime.now(timezone.utc).isoformat()

                    data = {
                        "status": "OK",
                        "timestamp": timestamp,
                        "country": variables.vp_sites_map['ES']['country'],
                        "reason": "URL in banner is OK srcset",
                        "url_image_expected": url_img_srcset,
                        "url_image_result": getattr(page_camp, "url"),
                        "tags": ["Ok", "check_picture_images_in_campaigns_es"]
                    }
                    # Inject into Elastic
                    # log_json_to_foundatoin_elastic(data=data)
                    # print in console
                    # logging.debug(f"check_picture_images_in_campaigns OK, Json LOG is {data}")
                    success += 1
            except Exception as e:

                timestamp = datetime.now(timezone.utc).isoformat()
                data = {
                    "status": "FAILED",
                    "timestamp": timestamp,
                    "country": variables.vp_sites_map['ES']['country'],
                    "reason": f"URL in banner expected and result does not match",
                    "url_image_expected": url_img_srcset,
                    "url_image_result": getattr(page_camp, "url"),
                    "tags": ["Failed", "check_picture_images_in_campaigns_es"]
                }
                # Inject into Elastic
                # todo: comment/uncomment to work
                log_json_to_foundatoin_elastic(data=data)
                # print in console
                logging.error(f"check_picture_images_in_campaigns FAILED, Json LOG is {data}")
                logging.error(traceback.format_exc(e))
                error += 1

    print_report_execution_error_success_in_console("check_picture_images_in_campaigns", start_time, error, success)


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(
        # headless=False
    )
    start_time = datetime.now()
    with browser.new_context() as context:
        # ---------------------
        test_homepage_check_campaigns_es(context=context)
        # ---------------------

    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
