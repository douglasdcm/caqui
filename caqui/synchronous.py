import requests
import json
from caqui.exceptions import WebDriverError
from caqui import helper

HEADERS = {
    "Accept-Encoding": "identity",
    "Accept": "application/json",
    "Content-Type": "application/json;charset=UTF-8",
    "Connection": "keep-alive",
}


def __get(url):
    try:
        return requests.request("GET", url, headers=HEADERS, data={}).json()
    except Exception as error:
        raise WebDriverError("'GET' request failed.") from error


def __post(url, payload):
    try:
        return requests.request("POST", url, headers=HEADERS, data=payload).json()
    except Exception as error:
        raise WebDriverError("'POST' request failed.") from error


def __delete(url):
    try:
        return requests.request("DELETE", url, headers={}, data={}).json()
    except Exception as error:
        raise WebDriverError("'DELETE' request failed.") from error


def go_back(driver_url, session):
    """
    This command causes the browser to traverse one step backward in the joint session history of the
    current browse. This is equivalent to pressing the back button in the browser.
    """
    try:
        url = f"{driver_url}/session/{session}/back"
        __post(url, {})
        return True
    except Exception as error:
        raise WebDriverError(f"Failed to go back to page.") from error


def get_url(driver_url, session):
    """Return the URL from web page:"""
    try:
        url = f"{driver_url}/session/{session}/url"
        response = __get(url)
        return response.get("value")
    except Exception as error:
        raise WebDriverError(f"Failed to get page url.") from error


def get_timeouts(driver_url, session):
    """
    Return the configured timeouts:
        {"implicit": 0, "pageLoad": 300000, "script": 30000}
    """
    try:
        url = f"{driver_url}/session/{session}/timeouts"
        response = __get(url)
        return response.get("value")
    except Exception as error:
        raise WebDriverError(f"Failed to get timeouts.") from error


def get_status(driver_url):
    """
    Return the status and details of the WebDriver:
        "build": {
                "version": "113.0.5672.63 (0e1a4471d5ae5bf128b1bd8f4d627c8cbd55f70c-refs/branch-heads/5672@{#912})"
            },
            "message": "ChromeDriver ready for new sessions.",
            "os": {"arch": "x86_64", "name": "Linux", "version": "5.4.0-150-generic"},
            "ready": True,
        }
    """
    try:
        url = f"{driver_url}/status"
        return __get(url)
    except Exception as error:
        raise WebDriverError(f"Failed to get status.") from error


def get_title(driver_url, session):
    """Get the page title"""
    try:
        url = f"{driver_url}/session/{session}/title"
        response = __get(url)
        return response.get("value")
    except Exception as error:
        raise WebDriverError(f"Failed to get page title.") from error


def find_elements(driver_url, session, locator_type, locator_value):
    """Search the DOM elements by 'locator', for example, 'xpath'"""
    try:
        url = f"{driver_url}/session/{session}/elements"
        payload = json.dumps({"using": locator_type, "value": locator_value})
        response = __post(url, payload)
        return [x.get("ELEMENT") for x in response.get("value")]
    except Exception as error:
        raise WebDriverError(
            f"Failed to find elements by '{locator_type}'-'{locator_value}'."
        ) from error


def get_property(driver_url, session, element, property):
    """Get the given HTML property of an element, for example, 'href'"""
    try:
        url = f"{driver_url}/session/{session}/element/{element}/property/{property}"
        response = __get(url)
        return response.get("value")
    except Exception as error:
        raise WebDriverError("Failed to get value from element.") from error


def go_to_page(driver_url, session, page_url):
    """Navigate to 'page_url'"""
    try:
        url = f"{driver_url}/session/{session}/url"
        payload = json.dumps({"url": page_url})
        __post(url, payload)
        return True
    except Exception as error:
        raise WebDriverError(f"Failed to navigate to '{page_url}'") from error


def close_session(driver_url, session):
    """Close an opened session and close the browser"""
    try:
        url = f"{driver_url}/session/{session}"
        __delete(url)
        return True
    except Exception as error:
        raise WebDriverError("Failed to close session.") from error


def get_text(driver_url, session, element):
    """Get the text of an element"""
    try:
        url = f"{driver_url}/session/{session}/element/{element}/text"
        response = __get(url)
        return response.get("value")
    except Exception as error:
        raise WebDriverError("Failed to get text from element.") from error


def send_keys(driver_url, session, element, text):
    """Fill an editable element, for example a textarea, with a given text"""
    try:
        url = f"{driver_url}/session/{session}/element/{element}/value"
        payload = json.dumps({"text": text, "value": [*text], "id": element})
        __post(url, payload)
        return True
    except Exception as error:
        raise WebDriverError(f"Failed to send key '{text}'.") from error


def click(driver_url, session, element):
    """Click on an element"""
    try:
        url = f"{driver_url}/session/{session}/element/{element}/click"
        payload = json.dumps({"id": element})
        __post(url, payload)
        return True
    except Exception as error:
        raise WebDriverError("Failed to click on element.") from error


def __get_session(response):
    # Firefox response
    value = response.get("value")
    session_id = value.get("sessionId")
    if session_id:
        return session_id

    # Chrome response
    return response.get("sessionId")


def get_session(driver_url, capabilities):
    """Opens a browser and a session. This session is used for all functions to perform events in the page"""
    try:
        url = f"{driver_url}/session"
        data = json.dumps(capabilities)
        response = __post(url, payload=data)
        return __get_session(response)
    except Exception as error:
        raise WebDriverError("Failed to open session.") from error


def find_element(driver_url, session, locator_type, locator_value):
    """Find an element by a 'locator', for example 'xpath'"""
    try:
        url = f"{driver_url}/session/{session}/element"
        payload = json.dumps({"using": locator_type, "value": locator_value})
        response = __post(url, payload)
        return helper.get_element(response)
    except Exception as error:
        raise WebDriverError(
            f"Failed to find element by '{locator_type}'-'{locator_value}'."
        ) from error
