import sys

sys.path.append(".")
from lib.utilities import *
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright._impl._api_types import Error as PlaywrightError

logging.basicConfig(level=logging.DEBUG)
variables = ConfigVariables()
retry_count = variables.retry


def robust_home_login_accept_cookies(page, local_retry_count=retry_count):
    logged_in = False
    try:
        if local_retry_count >= 0:
            logging.debug("# Login ES #")
            page.set_viewport_size({"width": 1654, "height": 1079})
            page.goto(
                variables.vp_sites_map['ES']['vp_site_root_url']
            )
            time.sleep(5)
            page.wait_for_load_state("domcontentloaded")
            button_login_visible = page.locator("button:has-text(\"Identificarme\")").is_visible()
            button_cookies_visible = page.locator("button[id='onetrust-accept-btn-handler']").is_visible()
            logging.debug(f"# Button Login visible {button_login_visible} / Button Cookies {button_cookies_visible}")
            if button_login_visible:
                if page.locator("button[id='onetrust-accept-btn-handler']").is_visible():
                    page.locator("button[id='onetrust-accept-btn-handler']").click()
                # page.locator("#onetrust-banner-sdk").click()
                logging.debug("# Login Process")
                page.locator("button:has-text(\"Identificarme\")").click()
                with page.expect_navigation():
                    page.locator("button:has-text(\"Conectarme\")").nth(1).click()
                # Click input[name="email"]
                page.locator("input[name=\"email\"]").is_visible()
                page.locator("input[name=\"email\"]").click()
                # Fill input[name="email"]
                page.locator("input[name=\"email\"]").is_visible()
                page.locator("input[name=\"email\"]").fill(
                    variables.vp_sites_map['ES']['user']
                )
                # Click input[name="password"]
                page.locator("input[name=\"password\"]").is_visible()
                page.locator("input[name=\"password\"]").click()
                # Fill input[name="password"]
                page.locator("input[name=\"password\"]").fill(
                    variables.vp_sites_map['ES']['pass']
                )
                with page.expect_navigation():
                    page.locator("button:has-text(\"Conectarme\")").click()
                logging.debug("End Login Process")
                logged_in = True
            # ----------------------------------------------------------------
        else:
            raise Exception(f"Not possible to Log in retry {variables.retry} times")

    except PlaywrightTimeoutError as e:
        logging.error(f"PLAYWRIGHT TIMEOUT ERROR countdown retry {local_retry_count}/{variables.retry}")
        local_retry_count -= 1
        if page.locator("button[id='onetrust-accept-btn-handler']").is_visible():
            page.locator("button[id='onetrust-accept-btn-handler']").click()
        # testing purposes use only running in local --------------------
        take_screenshot(page, "login_es_playwright_timeout")
        robust_home_login_accept_cookies(page, local_retry_count)
    except PlaywrightError as e:
        logging.error(
            f"PLAYWRIGHT ERROR: Target page, context or browser has been closed countdown retry {local_retry_count}/{variables.retry}")
        local_retry_count -= 1
        if page.locator("button[id='onetrust-accept-btn-handler']").is_visible():
            page.locator("button[id='onetrust-accept-btn-handler']").click()
        # testing purposes use only running in local --------------------
        take_screenshot(page, "login_es_playwright_timeout")
        robust_home_login_accept_cookies(page, local_retry_count)
    except TimeoutError as e:
        logging.error(f"TIMEOUT ERROR countdown retry {local_retry_count}/{variables.retry}")
        local_retry_count -= 1
        if page.locator("button[id='onetrust-accept-btn-handler']").is_visible():
            page.locator("button[id='onetrust-accept-btn-handler']").click()
        # testing purposes use only running in local --------------------
        take_screenshot(page, "login_es_timeout")
        robust_home_login_accept_cookies(page, local_retry_count)
    except Exception as e:
        logging.error(f"OTHER ERROR countdown retry {local_retry_count}/{variables.retry}")
        local_retry_count -= 1
        # testing purposes use only running in local --------------------
        take_screenshot(page, "login_es_other_exception")
        logging.error(f"Failed to login XX {e}")
    return page, logged_in
