import logging
import time
from datetime import datetime, timezone
from lib.config_variables import ConfigVariables

variables = ConfigVariables()


def scrolling_down_the_page(page):
    page.keyboard.down('End')
    time.sleep(1)


def ger_attributr_href_webelement(web_element_a):
    href_url = ""
    try:
        href_url = web_element_a.get_attribute('href') if web_element_a.get_attribute('href') is not None else ""
    except AttributeError as e:
        logging.error(f"href in web element is None {e}")
        href_url = ""
    except Exception as e:
        logging.error(e)

    return href_url


def get_operation_code(web_element_article):
    if web_element_article is None:
        return "no_value"
    else:
        data_operation_code = web_element_article.get_attribute('data-operation-code')
        return data_operation_code


def complete_href_url_with_vp_root_url(href_url, vp_root_link):
    if href_url != "":
        if href_url.startswith('/gr/catalog'):
            logging.debug(f"adding vp_root_link to href_url {complete_href_url_with_vp_root_url}")
            url_campaign = vp_root_link + href_url
            href_url = url_campaign
        # elif href_url.startswith('another_exp'):
        #     url_campaign = vp_root_link + href_url
        #     href_url = url_campaign

    return href_url


def get_operation_id(web_element_article):
    if web_element_article is None:
        return "no_value"
    elif web_element_article.get_attribute('data-operation-id') is None:
        #         operation_id = href_url.split('/')[-1]
        return "no_value"
    else:
        return web_element_article.get_attribute('data-operation-id')


def configure_criticality_error_link_dead(data, href_url, url_browser):
    try:
        if href_url.startswith('https://'):
            href_url = href_url.replace('https://', '')
            if '//' in href_url:
                data["reason"] = "double // is informed in the campaign url"
                data["fail_level"] = "low"
            elif 'home' in url_browser:
                data["reason"] = "Redirection to HOME PAGE"
                data["fail_level"] = "high"
    except Exception as e:
        logging.error(e)

    return data


def print_report_execution_in_console(start_time):
    end_time = datetime.now()
    logging.debug("--------------------XXX--------------------------")
    logging.debug('Elapsed time: {}'.format(end_time - start_time))
    logging.debug("--------------------XXX--------------------------")


def print_report_execution_error_success_in_console(name_function, start_time, error=0, success=0):
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
    print(f"XX----------  {name_function}  -------------XX")
    print('Elapsed time: {}'.format(end_time - start_time))
    print(f"Errors: {error}")
    print(f"Success: {success}")
    print("--------------------XXX--------------------------")


def check_if_url_in_exceptions(href_url):
    result = False
    url_exceptions = variables.url_exceptions
    for exception in url_exceptions:
        if exception in href_url:
            result = True

    return result
