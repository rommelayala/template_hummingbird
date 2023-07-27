import os
import sys

sys.path.append("../tests")
from lib.utilities import *

logging.basicConfig(level=logging.DEBUG)
variables = ConfigVariables()
# get variables from system global env (command line)
retry_count = variables.retry
run_type = os.getenv('RUN_TYPE')
banners_failed = []


def handle_exception(exception, href_url, url_browser, operation_id, operation_code, country, banner_number, component, section):
    exception_name = exception.__class__.__name__

    timestamp = datetime.now(timezone.utc).isoformat()
    data = {
        "banner_number": banner_number,
        "run_type": run_type,
        "status": "FAILED",
        "fail_level": "high",
        "timestamp": timestamp,
        "country": country,
        "debug": f"{exception_name} {str(exception)}",
        "reason": f"HOME PAGE {exception_name} ",
        "operation_id": operation_id,
        "operation_code": operation_code,
        "url_campaign_configured_in_href_banner": href_url,
        "url_campaign_result": url_browser,
        "error_type": exception_name,
        "tags": ["banner", "home_page_banners_link_redirect_to_home_page", section],
        "component": component
    }
    return data
