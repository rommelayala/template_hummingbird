import os
import sys

from playwright.sync_api import BrowserContext

sys.path.append(".")
from lib.utilities import *
from playwright.sync_api import sync_playwright
from lib.master_test import master_check_picture_images_in_articles, master_home_page_banners_link_redirect_to_home_page_v2
from lib.login.veepee_priv_es_login import robust_home_login_accept_cookies
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright._impl._api_types import Error as PlaywrightError
from integrations.elastic import log_json_to_foundation_elastic

logging.basicConfig(level=logging.DEBUG)
variables = ConfigVariables()
retry_count = variables.retry
run_type = os.getenv('RUN_TYPE')


def test_home_page_check_campaigns(context: BrowserContext, local_retry_count=retry_count):
    if local_retry_count >= 0:
        try:
            with context.new_page() as new_page:
                page, logging_in = robust_home_login_accept_cookies(new_page)
                time.sleep(1)
                if page.locator("button[id^='onetrust-accept']").is_visible():
                    page.locator("button[id^='onetrust-accept']").click()
                # ----------------------------------------------------------------
                logging.debug("Scrolling page to get all banners")
                page = scrolling_down_the_page(page, 2.5)
                # ----------------------------------------------------------------
                page.wait_for_load_state("networkidle")
                logging.debug("Getting all Webelements banners")
                # ----------------------------------------------------------------
                g_imgs = page.locator("img[alt='banner']").all()
                data_to_test_pictures = get_data_to_test_pictures(g_imgs, "PRIVALIA-ES")
                g_banners = page.query_selector_all('article')
                data_to_test_banners = get_data_to_test_home_banners(context, g_banners, "PRIVALIA-ES")
                # ------ Launching tests
                logging.debug("Launching check_campaign_link_is_not_dead_privalia")
                banners_to_retest = master_home_page_banners_link_redirect_to_home_page_v2(context, data_to_test_banners, "PRIVALIA-ES")
                if len(banners_to_retest) > 0:
                    if local_retry_count >= 0:
                        logging.debug("Relaunching failed banner")
                        master_home_page_banners_link_redirect_to_home_page_v2(context, banners_to_retest, "PRIVALIA-ES")
                    local_retry_count -= 1
                logging.debug("Launching check_picture_images_in_campaigns")
                master_check_picture_images_in_articles(data_to_test_pictures, "PRIVALIA-ES", "home_page")
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
                "country": variables.vp_sites_map['PRIVALIA-ES']['country'],
                "debug": f"PLAYWRIGHT TIMEOUT ERROR Collecting banners"
                         f"---{e}--- traceBack {traceback.print_tb(e.__traceback__)}",
                "reason": "MANUAL ACTION IS NEEDED, Hummingbird had problems collecting elements",
                "tags": ["FAILED", "test_homepage_check_campaigns"]
            }
            logging.debug("--------------------------------")
            logging.debug(f"{e}")
            # Inject into Elastic
            log_json_to_foundation_elastic(data)
            # ----------------------------------------------------------------
            test_home_page_check_campaigns(context, local_retry_count)
        except PlaywrightError as e:
            logging.error(f"PLAYWRIGHT ERROR BEFORE EXECUTING TEST countdown retry {local_retry_count}/{variables.retry}")
            local_retry_count -= 1
            timestamp = datetime.now(timezone.utc).isoformat()
            data = {
                "run_type": run_type,
                "status": "FAILED",
                "fail_level": "high",
                "timestamp": timestamp,
                "country": variables.vp_sites_map['PRIVALIA-ES']['country'],
                "debug": f"PLAYWRIGHT ERROR Collecting banners"
                         f"---{e}--- traceBack {traceback.print_tb(e.__traceback__)}",
                "reason": "MANUAL ACTION IS NEEDED, Hummingbird had problems collecting elements",
                "tags": ["FAILED", "test_homepage_check_campaigns"]
            }
            logging.debug("--------------------------------")
            logging.debug(f"{e}")
            # Inject into Elastic
            log_json_to_foundation_elastic(data)
            # ----------------------------------------------------------------
            test_home_page_check_campaigns(context, local_retry_count)
        except Exception as e:
            logging.error(f"ERROR BEFORE EXECUTING TEST countdown retry {local_retry_count}/{variables.retry}")
            local_retry_count -= 1
            timestamp = datetime.now(timezone.utc).isoformat()
            data = {
                "run_type": run_type,
                "status": "FAILED",
                "fail_level": "high",
                "timestamp": timestamp,
                "country": variables.vp_sites_map['PRIVALIA-ES']['country'],
                "debug": f"Exception, ERROR BEFORE Collecting banners"
                         f"---{e}--- traceBack {traceback.print_tb(e.__traceback__)}",
                "reason": "MANUAL ACTION IS NEEDED, Hummingbird had problems collecting elements",
                "tags": ["FAILED", "test_homepage_check_campaigns"]
            }
            logging.debug("--------------------------------")
            logging.error(f"{e}")
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
        test_home_page_check_campaigns(context=context)
        # ---------------------
    context.close()
    browser.close()
