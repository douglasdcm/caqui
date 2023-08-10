import requests as __requests
import json as __json
from caqui.exceptions import WebDriverError as __WebDriverError
from caqui import helper as __helper
from caqui.constants import HEADERS as __HEADERS


def __handle_response(response):
    result = None
    if response.status_code in range(200, 399):
        result = response.json()
    else:
        raise __WebDriverError(f"Status: {response.status_code}, {response.text}")

    if int(result.get("status", 0)) > 0:
        raise __WebDriverError(
            f"Status: {response.status_code}, {response.text}, Details: {result.get('value')}"
        )
    return result


def __get(url):
    try:
        response = __requests.request("GET", url, headers=__HEADERS, data={})
        return __handle_response(response)
    except Exception as error:
        raise __WebDriverError("'GET' request failed.") from error


def __post(url, payload):
    response = __requests.request(
        "POST", url, headers=__HEADERS, data=__json.dumps(payload)
    )
    try:
        return __handle_response(response)
    except Exception as error:
        raise __WebDriverError("'POST' request failed.") from error


def __delete(url):
    try:
        response = __requests.request("DELETE", url, headers={}, data={})
        return __handle_response(response)
    except Exception as error:
        raise __WebDriverError("'DELETE' request failed.") from error


def __handle_alerts(driver_url, session, command):
    url = f"{driver_url}/session/{session}/alert/{command}"
    payload = {"value": command}
    __post(url, payload)
    return True


def __handle_window(driver_url, session, command):
    url = f"{driver_url}/session/{session}/window/{command}"
    payload = {}
    __post(url, payload)
    return True


def add_cookie(driver_url, session, cookie):
    """Add cookie"""
    try:
        url = f"{driver_url}/session/{session}/cookie"
        payload = {"cookie": cookie}
        __post(url, payload)
        return True
    except Exception as error:
        raise __WebDriverError("Failed to add cookie.") from error


def delete_cookie(driver_url, session, name):
    """Delete cookie by name"""
    try:
        url = f"{driver_url}/session/{session}/cookie/{name}"
        __delete(url)
        return True
    except Exception as error:
        raise __WebDriverError("Failed to delete cookie '{name}'.") from error


def refresh_page(driver_url, session):
    """Refresh page"""
    try:
        url = f"{driver_url}/session/{session}/refresh"
        payload = {}
        __post(url, payload)
        return True
    except Exception as error:
        raise __WebDriverError("Failed to refresh page.") from error


def go_forward(driver_url, session):
    """Go to page forward"""
    try:
        url = f"{driver_url}/session/{session}/forward"
        payload = {}
        __post(url, payload)
        return True
    except Exception as error:
        raise __WebDriverError("Failed to go page forward.") from error


def set_window_rectangle(driver_url, session, width, height, x, y):
    """Set window rectangle"""
    try:
        url = f"{driver_url}/session/{session}/window/rect"
        payload = {"width": width, "height": height, "x": x, "y": y}
        __post(url, payload)
        return True
    except Exception as error:
        raise __WebDriverError("Failed to set window rectangle.") from error


def fullscreen_window(driver_url, session):
    """Fullscreen window"""
    try:
        return __handle_window(driver_url, session, command="fullscreen")
    except Exception as error:
        raise __WebDriverError("Failed to fullscreen window.") from error


def minimize_window(driver_url, session):
    """Minimize window"""
    try:
        return __handle_window(driver_url, session, command="minimize")
    except Exception as error:
        raise __WebDriverError("Failed to minimize window.") from error


def maximize_window(driver_url, session):
    """Maximize window"""
    try:
        return __handle_window(driver_url, session, command="maximize")
    except Exception as error:
        raise __WebDriverError("Failed to maximize window.") from error


def switch_to_window(driver_url, session, handle):
    """Switch to window"""
    try:
        url = f"{driver_url}/session/{session}/window"
        payload = {"name": handle}
        __post(url, payload)
        return True
    except Exception as error:
        raise __WebDriverError("Failed to switch to window.") from error


def new_window(driver_url, session, window_type="tab"):
    """Open a new window
    :param window_type (str): tab or window

    return (str): window handle
    """
    try:
        url = f"{driver_url}/session/{session}/window/new"
        payload = {"type": window_type}
        return __post(url, payload).get("value", {}).get("handle")
    except Exception as error:
        raise __WebDriverError("Failed to open a new window.") from error


def switch_to_parent_frame(driver_url, session, element_frame):
    """Switch to parent frame of 'element_frame'"""
    try:
        url = f"{driver_url}/session/{session}/frame/parent"
        payload = {"id": {"ELEMENT": element_frame}}
        __post(url, payload)
        return True
    except Exception as error:
        raise __WebDriverError("Failed to switch to parent frame.") from error


