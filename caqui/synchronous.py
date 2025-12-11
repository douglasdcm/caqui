# Copyright (C) 2023 Caqui - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://github.com/douglasdcm/caqui

from typing import Any, Dict, List, Optional

from orjson import dumps
from requests import Response, request

from caqui.constants import ELEMENT_JSONWIRE, ELEMENT_W3C, HEADERS
from caqui.exceptions import WebDriverError
from caqui.helper import (
    convert_locator_to_css_selector,
    get_element,
    get_element_jsonwire,
    get_elements,
    save_picture,
)


def _handle_response(response) -> dict:
    """
    Handles synchronous responses from a WebDriver.

    The function checks if the response status code falls within the range of 200-399.
    If it does, it extracts the JSON response and raises an error with the status code and text.
    Otherwise, it raises an error with the status code, text, and details (if available).

    Parameters:
    response (dict): The WebDriver response to be handled.

    Returns:
    dict: The parsed response data.
    """
    result = None
    if response.status_code in range(200, 399):
        result = response.json()
    else:
        raise WebDriverError(f"Status: {response.status_code}, {response.text}")

    if int(result.get("status", 0)) > 0:
        raise WebDriverError(
            f"Status: {response.status_code}, {response.text}, Details: {result.get('value')}"
        )
    return result


def _get(url: str) -> Dict[str, Any]:
    try:
        response: Response = request("GET", url, headers=HEADERS, data={})
        return _handle_response(response)
    except Exception as e:
        raise WebDriverError("'GET' request failed.") from e


