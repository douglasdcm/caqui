import aiohttp as __aiohttp
import json as __json
from caqui.constants import HEADERS as __HEADERS
from caqui.exceptions import WebDriverError as __WebDriverError
from caqui import helper as __helper


async def __handle_response(resp):
    result = None
    if resp.status in range(200, 399):
        result = await resp.json()
    else:
        raise __WebDriverError(f"Status code: {resp.status}, Body: {resp.text}")

    if int(result.get("status", 0)) > 0:
        raise __WebDriverError(f"Status code: {resp.status}, Body: {resp.text}")

    return result


async def __delete(url):
    try:
        async with __aiohttp.ClientSession() as session:
            async with session.delete(url, headers=__HEADERS) as resp:
                return await __handle_response(resp)
    except Exception as error:
        raise __WebDriverError("'DELETE' request failed.") from error


async def __post(url, payload):
    try:
        async with __aiohttp.ClientSession() as session:
            async with session.post(
                url, data=__json.dumps(payload), headers=__HEADERS
            ) as resp:
                return await __handle_response(resp)
    except Exception as error:
        raise __WebDriverError("'POST' request failed.") from error


async def __get(url):
    try:
        async with __aiohttp.ClientSession() as session:
            async with session.get(url, headers=__HEADERS) as resp:
                return await __handle_response(resp)
    except Exception as error:
        raise __WebDriverError("'GET' request failed.") from error


async def __handle_alert(driver_url, session, command):
    url = f"{driver_url}/session/{session}/alert/{command}"
    payload = {
        "value": command,
    }
    await __post(url, payload)
    return True


async def __handle_window(driver_url, session, command):
    url = f"{driver_url}/session/{session}/window/{command}"
    payload = {}
    await __post(url, payload)
    return True


async def add_cookie(driver_url, session, cookie):
    """Add cookie"""
    try:
        url = f"{driver_url}/session/{session}/cookie"
        payload = {"cookie": cookie}
        await __post(url, payload)
        return True
    except Exception as error:
        raise __WebDriverError("Failed to add cookie.") from error


async def delete_cookie(driver_url, session, name):
    """Delete cookie by name"""
    try:
        url = f"{driver_url}/session/{session}/cookie/{name}"
        await __delete(url)
        return True
    except Exception as error:
        raise __WebDriverError(f"Failed to delete cookie '{name}'.") from error


async def refresh_page(driver_url, session):
    """Refresh page"""
    try:
        url = f"{driver_url}/session/{session}/refresh"
        payload = {}
        await __post(url, payload)
        return True
    except Exception as error:
        raise __WebDriverError("Failed to refresh page.") from error


async def go_forward(driver_url, session):
    """Go to page forward"""
    try:
        url = f"{driver_url}/session/{session}/forward"
        payload = {}
        await __post(url, payload)
        return True
    except Exception as error:
        raise __WebDriverError("Failed to go to page forward.") from error


async def set_window_rectangle(driver_url, session, width, height, x, y):
    """Set window rectangle"""
    try:
        url = f"{driver_url}/session/{session}/window/rect"
        payload = {"width": width, "height": height, "x": x, "y": y}
        await __post(url, payload)
        return True
    except Exception as error:
        raise __WebDriverError("Failed to set window rectangle.") from error


async def fullscreen_window(driver_url, session):
    """Fullscreen window"""
    try:
        return await __handle_window(driver_url, session, command="fullscreen")
    except Exception as error:
        raise __WebDriverError("Failed to fullscreen window.") from error


async def minimize_window(driver_url, session):
    """Minimize window"""
    try:
        return await __handle_window(driver_url, session, command="minimize")
    except Exception as error:
        raise __WebDriverError("Failed to minimize window.") from error


async def maximize_window(driver_url, session):
    """Maximize window"""
    try:
        return await __handle_window(driver_url, session, command="maximize")
    except Exception as error:
        raise __WebDriverError("Failed to maximize window.") from error


async def switch_to_window(driver_url, session, handle):
    """Switch to window"""
    try:
        url = f"{driver_url}/session/{session}/window"
        payload = {"name": handle}
        await __post(url, payload)
        return True
    except Exception as error:
        raise __WebDriverError("Failed to switch to window.") from error