def switch_to_frame(driver_url, session, element_frame):
    """Switch to frame 'element_frame'"""
    try:
        url = f"{driver_url}/session/{session}/frame"
        payload = {"id": {"ELEMENT": element_frame}}
        __post(url, payload)
        return True
    except Exception as error:
        raise __WebDriverError("Failed to switch to frame.") from error


def delete_all_cookies(driver_url, session):
    """Delete all cookies"""
    try:
        url = f"{driver_url}/session/{session}/cookie"
        __delete(url)
        return True
    except Exception as error:
        raise __WebDriverError("Failed to delete cookies.") from error


def send_alert_text(driver_url, session, text):
    """Fill the alert text area and send the text"""
    try:
        url = f"{driver_url}/session/{session}/alert/text"
        payload = {"text": text}
        __post(url, payload)
        return True
    except Exception as error:
        raise __WebDriverError("Failed to sent text to alert.") from error


def accept_alert(driver_url, session):
    """Accept an alert"""
    try:
        return __handle_alerts(driver_url, session, "accept")
    except Exception as error:
        raise __WebDriverError("Failed to accept the alert.") from error


def dismiss_alert(driver_url, session):
    """Dismiss an alert"""
    try:
        return __handle_alerts(driver_url, session, "dismiss")
    except Exception as error:
        raise __WebDriverError("Failed to dismiss the alert.") from error


def take_screenshot_element(
    driver_url, session, element, path="/tmp", file_name="caqui"
):
    """Take screenshot of element."""
    try:
        url = f"{driver_url}/session/{session}/element/{element}/screenshot"
        response = __get(url).get("value")
        __helper.save_picture(session, path, file_name, response)
        return True
    except Exception as error:
        raise __WebDriverError("Failed to take screeshot.") from error


def take_screenshot(driver_url, session, path="/tmp", file_name="caqui"):
    """Take screenshot."""
    try:
        url = f"{driver_url}/session/{session}/screenshot"
        response = __get(url).get("value")
        __helper.save_picture(session, path, file_name, response)
        return True
    except Exception as error:
        raise __WebDriverError("Failed to take screeshot.") from error


def get_named_cookie(driver_url, session, name):
    """Get cookie by name."""
    try:
        url = f"{driver_url}/session/{session}/cookie/{name}"
        return __get(url).get("value")
    except Exception as error:
        raise __WebDriverError(f"Failed to get the cookie '{name}'.") from error


def get_computed_label(driver_url, session, element):
    """Get the element computed label. Get the accessibility name."""
    try:
        url = f"{driver_url}/session/{session}/element/{element}/computedlabel"
        return __get(url).get("value")
    except Exception as error:
        raise __WebDriverError("Failed to get the element computed label.") from error


def get_computed_role(driver_url, session, element):
    """Get the element computed role (the element role)"""
    try:
        url = f"{driver_url}/session/{session}/element/{element}/computedrole"
        return __get(url).get("value")
    except Exception as error:
        raise __WebDriverError("Failed to get the element computed role.") from error


def get_tag_name(driver_url, session, element):
    """Get the element tag name"""
    try:
        url = f"{driver_url}/session/{session}/element/{element}/name"
        return __get(url).get("value")
    except Exception as error:
        raise __WebDriverError("Failed to get the element name.") from error


def get_shadow_root(driver_url, session, element):
    """Get the shadow root element"""
    try:
        root_element = "shadow-6066-11e4-a52e-4f735466cecf"
        url = f"{driver_url}/session/{session}/element/{element}/shadow"
        return __get(url).get("value", {}).get(root_element)
    except Exception as error:
        raise __WebDriverError("Failed to get the element shadow.") from error


def get_rect(driver_url, session, element):
    """Get the element rectangle"""
    try:
        url = f"{driver_url}/session/{session}/element/{element}/rect"
        return __get(url).get("value")
    except Exception as error:
        raise __WebDriverError("Failed to get the element rect.") from error


def actions_move_to_element(driver_url, session, element):
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
        return actions(driver_url, session, payload)
    except Exception as error:
        raise __WebDriverError("Failed to move to element.") from error


def actions_scroll_to_element(driver_url, session, element):
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
        return actions(driver_url, session, payload)
    except Exception as error:
        raise __WebDriverError("Failed to scroll to element.") from error


def actions(driver_url, session, payload):
    url = f"{driver_url}/session/{session}/actions"
    __post(url, payload)
    return True


def submit(driver_url, session, element):
    """Submit a form. It is similar to 'submit' funtion in Seleniu
    It is not part of W3C WebDriver. Just added for convenience
    """
    try:
        submit_element = find_child_element(
            driver_url,
            session,
            element,
            locator_type="xpath",
            locator_value="//*[@type='submit']",
        )
        return click(driver_url, session, submit_element)
    except Exception as error:
        raise __WebDriverError("Failed to submit form.") from error


