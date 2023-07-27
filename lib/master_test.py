import os
import sys

import requests
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

from integrations.elastic import log_json_to_foundation_elastic

sys.path.append("../tests")
from lib.utilities import *
from lib.exceptions.exceptions import handle_exception

logging.basicConfig(level=logging.DEBUG)
variables = ConfigVariables()
# get variables from system global env (command line)
retry_count = variables.retry
run_type = os.getenv('RUN_TYPE')
banners_failed = []


def master_travel_check_campaign_link_is_not_dead_v2(context, data_to_test_banners, key_country, local_retry_count=retry_count):
    logging.debug("master_travel_check_campaign_link_is_not_dead_v2   ....called")
    error = 0
    success = 0
    skipped = 0
    start_time_before_all_checks = datetime.now()
    country = variables.vp_sites_map[key_country]['country']
    section = "travel"
    if local_retry_count >= 0:
        for banner in data_to_test_banners:
            banner_number = banner.get('index')
            operation_code = banner.get('data-operation-code') if banner.get('data-operation-code') else None
            operation_id = banner.get('data-operation-id') if banner.get('data-operation-id') else None
            href_url = banner.get('href_url') if banner.get('href_url') else None
            is_banners_in_soon_section = banner.get('data-facil-iti').endswith('-dark') if banner.get('data-facil-iti') is not None else False
            component = banner.get('component') if banner.get('component') else None
            url_browser = None
            # if operation_code != "VPV_SP_BBWL216":
            # if operation_id != '849069':
            #    continue
            # if banner_number <= 21:
            #    logging.debug(f'SKIPPING Test for banner {banner_number} / {len(data_to_test_banners)}')
            #    continue
            try:
                if href_url is None:
                    if is_banners_in_soon_section:
                        logging.debug("--------------------------------")
                        logging.debug(
                            f'SKIPPING Empty Url "{href_url}"==None operation-code="{operation_code}" operation-id="{operation_id}" banner-number = "{banner_number}" in soon section = {is_banners_in_soon_section}')
                        skipped += 1

                    else:
                        logging.debug("--------------------------------")
                        logging.debug(
                            f'SKIPPING Empty Url "{href_url}"==None operation-code="{operation_code}" operation-id="{operation_id}" banner-number = "{banner_number}" in soon section = {is_banners_in_soon_section}')
                        skipped += 1
                        timestamp = datetime.now(timezone.utc).isoformat()
                        data = {
                            "run_type": run_type,
                            "status": "FAILED",
                            "fail_level": "high",
                            "timestamp": timestamp,
                            "country": country,
                            "debug": f"URL is None in web element, href_url='{href_url}'"
                                     f"get_href_a_lazy_a(campaign)=> '{href_url}'",
                            "reason": f" href_url = None, Potential Timeout in banner",
                            "operation_id": operation_id,
                            "operation_code": operation_code,
                            "url_campaign_configured_in_href_banner": href_url,
                            "url_campaign_result": url_browser,
                            "error_type": "href_url is None",
                            # ["banner","travel", section]
                            "tags": ["banner", section, "travel_check_campaign_link_is_not_dead"],
                            "component": component
                        }
                        data_configured = configure_criticality_error_link_dead(data, href_url, url_browser)
                        log_json_to_foundation_elastic(data_configured)
                        ################################################################

                else:
                    with context.new_page() as page_banner:
                        timestamp_ini = datetime.now()
                        url_page_href_url = None
                        page_banner.goto(href_url)
                        pages_in_context = len(context.pages) if context.pages else 0

                        last_page = context.pages[-1]
                        last_page.wait_for_load_state("networkidle")

                        url_page_href_url = getattr(last_page, "url")
                        logging.debug(f"------------------------------------------------{banner_number}/{len(data_to_test_banners)}")
                        logging.debug(f"pages {pages_in_context}")
                        logging.debug(f"Url in the browser is --> '{url_page_href_url}'")
                        logging.debug(f"operation_id = '{operation_id}'/ operation_code = '{operation_code}'")
                        logging.debug('---------------------------------XXX---------------------------------XXX')
                        '''
                        if check_if_url_in_home_exceptions(url_page_href_url):
                            skipped += 1
                            logging.debug(f'SKIPPING Url "{url_page_href_url}" operation-code "{operation_code}"  operation-id "{operation_id}"')
                            base_page = context.pages[0]
                            url_base_page = getattr(base_page, 'url')
                            last_page.goto(url_base_page)
                            last_page.wait_for_load_state("domcontentloaded")
                        
                        else:
                            '''
                        assert not url_page_href_url.endswith('/gr/home/travel')
                        success += 1
                        # ----------------------------------------------------------------
                        elapsed_time = (datetime.now() - timestamp_ini).total_seconds()
                        data = {
                            "run_type": run_type,
                            "status": "SUCCESS",
                            "elapsed_time": elapsed_time,
                            "country": country,
                            "error_type": "None",
                            "debug": f"SUCCESS",
                            "reason": f"SUCCESS",
                            "operation_id": operation_id,
                            "operation_code": operation_code,
                            "url_campaign_configured_in_href_banner": href_url,
                            "url_campaign_result": url_browser,
                            "tags": ["banner", section, "travel_check_campaign_link_is_not_dead"],
                            "component": component
                        }
                        log_json_to_foundation_elastic(data)
                        # ----------------------------------------------------------------
                        last_page.go_back()
                        last_page.wait_for_load_state("domcontentloaded")

            except AssertionError as e:
                logging.error(f"AssertionError Redirection to homepage the url in banner '{banner_number}/{len(data_to_test_banners)}'\n"
                              f"operation_id={operation_id}/operation_code={operation_code}")
                timestamp = datetime.now(timezone.utc).isoformat()
                data = {
                    "run_type": run_type,
                    "status": "FAILED",
                    "fail_level": "high",
                    "timestamp": timestamp,
                    "country": country,
                    "error_type": "AssertionError",
                    "debug": f"AssertionError operation_id={operation_id}/operation_code={operation_code}\n"
                             f"---{str(e)}--- ",
                    "reason": f"HOME PAGE Redirection detected is redirecting to Home page operation_id={operation_id}/operation_code={operation_code} ",
                    "operation_id": operation_id,
                    "operation_code": operation_code,
                    "url_campaign_configured_in_href_banner": href_url,
                    "url_campaign_result": url_browser,
                    "tags": ["banner", section],
                    "component": component
                }
                data_configured = configure_criticality_error_link_dead(data, href_url)
                banners_failed.append(data_configured)
                logging.debug("# Inject into Elastic ---------------------")
                logging.debug(data_configured)
                log_json_to_foundation_elastic(data_configured=data_configured)

                logging.debug("--------------------------------")
                logging.exception(e)
                logging.debug("--------------------------------")
                error += 1
                continue
            except (PlaywrightTimeoutError, TimeoutError, Exception) as e:
                logging.debug("--------------------------------")
                logging.error(f"{e.__class__.__name__} in banner '{banner_number}/{len(data_to_test_banners)}'"
                              f"operation_id={operation_id}/operation_code={operation_code}"
                              f" countdown retry {local_retry_count}/{variables.retry}")
                logging.debug("--------------------------------")
                data = handle_exception(e, href_url, url_browser, operation_id, operation_code, country, banner_number, banner, component, section)
                data_configured = configure_criticality_error_link_dead(data, href_url, url_browser)
                log_json_to_foundation_elastic(data_configured=data_configured)
                banners_failed.append(data_configured)
                error += 1
                local_retry_count -= 1
                continue

    print_report_execution_error_success_in_console(f"travel_page_banners_link_redirect_to_home_page - {section}",
                                                    start_time_before_all_checks, error, success, skipped)
    elapsed_time = (datetime.now() - start_time_before_all_checks).total_seconds()
    data_report = {
        "timestamp": start_time_before_all_checks,
        "elapsed_time": elapsed_time,
        "country": country,
        "tags": ["report", "travel", "banner", "home_page_banners_link_redirect_to_home_page"],
        "sales_error": error,
        "sales_success": success,
        "sales_skipped": skipped
    }
    log_json_to_foundation_elastic(data_report)
    return banners_failed


