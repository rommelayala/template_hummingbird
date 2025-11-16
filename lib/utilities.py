import logging
import time
import traceback
from datetime import datetime, timezone
from lib.config_variables import ConfigVariables
import playwright

variables = ConfigVariables()


def take_screenshot(page, source="_need_to_pass_the_source"):
    timestamp = datetime.now()
    str_timestamp = timestamp.strftime("%d-%m-%Y_%H-%M-%S")
    # ----------------------------------------------------------------
    page.screenshot(path=str_timestamp + f"_{source}_.jpg")
    # ----------------------------------------------------------------

def scrolling_down_the_page(page, sleep=0):
    try:
        count = 1
        sections = page.locator("section[class^='styles__Section-groot']").all()

        for section in sections:
            logging.debug(
                f"Scrolling {count}/{len(sections)} section id '{section.get_attribute('id')}' with text '{section.all_inner_texts()}'")
            page.keyboard.press('End')
            page.wait_for_load_state("networkidle")
            time.sleep(sleep)
            button_cookies_visible = page.locator("button[id='onetrust-accept-btn-handler']").is_visible()
            logging.debug(f"# Button Cookies {button_cookies_visible}")
            if button_cookies_visible:
                page.locator("button[id='onetrust-accept-btn-handler']").click()
            page.wait_for_load_state("networkidle")
            page.keyboard.press('Control+Home')
            time.sleep(sleep)
            count += 1

        return page

    except Exception as e:
        logging.error(f"An error occurred while scrolling the page: {str(e)}")
        # Realizar cualquier otro manejo de errores necesario aquí


def get_data_to_test_pictures(g_imgs, key_country):
    count = 0
    data_to_test_pictures = []
    try:
        for img in g_imgs:
            url_src = img.get_attribute('src')
            a_href = img.locator('..').locator('..').locator('..').locator('..')
            # Pending check tagname = article
            pic_data = {
                "index": count,
                "url_src": url_src,
                "data-operation-code": a_href.get_attribute('data-operation-code') if a_href.get_attribute('data-operation-code') else None,
                "data-operation-id": a_href.get_attribute('data-operation-id') if a_href.get_attribute('data-operation-id') else None,
                "country": variables.vp_sites_map[key_country]['country']
            }
            data_to_test_pictures.append(pic_data)
            count += 1
            # logging.debug(f"------------------------------------------  {count} / {len(g_imgs)}")
            # logging.debug(f"url = {pic_data} ")
    except Exception as e:
        logging.debug(f"Exception get_data_to_test_pictures getting data to test pictures: {str(e)}")
    return data_to_test_pictures


def get_data_to_test_home_banners(context, g_banners, key_country):
    count = 0
    data_op_id = None
    data_op_code = None
    data_to_test_redirection_to_home = []
    vp_root_link = variables.vp_sites_map[key_country]['vp_site_root_url']

    try:
        for index, article in enumerate(g_banners):
            data_op_code = article.get_attribute('data-operation-code') if article.get_attribute('data-operation-code') else None
            data_op_id = article.get_attribute('data-operation-id') if article.get_attribute('data-operation-id') else None
            data_facil_iti = article.get_attribute('data-facil-iti') if article.get_attribute('data-facil-iti') else None
            article_html = article.inner_html() if article.inner_html() else None
            href_url = get_href_a_lazy_a(article)
            href_complete_url = complete_href_url_with_vp_root_url(href_url, vp_root_link)
            banner_data = {
                "index": index,
                "href_url": href_complete_url,
                "data-operation-code": data_op_code,
                "data-operation-id": data_op_id,
                "data-facil-iti": data_facil_iti,
                "country": variables.vp_sites_map[key_country]['country'],
                "component": article_html
            }
            data_to_test_redirection_to_home.append(banner_data)
            # logging.debug(f"------------------------------------------  {count} / {len(g_imgs)}")
            # logging.debug(f"url = {pic_data} ")
    except Exception as e:
        logging.debug(f"{e.__class__.__name__}Exception get_data_to_test_pictures getting data to test pictures: {str(e)}")

    return data_to_test_redirection_to_home


def get_attribute_from_web_element(web_element_a, attribute):
    att_value = ""
    try:
        att_value = web_element_a.get_attribute(attribute) if web_element_a.get_attribute(
            attribute) is not None else "No attibute"
    except AttributeError as e:
        logging.error(f"'{attribute}' in web element is None {e}")
        att_value = ""
    except Exception as e:
        logging.error(e)

    return att_value


def get_attribute_href_web_element(web_element_a):
    href_url = ""
    try:

        href_url = web_element_a.get_attribute('href') if web_element_a.get_attribute(
            'href') is not None else None
        # "No attribute in href in locator a, get_attribute_href_webelement"
        if href_url is not None:
            lazy_web_element_a = web_element_a.locator("div[class*='lazyload']>div>a")
            href_url = lazy_web_element_a.get_attribute('href') if lazy_web_element_a.get_attribute('href') is not None else None

    except AttributeError as e:
        logging.error(f"href in web element is None {e}")
        href_url = ""
    except Exception as e:
        logging.error(e)

    return href_url


def get_operation_code(campaign, context):
    data_operation_code = None
    try:
        with context.new_page() as new_page:
            new_page.wait_for_load_state("domcontentloaded")
            if campaign is None:
                return data_operation_code
            else:
                data_operation_code = campaign.get_attribute('data-operation-code')
                return data_operation_code
    except Exception as e:
        logging.error(f"Error getting get_operation_code {e}")