async def new_window(driver_url, session, window_type="tab"):
    """Open a new window
    :param window_type (str): tab or window

    return (str): window handle
    """
    try:
        url = f"{driver_url}/session/{session}/window/new"
        payload = {"type": window_type}
        result = await __post(url, payload)
        return result.get("value", {}).get("handle")
    except Exception as error:
        raise __WebDriverError("Failed to open window.") from error


async def switch_to_parent_frame(driver_url, session, element_frame):
    """Switch to parent frame of 'element_frame'"""
    try:
        url = f"{driver_url}/session/{session}/frame/parent"
        payload = {"id": {"ELEMENT": element_frame}}
        await __post(url, payload)
        return True
    except Exception as error:
        raise __WebDriverError("Failed to switch to parent frame.") from error


async def switch_to_frame(driver_url, session, element_frame):
    """Switch to frame 'element_frame'"""
    try:
        url = f"{driver_url}/session/{session}/frame"
        payload = {"id": {"ELEMENT": element_frame}}
        await __post(url, payload)
        return True
    except Exception as error:
        raise __WebDriverError("Failed to switch to frame.") from error


async def delete_all_cookies(driver_url, session):
    """Delete all cookies"""
    try:
        url = f"{driver_url}/session/{session}/cookie"
        await __delete(url)
        return True
    except Exception as error:
        raise __WebDriverError("Failed to delete cookies.") from error


async def send_alert_text(driver_url, session, text):
    """Fill the alert text area and send the text"""
    try:
        url = f"{driver_url}/session/{session}/alert/text"
        payload = {
            "text": text,
        }
        await __post(url, payload)
        return True
    except Exception as error:
        raise __WebDriverError("Failed to sent text to alert.") from error


async def accept_alert(driver_url, session):
    """Accept alert"""
    try:
        return await __handle_alert(driver_url, session, "accept")
    except Exception as error:
        raise __WebDriverError("Failed to accept alert.") from error


async def dismiss_alert(driver_url, session):
    """Dismiss alert"""
    try:
        return await __handle_alert(driver_url, session, "dismiss")
    except Exception as error:
        raise __WebDriverError("Failed to dismiss alert.") from error


async def take_screenshot_element(
    driver_url, session, element, path="/tmp", file_name="caqui"
):
    """Take screenshot of element"""
    try:
        url = f"{driver_url}/session/{session}/element/{element}/screenshot"
        response = await __get(url)
        picture = response.get("value")
        __helper.save_picture(session, path, file_name, picture)
        return True
    except Exception as error:
        raise __WebDriverError("Failed to take screenshot from element.") from error


async def take_screenshot(driver_url, session, path="/tmp", file_name="caqui"):
    """Take screenshot"""
    try:
        url = f"{driver_url}/session/{session}/screenshot"
        response = await __get(url)
        picture = response.get("value")
        __helper.save_picture(session, path, file_name, picture)
        return True
    except Exception as error:
        raise __WebDriverError("Failed to take screenshot.") from error


async def get_named_cookie(driver_url, session, name):
    """Get cookie by name"""
    try:
        url = f"{driver_url}/session/{session}/cookie/{name}"
        response = await __get(url)
        return response.get("value")
    except Exception as error:
        raise __WebDriverError(f"Failed to get cookie '{name}'.") from error


async def get_computed_label(driver_url, session, element):
    """Get the element tag computed label. Get the accessibility name"""
    try:
        url = f"{driver_url}/session/{session}/element/{element}/computedlabel"
        response = await __get(url)
        return response.get("value")
    except Exception as error:
        raise __WebDriverError("Failed to get element computed label.") from error


async def get_computed_role(driver_url, session, element):
    """Get the element tag computed role (the element role)"""
    try:
        url = f"{driver_url}/session/{session}/element/{element}/computedrole"
        response = await __get(url)
        return response.get("value")
    except Exception as error:
        raise __WebDriverError("Failed to get element computed role.") from error