def master_check_picture_images_in_articles(data_to_test_pictures, key_country, section="d_home"):
    error = 0
    success = 0
    count = 0
    total_elements = len(data_to_test_pictures)
    start_time_before_all_checks = datetime.now()
    country = variables.vp_sites_map[key_country]['country']
    for data in data_to_test_pictures:
        count += 1
        # testing purposes ----------------------------------------------------------------
        # if count == variables.number_elements_to_test:
        #    break
        operation_code = data["data-operation-code"]
        operation_id = data["data-operation-id"]
        # Cleaning previous value
        response = ""
        url_src = data["url_src"]
        try:
            logging.debug(f"{section}----------------------------------------{count}/{total_elements}")
            if data["url_src"] != "":
                response = requests.get(url_src, timeout=5)
                response.raise_for_status()
                success += 1
            else:
                url_src = "(empty_url_in_img)"
                raise Exception
            logging.debug('--------------------------XXX-----------------------------XXX')

        except requests.exceptions.HTTPError as e:
            timestamp = datetime.now(timezone.utc).isoformat()
            # Possible values
            # "run_type": "manual"/"scheduled"
            data = {
                "run_type": run_type,
                "status": "FAILED",
                "fail_level": "high",
                "timestamp": timestamp,
                "error_type": "HTTPError",
                "operation_id": operation_id,
                "operation_code": operation_code,
                "country": country,
                "reason": "Image link not reachable",
                "url_source": url_src,
                "debug": f"NOT FOUND picture url request to '{url_src}' country '{country}' operationId ='{operation_id}' "
                         f"opcode = '{operation_code}' element '{count}/{total_elements}'",
                "tags": ["banner", "picture", section, "check_picture_images_in_campaigns"]
            }
            # Inject into Elastic
            log_json_to_foundation_elastic(data)
            # print in console
            logging.error(f"FAILED check_picture_campaigns , Json LOG is {data}")
            logging.error(e)
            error += 1
        except Exception as e:
            timestamp = datetime.now(timezone.utc).isoformat()
            # Possible values
            # "run_type": "manual"/"scheduled"
            data = {
                "run_type": run_type,
                "status": "FAILED",
                "fail_level": "high",
                "timestamp": timestamp,
                "error_type": "Exception",
                "operation_id": operation_id,
                "operation_code": operation_code,
                "country": country,
                "reason": "Image link missing",
                "url_source": url_src,
                "debug": f"An exception | {e} | requesting to '{url_src}' country '{country}' operationId ='{operation_id}' "
                         f"opcode = '{operation_code}' element '{count}/{total_elements}'",
                "tags": ["banner", "picture", section, "check_picture_images_in_campaigns"]
            }
            # Inject into Elastic
            log_json_to_foundation_elastic(data)
            # print in console
            logging.error(f"FAILED check_picture_campaigns , Json LOG is {data}")
            logging.error(e)
            error += 1
            # ----------------------------------------------------------------

    print_report_execution_error_success_in_console(f"check_picture_in_campaigns - {section}",
                                                    start_time_before_all_checks, error, success)
    elapsed_time = (datetime.now() - start_time_before_all_checks).total_seconds()
    data_report = {
        "timestamp": start_time_before_all_checks,
        "elapsed_time": elapsed_time,
        "country": country,
        "tags": ["report", "banner", "picture", section, "check_picture_images_in_campaigns"],
        "sales_error": error,
        "sales_success": success
    }
    log_json_to_foundation_elastic(data_report)


