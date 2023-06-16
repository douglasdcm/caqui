import aiohttp
import json
from caqui.constants import HEADERS
from caqui.exceptions import WebDriverError
from caqui import helper


async def __delete(url):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.delete(url, headers=HEADERS) as resp:
                response = await resp.json()
                return response
    except Exception as error:
        raise WebDriverError("'DELETE' request failed.") from error


async def __post(url, payload):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                url, data=json.dumps(payload), headers=HEADERS
            ) as resp:
                response = await resp.json()
                return response
    except Exception as error:
        raise WebDriverError("'POST' request failed.") from error


async def __get(url):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=HEADERS) as resp:
                response = await resp.json()
                return response
    except Exception as error:
        raise WebDriverError("'GET' request failed.") from error


async def set_timeouts(driver_url, session, timeouts):
    """Set timeouts"""
    try:
        url = f"{driver_url}/session/{session}/timeouts"
        payload = {
            "implicit": timeouts,
        }
        await __post(url, payload)
        return True
    except Exception as error:
        raise WebDriverError(f"Failed to set timeouts.") from error


async def find_children_elements(
    driver_url, session, parent_element, locator_type, locator_value
):
    """Find the children elements by 'locator_type'"""
    try:
        url = f"{driver_url}/session/{session}/element/{parent_element}/elements"
        payload = {"using": locator_type, "value": locator_value, "id": parent_element}
        response = await __post(url, payload)
        return helper.get_elements(response)
    except Exception as error:
        raise WebDriverError(
            f"Failed to find the children elements from '{parent_element}'."
        ) from error


async def find_child_element(
    driver_url, session, parent_element, locator_type, locator_value
):
    """Find the child element by 'locator_type'"""
    try:
        url = f"{driver_url}/session/{session}/element/{parent_element}/element"
        payload = {"using": locator_type, "value": locator_value, "id": parent_element}
        response = await __post(url, payload)
        return helper.get_element(response)
    except Exception as error:
        raise WebDriverError(
            f"Failed to find the child element from '{parent_element}'."
        ) from error


async def get_page_source(driver_url, session):
    """Get the page source (all content)"""
    try:
        url = f"{driver_url}/session/{session}/source"
        response = await __get(url)
        return response.get("value")
    except Exception as error:
        raise WebDriverError("Failed to get the page source.") from error


async def execute_script(driver_url, session, script, args=[]):
    """Executes a script, like 'alert('something')' to open an alert window"""
    try:
        url = f"{driver_url}/session/{session}/execute/sync"
        payload = {"script": script, "args": args}
        response = await __post(url, payload)
        return response.get("value")
    except Exception as error:
        raise WebDriverError("Failed to open session.") from error


async def get_alert_text(driver_url, session):
    """Get the text from an alert"""
    try:
        url = f"{driver_url}/session/{session}/alert/text"
        response = await __get(url)
        return response.get("value")
    except Exception as error:
        raise WebDriverError("Failed to get the alert text.") from error


async def get_active_element(driver_url, session):
    """Get the active element"""
    try:
        url = f"{driver_url}/session/{session}/element/active"
        response = await __get(url)
        return helper.get_element(response)
    except Exception as error:
        raise WebDriverError("Failed to check if element is selected.") from error


async def clear_element(driver_url, session, element):
    """Clear the element text"""
    try:
        url = f"{driver_url}/session/{session}/element/{element}/clear"
        payload = {"id": element}
        await __post(url, payload)
        return True
    except Exception as error:
        raise WebDriverError("Failed to clear the element text.") from error


async def is_element_enabled(driver_url, session, element):
    """Check if element is enabled"""
    try:
        url = f"{driver_url}/session/{session}/element/{element}/enabled"
        response = await __get(url)
        return response.get("value")
    except Exception as error:
        raise WebDriverError("Failed to check if element is enabled.") from error


async def get_css_value(driver_url, session, element, property_name):
    """Check if element is selected"""
    try:
        url = f"{driver_url}/session/{session}/element/{element}/css/{property_name}"
        response = await __get(url)
        return response.get("value")
    except Exception as error:
        raise WebDriverError("Failed to check if element is selected.") from error


async def is_element_selected(driver_url, session, element):
    """Check if element is selected"""
    try:
        url = f"{driver_url}/session/{session}/element/{element}/selected"
        response = await __get(url)
        return response.get("value")
    except Exception as error:
        raise WebDriverError("Failed to check if element is selected.") from error


async def get_window_rectangle(driver_url, session):
    """Get window rectangle"""
    try:
        url = f"{driver_url}/session/{session}/window/rect"
        response = await __get(url)
        return response.get("value")
    except Exception as error:
        raise WebDriverError("Failed to get window rectangle.") from error


async def get_window_handles(driver_url, session):
    """Get window handles"""
    try:
        url = f"{driver_url}/session/{session}/window/handles"
        response = await __get(url)
        return response.get("value")
    except Exception as error:
        raise WebDriverError("Failed to get window handles.") from error


async def close_window(driver_url, session):
    """Close active window"""
    try:
        url = f"{driver_url}/session/{session}/window"
        response = await __delete(url)
        return response.get("value")
    except Exception as error:
        raise WebDriverError("Failed to close active window.") from error