def actions_click(driver_url, session, element):
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
        return actions(driver_url, session, payload)
    except Exception as error:
        raise __WebDriverError("Failed to click the element.") from error


def set_timeouts(driver_url, session, timeouts):
    """Set timeouts"""
    try:
        url = f"{driver_url}/session/{session}/timeouts"
        payload = {
            "implicit": timeouts,
        }
        __post(url, payload)
        return True
    except Exception as error:
        raise __WebDriverError("Failed to set timeouts.") from error


def find_children_elements(
    driver_url, session, parent_element, locator_type, locator_value
):
    """Find the children elements by 'locator_type'

    If the 'parent_element' is a shadow element, set the 'locator_type' as 'id' or
    'css selector'
    """
    try:
        url = f"{driver_url}/session/{session}/element/{parent_element}/elements"
        payload = {"using": locator_type, "value": locator_value, "id": parent_element}
        response = __post(url, payload)
        return __helper.get_elements(response)
    except Exception as error:
        raise __WebDriverError(
            f"Failed to find the children elements from '{parent_element}'."
        ) from error


def find_child_element(
    driver_url, session, parent_element, locator_type, locator_value
):
    """Find the child element by 'locator_type'"""
    try:
        url = f"{driver_url}/session/{session}/element/{parent_element}/element"
        payload = {"using": locator_type, "value": locator_value, "id": parent_element}
        response = __post(url, payload)
        return __helper.get_element(response)
    except Exception as error:
        raise __WebDriverError(
            f"Failed to find the child element from '{parent_element}'."
        ) from error


def get_page_source(driver_url, session):
    """Get the page source (all content)"""
    try:
        url = f"{driver_url}/session/{session}/source"
        return __get(url).get("value")
    except Exception as error:
        raise __WebDriverError("Failed to get the page source.") from error


def execute_script(driver_url, session, script, args=[]):
    """Executes a script, like 'alert('something')' to open an alert window"""
    try:
        url = f"{driver_url}/session/{session}/execute/sync"
        payload = {"script": script, "args": args}
        response = __post(url, payload)
        return response.get("value")
    except Exception as error:
        raise __WebDriverError("Failed to run the script.") from error


def get_alert_text(driver_url, session):
    """Get the text from an alert"""
    try:
        url = f"{driver_url}/session/{session}/alert/text"
        return __get(url).get("value")
    except Exception as error:
        raise __WebDriverError("Failed to get the alert text.") from error


def get_active_element(driver_url, session):
    """Get the active element"""
    try:
        url = f"{driver_url}/session/{session}/element/active"
        response = __get(url)
        return __helper.get_element(response)
    except Exception as error:
        raise __WebDriverError("Failed to get the active element.") from error


def clear_element(driver_url, session, element):
    """Clear the element text"""
    try:
        url = f"{driver_url}/session/{session}/element/{element}/clear"
        payload = {"id": element}
        __post(url, payload)
        return True
    except Exception as error:
        raise __WebDriverError("Failed to clear the element text.") from error


def is_element_enabled(driver_url, session, element):
    """Check if element is enabled"""
    try:
        url = f"{driver_url}/session/{session}/element/{element}/enabled"
        return __get(url).get("value")
    except Exception as error:
        raise __WebDriverError("Failed to check if element is enabled.") from error


def get_css_value(driver_url, session, element, property_name):
    """Get the css property value"""
    try:
        url = f"{driver_url}/session/{session}/element/{element}/css/{property_name}"
        return __get(url).get("value")
    except Exception as error:
        raise __WebDriverError("Failed to get the css property value.") from error


def is_element_selected(driver_url, session, element):
    """Check if element is selected"""
    try:
        url = f"{driver_url}/session/{session}/element/{element}/selected"
        return __get(url).get("value")
    except Exception as error:
        raise __WebDriverError("Failed to check if element is selected.") from error


def get_window_rectangle(driver_url, session):
    """Get window rectangle"""
    try:
        url = f"{driver_url}/session/{session}/window/rect"
        return __get(url).get("value")
    except Exception as error:
        raise __WebDriverError("Failed to get window rectangle.") from error


def get_window_handles(driver_url, session):
    """Get window handles"""
    try:
        url = f"{driver_url}/session/{session}/window/handles"
        return __get(url).get("value")
    except Exception as error:
        raise __WebDriverError("Failed to get window handles.") from error


def close_window(driver_url, session):
    """Close active window"""
    try:
        url = f"{driver_url}/session/{session}/window"
        return __delete(url).get("value")
    except Exception as error:
        raise __WebDriverError("Failed to close active window.") from error


