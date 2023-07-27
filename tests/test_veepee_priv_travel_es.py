import os
import sys

from playwright.sync_api import BrowserContext, TimeoutError as PlaywrightTimeoutError

sys.path.append(".")
from lib.utilities import *
from playwright.sync_api import sync_playwright
from lib.master_test import master_check_picture_images_in_articles, master_travel_check_campaign_link_is_not_dead_v2
from lib.login.veepee_priv_es_login import robust_home_login_accept_cookies

logging.basicConfig(level=logging.DEBUG)
variables = ConfigVariables()
retry_count = variables.retry
run_type = os.getenv('RUN_TYPE')


def test_travel_page_campaigns(context: BrowserContext, local_retry_count=retry_count):
    if local_retry_count >= 0:
        try:

            with context.new_page() as new_page:
                # ----------------------------------------------------------------
                page, logging_in = robust_home_login_accept_cookies(new_page)
                time.sleep(2)
                # ----------------------------------------------------------------
                url = f"{variables.vp_sites_map['PRIVALIA-ES']['vp_site_root_url']}{variables.vp_sites_map['PRIVALIA-ES']['vp_site_travel_top_menu']}"
                page.goto(url)
                # ----------------------------------------------------------------
                logging.debug("Scrolling page to get all banners")
                page = scrolling_down_the_page(page)
                # ----------------------------------------------------------------
                logging.debug("Getting all Webelements banners")
                campaigns_catalogs = [
                    page.get_by_role('article').all(),
                ]
                logging.debug("All article collected")
                g_imgs = page.locator("img[alt='banner']").all()
                logging.debug("All images collected")
                data_to_test_pictures = get_data_to_test_pictures(g_imgs, "PRIVALIA-ES")
                g_banners = page.query_selector_all('article')
                data_to_test_banners = get_data_to_test_home_banners(context, g_banners, "PRIVALIA-ES")
                logging.debug("Launching master_travel_check_campaign_link_is_not_dead_v2")
                banners_to_retest = master_travel_check_campaign_link_is_not_dead_v2(context, data_to_test_banners, "PRIVALIA-ES")
                if len(banners_to_retest) > 0:
                    if local_retry_count >= 0:
                        logging.debug("Relaunching failed banner")
                        master_travel_check_campaign_link_is_not_dead_v2(context, banners_to_retest, "PRIVALIA-ES")
                    local_retry_count -= 1

                # ------ Launching tests
                #if logging_in:
                #    master_travel_check_campaign_link_is_not_dead(context, campaigns_catalogs, "PRIVALIA-ES")
                master_check_picture_images_in_articles(data_to_test_pictures, "PRIVALIA-ES", "travel_page")
                # ------ Logging OUT
                logging_out(page)

        except (PlaywrightTimeoutError, TimeoutError, Exception) as e:
            logging.error(f"{e.__class__.__name__} ")


with sync_playwright() as playwright:
    browser = playwright.chromium.launch(
        # headless=False,
        # slow_mo = 1000
    )
    with browser.new_context(
            user_agent="hummingbird-sales-opening-test-all-veepee-sites"
    ) as context:
        # ---------------------
        test_travel_page_campaigns(context=context)
        # ---------------------
    context.close()
    browser.close()