async def get_tag_name(driver_url, session, element):
    """Get the element tag name"""
    try:
        url = f"{driver_url}/session/{session}/element/{element}/name"
        response = await __get(url)
        return response.get("value")
    except Exception as error:
        raise __WebDriverError("Failed to get element name.") from error


async def get_shadow_root(driver_url, session, element):
    """Get the shadow root element"""
    try:
        root_element = "shadow-6066-11e4-a52e-4f735466cecf"
        url = f"{driver_url}/session/{session}/element/{element}/shadow"
        response = await __get(url)
        return response.get("value", {}).get(root_element)
    except Exception as error:
        raise __WebDriverError("Failed to get element shadow.") from error


async def get_rect(driver_url, session, element):
    """Get the element rectangle"""
    try:
        url = f"{driver_url}/session/{session}/element/{element}/rect"
        response = await __get(url)
        return response.get("value")
    except Exception as error:
        raise __WebDriverError("Failed to get element rect.") from error


async def actions(driver_url, session, payload):
    url = f"{driver_url}/session/{session}/actions"
    await __post(url, payload)
    return True


async def actions_move_to_element(driver_url, session, element):
    """Move to an element simulating a mouse movement"""
    try:
        payload = {
            "actions": [
                {
                    "type": "pointer",
                    "parameters": {"pointerType": "mouse"},
                    "id": "mouse",
                    "actions": [
                        {
                            "type": "pointerMove",
                            "duration": 250,
                            "x": 0,
                            "y": 0,
                            "origin": {"ELEMENT": element},
                        }
                    ],
                },
                {
                    "type": "key",
                    "id": "key",
                    "actions": [{"type": "pause", "duration": 0}],
                },
            ]
        }
        return await actions(driver_url, session, payload)
    except Exception as error:
        raise __WebDriverError("Failed to move to element.") from error


async def actions_scroll_to_element(driver_url, session, element):
    """Scroll to an element simulating a mouse movement"""
    try:
        payload = {
            "actions": [
                {
                    "type": "wheel",
                    "id": "wheel",
                    "actions": [
                        {
                            "type": "scroll",
                            "x": 0,
                            "y": 0,
                            "deltaX": 0,
                            "deltaY": 0,
                            "duration": 0,
                            "origin": {"ELEMENT": element},
                        }
                    ],
                }
            ]
        }
        return await actions(driver_url, session, payload)
    except Exception as error:
        raise __WebDriverError("Failed to scroll to element.") from error


async def submit(driver_url, session, element):
    """Submit a form. It is similar to 'submit' funtion in Seleniu
    It is not part of W3C WebDriver. Just added for convenience
    """
    try:
        submit_element = await find_child_element(
            driver_url,
            session,
            element,
            locator_type="xpath",
            locator_value="*[@type='submit']",
        )
        return await click(driver_url, session, submit_element)
    except Exception as error:
        raise __WebDriverError("Failed to submit form.") from error


async def actions_click(driver_url, session, element):
    """Click an element simulating a mouse movement"""
    try:
        payload = {
            "actions": [
                {
                    "type": "pointer",
                    "parameters": {"pointerType": "mouse"},
                    "id": "mouse",
                    "actions": [
                        {
                            "type": "pointerMove",
                            "duration": 250,
                            "x": 0,
                            "y": 0,
                            "origin": {"ELEMENT": element},
                        },
                        {"type": "pointerDown", "duration": 0, "button": 0},
                        {"type": "pointerUp", "duration": 0, "button": 0},
                    ],
                },
                {
                    "type": "key",
                    "id": "key",
                    "actions": [
                        {"type": "pause", "duration": 0},
                        {"type": "pause", "duration": 0},
                        {"type": "pause", "duration": 0},
                    ],
                },
            ]
        }
        return await actions(driver_url, session, payload)
    except Exception as error:
        raise __WebDriverError("Failed to click the element.") from error


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
        raise __WebDriverError("Failed to set timeouts.") from error