def get_window(driver_url, session):
    """Get window"""
    try:
        url = f"{driver_url}/session/{session}/window"
        return __get(url).get("value")
    except Exception as error:
        raise __WebDriverError("Failed to get window.") from error


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
        raise __WebDriverError("Failed to go back to page.") from error


def get_url(driver_url, session):
    """Return the URL from web page:"""
    try:
        url = f"{driver_url}/session/{session}/url"
        response = __get(url)
        return response.get("value")
    except Exception as error:
        raise __WebDriverError("Failed to get page url.") from error


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
        raise __WebDriverError("Failed to get timeouts.") from error


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
        raise __WebDriverError("Failed to get status.") from error


def get_title(driver_url, session):
    """Get the page title"""
    try:
        url = f"{driver_url}/session/{session}/title"
        response = __get(url)
        return response.get("value")
    except Exception as error:
        raise __WebDriverError("Failed to get page title.") from error


def find_elements(driver_url, session, locator_type, locator_value):
    """Search the DOM elements by 'locator', for example, 'xpath'"""
    try:
        url = f"{driver_url}/session/{session}/elements"
        payload = {"using": locator_type, "value": locator_value}
        response = __post(url, payload)
        return [x.get("ELEMENT") for x in response.get("value")]
    except Exception as error:
        raise __WebDriverError(
            f"Failed to find elements by '{locator_type}'-'{locator_value}'."
        ) from error


def get_property(driver_url, session, element, property_name):
    """Get the given HTML property of an element, for example, 'href'"""
    try:
        url = (
            f"{driver_url}/session/{session}/element/{element}/property/{property_name}"
        )
        response = __get(url)
        return response.get("value")
    except Exception as error:
        raise __WebDriverError("Failed to get value from element.") from error


def get_attribute(driver_url, session, element, attribute):
    """Get the given HTML attribute of an element, for example, 'aria-valuenow'"""
    try:
        url = f"{driver_url}/session/{session}/element/{element}/attribute/{attribute}"
        response = __get(url)
        return response.get("value")
    except Exception as error:
        raise __WebDriverError("Failed to get value from element.") from error


def get_cookies(driver_url, session):
    """Get the page cookies"""
    try:
        url = f"{driver_url}/session/{session}/cookie"
        response = __get(url)
        return response.get("value")
    except Exception as error:
        raise __WebDriverError("Failed to get page cookies.") from error


def get(driver_url, session, page_url):
    """Does the same of 'go_to_page'. Added to be compatible with selenium method name'"""
    return go_to_page(driver_url, session, page_url)


def go_to_page(driver_url, session, page_url):
    """Navigate to 'page_url'"""
    try:
        url = f"{driver_url}/session/{session}/url"
        payload = {"url": page_url}
        __post(url, payload)
        return True
    except Exception as error:
        raise __WebDriverError(f"Failed to navigate to '{page_url}'") from error


def close_session(driver_url, session):
    """Close an opened session and close the browser"""
    try:
        url = f"{driver_url}/session/{session}"
        __delete(url)
        return True
    except Exception as error:
        raise __WebDriverError("Failed to close session.") from error


def get_text(driver_url, session, element):
    """Get the text of an element"""
    try:
        url = f"{driver_url}/session/{session}/element/{element}/text"
        response = __get(url)
        return response.get("value")
    except Exception as error:
        raise __WebDriverError("Failed to get text from element.") from error


def send_keys(driver_url, session, element, text):
    """Fill an editable element, for example a textarea, with a given text"""
    try:
        url = f"{driver_url}/session/{session}/element/{element}/value"
        payload = {"text": text, "value": [*text], "id": element}
        __post(url, payload)
        return True
    except Exception as error:
        raise __WebDriverError(f"Failed to send key '{text}'.") from error


def click(driver_url, session, element):
    """Click on an element"""
    try:
        url = f"{driver_url}/session/{session}/element/{element}/click"
        payload = {"id": element}
        __post(url, payload)
        return True
    except Exception as error:
        raise __WebDriverError("Failed to click on element.") from error


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
        data = capabilities
        response = __post(url, payload=data)
        return __get_session(response)
    except Exception as error:
        raise __WebDriverError("Failed to open session.") from error


def find_element(driver_url, session, locator_type, locator_value):
    """Find an element by a 'locator', for example 'xpath'"""
    try:
        url = f"{driver_url}/session/{session}/element"
        payload = {"using": locator_type, "value": locator_value}
        response = __post(url, payload)

        # Firefox does not support id locator, so it prints the error message to the user
        # It helps on debug
        if response.get("value").get("error"):
            raise __WebDriverError(f"Failed to find element. {response}")

        return __helper.get_element(response)
    except Exception as error:
        raise __WebDriverError(
            f"Failed to find element by '{locator_type}'-'{locator_value}'."
        ) from error
