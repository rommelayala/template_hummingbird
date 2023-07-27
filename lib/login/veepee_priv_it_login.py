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
            logging.debug("# Login Priv-Italy #")
            page.set_viewport_size({"width": 1654, "height": 1079})
            logging.debug(f"# Going to {variables.vp_sites_map['PRIVALIA-IT']['vp_site_root_url']}")
            page.goto(
                variables.vp_sites_map['PRIVALIA-IT']['vp_site_root_url']
            )
            # ----------------------------------------------------------------
            page.wait_for_load_state("domcontentloaded")
            time.sleep(2)
            button_login_visible = page.locator("button[class*='styles__Button-groot']").is_visible()
            button_cookies_visible = page.locator("button[id='onetrust-accept-btn-handler']").is_visible()
            logging.debug(f"# Button Login visible {button_login_visible} / Button Cookies {button_cookies_visible}")
            if button_login_visible:
                if page.locator("button[id^='onetrust-accept']").is_visible():
                    page.locator("button[id^='onetrust-accept']").click()
                # page.locator("#onetrust-banner-sdk").click()
                logging.debug("# Login Process")
                page.locator("button:has-text(\"Accedi\")").click()
                with page.expect_navigation():
                    page.locator("button:has-text(\"Fai login\")").nth(1).click()
                # Click input[name="email"]
                page.locator("input[name=\"email\"]").is_visible()
                page.locator("input[name=\"email\"]").click()
                # Fill input[name="email"]
                page.locator("input[name=\"email\"]").is_visible()
                page.locator("input[name=\"email\"]").fill(
                    variables.vp_sites_map['PRIVALIA-IT']['user']
                )
                # Click input[name="password"]
                page.locator("input[name=\"password\"]").is_visible()
                page.locator("input[name=\"password\"]").click()
                # Fill input[name="password"]
                page.locator("input[name=\"password\"]").fill(
                    variables.vp_sites_map['PRIVALIA-IT']['pass']
                )
                with page.expect_navigation():
                    page.locator("button:has-text(\"Entra\")").click()
                logging.debug("End Login Process")
                logged_in = True
            # ----------------------------------------------------------------
        else:
            raise Exception(f"Not possible to Log in retry {variables.retry} times")

    except PlaywrightTimeoutError as e:
        logging.error(f"PLAYWRIGHT TIMEOUT ERROR countdown retry {local_retry_count}/{variables.retry}")
        local_retry_count -= 1
        if page.locator("button[id^='onetrust-accept']").is_visible():
            page.locator("button[id^='onetrust-accept']").click()
        # testing purposes use only running in local --------------------
        take_screenshot(page, "login_prv_it_playwright_timeout")
        robust_home_login_accept_cookies(page, local_retry_count)
    except PlaywrightError as e:
        logging.error(
            f"PLAYWRIGHT ERROR: Target page, context or browser has been closed countdown retry {local_retry_count}/{variables.retry}")
        local_retry_count -= 1
        if page.locator("button[id^='onetrust-accept']").is_visible():
            page.locator("button[id^='onetrust-accept']").click()
        # testing purposes use only running in local --------------------
        take_screenshot(page, "login_prv_it_playwright_timeout")
        robust_home_login_accept_cookies(page, local_retry_count)
    except TimeoutError as e:
        logging.error(f"TIMEOUT ERROR countdown retry {local_retry_count}/{variables.retry}")
        local_retry_count -= 1
        if page.locator("button[id^='onetrust-accept']").is_visible():
            page.locator("button[id^='onetrust-accept']").click()
        # testing purposes use only running in local --------------------
        take_screenshot(page, "login_prv_it_timeout")
        robust_home_login_accept_cookies(page, local_retry_count)
    except Exception as e:
        logging.error(f"OTHER ERROR countdown retry {local_retry_count}/{variables.retry}")
        local_retry_count -= 1
        # testing purposes use only running in local --------------------
        take_screenshot(page, "login_prv_it_other_exception")
        logging.error(f"Failed to login XX {e}")
    return page, logged_in