async def find_children_elements(
    driver_url, session, parent_element, locator_type, locator_value
):
    """Find the children elements by 'locator_type'

    If the 'parent_element' is a shadow element, set the 'locator_type' as 'id' or
    'css selector'
    """
    try:
        url = f"{driver_url}/session/{session}/element/{parent_element}/elements"
        payload = {"using": locator_type, "value": locator_value, "id": parent_element}
        response = await __post(url, payload)
        return __helper.get_elements(response)
    except Exception as error:
        raise __WebDriverError(
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
        return __helper.get_element(response)
    except Exception as error:
        raise __WebDriverError(
            f"Failed to find the child element from '{parent_element}'."
        ) from error


async def get_page_source(driver_url, session):
    """Get the page source (all content)"""
    try:
        url = f"{driver_url}/session/{session}/source"
        response = await __get(url)
        return response.get("value")
    except Exception as error:
        raise __WebDriverError("Failed to get the page source.") from error


async def execute_script(driver_url, session, script, args=[]):
    """Executes a script, like 'alert('something')' to open an alert window"""
    try:
        url = f"{driver_url}/session/{session}/execute/sync"
        payload = {"script": script, "args": args}
        response = await __post(url, payload)
        return response.get("value")
    except Exception as error:
        raise __WebDriverError("Failed to execute script.") from error


async def get_alert_text(driver_url, session):
    """Get the text from an alert"""
    try:
        url = f"{driver_url}/session/{session}/alert/text"
        response = await __get(url)
        return response.get("value")
    except Exception as error:
        raise __WebDriverError("Failed to get the alert text.") from error


async def get_active_element(driver_url, session):
    """Get the active element"""
    try:
        url = f"{driver_url}/session/{session}/element/active"
        response = await __get(url)
        return __helper.get_element(response)
    except Exception as error:
        raise __WebDriverError("Failed to check if element is selected.") from error


async def clear_element(driver_url, session, element):
    """Clear the element text"""
    try:
        url = f"{driver_url}/session/{session}/element/{element}/clear"
        payload = {"id": element}
        await __post(url, payload)
        return True
    except Exception as error:
        raise __WebDriverError("Failed to clear the element text.") from error


async def is_element_enabled(driver_url, session, element):
    """Check if element is enabled"""
    try:
        url = f"{driver_url}/session/{session}/element/{element}/enabled"
        response = await __get(url)
        return response.get("value")
    except Exception as error:
        raise __WebDriverError("Failed to check if element is enabled.") from error


async def get_css_value(driver_url, session, element, property_name):
    """Check if element is selected"""
    try:
        url = f"{driver_url}/session/{session}/element/{element}/css/{property_name}"
        response = await __get(url)
        return response.get("value")
    except Exception as error:
        raise __WebDriverError("Failed to check if element is selected.") from error


async def is_element_selected(driver_url, session, element):
    """Check if element is selected"""
    try:
        url = f"{driver_url}/session/{session}/element/{element}/selected"
        response = await __get(url)
        return response.get("value")
    except Exception as error:
        raise __WebDriverError("Failed to check if element is selected.") from error


async def get_window_rectangle(driver_url, session):
    """Get window rectangle"""
    try:
        url = f"{driver_url}/session/{session}/window/rect"
        response = await __get(url)
        return response.get("value")
    except Exception as error:
        raise __WebDriverError("Failed to get window rectangle.") from error


async def get_window_handles(driver_url, session):
    """Get window handles"""
    try:
        url = f"{driver_url}/session/{session}/window/handles"
        response = await __get(url)
        return response.get("value")
    except Exception as error:
        raise __WebDriverError("Failed to get window handles.") from error


async def close_window(driver_url, session):
    """Close active window"""
    try:
        url = f"{driver_url}/session/{session}/window"
        response = await __delete(url)
        return response.get("value")
    except Exception as error:
        raise __WebDriverError("Failed to close active window.") from error


async def get_window(driver_url, session):
    """Get window"""
    try:
        url = f"{driver_url}/session/{session}/window"
        response = await __get(url)
        return response.get("value")
    except Exception as error:
        raise __WebDriverError("Failed to get window.") from error


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
        raise __WebDriverError("Failed to go back to page.") from error


async def get_url(driver_url, session):
    """Return the URL from web page:"""
    try:
        url = f"{driver_url}/session/{session}/url"
        response = await __get(url)
        return response.get("value")
    except Exception as error:
        raise __WebDriverError("Failed to get page url.") from error


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
        raise __WebDriverError("Failed to get timeouts.") from error


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
        raise __WebDriverError("Failed to get status.") from error


async def get_title(driver_url, session):
    """Get the page title"""
    try:
        url = f"{driver_url}/session/{session}/title"
        response = await __get(url)
        return response.get("value")
    except Exception as error:
        raise __WebDriverError("Failed to get page title.") from error


async def find_elements(driver_url, session, locator_type, locator_value):
    """Search the DOM elements by 'locator', for example, 'xpath'"""
    try:
        payload = {"using": locator_type, "value": locator_value}
        url = f"{driver_url}/session/{session}/elements"
        response = await __post(url, payload)
        return [x.get("ELEMENT") for x in response.get("value")]
    except Exception as error:
        raise __WebDriverError(
            f"Failed to find element by '{locator_type}'-'{locator_value}'."
        ) from error


async def get_property(driver_url, session, element, property):
    """Get the given HTML property of an element, for example, 'href'"""
    try:
        url = f"{driver_url}/session/{session}/element/{element}/property/{property}"
        response = await __get(url)
        return response.get("value")
    except Exception as error:
        raise __WebDriverError("Failed to get value from element.") from error


async def get_attribute(driver_url, session, element, attribute):
    """Get the given HTML attribute of an element, for example, 'aria-valuenow'"""
    try:
        url = f"{driver_url}/session/{session}/element/{element}/attribute/{attribute}"
        response = await __get(url)
        return response.get("value")
    except Exception as error:
        raise __WebDriverError("Failed to get value from element.") from error


async def get_text(driver_url, session, element):
    """Get the text of an element"""
    try:
        url = f"{driver_url}/session/{session}/element/{element}/text"
        response = await __get(url)
        return response.get("value")
    except Exception as error:
        raise __WebDriverError("Failed to get text from element.") from error


async def get_cookies(driver_url, session):
    """Get the page cookies"""
    try:
        url = f"{driver_url}/session/{session}/cookie"
        response = await __get(url)
        return response.get("value")
    except Exception as error:
        raise __WebDriverError("Failed to get page cookies.") from error


async def close_session(driver_url, session):
    """Close an opened session and close the browser"""
    try:
        url = f"{driver_url}/session/{session}"
        await __delete(url)
        return True
    except Exception as error:
        raise __WebDriverError("Failed to close session.") from error


async def get(driver_url, session, page_url):
    """Does the same of 'go_to_page'. Added to be compatible with selenium method name'"""
    return go_to_page(driver_url, session, page_url)


async def go_to_page(driver_url, session, page_url):
    """Navigate to 'page_url'"""
    try:
        url = f"{driver_url}/session/{session}/url"
        payload = {"url": page_url}
        await __post(url, payload)
        return True
    except Exception as error:
        raise __WebDriverError(f"Failed to navigate to page '{page_url}'.") from error


async def send_keys(driver_url, session, element, text):
    """Fill an editable element, for example a textarea, with a given text"""
    try:
        url = f"{driver_url}/session/{session}/element/{element}/value"
        payload = {"text": text, "value": [*text], "id": element}
        await __post(url, payload)
        return True
    except Exception as error:
        raise __WebDriverError(f"Failed to send key '{text}'.") from error


async def click(driver_url, session, element):
    """Click on an element"""
    try:
        payload = {"id": element}
        url = f"{driver_url}/session/{session}/element/{element}/click"
        await __post(url, payload)
        return True
    except Exception as error:
        raise __WebDriverError("Failed to click on element.") from error


async def find_element(driver_url, session, locator_type, locator_value):
    """Find an element by a 'locator', for example 'xpath'"""

    try:
        payload = {"using": locator_type, "value": locator_value}
        url = f"{driver_url}/session/{session}/element"
        response = await __post(url, payload)

        # Firefox does not support id locator, so it prints the error message to the user
        # It helps on debug
        if response.get("value").get("error"):
            raise __WebDriverError(f"Failed to find element. {response}")
        return __helper.get_element(response)
    except Exception as error:
        raise __WebDriverError(
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
        raise __WebDriverError("Failed to open session.") from error