def master_home_page_banners_link_redirect_to_home_page_v2(context, data_to_test_banners, key_country, local_retry_count=retry_count):
    logging.debug("master_home_page_banners_link_not_redirect_to_home_page_v2   ....called")
    error = 0
    success = 0
    skipped = 0
    section = "home_page"
    start_time_before_all_checks = datetime.now()
    country = variables.vp_sites_map[key_country]['country']
    if local_retry_count >= 0:
        for banner in data_to_test_banners:
            href_url = banner.get('href_url') if banner.get('href_url') else None
            banner_number = banner.get('index') if banner.get('index') else 0
            operation_code = banner.get('data-operation-code') if banner.get('data-operation-code') else None
            operation_id = banner.get('data-operation-id') if banner.get('data-operation-id') else None
            is_banners_in_soon_section = banner.get('data-facil-iti').endswith('-dark') if banner.get('data-facil-iti') is not None else False
            component = banner.get('component') if banner.get('component') else None
            url_browser = None
            # if operation_code != "VPV_SP_BBWL216":
            # if operation_id != '849069':
            #    continue
            # if banner_number <= 21:
            #    logging.debug(f'SKIPPING Test for banner {banner_number} / {len(data_to_test_banners)}')
            #    continue
            try:
                if href_url is None:
                    if is_banners_in_soon_section:
                        logging.debug("--------------------------------")
                        logging.debug(
                            f'SKIPPING Empty Url "{href_url}"==None operation-code="{operation_code}" operation-id="{operation_id}" banner-number = "{banner_number}" in soon section = {is_banners_in_soon_section}')
                        skipped += 1

                    else:
                        logging.debug("--------------------------------")
                        logging.debug(
                            f'SKIPPING Empty Url "{href_url}"==None operation-code="{operation_code}" operation-id="{operation_id}" banner-number = "{banner_number}" in soon section = {is_banners_in_soon_section}')
                        skipped += 1
                        ################################################################
                        timestamp = datetime.now(timezone.utc).isoformat()
                        data = {
                            "run_type": run_type,
                            "status": "FAILED",
                            "fail_level": "high",
                            "timestamp": timestamp,
                            "country": country,
                            "debug": f"URL href_url='{href_url}', banner in SOON section = {is_banners_in_soon_section}, banner index = {banner_number}",
                            "reason": f"Potential Timeout in banner, test is skipped because href_url in not present, banner in soon section = {is_banners_in_soon_section}",
                            "operation_id": operation_id,
                            "operation_code": operation_code,
                            "url_campaign_configured_in_href_banner": href_url,
                            "url_campaign_result": url_browser,
                            "error_type": "href_url is None",
                            "tags": ["banner", "home_page_banners_link_redirect_to_home_page", section],
                            "component": component
                        }
                        data_configured = configure_criticality_error_link_dead(data, href_url, url_browser)
                        log_json_to_foundation_elastic(data_configured)
                        ################################################################

                    # if is_banners_in_soon_section is not None and is_banners_in_soon_section.endswith('-dark'):
                    #    logging.debug(f'SKIPPING Test for operation-code "{operation_code}"  operation-id "{operation_id}" Soon section')
                    #    skipped += 1
                    #    continue

                else:
                    with context.new_page() as page_banner:
                        timestamp_ini = datetime.now()
                        url_page_href_url = None
                        page_banner.goto(href_url)
                        pages_in_context = len(context.pages) if context.pages else 0

                        last_page = context.pages[-1]
                        last_page.wait_for_load_state("networkidle")

                        url_page_href_url = getattr(last_page, "url")
                        logging.debug(f"------------------------------------------------{banner_number}/{len(data_to_test_banners)}")
                        logging.debug(f"pages {pages_in_context}")
                        logging.debug(f"Url in the browser is --> '{url_page_href_url}'")
                        logging.debug(f"operation_id = '{operation_id}'/ operation_code = '{operation_code}'")
                        logging.debug('---------------------------------XXX---------------------------------XXX')

                        if check_if_url_in_home_exceptions(url_page_href_url):
                            skipped += 1
                            logging.debug(f'SKIPPING Url "{url_page_href_url}" operation-code "{operation_code}"  operation-id "{operation_id}"')
                            base_page = context.pages[0]
                            url_base_page = getattr(base_page, 'url')
                            last_page.goto(url_base_page)
                            last_page.wait_for_load_state("domcontentloaded")
                        else:
                            # assert '/gr/home' not in url_page_href_url
                            assert not url_page_href_url.endswith('/gr/home')
                            success += 1
                            # ----------------------------------------------------------------
                            elapsed_time = (datetime.now() - timestamp_ini).total_seconds()
                            data = {
                                "run_type": run_type,
                                "status": "SUCCESS",
                                "elapsed_time": elapsed_time,
                                "country": country,
                                "error_type": "None",
                                "debug": f"SUCCESS",
                                "reason": f"SUCCESS",
                                "operation_id": operation_id,
                                "operation_code": operation_code,
                                "url_campaign_configured_in_href_banner": href_url,
                                "url_campaign_result": url_browser,
                                "tags": ["banner", section],
                                "component": component
                            }
                            log_json_to_foundation_elastic(data)
                            # ----------------------------------------------------------------

                            last_page.go_back()
                            last_page.wait_for_load_state("domcontentloaded")

            except AssertionError as e:
                logging.error(f"AssertionError Redirection to homepage the url in banner '{banner_number}/{len(data_to_test_banners)}'\n"
                              f"operation_id={operation_id}/operation_code={operation_code}")
                logging.debug("--------------------------------")
                logging.exception(e)
                logging.debug("--------------------------------")
                timestamp = datetime.now(timezone.utc).isoformat()
                data = {
                    "run_type": run_type,
                    "status": "FAILED",
                    "fail_level": "high",
                    "timestamp": timestamp,
                    "country": country,
                    "debug": f"AssertionError operation_id={operation_id}/operation_code={operation_code}\n"
                             f"---{str(e)}--- ",
                    "reason": f"HOME PAGE Redirection detected is redirecting to Home page",
                    "operation_id": operation_id,
                    "operation_code": operation_code,
                    "url_campaign_configured_in_href_banner": href_url,
                    "url_campaign_result": url_browser,
                    "error_type": "AssertionError",
                    "tags": ["banner", "home_page_banners_link_redirect_to_home_page", section],
                    "component": component
                }
                # Inject into Elastic
                data_configured = configure_criticality_error_link_dead(data, href_url, url_page_href_url)
                log_json_to_foundation_elastic(data_configured)
                banners_failed.append(data_configured)
                error += 1
                continue
            except (PlaywrightTimeoutError, TimeoutError, Exception) as e:
                logging.error(f"{e.__class__.__name__} in banner '{banner_number}/{len(data_to_test_banners)}'"
                              f"operation_id={operation_id}/operation_code={operation_code}"
                              f" countdown retry {local_retry_count}/{variables.retry}")
                data_configured = handle_exception(e, href_url, url_browser, operation_id, operation_code, country, banner_number, component, section)
                # Inject into Elastic
                log_json_to_foundation_elastic(data_configured)
                error += 1
                local_retry_count -= 1
                continue

    print_report_execution_error_success_in_console(f"home_page_banners_link_redirect_to_home_page - home_page",
                                                    start_time_before_all_checks, error, success, skipped)
    elapsed_time = (datetime.now() - start_time_before_all_checks).total_seconds()
    data_report = {
        "timestamp": start_time_before_all_checks,
        "elapsed_time": elapsed_time,
        "country": country,
        "tags": ["report", "home_page_banners_link_redirect_to_home_page"],
        "sales_error": error,
        "sales_success": success
    }
    log_json_to_foundation_elastic(data_report)
    return banners_failed