def _post(url: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    try:
        response: Response = request("POST", url, headers=HEADERS, data=dumps(payload), timeout=60)
        return _handle_response(response)
    except Exception as e:
        raise WebDriverError("'POST' request failed.") from e


def _delete(url: str) -> Dict[str, Any]:
    try:
        response: Response = request("DELETE", url, headers={}, data={})
        return _handle_response(response)
    except Exception as e:
        raise WebDriverError("'DELETE' request failed.") from e


def _handle_alerts(server_url: str, session: str, command: str) -> bool:
    url: str = f"{server_url}/session/{session}/alert/{command}"
    payload: Dict[str, str] = {"value": command}
    _post(url, payload)
    return True


def _handle_window(server_url: str, session: str, command: str) -> bool:
    url: str = f"{server_url}/session/{session}/window/{command}"
    payload: Dict[str, Any] = {}
    _post(url, payload)
    return True


def add_cookie(server_url: str, session: str, cookie: Dict[str, Any]) -> bool:
    """Add cookie"""
    try:
        url: str = f"{server_url}/session/{session}/cookie"
        payload: Dict[str, Dict[str, Any]] = {"cookie": cookie}
        _post(url, payload)
        return True
    except Exception as e:
        raise WebDriverError("Failed to add cookie.") from e


def delete_cookie(server_url: str, session: str, name: str) -> bool:
    """Delete cookie by name"""
    try:
        url: str = f"{server_url}/session/{session}/cookie/{name}"
        _delete(url)
        return True
    except Exception as e:
        raise WebDriverError("Failed to delete cookie '{name}'.") from e


def refresh_page(server_url: str, session: str) -> bool:
    """Refresh page"""
    try:
        url: str = f"{server_url}/session/{session}/refresh"
        payload: Dict[str, Any] = {}
        _post(url, payload)
        return True
    except Exception as e:
        raise WebDriverError("Failed to refresh page.") from e


def go_forward(server_url: str, session: str) -> bool:
    """Go to page forward"""
    try:
        url: str = f"{server_url}/session/{session}/forward"
        payload: Dict[str, Any] = {}
        _post(url, payload)
        return True
    except Exception as e:
        raise WebDriverError("Failed to go page forward.") from e


def set_window_rectangle(
    server_url: str, session: str, width: int, height: int, x: int, y: int
) -> bool:
    """Set window rectangle"""
    try:
        url: str = f"{server_url}/session/{session}/window/rect"
        payload: Dict[str, int] = {"width": width, "height": height, "x": x, "y": y}
        _post(url, payload)
        return True
    except Exception as e:
        raise WebDriverError("Failed to set window rectangle.") from e


def fullscreen_window(server_url: str, session: str) -> bool:
    """Fullscreen window"""
    try:
        return _handle_window(server_url, session, command="fullscreen")
    except Exception as e:
        raise WebDriverError("Failed to fullscreen window.") from e


def minimize_window(server_url: str, session: str) -> bool:
    """Minimize window"""
    try:
        return _handle_window(server_url, session, command="minimize")
    except Exception as e:
        raise WebDriverError("Failed to minimize window.") from e


def maximize_window(server_url: str, session: str) -> bool:
    """Maximize window"""
    try:
        return _handle_window(server_url, session, command="maximize")
    except Exception as e:
        raise WebDriverError("Failed to maximize window.") from e


def switch_to_window(server_url: str, session: str, handle: str) -> bool:
    """Switch to window"""
    try:
        url: str = f"{server_url}/session/{session}/window"
        payload: Dict[str, str] = {"handle": handle}
        _post(url, payload)
        return True
    except Exception as e:
        raise WebDriverError("Failed to switch to window.") from e


def switch_to_window_jsonwire(server_url: str, session: str, handle: str) -> bool:
    """Switch to window"""
    try:
        url: str = f"{server_url}/session/{session}/window"
        payload: Dict[str, str] = {"name": handle}
        _post(url, payload)
        return True
    except Exception as e:
        raise WebDriverError("Failed to switch to window.") from e


def new_window(server_url: str, session: str, window_type: str = "tab") -> str:
    """Open a new window
    :param window_type (str): tab or window

    return (str): window handle
    """
    try:
        url: str = f"{server_url}/session/{session}/window/new"
        payload: Dict[str, str] = {"type": window_type}
        return _post(url, payload).get("value", {}).get("handle")
    except Exception as e:
        raise WebDriverError("Failed to open a new window.") from e


def switch_to_parent_frame(server_url: str, session: str, element_frame: str) -> bool:
    """Switch to parent frame of 'element_frame'"""
    try:
        url: str = f"{server_url}/session/{session}/frame/parent"
        payload: Dict[str, Dict[str, str]] = {"id": {ELEMENT_W3C: element_frame}}
        _post(url, payload)
        return True
    except Exception as e:
        raise WebDriverError("Failed to switch to parent frame.") from e


def switch_to_parent_frame_jsonwire(server_url: str, session: str, element_frame: str) -> bool:
    """Switch to parent frame of 'element_frame'"""
    try:
        url: str = f"{server_url}/session/{session}/frame/parent"
        payload: Dict[str, Dict[str, str]] = {"id": {ELEMENT_JSONWIRE: element_frame}}
        _post(url, payload)
        return True
    except Exception as e:
        raise WebDriverError("Failed to switch to parent frame.") from e


def switch_to_frame(server_url: str, session: str, element_frame: str) -> bool:
    """Switch to frame 'element_frame'"""
    try:
        url: str = f"{server_url}/session/{session}/frame"
        payload: Dict[str, Dict[str, str]] = {"id": {ELEMENT_W3C: element_frame}}
        _post(url, payload)
        return True
    except Exception as e:
        raise WebDriverError("Failed to switch to frame.") from e


def switch_to_frame_jsonwire(server_url: str, session: str, element_frame: str) -> bool:
    """Switch to frame 'element_frame'"""
    try:
        url: str = f"{server_url}/session/{session}/frame"
        payload: Dict[str, Dict[str, str]] = {"id": {ELEMENT_JSONWIRE: element_frame}}
        _post(url, payload)
        return True
    except Exception as e:
        raise WebDriverError("Failed to switch to frame.") from e


def delete_all_cookies(server_url: str, session: str) -> bool:
    """Delete all cookies"""
    try:
        url: str = f"{server_url}/session/{session}/cookie"
        _delete(url)
        return True
    except Exception as e:
        raise WebDriverError("Failed to delete cookies.") from e


def send_alert_text(server_url: str, session: str, text: str) -> bool:
    """Fill the alert text area and send the text"""
    try:
        url: str = f"{server_url}/session/{session}/alert/text"
        payload: Dict[str, str] = {"text": text}
        _post(url, payload)
        return True
    except Exception as e:
        raise WebDriverError("Failed to sent text to alert.") from e


def accept_alert(server_url: str, session: str) -> bool:
    """Accept an alert"""
    try:
        return _handle_alerts(server_url, session, "accept")
    except Exception as e:
        raise WebDriverError("Failed to accept the alert.") from e


def dismiss_alert(server_url: str, session: str) -> bool:
    """Dismiss an alert"""
    try:
        return _handle_alerts(server_url, session, "dismiss")
    except Exception as e:
        raise WebDriverError("Failed to dismiss the alert.") from e


def take_screenshot_element(
    server_url: str, session: str, element: str, path: str = "/tmp", file_name: str = "caqui"
) -> bool:
    """Take screenshot of element."""
    try:
        url: str = f"{server_url}/session/{session}/element/{element}/screenshot"
        response: Any = _get(url).get("value")
        save_picture(session, path, file_name, response)
        return True
    except Exception as e:
        raise WebDriverError("Failed to take screeshot.") from e


def take_screenshot(
    server_url: str, session: str, path: str = "/tmp", file_name: str = "caqui"
) -> bool:
    """Take screenshot."""
    try:
        url: str = f"{server_url}/session/{session}/screenshot"
        response: Any = _get(url).get("value")
        save_picture(session, path, file_name, response)
        return True
    except Exception as e:
        raise WebDriverError("Failed to take screeshot.") from e


def get_named_cookie(server_url: str, session: str, name: str) -> Optional[Dict[str, Any]]:
    """Get cookie by name."""
    try:
        url: str = f"{server_url}/session/{session}/cookie/{name}"
        return _get(url).get("value")
    except Exception as e:
        raise WebDriverError(f"Failed to get the cookie '{name}'.") from e


def get_computed_label(server_url: str, session: str, element: str) -> str:
    """Get the element computed label. Get the accessibility name."""
    try:
        url: str = f"{server_url}/session/{session}/element/{element}/computedlabel"
        return _get(url).get("value", "")
    except Exception as e:
        raise WebDriverError("Failed to get the element computed label.") from e


def get_computed_role(server_url: str, session: str, element: str) -> str:
    """Get the element computed role (the element role)"""
    try:
        url: str = f"{server_url}/session/{session}/element/{element}/computedrole"
        return _get(url).get("value", "")
    except Exception as e:
        raise WebDriverError("Failed to get the element computed role.") from e


def get_tag_name(server_url: str, session: str, element: str) -> str:
    """Get the element tag name"""
    try:
        url: str = f"{server_url}/session/{session}/element/{element}/name"
        return _get(url).get("value", "")
    except Exception as e:
        raise WebDriverError("Failed to get the element name.") from e


def get_shadow_root(server_url: str, session: str, element: str) -> str:
    """Get the shadow root element"""
    try:
        root_element: str = "shadow-6066-11e4-a52e-4f735466cecf"
        url: str = f"{server_url}/session/{session}/element/{element}/shadow"
        return _get(url).get("value", {}).get(root_element)
    except Exception as e:
        raise WebDriverError("Failed to get the root shadow element.") from e


def get_shadow_element(
    server_url: str, session: str, shadow_element: str, locator_type: str, locator_value: str
) -> str:
    """Get the shadow root element"""
    try:
        locator_type, locator_value = convert_locator_to_css_selector(locator_type, locator_value)
        url: str = f"{server_url}/session/{session}/shadow/{shadow_element}/element"
        payload: Dict[str, str] = {"using": locator_type, "value": locator_value}
        response: Dict[str, Any] = _post(url, payload)
        return response.get("value", {}).get(ELEMENT_W3C, "")
    except Exception as e:
        raise WebDriverError("Failed to get the element shadow.") from e


def get_shadow_element_jsonwire(
    server_url: str, session: str, shadow_element: str, locator_type: str, locator_value: str
) -> str:
    """Get the shadow root element"""
    try:
        locator_type, locator_value = convert_locator_to_css_selector(locator_type, locator_value)
        url: str = f"{server_url}/session/{session}/shadow/{shadow_element}/element"
        payload: Dict[str, str] = {"using": locator_type, "value": locator_value}
        response: Dict[str, Any] = _post(url, payload)
        return response.get("value", {}).get(ELEMENT_JSONWIRE, "")
    except Exception as e:
        raise WebDriverError("Failed to get the element shadow.") from e


def get_shadow_elements(
    server_url: str, session: str, shadow_element: str, locator_type: str, locator_value: str
) -> List[str]:
    """Get the list of shadow root element"""
    try:
        locator_type, locator_value = convert_locator_to_css_selector(locator_type, locator_value)
        url: str = f"{server_url}/session/{session}/shadow/{shadow_element}/elements"
        payload: Dict[str, str] = {"using": locator_type, "value": locator_value}
        response: Dict[str, Any] = _post(url, payload)
        return [x.get(ELEMENT_W3C) for x in response.get("value", {})]
    except Exception as e:
        raise WebDriverError("Failed to get the element shadow.") from e


def get_shadow_elements_jsonwire(
    server_url: str, session: str, shadow_element: str, locator_type: str, locator_value: str
) -> List[str]:
    """Get the list of shadow root element"""
    try:
        locator_type, locator_value = convert_locator_to_css_selector(locator_type, locator_value)
        url: str = f"{server_url}/session/{session}/shadow/{shadow_element}/elements"
        payload: Dict[str, str] = {"using": locator_type, "value": locator_value}
        response: Dict[str, Any] = _post(url, payload)
        return [x.get(ELEMENT_JSONWIRE) for x in response.get("value", {})]
    except Exception as e:
        raise WebDriverError("Failed to get the element shadow.") from e


def get_rect(server_url: str, session: str, element: str) -> Dict[str, Any]:
    """Get the element rectangle"""
    try:
        url: str = f"{server_url}/session/{session}/element/{element}/rect"
        return _get(url).get("value", {})
    except Exception as e:
        raise WebDriverError("Failed to get the element rect.") from e


def actions_move_to_element(server_url: str, session: str, element: str) -> bool:
    """Move to an element simulating a mouse movement"""
    try:
        payload: Dict[str, List[Dict[str, Any]]] = {
            "actions": [
                {
                    "type": "pointer",
                    "parameters": {"pointerType": "mouse"},
                    "id": "mouse",
                    "actions": [
                        {
                            "type": "pointerMove",
                            "duration": 0,
                            "x": 0,
                            "y": 0,
                            "origin": {ELEMENT_W3C: element},
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
        return actions(server_url, session, payload)
    except Exception as e:
        raise WebDriverError("Failed to move to element.") from e


def actions_move_to_element_jsonwire(server_url: str, session: str, element: str) -> bool:
    """Move to an element simulating a mouse movement"""
    try:
        payload: Dict[str, List[Dict[str, Any]]] = {
            "actions": [
                {
                    "type": "pointer",
                    "parameters": {"pointerType": "mouse"},
                    "id": "mouse",
                    "actions": [
                        {
                            "type": "pointerMove",
                            "duration": 0,
                            "x": 0,
                            "y": 0,
                            "origin": {ELEMENT_JSONWIRE: element},
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
        return actions(server_url, session, payload)
    except Exception as e:
        raise WebDriverError("Failed to move to element.") from e


def actions_scroll_to_element(server_url: str, session: str, element: str, delta_y=1000) -> bool:
    """Scroll to an element simulating a mouse movement"""
    try:
        payload: Dict[str, List[Dict[str, Any]]] = {
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
                            "deltaY": delta_y,
                            "duration": 0,
                            "origin": {ELEMENT_W3C: element},
                        }
                    ],
                }
            ]
        }
        return actions(server_url, session, payload)
    except Exception as e:
        raise WebDriverError("Failed to scroll to element.") from e


def actions_scroll_to_element_jsonwire(
    server_url: str, session: str, element: str, delta_y=1000
) -> bool:
    """Scroll to an element simulating a mouse movement"""
    try:
        payload: Dict[str, List[Dict[str, Any]]] = {
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
                            "deltaY": delta_y,
                            "duration": 0,
                            "origin": {ELEMENT_JSONWIRE: element},
                        }
                    ],
                }
            ]
        }
        return actions(server_url, session, payload)
    except Exception as e:
        raise WebDriverError("Failed to scroll to element.") from e


def actions(server_url: str, session: str, payload: Dict[str, Any]) -> bool:
    url: str = f"{server_url}/session/{session}/actions"
    _post(url, payload)
    return True


def submit(server_url: str, session: str, element: str) -> bool:
    """Submit a form. It is similar to 'submit' funtion in Seleniu
    It is not part of W3C WebDriver. Just added for convenience
    """
    try:
        submit_element: str = find_child_element(
            server_url,
            session,
            element,
            locator_type="xpath",
            locator_value="//*[@type='submit']",
        )
        return click(server_url, session, submit_element)
    except Exception as e:
        raise WebDriverError("Failed to submit form.") from e


def actions_click(server_url: str, session: str, element: str) -> bool:
    """Click an element simulating a mouse movement"""
    try:
        payload: Dict[str, List[Dict[str, Any]]] = {
            "actions": [
                {
                    "type": "pointer",
                    "parameters": {"pointerType": "mouse"},
                    "id": "mouse",
                    "actions": [
                        {
                            "type": "pointerMove",
                            "duration": 0,
                            "x": 0,
                            "y": 0,
                            "origin": {ELEMENT_W3C: element},
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
        return actions(server_url, session, payload)
    except Exception as e:
        raise WebDriverError("Failed to click the element.") from e


def actions_click_jsonwire(server_url: str, session: str, element: str) -> bool:
    """Click an element simulating a mouse movement"""
    try:
        payload: Dict[str, List[Dict[str, Any]]] = {
            "actions": [
                {
                    "type": "pointer",
                    "parameters": {"pointerType": "mouse"},
                    "id": "mouse",
                    "actions": [
                        {
                            "type": "pointerMove",
                            "duration": 0,
                            "x": 0,
                            "y": 0,
                            "origin": {ELEMENT_JSONWIRE: element},
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
        return actions(server_url, session, payload)
    except Exception as e:
        raise WebDriverError("Failed to click the element.") from e


def set_timeouts(server_url: str, session: str, timeouts: int) -> bool:
    """Set timeouts"""
    try:
        url: str = f"{server_url}/session/{session}/timeouts"
        payload: Dict[str, int] = {
            "implicit": timeouts,
        }
        _post(url, payload)
        return True
    except Exception as e:
        raise WebDriverError("Failed to set timeouts.") from e


def find_children_elements(
    server_url: str, session: str, parent_element: str, locator_type: str, locator_value: str
) -> List[str]:
    """Find the children elements by 'locator_type'

    If the 'parent_element' is a shadow element, set the 'locator_type' as 'id' or
    'css selector'
    """
    locator_type, locator_value = convert_locator_to_css_selector(locator_type, locator_value)
    try:
        url: str = f"{server_url}/session/{session}/element/{parent_element}/elements"
        payload: Dict[str, str] = {
            "using": locator_type,
            "value": locator_value,
            "id": parent_element,
        }
        response: Dict[str, Any] = _post(url, payload)
        return get_elements(response)
    except Exception as e:
        raise WebDriverError(
            f"Failed to find the children elements from '{parent_element}'."
        ) from e


def find_child_element(
    server_url: str, session: str, parent_element: str, locator_type: str, locator_value: str
) -> str:
    """Find the child element by 'locator_type'"""
    locator_type, locator_value = convert_locator_to_css_selector(locator_type, locator_value)
    try:
        url: str = f"{server_url}/session/{session}/element/{parent_element}/element"
        payload: Dict[str, str] = {
            "using": locator_type,
            "value": locator_value,
            "id": parent_element,
        }
        response: Dict[str, Any] = _post(url, payload)
        return get_element(response)
    except Exception as e:
        raise WebDriverError(f"Failed to find the child element from '{parent_element}'.") from e


def get_page_source(server_url: str, session: str) -> str:
    """Get the page source (all content)"""
    try:
        url: str = f"{server_url}/session/{session}/source"
        return _get(url).get("value", "")
    except Exception as e:
        raise WebDriverError("Failed to get the page source.") from e


def execute_script(server_url: str, session: str, script: str, args: List[Any] = []) -> Any:
    """Executes a script, like 'alert('something')' to open an alert window"""
    try:
        url: str = f"{server_url}/session/{session}/execute/sync"
        payload: Dict[str, Any] = {"script": script, "args": args}
        response: Dict[str, Any] = _post(url, payload)
        return response.get("value")
    except Exception as e:
        raise WebDriverError("Failed to run the script.") from e


def get_alert_text(server_url: str, session: str) -> str:
    """Get the text from an alert"""
    try:
        url: str = f"{server_url}/session/{session}/alert/text"
        return _get(url).get("value", "")
    except Exception as e:
        raise WebDriverError("Failed to get the alert text.") from e


def get_active_element(server_url: str, session: str) -> str:
    """Get the active element"""
    try:
        url: str = f"{server_url}/session/{session}/element/active"
        response: Dict[str, Any] = _get(url)
        return get_element(response)
    except Exception as e:
        raise WebDriverError("Failed to get the active element.") from e


def get_active_element_jsonwire(server_url: str, session: str) -> str:
    """Get the active element"""
    try:
        url: str = f"{server_url}/session/{session}/element/active"
        response: Dict[str, Any] = _get(url)
        return get_element_jsonwire(response)
    except Exception as e:
        raise WebDriverError("Failed to get the active element.") from e


def clear_element(server_url: str, session: str, element: str) -> bool:
    """Clear the element text"""
    try:
        url: str = f"{server_url}/session/{session}/element/{element}/clear"
        payload: Dict[str, str] = {"id": element}
        _post(url, payload)
        return True
    except Exception as e:
        raise WebDriverError("Failed to clear the element text.") from e


def is_element_enabled(server_url: str, session: str, element: str) -> bool:
    """Check if element is enabled"""
    try:
        url: str = f"{server_url}/session/{session}/element/{element}/enabled"
        return _get(url).get("value", False)
    except Exception as e:
        raise WebDriverError("Failed to check if element is enabled.") from e


def get_css_value(server_url: str, session: str, element: str, property_name: str) -> str:
    """Get the css property value"""
    try:
        url: str = f"{server_url}/session/{session}/element/{element}/css/{property_name}"
        return _get(url).get("value", "")
    except Exception as e:
        raise WebDriverError("Failed to get the css property value.") from e


def is_element_selected(server_url: str, session: str, element: str) -> bool:
    """Check if element is selected"""
    try:
        url: str = f"{server_url}/session/{session}/element/{element}/selected"
        return _get(url).get("value", False)
    except Exception as e:
        raise WebDriverError("Failed to check if element is selected.") from e


def get_window_rectangle(server_url: str, session: str) -> Dict[str, Any]:
    """Get window rectangle"""
    try:
        url: str = f"{server_url}/session/{session}/window/rect"
        return _get(url).get("value", {})
    except Exception as e:
        raise WebDriverError("Failed to get window rectangle.") from e


def get_window_handles(server_url: str, session: str) -> List[str]:
    """Get window handles"""
    try:
        url: str = f"{server_url}/session/{session}/window/handles"
        return _get(url).get("value", [])
    except Exception as e:
        raise WebDriverError("Failed to get window handles.") from e


def close_window(server_url: str, session: str) -> Optional[List[str]]:
    """Close active window"""
    try:
        url: str = f"{server_url}/session/{session}/window"
        return _delete(url).get("value")
    except Exception as e:
        raise WebDriverError("Failed to close active window.") from e


def get_window(server_url: str, session: str) -> str:
    """Get window"""
    try:
        url: str = f"{server_url}/session/{session}/window"
        return _get(url).get("value", "")
    except Exception as e:
        raise WebDriverError("Failed to get window.") from e


def go_back(server_url: str, session: str) -> bool:
    """
    This command causes the browser to traverse one step backward
    in the joint session history of the
    current browse. This is equivalent to pressing the back button in the browser.
    """
    try:
        url: str = f"{server_url}/session/{session}/back"
        _post(url, {})
        return True
    except Exception as e:
        raise WebDriverError("Failed to go back to page.") from e


def get_url(server_url: str, session: str) -> str:
    """Return the URL from web page:"""
    try:
        url: str = f"{server_url}/session/{session}/url"
        response: Dict[str, Any] = _get(url)
        return response.get("value", "")
    except Exception as e:
        raise WebDriverError("Failed to get page url.") from e


def get_timeouts(server_url: str, session: str) -> Dict[str, Any]:
    """
    Return the configured timeouts:
        {"implicit": 0, "pageLoad": 300000, "script": 30000}
    """
    try:
        url: str = f"{server_url}/session/{session}/timeouts"
        response: Dict[str, Any] = _get(url)
        return response.get("value", {})
    except Exception as e:
        raise WebDriverError("Failed to get timeouts.") from e


def get_status(server_url: str) -> Dict[str, Any]:
    """Return the status and details of the WebDriver:"""
    try:
        url: str = f"{server_url}/status"
        return _get(url)
    except Exception as e:
        raise WebDriverError("Failed to get status.") from e


def get_title(server_url: str, session: str) -> str:
    """Get the page title"""
    try:
        url: str = f"{server_url}/session/{session}/title"
        response: Dict[str, Any] = _get(url)
        return response.get("value", "")
    except Exception as e:
        raise WebDriverError("Failed to get page title.") from e


def find_elements(
    server_url: str, session: str, locator_type: str, locator_value: str
) -> List[str]:
    """Search the DOM elements by 'locator', for example, 'xpath'"""
    locator_type, locator_value = convert_locator_to_css_selector(locator_type, locator_value)
    try:
        url: str = f"{server_url}/session/{session}/elements"
        payload: Dict[str, str] = {"using": locator_type, "value": locator_value}
        response: Dict[str, Any] = _post(url, payload)
        return [x.get(ELEMENT_W3C) for x in response.get("value", {})]
    except Exception as e:
        raise WebDriverError(
            f"Failed to find elements by '{locator_type}'-'{locator_value}'."
        ) from e


def find_elements_jsonwire(
    server_url: str, session: str, locator_type: str, locator_value: str
) -> List[str]:
    """Search the DOM elements by 'locator', for example, 'xpath'"""
    locator_type, locator_value = convert_locator_to_css_selector(locator_type, locator_value)
    try:
        url: str = f"{server_url}/session/{session}/elements"
        payload: Dict[str, str] = {"using": locator_type, "value": locator_value}
        response: Dict[str, Any] = _post(url, payload)
        return [x.get(ELEMENT_JSONWIRE) for x in response.get("value", {})]
    except Exception as e:
        raise WebDriverError(
            f"Failed to find elements by '{locator_type}'-'{locator_value}'."
        ) from e


def get_property(server_url: str, session: str, element: str, property_name: str) -> Any:
    """Get the given HTML property of an element, for example, 'href'"""
    try:
        url: str = f"{server_url}/session/{session}/element/{element}/property/{property_name}"
        response: Dict[str, Any] = _get(url)
        return response.get("value")
    except Exception as e:
        raise WebDriverError("Failed to get value from element.") from e


def get_attribute(server_url: str, session: str, element: str, attribute: str) -> str:
    """Get the given HTML attribute of an element, for example, 'aria-valuenow'"""
    try:
        url: str = f"{server_url}/session/{session}/element/{element}/attribute/{attribute}"
        response: Dict[str, Any] = _get(url)
        if not response.get("value"):
            return ""
        return response.get("value", "")
    except Exception as e:
        raise WebDriverError("Failed to get value from element.") from e


def get_cookies(server_url: str, session: str) -> List[Dict[str, Any]]:
    """Get the page cookies"""
    try:
        url: str = f"{server_url}/session/{session}/cookie"
        response: Dict[str, Any] = _get(url)
        return response.get("value", [])
    except Exception as e:
        raise WebDriverError("Failed to get page cookies.") from e


def get(server_url: str, session: str, page_url: str) -> bool:
    """Does the same of 'go_to_page'. Added to be compatible with selenium method name'"""
    return go_to_page(server_url, session, page_url)


def go_to_page(server_url: str, session: str, page_url: str) -> bool:
    """Navigate to 'page_url'"""
    try:
        url: str = f"{server_url}/session/{session}/url"
        payload: Dict[str, str] = {"url": page_url}
        _post(url, payload)
        return True
    except Exception as e:
        raise WebDriverError(f"Failed to navigate to '{page_url}'") from e


def close_session(server_url: str, session: str) -> bool:
    """Close an opened session and close the browser"""
    # from requests import head
    # head(server_url, timeout=30)
    try:
        url: str = f"{server_url}/session/{session}"
        _delete(url)
        return True
    except Exception as e:
        raise WebDriverError("Failed to close session.") from e


def get_text(server_url: str, session: str, element: str) -> str:
    """Get the text of an element"""
    try:
        url: str = f"{server_url}/session/{session}/element/{element}/text"
        response: Dict[str, Any] = _get(url)
        return response.get("value", "")
    except Exception as e:
        raise WebDriverError("Failed to get text from element.") from e


def send_keys(server_url: str, session: str, element: str, text: str) -> bool:
    """Fill an editable element, for example a textarea, with a given text"""
    try:
        url: str = f"{server_url}/session/{session}/element/{element}/value"
        payload: Dict[str, Any] = {"text": text, "value": [*text], "id": element}
        _post(url, payload)
        return True
    except Exception as e:
        raise WebDriverError(f"Failed to send key '{text}'.") from e


def click(server_url: str, session: str, element: str) -> bool:
    """Click on an element"""
    try:
        url: str = f"{server_url}/session/{session}/element/{element}/click"
        payload: Dict[str, str] = {"id": element}
        _post(url, payload)
        return True
    except Exception as e:
        raise WebDriverError("Failed to click on element.") from e


def _get_session(response: Dict[str, Any]) -> str:
    # Firefox response
    value: Dict[str, Any] = response.get("value", {})
    session_id: str = value.get("sessionId", "")
    if session_id:
        return session_id

    # Chrome response
    return response.get("sessionId", "")


def get_session(server_url: str, capabilities: Optional[Dict[str, Any]] = None) -> str:
    """
    Opens a browser and a session.
     This session is used for all functions to perform events in the page
    """
    try:
        url: str = f"{server_url}/session"
        if not capabilities:
            capabilities = {}
        response: Dict[str, Any] = _post(url, payload=capabilities)
        return _get_session(response)
    except Exception as e:
        raise WebDriverError("Failed to open session. Check the browser capabilities.") from e


def find_element(server_url: str, session: str, locator_type: str, locator_value: str) -> str:
    """Find an element by a 'locator', for example 'xpath'"""
    locator_type, locator_value = convert_locator_to_css_selector(locator_type, locator_value)
    try:
        url: str = f"{server_url}/session/{session}/element"
        payload: Dict[str, str] = {"using": locator_type, "value": locator_value}
        response: Dict[str, Any] = _post(url, payload)

        # Firefox does not support id locator, so it prints the error message to the user
        # It helps on debug
        if response.get("value", {}).get("error"):
            raise WebDriverError(f"Failed to find element. {response}")

        return get_element(response)
    except Exception as e:
        raise WebDriverError(
            f"Failed to find element by '{locator_type}'-'{locator_value}'."
        ) from e