def get_operation_id(web_element_article, context):
    operation_id = None
    try:
        with context.new_page() as new_page:
            new_page.wait_for_load_state("domcontentloaded")
            if web_element_article is None:
                return operation_id
            elif web_element_article.get_attribute('data-operation-id') is None:
                return operation_id
            else:
                return web_element_article.get_attribute('data-operation-id')
    except Exception as e:
        logging.error(f"Error getting get_operation_id {e}")


def complete_href_url_with_vp_root_url(href_url, vp_root_link):
    href_url_banner = None
    try:
        if href_url is None:
            return href_url_banner
        elif len(href_url) > 2 and href_url != "":
            if href_url.startswith('/gr/catalog') or href_url.startswith('/web'):
                logging.debug(f"adding vp_root_link to href_url {href_url}")
                href_url_banner = vp_root_link + href_url
            elif href_url.startswith('https://'):
                href_url_banner = href_url
        else:
            logging.error("adding vp_root_link to href_url has failed")

        return href_url_banner
    except Exception as e:
        logging.error(f"complete_href_url_with_vp_root_url An error occurred: {str(e)}\n"
                      f"--------------------------------\n"
                      f"{e.__traceback__}")


def configure_criticality_error_link_dead(data, href_url, url_browser):
    try:
        if href_url.startswith('https://'):
            href_url = href_url.replace('https://', '')
            if '//' in href_url:
                data["reason"] = "double // found in the campaign url"
                data["fail_level"] = "low"
            elif 'home' in url_browser:
                data["reason"] = "Redirection to homepage"
                data["fail_level"] = "high"
    except Exception as e:
        logging.error(e)

    return data


def print_report_execution_in_console(start_time):
    end_time = datetime.now()
    logging.debug("--------------------XXX--------------------------")
    logging.debug('Elapsed time: {}'.format(end_time - start_time))
    logging.debug("--------------------XXX--------------------------")


def print_report_execution_error_success_in_console(name_function, start_time, error=0, success=0, skipped=0):
    """
    This function generates a report of the execution of a given function and prints it in the console.

    Parameters:
    name_function (str): The name of the function whose execution report is being generated.
    start_time (datetime): The timestamp when the function execution started.
    error (int): The number of errors that occurred during the function execution.
    success (int): The number of successful executions of the function.

    Returns:
    None

    Example Usage:
    start_time = datetime.now()
    # call some function here
    print_report_execution_in_console('my_function', start_time, 2, 8)

    Output:
    ----------X my_function X-------------
    Elapsed time: 0:00:10.123456
    Errors: 2
    Success: 8
    ----------XXX-------------
    """
    end_time = datetime.now()
    Elapsed = end_time - start_time
    print(f"XX----------  {name_function}  -------------XX")
    print('Elapsed time: {}'.format(Elapsed))
    print(f"Errors: {error}")
    print(f"Success: {success}")
    print(f"Skipped: {skipped}")
    print("--------------------XXX--------------------------")
    return end_time - start_time


def check_if_url_in_exceptions(href_url):
    result = False
    try:

        url_exceptions = variables.url_exceptions
        for exception in url_exceptions:
            if exception in href_url:
                result = True
    except Exception as e:
        logging.debug(f"Exception in check_if_url_in_exceptions {str(e)}")

    return result


def start_save_trace(context):
    # Start tracing before creating / navigating a page.
    context.tracing.start(screenshots=True, snapshots=True, sources=True)


def stop_and_save_trace(context, country, timestamp):
    # Stop tracing and export it into a zip archive.
    # playwright show-trace xxxx_yyyy_zzzz.zip
    adjustName = timestamp.replace("+", "_")
    name_file = "Trace_" + country + "-" + adjustName + ".zip"
    context.tracing.stop(path=name_file)
    # page_camp.on("_XXX_", lambda request: print(request.url + " " + request.failure.error_text))
    logging.debug(f"trace saved in {name_file}")


def campaign_banner_is_in_soon_section(campaign):
    is_in_soon_section = False
    try:
        if campaign.get_attribute('data-facil-iti') is not None and '-dark' in campaign.get_attribute('data-facil-iti'):
            is_in_soon_section = True
    except Exception as e:
        logging.error(f"{e.__class__.__name__}")

    return is_in_soon_section


def check_if_url_in_home_exceptions(href_url):
    result = False
    try:
        if href_url is not None:
            url_h_exceptions = variables.url_home_exceptions
            for exception in url_h_exceptions:
                if exception in href_url:
                    result = True
                    break

    except Exception as e:
        logging.error(f"{e.__class__.__name__}\n"
                      f"{str(e)}")

    return result


def get_h_operation_code(campaign, context):
    data_operation_code = None
    try:
        with context.new_page() as new_page:
            new_page.wait_for_load_state("domcontentloaded")
            if campaign is None:
                return data_operation_code
            else:
                data_operation_code = campaign.get_attribute('data-operation-code')
                return data_operation_code
    except Exception as e:
        logging.error(f"Error getting get_operation_code {e}")


def get_h_operation_id(web_element_article, context):
    operation_id = None
    try:
        with context.new_page() as new_page:
            new_page.wait_for_load_state("domcontentloaded")
            if web_element_article is None:
                return operation_id
            elif web_element_article.get_attribute('data-operation-id') is None:
                return operation_id
            else:
                return web_element_article.get_attribute('data-operation-id')
    except Exception as e:
        logging.error(f"Error getting get_operation_id {e}")
