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


def test_homepage_check_campaigns(context: BrowserContext):
    logging.debug("# Open new page")
    page = context.new_page()
    page.set_viewport_size({"width": 1654, "height": 1079})
    logging.debug(f"# Going to {variables.vp_sites_map['DE']['vp_site_root_url']}")
    page.goto(
        variables.vp_sites_map['DE']['vp_site_root_url']
    )
    logging.debug("Authorise cookies")

    page.locator("button[id^='onetrust-accept']").click()
    time.sleep(2)
    logging.debug("# Login Process")
    page.locator("button[class*='styles__Button-groot']").is_visible()
    page.locator("button[class*='styles__Button-groot']").click()

    with page.expect_navigation():
        page.locator("button:has-text(\"Einloggen\")").nth(1).click()

    # Click input[name="email"]
    page.locator("input[name=\"email\"]").click()

    # Fill input[name="email"]
    page.locator("input[name=\"email\"]").fill(
        variables.vp_sites_map['DE']['user'])

    # Click input[name="password"]
    page.locator("input[name=\"password\"]").click()

    # Fill input[name="password"]
    page.locator("input[name=\"password\"]").fill(variables.vp_sites_map['DE']['pass'])

    with page.expect_navigation():
        page.locator("button:has-text(\"Einloggen\")").click()
    logging.debug("End Login Process")

    logging.debug("Scrolling page to get all banners")

    page.get_by_role("heading", name="BRANDNEU").click()
    page.keyboard.down('End')
    page.get_by_role("heading", name="JETZT").click()
    page.keyboard.down('End')
    page.get_by_role("heading", name="LETZTE CHANCE").click()
    page.keyboard.down('End')
    page.get_by_role("heading", name="IN KÜRZE").click()
    page.keyboard.down('End')
    page.locator(".sc-hYdjyz").click()
    time.sleep(1)


    logging.debug("End Scrolling page")
    logging.debug("Getting all WebElements...")
    pictures = page.query_selector_all("picture[class*='navigation']")
    logging.debug("Getting all Webelements banners")

    campaigns_catalogs = [
        page.get_by_role('article').all(),
    ]

    # ------ Launching tests
    logging.debug("Launching check_campaign_link_is_not_dead")
    check_campaign_link_is_not_dead(context, campaigns_catalogs)
    logging.debug("Launching check_picture_images_in_campaigns")
    # todo: comment/uncomment to work
    check_picture_images_in_campaigns(context, pictures)


def check_campaign_link_is_not_dead(context, campaigns_catalogs):
    error = 0
    success = 0
    vp_root_link = variables.vp_sites_map['DE']['vp_site_root_url']
    start_time_before_all_checks = datetime.now()
    for campaigns_catalog in campaigns_catalogs:
        for campaign in campaigns_catalog:
            try:
                href_url = ""
                url_browser = ""
                web_element_a = campaign.locator('..')
                #href_url = ger_attributr_href_webelement(web_element_a)
                href_url = complete_href_url_with_vp_root_url(ger_attributr_href_webelement(web_element_a),
                                                              vp_root_link)
                # pass href_url from bew element to complete the url if url do not start with
                # href_url_completed = complete_href_url_with_vp_root_url(href_url, vp_root_link)
                operation_code = get_operation_code(campaign)
                operation_id = get_operation_id(campaign)
                # logging.debug(f"href: {href_url} ,operation_code: {operation_code} , operation_id: {operation_id}")
                if (
                        href_url == ""
                        or "/web/catalog/v1/sale/" in href_url
                        or "bit.ly" in href_url
                        or "ad.doubleclick.net" in href_url
                        or "clarins.commander" in href_url
                        or "experiences" in href_url

                ):
                    logging.debug(f'SKIPPING Url "{href_url}"')
                    # you are able to check web element that is skipped
                    # logging.debug(f'SKIPPING Url {href_url} in component {web_element_a.inner_html()}')

                else:
                    with context.new_page() as page_camp:
                        start_time_check_campaign = datetime.now()
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
                        # print_report_execution_in_console(start_time_check_campaign)
                        success += 1
            except PlaywrightTimeoutError as e:
                logging.error("PLAYWRIGHT TIMEOUT ERROR")
                timestamp = datetime.now(timezone.utc).isoformat()
                data = {
                    "status": "FAILED",
                    "fail_level": "high",
                    "timestamp": timestamp,
                    "country": variables.vp_sites_map['DE']['country'],
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
                    "country": variables.vp_sites_map['DE']['country'],
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
                # todo: confirm json using data form web_element_a.inner_html() if something does not match
                data = {
                    "status": "FAILED",
                    "fail_level": "default",
                    "timestamp": timestamp,
                    "country": variables.vp_sites_map['DE']['country'],
                    "reason": "Campaign URL mismatch",
                    "operation_id": operation_id,
                    "url_campaign_configured in href banner": href_url,
                    "url_campaign_expected": href_url,
                    "url_campaign_result": url_browser,
                    "tags": ["FAILED", "check_campaign_link_is_not_dead"],
                    "component": web_element_a.inner_html()
                }
                # def configure_criticality_error_link_dead(data, href_url, page_camp):
                # print("")
                # print("configuring FAILED...")
                logging.debug("--------------------------------")
                data_configured = configure_criticality_error_link_dead(data, href_url, url_browser)
                logging.debug(data_configured)
                # Inject into Elastic
                # todo: comment/uncomment to work
                log_json_to_foundatoin_elastic(data_configured=data_configured)
                # page_camp.screenshot(path=timestamp)
                logging.exception(e)
                error += 1
            finally:
                if 'page_camp' in locals():
                    page_camp.close()

    print_report_execution_error_success_in_console("check_campaign_link_is_not_dead", start_time_before_all_checks,
                                                    error,
                                                    success)


def check_picture_images_in_campaigns(context, pictures):
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
                    timestamp = datetime.now(timezone.utc).isoformat()
                    page_camp.goto(url_img_srcset)
                    page_camp.wait_for_selector("img")
                    page_camp.wait_for_selector("img").is_visible()
                    url_browser = getattr(page_camp, "url").strip()

                    success += 1
            except Exception as e:
                timestamp = datetime.now(timezone.utc).isoformat()
                data = {
                    "status": "FAILED",
                    "timestamp": timestamp,
                    "country": variables.vp_sites_map['DE']['country'],
                    "reason": f"URL expected in the picture does not match",
                    "url_image_expected": url_img_srcset,
                    "url_image_result": url_browser,
                    "tags": ["Failed", "check_picture_images_in_campaigns"]
                }
                # Inject into Elastic
                log_json_to_foundatoin_elastic(data=data)
                # print in console
                # todo: comment/uncomment to work
                logging.error(f"check_picture_images_in_campaigns FAILED, Json LOG is {data}")
                logging.error(traceback.format_exc(e))
                error += 1

    print_report_execution_error_success_in_console("check_picture_images_in_campaigns", start_time, error, success)


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(
      #  headless=False
    )
    with browser.new_context() as context:
        # ---------------------
        test_homepage_check_campaigns(context=context)
        # ---------------------

    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