async def get_window(driver_url, session):
    """Get window"""
    try:
        url = f"{driver_url}/session/{session}/window"
        response = await __get(url)
        return response.get("value")
    except Exception as error:
        raise WebDriverError("Failed to get window.") from error


async def go_back(driver_url, session):
    """
    This command causes the browser to traverse one step backward in the joint session history of the
    current browse. This is equivalent to pressing the back button in the browser.
    """
    try:
        url = f"{driver_url}/session/{session}/back"
        await __post(url, {})
        return True
    except Exception as error:
        raise WebDriverError("Failed to go back to page.") from error


async def get_url(driver_url, session):
    """Return the URL from web page:"""
    try:
        url = f"{driver_url}/session/{session}/url"
        response = await __get(url)
        return response.get("value")
    except Exception as error:
        raise WebDriverError("Failed to get page url.") from error


async def get_timeouts(driver_url, session):
    """
    Return the configured timeouts:
        {"implicit": 0, "pageLoad": 300000, "script": 30000}
    """
    try:
        url = f"{driver_url}/session/{session}/timeouts"
        response = await __get(url)
        return response.get("value")
    except Exception as error:
        raise WebDriverError("Failed to get timeouts.") from error


async def get_status(driver_url):
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
        response = await __get(url)
        return response
    except Exception as error:
        raise WebDriverError("Failed to get status.") from error


async def get_title(driver_url, session):
    """Get the page title"""
    try:
        url = f"{driver_url}/session/{session}/title"
        response = await __get(url)
        return response.get("value")
    except Exception as error:
        raise WebDriverError("Failed to get page title.") from error


async def find_elements(driver_url, session, locator_type, locator_value):
    """Search the DOM elements by 'locator', for example, 'xpath'"""
    try:
        payload = {"using": locator_type, "value": locator_value}
        url = f"{driver_url}/session/{session}/elements"
        response = await __post(url, payload)
        return [x.get("ELEMENT") for x in response.get("value")]
    except Exception as error:
        raise WebDriverError(
            f"Failed to find element by '{locator_type}'-'{locator_value}'."
        ) from error


async def get_property(driver_url, session, element, property):
    """Get the given HTML property of an element, for example, 'href'"""
    try:
        url = f"{driver_url}/session/{session}/element/{element}/property/{property}"
        response = await __get(url)
        return response.get("value")
    except Exception as error:
        raise WebDriverError("Failed to get value from element.") from error


async def get_attribute(driver_url, session, element, attribute):
    """Get the given HTML attribute of an element, for example, 'aria-valuenow'"""
    try:
        url = f"{driver_url}/session/{session}/element/{element}/attribute/{attribute}"
        response = await __get(url)
        return response.get("value")
    except Exception as error:
        raise WebDriverError("Failed to get value from element.") from error


async def get_text(driver_url, session, element):
    """Get the text of an element"""
    try:
        url = f"{driver_url}/session/{session}/element/{element}/text"
        response = await __get(url)
        return response.get("value")
    except Exception as error:
        raise WebDriverError("Failed to get text from element.") from error


async def get_cookies(driver_url, session):
    """Get the page cookies"""
    try:
        url = f"{driver_url}/session/{session}/cookie"
        response = await __get(url)
        return response.get("value")
    except Exception as error:
        raise WebDriverError("Failed to get page cookies.") from error


async def close_session(driver_url, session):
    """Close an opened session and close the browser"""
    try:
        url = f"{driver_url}/session/{session}"
        await __delete(url)
        return True
    except Exception as error:
        raise WebDriverError("Failed to close session.") from error


async def go_to_page(driver_url, session, page_url):
    """Navigate to 'page_url'"""
    try:
        url = f"{driver_url}/session/{session}/url"
        payload = {"url": page_url}
        await __post(url, payload)
        return True
    except Exception as error:
        raise WebDriverError(f"Failed to navigate to page '{page_url}'.") from error


async def send_keys(driver_url, session, element, text):
    """Fill an editable element, for example a textarea, with a given text"""
    try:
        url = f"{driver_url}/session/{session}/element/{element}/value"
        payload = {"text": text, "value": [*text], "id": element}
        await __post(url, payload)
        return True
    except Exception as error:
        raise WebDriverError(f"Failed to send key '{text}'.") from error


async def click(driver_url, session, element):
    """Click on an element"""
    try:
        payload = {"id": element}
        url = f"{driver_url}/session/{session}/element/{element}/click"
        await __post(url, payload)
        return True
    except Exception as error:
        raise WebDriverError("Failed to click on element.") from error


async def find_element(driver_url, session, locator_type, locator_value):
    """Find an element by a 'locator', for example 'xpath'"""

    try:
        payload = {"using": locator_type, "value": locator_value}
        url = f"{driver_url}/session/{session}/element"
        response = await __post(url, payload)
        return helper.get_element(response)
    except Exception as error:
        raise WebDriverError(
            f"Failed to find element by '{locator_type}'-'{locator_value}'."
        ) from error


async def get_session(driver_url, capabilities):
    """Opens a browser and a session. This session is used for all functions to perform events in the page"""
    try:
        payload = capabilities
        url = f"{driver_url}/session"
        response = await __post(url, payload)
        return response.get("sessionId")
    except Exception as error:
        raise WebDriverError("Failed to open session.") from error
