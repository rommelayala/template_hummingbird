import os
import sys

from playwright.sync_api import BrowserContext
from playwright.sync_api import sync_playwright

sys.path.append(".")
from lib.utilities import *
from lib.master_test import master_check_picture_images_in_articles, master_travel_check_campaign_link_is_not_dead_v2
from lib.login.veepee_nl_login import robust_home_login_accept_cookies
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright._impl._api_types import Error as PlaywrightError
from integrations.elastic import log_json_to_foundation_elastic

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
                url = f"{variables.vp_sites_map['NL']['vp_site_root_url']}{variables.vp_sites_map['NL']['vp_site_travel_top_menu']}"
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
                data_to_test_pictures = get_data_to_test_pictures(g_imgs, "NL")

                g_banners = page.query_selector_all('article')
                data_to_test_banners = get_data_to_test_home_banners(context, g_banners, "NL")
                # ------ Launching tests
                logging.debug("Launching master_travel_check_campaign_link_is_not_dead_v2")
                banners_to_retest = master_travel_check_campaign_link_is_not_dead_v2(context, data_to_test_banners, "NL")
                if len(banners_to_retest) > 0:
                    if local_retry_count >= 0:
                        logging.debug("Relaunching failed banner")
                        master_travel_check_campaign_link_is_not_dead_v2(context, banners_to_retest, "NL")
                    local_retry_count -= 1

                master_check_picture_images_in_articles(data_to_test_pictures, "NL", "travel_page")
                # ------ Logging OUT
                logging_out(page)
        except PlaywrightTimeoutError as e:
            logging.error(f"PLAYWRIGHT TIMEOUT ERROR BEFORE EXECUTING TEST countdown retry {local_retry_count}/{variables.retry}")
            local_retry_count -= 1
            timestamp = datetime.now(timezone.utc).isoformat()
            data = {
                "run_type": run_type,
                "status": "FAILED",
                "fail_level": "high",
                "timestamp": timestamp,
                "country": variables.vp_sites_map['DE']['country'],
                "debug": f"PLAYWRIGHT TIMEOUT ERROR BEFORE EXECUTING TEST",
                "reason": "MANUAL ACTION IS NEEDED, Hummy had problems collecting elements",
                "tags": ["FAILED", "test_travel_page_campaigns"]
            }
            logging.debug("--------------------------------")
            logging.debug(f"{data} / {e}")
            # Inject into Elastic
            log_json_to_foundation_elastic(data)
            # ----------------------------------------------------------------
            test_travel_page_campaigns(context, local_retry_count)
        except PlaywrightError as e:
            logging.error(f"PLAYWRIGHT ERROR BEFORE EXECUTING TEST countdown retry {local_retry_count}/{variables.retry}")
            local_retry_count -= 1
            timestamp = datetime.now(timezone.utc).isoformat()
            data = {
                "run_type": run_type,
                "status": "FAILED",
                "fail_level": "high",
                "timestamp": timestamp,
                "country": variables.vp_sites_map['DE']['country'],
                "debug": f"PLAYWRIGHT ERROR BEFORE EXECUTING TEST",
                "reason": "MANUAL ACTION IS NEEDED, Hummy had problems collecting elements",
                "tags": ["FAILED", "test_travel_page_campaigns"]
            }
            logging.debug("--------------------------------")
            logging.debug(f"{data} / {e}")
            # Inject into Elastic
            log_json_to_foundation_elastic(data)
            # ----------------------------------------------------------------
            test_travel_page_campaigns(context, local_retry_count)
        except Exception as e:
            logging.error(f"ERROR BEFORE EXECUTING TEST countdown retry {local_retry_count}/{variables.retry}")
            local_retry_count -= 1
            timestamp = datetime.now(timezone.utc).isoformat()
            data = {
                "run_type": run_type,
                "status": "FAILED",
                "fail_level": "high",
                "timestamp": timestamp,
                "country": variables.vp_sites_map['DE']['country'],
                "debug": f"ERROR BEFORE EXECUTING TEST",
                "reason": "MANUAL ACTION IS NEEDED, Hummy had problems collecting elements",
                "tags": ["FAILED", "test_travel_page_campaigns"]
            }
            logging.debug("--------------------------------")
            logging.debug(f"{data} / {e}")
            # Inject into Elastic
            log_json_to_foundation_elastic(data)


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
