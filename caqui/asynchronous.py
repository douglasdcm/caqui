# Copyright (C) 2023 Caqui - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://github.com/douglasdcm/caqui

from typing import Any, Dict, List, Optional, Union

from aiohttp import ClientSession
from orjson import dumps

from caqui.constants import ELEMENT_JSONWIRE, ELEMENT_W3C, HEADERS
from caqui.exceptions import WebDriverError
from caqui.helper import (
    convert_locator_to_css_selector,
    get_element,
    get_element_jsonwire,
    get_elements,
    save_picture,
)


async def _handle_response(resp) -> Any:
    """
    Handles the HTTP response from the WebDriver server.

    Args:
        resp: The HTTP response object.

    Returns:
        The parsed JSON result from the response.

    Raises:
        WebDriverError: If the response status is not successful or contains an error.
    """
    result = None
    if resp.status in range(200, 399):
        result = await resp.json()
    else:
        raise WebDriverError(f"Status code: {resp.status}, Body: {resp.text}")

    if int(result.get("status", 0)) > 0:
        raise WebDriverError(
            f"Status code: {resp.status}, Body: {resp.text}, Details: {result.get('value')}"
        )

    return result


async def _delete(url, session_http: Union[ClientSession, None] = None):
    """
    Sends a DELETE request to the WebDriver server.

    Args:
        url (str): The endpoint URL.
        session_http (ClientSession, optional): An existing aiohttp session.

    Returns:
        The parsed JSON result from the response.

    Raises:
        WebDriverError: If the request fails.
    """
    if session_http:
        try:
            async with session_http.delete(url, headers=HEADERS) as resp:
                return await _handle_response(resp)
        except Exception as e:
            raise WebDriverError("'DELETE' request failed.") from e

    else:
        try:
            async with ClientSession() as session_http:
                async with session_http.delete(url, headers=HEADERS) as resp:
                    return await _handle_response(resp)
        except Exception as e:
            raise WebDriverError("'DELETE' request failed.") from e


async def _post(url, payload: dict, session_http: Union[ClientSession, None] = None):
    """
    Sends a POST request to the WebDriver server.

    Args:
        url (str): The endpoint URL.
        payload (dict): The data to send in the request body.
        session_http (ClientSession, optional): An existing aiohttp session.

    Returns:
        The parsed JSON result from the response.

    Raises:
        WebDriverError: If the request fails.
    """
    if session_http:
        try:
            async with session_http.post(url, data=dumps(payload), headers=HEADERS) as resp:
                return await _handle_response(resp)
        except Exception as e:
            raise WebDriverError("'POST' request failed.") from e
    else:
        try:
            async with ClientSession() as session_http:
                async with session_http.post(url, data=dumps(payload), headers=HEADERS) as resp:
                    return await _handle_response(resp)
        except Exception as e:
            raise WebDriverError("'POST' request failed.") from e


async def _get(url: str, session_http: Union[ClientSession, None] = None) -> dict:
    """
    Sends a GET request to the WebDriver server.

    Args:
        url (str): The endpoint URL.
        session_http (ClientSession, optional): An existing aiohttp session.

    Returns:
        dict: The parsed JSON result from the response.

    Raises:
        WebDriverError: If the request fails.
    """
    if session_http:
        try:
            async with session_http.get(url, headers=HEADERS) as resp:
                return await _handle_response(resp)
        except Exception as e:
            raise WebDriverError("'GET' request failed.") from e
    else:
        try:
            async with ClientSession() as session_http:
                async with session_http.get(url, headers=HEADERS) as resp:
                    return await _handle_response(resp)
        except Exception as e:
            raise WebDriverError("'GET' request failed.") from e


async def _handle_alert(server_url, session, command, session_http) -> bool:
    """
    Handles alert actions (accept/dismiss) for the current session.

    Args:
        server_url (str): The WebDriver server URL.
        session (str): The session ID.
        command (str): The alert command ('accept' or 'dismiss').
        session_http (ClientSession): An existing aiohttp session.

    Returns:
        bool: True if the alert was handled successfully.
    """
    url = f"{server_url}/session/{session}/alert/{command}"
    payload = {
        "value": command,
    }
    await _post(url, payload, session_http=session_http)
    return True


async def _handle_window(
    server_url, session, command, session_http: Union[ClientSession, None] = None
):
    """
    Handles window actions (fullscreen, minimize, maximize) for the current session.

    Args:
        server_url (str): The WebDriver server URL.
        session (str): The session ID.
        command (str): The window command.
        session_http (ClientSession, optional): An existing aiohttp session.

    Returns:
        bool: True if the window action was successful.
    """
    url = f"{server_url}/session/{session}/window/{command}"
    payload: dict = {}
    await _post(url, payload, session_http=session_http)
    return True


async def add_cookie(server_url, session, cookie, session_http: Union[ClientSession, None] = None):
    """Add cookie"""
    try:
        url = f"{server_url}/session/{session}/cookie"
        payload = {"cookie": cookie}
        await _post(url, payload, session_http=session_http)
        return True
    except Exception as e:
        raise WebDriverError("Failed to add cookie.") from e


async def delete_cookie(server_url, session, name, session_http: Union[ClientSession, None] = None):
    """
    Delete cookie by name

    This function deletes a cookie with the specified name from the WebDriver session.
    Based on W3C WebDriver Specification.

    Args:
        server_url: The base URL of the WebDriver server
        session: The session identifier for the WebDriver session
        name: The name of the cookie to delete
        session_http: Optional HTTP client session for making requests.
        If not provided, a default session will be used

    Returns:
        True if the cookie was successfully deleted

    Raises:
        WebDriverError: If the cookie deletion fails
    """
    try:
        url = f"{server_url}/session/{session}/cookie/{name}"
        await _delete(url, session_http)
        return True
    except Exception as e:
        raise WebDriverError(f"Failed to delete cookie '{name}'.") from e


async def refresh_page(server_url, session, session_http: Union[ClientSession, None] = None):
    """
    Refreshes the current page by making an HTTP POST request to the server URL.

    Args:
        server_url (str): The base URL of the server.
        session (Session or None): The current session object.
        If not provided, a new one will be created.
        session_http (ClientSession or None, optional): An existing client
        session object. Defaults to None.

    Returns:
        bool: True if the refresh operation was successful, False otherwise.
    """
    try:
        url = f"{server_url}/session/{session}/refresh"
        payload: dict = {}
        await _post(url, payload, session_http=session_http)
        return True
    except Exception as e:
        raise WebDriverError("Failed to refresh page.") from e


async def go_forward(server_url, session, session_http: Union[ClientSession, None] = None):
    """
    Go to page forward.

    This function sends a POST request to the specified URL,
    with an empty payload, and returns True if successful.

    Parameters:
        server_url (str): The base URL of the server.
        session (Session or None): The current session.
        If not provided, it will be obtained from the session HTTP object.
        session_http (ClientSession or None): An optional ClientSession object to use for
        the POST request. Defaults to None.

    Returns:
        bool: True if the page forward operation is successful, False otherwise.
    """
    try:
        url = f"{server_url}/session/{session}/forward"
        payload: dict = {}
        await _post(url, payload, session_http=session_http)
        return True
    except Exception as e:
        raise WebDriverError("Failed to go to page forward.") from e


async def set_window_rectangle(
    server_url: str,
    session: str,
    width: int,
    height: int,
    x: int,
    y: int,
    session_http: Union[ClientSession, None] = None,
):
    """
    Set window rectangle.

    This function sets the window size and position based on W3C WebDriver Specification.

    Args:
        server_url: The base URL of the WebDriver server
        session: The session identifier for the WebDriver session
        width: The desired window width in pixels
        height: The desired window height in pixels
        x: The desired window x coordinate
        y: The desired window y coordinate
        session_http: Optional HTTP client session for making requests.
        If not provided, a default session will be used

    Returns:
        True if the window rectangle was successfully set

    Raises:
        WebDriverError: If the window rectangle setting fails
    """
    try:
        url = f"{server_url}/session/{session}/window/rect"
        payload = {"width": width, "height": height, "x": x, "y": y}
        await _post(url, payload, session_http=session_http)
        return True
    except Exception as e:
        raise WebDriverError("Failed to set window rectangle.") from e


async def fullscreen_window(
    server_url: str, session: str, session_http: Union[ClientSession, None] = None
):
    """
    Fullscreen window.

    This function fullscreens the window based on W3C WebDriver Specification.

    Args:
        server_url: The base URL of the WebDriver server
        session: The session identifier for the WebDriver session
        session_http: Optional HTTP client session for making requests.
        If not provided, a default session will be used

    Returns:
        True if the window was successfully fullscreened

    Raises:
        WebDriverError: If the fullscreen operation fails
    """
    try:
        return await _handle_window(
            server_url, session, command="fullscreen", session_http=session_http
        )
    except Exception as e:
        raise WebDriverError("Failed to fullscreen window.") from e


async def minimize_window(
    server_url: str, session: str, session_http: Union[ClientSession, None] = None
):
    """
    Minimize window.

    This function minimizes the window based on W3C WebDriver Specification.

    Args:
        server_url: The base URL of the WebDriver server
        session: The session identifier for the WebDriver session
        session_http: Optional HTTP client session for making requests.
        If not provided, a default session will be used

    Returns:
        True if the window was successfully minimized

    Raises:
        WebDriverError: If the minimize operation fails
    """
    try:
        return await _handle_window(
            server_url, session, command="minimize", session_http=session_http
        )
    except Exception as e:
        raise WebDriverError("Failed to minimize window.") from e


async def maximize_window(
    server_url: str, session: str, session_http: Union[ClientSession, None] = None
):
    """
    Maximize window.

    This function maximizes the window based on W3C WebDriver Specification.

    Args:
        server_url: The base URL of the WebDriver server
        session: The session identifier for the WebDriver session
        session_http: Optional HTTP client session for making requests.
        If not provided, a default session will be used

    Returns:
        True if the window was successfully maximized

    Raises:
        WebDriverError: If the maximize operation fails
    """
    try:
        return await _handle_window(
            server_url, session, command="maximize", session_http=session_http
        )
    except Exception as e:
        raise WebDriverError("Failed to maximize window.") from e


async def switch_to_window(
    server_url: str, session: str, handle: str, session_http: Union[ClientSession, None] = None
):
    """
    Switch to window.

    This function switches the WebDriver context to a different window by its handle.
    Based on W3C WebDriver Specification.

    Args:
        server_url: The URL of the WebDriver server.
        session: The session identifier for the current WebDriver session.
        handle: The window handle to switch to.
        session_http: Optional HTTP client session for making requests. If not provided,
                      a default session will be used.

    Returns:
        True if the window switch was successful.

    Raises:
        WebDriverError: If the switch to window operation fails.
    """
    try:
        url = f"{server_url}/session/{session}/window"
        payload = {"handle": handle}
        await _post(url, payload, session_http=session_http)
        return True
    except Exception as e:
        raise WebDriverError("Failed to switch to window.") from e


async def switch_to_window_jsonwire(
    server_url, session, handle, session_http: Union[ClientSession, None] = None
):
    """
    Switch to window.

    This function switches the WebDriver context to a different window by its handle.
    Based on W3C WebDriver Specification (JsonWire protocol).

    Args:
        server_url: The URL of the WebDriver server.
        session: The session identifier for the current WebDriver session.
        handle: The window handle to switch to.
        session_http: Optional HTTP client session for making requests. If not provided,
                      a default session will be used.

    Returns:
        True if the window switch was successful.

    Raises:
        WebDriverError: If the switch to window operation fails.
    """
    try:
        url = f"{server_url}/session/{session}/window"
        payload = {"name": handle}
        await _post(url, payload, session_http=session_http)
        return True
    except Exception as e:
        raise WebDriverError("Failed to switch to window.") from e


async def new_window(
    server_url, session, window_type="tab", session_http: Union[ClientSession, None] = None
) -> str:
    """
    Open a new window.

    This function opens a new window or tab based on W3C WebDriver Specification.

    Args:
        server_url: The base URL of the WebDriver server
        session: The session identifier for the WebDriver session
        window_type: The type of window to open ('tab' or 'window'). Defaults to 'tab'
        session_http: Optional HTTP client session for making requests.
        If not provided, a default session will be used

    Returns:
        The handle of the newly opened window

    Raises:
        WebDriverError: If the window creation fails
    """
    try:
        url = f"{server_url}/session/{session}/window/new"
        payload = {"type": window_type}
        result = await _post(url, payload, session_http=session_http)
        return result.get("value", {}).get("handle")
    except Exception as e:
        raise WebDriverError("Failed to open window.") from e


async def switch_to_parent_frame(
    server_url, session, element_frame, session_http: Union[ClientSession, None] = None
):
    """
    Switch to parent frame of 'element_frame'.

    This function switches the WebDriver context to the parent frame of the specified frame element.
    Based on W3C WebDriver Specification.

    Args:
        server_url: The base URL of the WebDriver server
        session: The session identifier for the WebDriver session
        element_frame: The frame element identifier whose parent frame to switch to
        session_http: Optional HTTP client session for making requests.
        If not provided, a default session will be used

    Returns:
        True if the switch to parent frame was successful

    Raises:
        WebDriverError: If the switch to parent frame operation fails
    """
    try:
        url = f"{server_url}/session/{session}/frame/parent"
        payload = {"id": {ELEMENT_W3C: element_frame}}
        await _post(url, payload, session_http=session_http)
        return True
    except Exception as e:
        raise WebDriverError("Failed to switch to parent frame.") from e


async def switch_to_parent_frame_jsonwire(
    server_url, session, element_frame, session_http: Union[ClientSession, None] = None
):
    """
    Switch to parent frame of 'element_frame'.

    This function switches the WebDriver context to the parent frame of the specified frame element.
    Based on W3C WebDriver Specification (JsonWire protocol).

    Args:
        server_url: The base URL of the WebDriver server
        session: The session identifier for the WebDriver session
        element_frame: The frame element identifier whose parent frame to switch to
        session_http: Optional HTTP client session for making requests.
        If not provided, a default session will be used

    Returns:
        True if the switch to parent frame was successful

    Raises:
        WebDriverError: If the switch to parent frame operation fails
    """
    try:
        url = f"{server_url}/session/{session}/frame/parent"
        payload = {"id": {ELEMENT_JSONWIRE: element_frame}}
        await _post(url, payload, session_http=session_http)
        return True
    except Exception as e:
        raise WebDriverError("Failed to switch to parent frame.") from e


async def switch_to_frame(
    server_url, session, element_frame, session_http: Union[ClientSession, None] = None
):
    """
    Switch to frame 'element_frame'.

    This function switches the WebDriver context to the specified frame element.
    Based on W3C WebDriver Specification.

    Args:
        server_url: The base URL of the WebDriver server
        session: The session identifier for the WebDriver session
        element_frame: The frame element identifier to switch to
        session_http: Optional HTTP client session for making requests.
        If not provided, a default session will be used

    Returns:
        True if the switch to frame was successful

    Raises:
        WebDriverError: If the switch to frame operation fails
    """
    try:
        url = f"{server_url}/session/{session}/frame"
        payload = {"id": {ELEMENT_W3C: element_frame}}
        await _post(url, payload, session_http=session_http)
        return True
    except Exception as e:
        raise WebDriverError("Failed to switch to frame.") from e


async def switch_to_frame_jsonwire(
    server_url, session, element_frame, session_http: Union[ClientSession, None] = None
):
    """
    Switch to frame 'element_frame'.

    This function switches the WebDriver context to the specified frame element.
    Based on W3C WebDriver Specification (JsonWire protocol).

    Args:
        server_url: The base URL of the WebDriver server
        session: The session identifier for the WebDriver session
        element_frame: The frame element identifier to switch to
        session_http: Optional HTTP client session for making requests.
        If not provided, a default session will be used

    Returns:
        True if the switch to frame was successful

    Raises:
        WebDriverError: If the switch to frame operation fails
    """
    try:
        url = f"{server_url}/session/{session}/frame"
        payload = {"id": {ELEMENT_JSONWIRE: element_frame}}
        await _post(url, payload, session_http=session_http)
        return True
    except Exception as e:
        raise WebDriverError("Failed to switch to frame.") from e


async def delete_all_cookies(server_url, session, session_http: Union[ClientSession, None] = None):
    """
    Delete all cookies for the current session.

    This function removes all cookies associated with the active session,
    following the W3C WebDriver Specification for cookie management.

    Args:
        server_url: The base URL of the WebDriver server.
        session: The session identifier for the current WebDriver session.
        session_http: An optional ClientSession instance used to make HTTP requests.
                      If None, a default session will be used.

    Returns:
        True if cookies were successfully deleted.

    Raises:
        WebDriverError: If the cookie deletion request fails or an error occurs
                        during the deletion process.
    """
    """Delete all cookies"""
    try:
        url = f"{server_url}/session/{session}/cookie"
        await _delete(url, session_http)
        return True
    except Exception as e:
        raise WebDriverError("Failed to delete cookies.") from e


async def send_alert_text(
    server_url, session, text, session_http: Union[ClientSession, None] = None
):
    """
    Send text to an alert dialog.

    This function sends text to the currently open alert dialog.
    Based on W3C WebDriver Specification.

    Args:
        server_url: The base URL of the WebDriver server
        session: The session identifier for the WebDriver session
        text: The text to send to the alert dialog
        session_http: Optional HTTP client session for making requests.
        If not provided, a default session will be used

    Returns:
        True if the text was successfully sent to the alert

    Raises:
        WebDriverError: If sending text to the alert fails
    """
    try:
        url = f"{server_url}/session/{session}/alert/text"
        payload = {
            "text": text,
        }
        await _post(url, payload, session_http=session_http)
        return True
    except Exception as e:
        raise WebDriverError("Failed to sent text to alert.") from e


async def accept_alert(server_url, session, session_http: Union[ClientSession, None] = None):
    """
    Accept alert.

    This function accepts the currently open alert dialog.
    Based on W3C WebDriver Specification.

    Args:
        server_url: The base URL of the WebDriver server
        session: The session identifier for the WebDriver session
        session_http: Optional HTTP client session for making requests.
        If not provided, a default session will be used

    Returns:
        True if the alert was successfully accepted

    Raises:
        WebDriverError: If the alert acceptance fails
    """
    try:
        return await _handle_alert(server_url, session, "accept", session_http=session_http)
    except Exception as e:
        raise WebDriverError("Failed to accept alert.") from e


async def dismiss_alert(server_url, session, session_http: Union[ClientSession, None] = None):
    """Dismiss alert

    This function dismisses the currently open alert dialog.
    Based on W3C WebDriver Specification.

    Args:
        server_url: The base URL of the WebDriver server.
        session: The session identifier for the WebDriver session.
        session_http: Optional HTTP client session for making requests.
        If not provided, a default session will be used.

    Returns:
        True if the alert was successfully dismissed.

    Raises:
        WebDriverError: If the alert dismissal fails.
    """
    try:
        return await _handle_alert(server_url, session, "dismiss", session_http=session_http)
    except Exception as e:
        raise WebDriverError("Failed to dismiss alert.") from e


async def take_screenshot_element(
    server_url,
    session,
    element,
    path="/tmp",
    file_name="caqui",
    session_http: Union[ClientSession, None] = None,
):
    """Take screenshot of element

    Args:
        server_url: The base URL of the WebDriver server.
        session: The session identifier for the WebDriver session.
        element: The identifier of the element to take a screenshot of.
        path: The directory path where the screenshot will be saved.
        file_name: The name of the file to save the screenshot as.
        session_http: An optional HTTP client session for making requests.
        If not provided, a default session will be used.

    Returns:
        True if the screenshot was successfully taken and saved.

    Raises:
        WebDriverError: If taking the screenshot fails.
    """
    try:
        url = f"{server_url}/session/{session}/element/{element}/screenshot"
        response = await _get(url, session_http)
        picture = response.get("value", "")
        save_picture(session, path, file_name, picture)
        return True
    except Exception as e:
        raise WebDriverError("Failed to take screenshot from element.") from e


async def take_screenshot(
    server_url: str,
    session: str,
    path: str = "/tmp",
    file_name: str = "caqui",
    session_http: Union[ClientSession, None] = None,
):
    """Take screenshot

    Args:
        server_url: The base URL of the WebDriver server.
        session: The session identifier for the WebDriver session.
        path: The directory path where the screenshot will be saved.
        file_name: The name of the file to save the screenshot as.
        session_http: An optional HTTP client session for making requests.
        If not provided, a default session will be used.

    Returns:
        True if the screenshot was successfully taken and saved.

    Raises:
        WebDriverError: If taking the screenshot fails.
    """
    try:
        url = f"{server_url}/session/{session}/screenshot"
        response = await _get(url, session_http)
        picture = response.get("value", "")
        save_picture(session, path, file_name, picture)
        return True
    except Exception as e:
        raise WebDriverError("Failed to take screenshot.") from e


async def get_named_cookie(
    server_url, session, name, session_http: Union[ClientSession, None] = None
) -> dict:
    """Get cookie by name.

    This function retrieves a cookie from the WebDriver session based on the specified name.

    Args:
        server_url: The base URL of the WebDriver server.
        session: The session identifier for the WebDriver session.
        name: The name of the cookie to retrieve.
        session_http: An optional HTTP client session for making requests.
        If not provided, a default session will be used.

    Returns:
        A dictionary representing the cookie if found, otherwise an empty dictionary.

    Raises:
        WebDriverError: If the request to get the cookie fails.
    """
    try:
        url = f"{server_url}/session/{session}/cookie/{name}"
        response = await _get(url, session_http)
        return response.get("value", {})
    except Exception as e:
        raise WebDriverError(f"Failed to get cookie '{name}'.") from e


async def get_computed_label(
    server_url, session, element, session_http: Union[ClientSession, None] = None
) -> str:
    """Get the element tag computed label. Get the accessibility name.

    Args:
        server_url: The base URL of the WebDriver server.
        session: The session identifier for the WebDriver session.
        element: The identifier of the element to retrieve the computed label for.
        session_http: An optional HTTP client session for making requests.
        If not provided, a default session will be used.

    Returns:
        The computed label of the element, which represents its accessibility name.

    Raises:
        WebDriverError: If retrieving the computed label fails.
    """
    try:
        url = f"{server_url}/session/{session}/element/{element}/computedlabel"
        response = await _get(url, session_http)
        return response.get("value", "")
    except Exception as e:
        raise WebDriverError("Failed to get element computed label.") from e


async def get_computed_role(
    server_url, session, element, session_http: Union[ClientSession, None] = None
) -> str:
    """Get the element tag computed role (the element role).

    Args:
        server_url: The base URL of the WebDriver server.
        session: The session identifier for the WebDriver session.
        element: The identifier of the element to retrieve the computed role for.
        session_http: An optional HTTP client session for making requests.
        If not provided, a default session will be used.

    Returns:
        The computed role of the element, which represents its accessibility role.

    Raises:
        WebDriverError: If retrieving the computed role fails.
    """
    try:
        url = f"{server_url}/session/{session}/element/{element}/computedrole"
        response = await _get(url, session_http)
        return response.get("value", "")
    except Exception as e:
        raise WebDriverError("Failed to get element computed label.") from e


async def get_tag_name(
    server_url, session, element, session_http: Union[ClientSession, None] = None
) -> str:
    """
    Get the tag name of a specified element in a WebDriver session.

    Parameters:
        server_url: The base URL of the WebDriver server.
        session: The identifier for the WebDriver session.
        element: The identifier for the specific element whose tag name is to be retrieved.
        session_http: An optional HTTP session object for making requests.

    Returns:
        A string representing the tag name of the specified element.

    Raises:
        WebDriverError: If there is an error while attempting to retrieve the element's tag name.
    """
    """Get the element tag name"""
    try:
        url = f"{server_url}/session/{session}/element/{element}/name"
        response = await _get(url, session_http)
        return response.get("value", "")
    except Exception as e:
        raise WebDriverError("Failed to get element name.") from e


async def get_shadow_root(
    server_url: str, session: str, element: str, session_http: Union[ClientSession, None] = None
) -> str:
    """
    Get the shadow root element from a specified web element.

    Args:
        server_url: The URL of the WebDriver server.
        session: The session ID for the current WebDriver session.
        element: The ID of the web element for which to retrieve the shadow root.
        session_http: An optional HTTP session for making requests.

    Returns:
        The shadow root element associated with the specified web element.

    Raises:
        WebDriverError: If there is an error retrieving the shadow root element.
    """
    """Get the shadow root element"""
    try:
        root_element = "shadow-6066-11e4-a52e-4f735466cecf"
        url = f"{server_url}/session/{session}/element/{element}/shadow"
        response = await _get(url, session_http)
        return response.get("value", {}).get(root_element)
    except Exception as e:
        raise WebDriverError("Failed to get element shadow.") from e


async def get_shadow_element(
    server_url: str,
    session: str,
    shadow_element: str,
    locator_type: str,
    locator_value: str,
    session_http: Union[ClientSession, None] = None,
) -> str:
    """Get the shadow root element"""
    """
    Get the shadow root element from a web page using the W3C WebDriver Specification.

    Parameters:
        server_url: The base URL of the WebDriver server.
        session: The session ID for the current WebDriver session.
        shadow_element: The ID or name of the shadow element to retrieve.
        locator_type: The type of locator to use (e.g., 'css selector', 'xpath').
        locator_value: The value of the locator to find the element.
        session_http: An optional HTTP session for making requests.

    Returns:
        The shadow root element as a string, or an empty string if not found.

    Raises:
        WebDriverError: If there is an error retrieving the shadow element.
    """
    try:
        locator_type, locator_value = convert_locator_to_css_selector(locator_type, locator_value)
        url: str = f"{server_url}/session/{session}/shadow/{shadow_element}/element"
        payload: Dict[str, str] = {"using": locator_type, "value": locator_value}
        response: Dict[str, Any] = await _post(url, payload, session_http)
        return response.get("value", {}).get(ELEMENT_W3C, "")
    except Exception as e:
        raise WebDriverError("Failed to get the element shadow.") from e


async def get_shadow_element_jsonwire(
    server_url: str,
    session: str,
    shadow_element: str,
    locator_type: str,
    locator_value: str,
    session_http: Union[ClientSession, None] = None,
) -> str:
    """
    Get the shadow root element from a specified session.

    Parameters:
        server_url: The base URL of the WebDriver server.
        session: The session ID for the current WebDriver session.
        shadow_element: The ID of the shadow element to retrieve.
        locator_type: The type of locator to use (e.g., 'css selector', 'xpath').
        locator_value: The value of the locator to find the element.
        session_http: An optional HTTP session for making requests.

    Returns:
        A string representation of the shadow root element in JSON format.

    Raises:
        WebDriverError: If there is an error in retrieving the shadow element.
    """
    """Get the shadow root element"""
    try:
        locator_type, locator_value = convert_locator_to_css_selector(locator_type, locator_value)
        url: str = f"{server_url}/session/{session}/shadow/{shadow_element}/element"
        payload: Dict[str, str] = {"using": locator_type, "value": locator_value}
        response: Dict[str, Any] = await _post(url, payload, session_http)
        return response.get("value", {}).get(ELEMENT_JSONWIRE, "")
    except Exception as e:
        raise WebDriverError("Failed to get the element shadow.") from e


async def get_shadow_elements(
    server_url: str,
    session: str,
    shadow_element: str,
    locator_type: str,
    locator_value: str,
    session_http: Union[ClientSession, None] = None,
) -> List[str]:
    """
    Get the list of shadow root elements.

    Args:
        server_url: The base URL of the WebDriver server.
        session: The session ID for the current WebDriver session.
        shadow_element: The identifier for the shadow element to retrieve.
        locator_type: The type of locator to use (e.g., 'css selector', 'xpath').
        locator_value: The value of the locator to find the element.
        session_http: An optional HTTP session for making requests.

    Returns:
        A list of shadow root element identifiers.

    Raises:
        WebDriverError: If there is an error retrieving the shadow elements.
    """
    """Get the list of shadow root elements"""
    try:
        locator_type, locator_value = convert_locator_to_css_selector(locator_type, locator_value)
        url: str = f"{server_url}/session/{session}/shadow/{shadow_element}/elements"
        payload: Dict[str, str] = {"using": locator_type, "value": locator_value}
        response: Dict[str, Any] = await _post(url, payload, session_http)
        return [x.get(ELEMENT_W3C) for x in response.get("value", {})]
    except Exception as e:
        raise WebDriverError("Failed to get the element shadow.") from e


async def get_shadow_elements_jsonwire(
    server_url: str,
    session: str,
    shadow_element: str,
    locator_type: str,
    locator_value: str,
    session_http: Union[ClientSession, None] = None,
) -> List[str]:
    """Get the list of shadow root element"""
    try:
        locator_type, locator_value = convert_locator_to_css_selector(locator_type, locator_value)
        url: str = f"{server_url}/session/{session}/shadow/{shadow_element}/elements"
        payload: Dict[str, str] = {"using": locator_type, "value": locator_value}
        response: Dict[str, Any] = await _post(url, payload, session_http)
        return [x.get(ELEMENT_JSONWIRE) for x in response.get("value", {})]
    except Exception as e:
        raise WebDriverError("Failed to get the element shadow.") from e


async def get_rect(
    server_url, session, element, session_http: Union[ClientSession, None] = None
) -> dict:
    """Get the element rectangle"""
    try:
        url = f"{server_url}/session/{session}/element/{element}/rect"
        response = await _get(url, session_http)
        return response.get("value", {})
    except Exception as e:
        raise WebDriverError("Failed to get element rect.") from e


async def actions(server_url, session, payload, session_http: Union[ClientSession, None] = None):
    url = f"{server_url}/session/{session}/actions"
    await _post(url, payload, session_http=session_http)
    return True


async def actions_move_to_element(
    server_url: str, session: str, element: str, session_http: Union[ClientSession, None] = None
) -> bool:
    """
    Move to an element simulating a mouse movement.

    This function sends a WebDriver Actions command to move the mouse pointer to a
    specified element, following the W3C WebDriver Specification.

    Args:
        server_url: The URL of the WebDriver server.
        session: The session identifier for the WebDriver session.
        element: The element identifier (W3C element reference) to move the pointer to.
        session_http: Optional HTTP client session for making requests. If not provided,
                      a new session will be created.

    Returns:
        A boolean indicating whether the move action was successfully executed.

    Raises:
        WebDriverError: If the action fails to move to the element.

    Note:
        The mouse movement is performed with zero duration, resulting in an instant
        pointer movement to the element's location. The element reference follows the
        W3C WebDriver specification format.
    """
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
                            "duration": 0,
                            "x": 0,
                            "y": 0,
                            "origin": {ELEMENT_W3C: element},
                        }
                    ],
                },
            ]
        }
        return await actions(server_url, session, payload, session_http=session_http)
    except Exception as e:
        raise WebDriverError("Failed to move to element.") from e


async def actions_move_to_element_jsonwire(
    server_url: str, session: str, element: str, session_http: Union[ClientSession, None] = None
) -> bool:
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
                            "duration": 0,
                            "x": 0,
                            "y": 0,
                            "origin": {ELEMENT_JSONWIRE: element},
                        }
                    ],
                },
            ]
        }
        return await actions(server_url, session, payload, session_http=session_http)
    except Exception as e:
        raise WebDriverError("Failed to move to element.") from e


async def actions_scroll_to_element(
    server_url,
    session,
    element,
    delta_y: int = 1000,
    session_http: Union[ClientSession, None] = None,
):
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
                            "deltaY": delta_y,
                            "duration": 0,
                            "origin": {ELEMENT_W3C: element},
                        }
                    ],
                }
            ]
        }
        return await actions(server_url, session, payload, session_http=session_http)
    except Exception as e:
        raise WebDriverError("Failed to scroll to element.") from e


async def actions_scroll_to_element_jsonwire(
    server_url,
    session,
    element,
    delta_y: int = 1000,
    session_http: Union[ClientSession, None] = None,
):
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
                            "deltaY": delta_y,
                            "duration": 0,
                            "origin": {ELEMENT_JSONWIRE: element},
                        }
                    ],
                }
            ]
        }
        return await actions(server_url, session, payload, session_http=session_http)
    except Exception as e:
        raise WebDriverError("Failed to scroll to element.") from e


async def submit(server_url, session, element, session_http: Union[ClientSession, None] = None):
    """Submit a form. It is similar to 'submit' funtion in Seleniu
    It is not part of W3C WebDriver. Just added for convenience
    """
    try:
        submit_element = await find_child_element(
            server_url,
            session,
            element,
            locator_type="xpath",
            locator_value="*[@type='submit']",
            session_http=session_http,
        )
        return await click(server_url, session, submit_element, session_http=session_http)
    except Exception as e:
        raise WebDriverError("Failed to submit form.") from e


async def actions_click(
    server_url, session, element, session_http: Union[ClientSession, None] = None
):
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
        return await actions(server_url, session, payload, session_http=session_http)
    except Exception as e:
        raise WebDriverError("Failed to click the element.") from e


async def actions_click_jsonwire(
    server_url, session, element, session_http: Union[ClientSession, None] = None
):
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
        return await actions(server_url, session, payload, session_http=session_http)
    except Exception as e:
        raise WebDriverError("Failed to click the element.") from e


async def set_timeouts(
    server_url, session, timeouts, session_http: Union[ClientSession, None] = None
):
    """Set timeouts"""
    try:
        url = f"{server_url}/session/{session}/timeouts"
        payload = {
            "implicit": timeouts,
        }
        await _post(url, payload, session_http=session_http)
        return True
    except Exception as e:
        raise WebDriverError("Failed to set timeouts.") from e


async def find_children_elements(
    server_url: str,
    session: str,
    parent_element: str,
    locator_type: str,
    locator_value: str,
    session_http: Union[ClientSession, None] = None,
):
    """Find the children elements by 'locator_type'

    If the 'parent_element' is a shadow element, set the 'locator_type' as 'id' or
    'css selector'
    """
    locator_type, locator_value = convert_locator_to_css_selector(locator_type, locator_value)
    try:
        url = f"{server_url}/session/{session}/element/{parent_element}/elements"
        payload = {"using": locator_type, "value": locator_value, "id": parent_element}
        response = await _post(url, payload, session_http=session_http)
        return get_elements(response)
    except Exception as e:
        raise WebDriverError(
            f"Failed to find the children elements from '{parent_element}'."
        ) from e


async def find_child_element(
    server_url: str,
    session: str,
    parent_element: str,
    locator_type: str,
    locator_value: str,
    session_http: Union[ClientSession, None] = None,
):
    """Find the child element by 'locator_type'"""
    locator_type, locator_value = convert_locator_to_css_selector(locator_type, locator_value)
    try:
        url = f"{server_url}/session/{session}/element/{parent_element}/element"
        payload = {"using": locator_type, "value": locator_value, "id": parent_element}
        response = await _post(url, payload, session_http=session_http)
        return get_element(response)
    except Exception as e:
        raise WebDriverError(f"Failed to find the child element from '{parent_element}'.") from e


async def get_page_source(
    server_url, session, session_http: Union[ClientSession, None] = None
) -> str:
    """Get the page source (all content)"""
    try:
        url = f"{server_url}/session/{session}/source"
        response = await _get(url, session_http=session_http)
        return response.get("value", "")
    except Exception as e:
        raise WebDriverError("Failed to get the page source.") from e


async def execute_script(
    server_url: str,
    session: str,
    script: str,
    args: List = [],
    session_http: Union[ClientSession, None] = None,
):
    """Executes a script, like 'alert('something')' to open an alert window"""
    try:
        url = f"{server_url}/session/{session}/execute/async"
        payload = {"script": script, "args": args}
        response = await _post(url, payload, session_http=session_http)
        return response.get("value")
    except Exception as e:
        raise WebDriverError("Failed to execute script.") from e


async def get_alert_text(
    server_url, session, session_http: Union[ClientSession, None] = None
) -> str:
    """Get the text from an alert"""
    try:
        url = f"{server_url}/session/{session}/alert/text"
        response = await _get(url, session_http=session_http)
        return response.get("value", "")
    except Exception as e:
        raise WebDriverError("Failed to get the alert text.") from e


async def get_active_element(server_url, session, session_http: Union[ClientSession, None] = None):
    """Get the active element"""
    try:
        url = f"{server_url}/session/{session}/element/active"
        response = await _get(url, session_http=session_http)
        return get_element(response)
    except Exception as e:
        raise WebDriverError("Failed to check if element is selected.") from e


async def clear_element(
    server_url, session, element, session_http: Union[ClientSession, None] = None
):
    """Clear the element text"""
    try:
        url = f"{server_url}/session/{session}/element/{element}/clear"
        payload = {"id": element}
        await _post(url, payload, session_http=session_http)
        return True
    except Exception as e:
        raise WebDriverError("Failed to clear the element text.") from e


async def is_element_enabled(
    server_url, session, element, session_http: Union[ClientSession, None] = None
) -> bool:
    """Check if element is enabled"""
    try:
        url = f"{server_url}/session/{session}/element/{element}/enabled"
        response = await _get(url, session_http=session_http)
        return response.get("value", False)
    except Exception as e:
        raise WebDriverError("Failed to check if element is enabled.") from e


async def get_css_value(
    server_url, session, element, property_name, session_http: Union[ClientSession, None] = None
) -> str:
    """Get CSS value"""
    try:
        url = f"{server_url}/session/{session}/element/{element}/css/{property_name}"
        response = await _get(url, session_http=session_http)
        return response.get("value", "")
    except Exception as e:
        raise WebDriverError("Failed to get css value.") from e


async def is_element_selected(
    server_url, session, element, session_http: Union[ClientSession, None] = None
) -> bool:
    """Check if element is selected"""
    try:
        url = f"{server_url}/session/{session}/element/{element}/selected"
        response = await _get(url, session_http=session_http)
        return bool(response.get("value"))
    except Exception as e:
        raise WebDriverError("Failed to check if element is selected.") from e


async def get_window_rectangle(
    server_url, session, session_http: Union[ClientSession, None] = None
) -> dict:
    """Get window rectangle"""
    try:
        url = f"{server_url}/session/{session}/window/rect"
        response = await _get(url, session_http=session_http)
        return response.get("value", {})
    except Exception as e:
        raise WebDriverError("Failed to get window rectangle.") from e


async def get_window_handles(
    server_url, session, session_http: Union[ClientSession, None] = None
) -> list:
    """Get window handles"""
    try:
        url = f"{server_url}/session/{session}/window/handles"
        response = await _get(url, session_http=session_http)
        return response.get("value", [])
    except Exception as e:
        raise WebDriverError("Failed to get window handles.") from e


async def close_window(
    server_url, session, session_http: Union[ClientSession, None] = None
) -> list:
    """Close active window"""
    try:
        url = f"{server_url}/session/{session}/window"
        response = await _delete(url, session_http=session_http)
        return response.get("value")
    except Exception as e:
        raise WebDriverError("Failed to close active window.") from e


async def get_window(server_url, session, session_http: Union[ClientSession, None] = None) -> str:
    """Get window"""
    try:
        url = f"{server_url}/session/{session}/window"
        response = await _get(url, session_http=session_http)
        return response.get("value", "")
    except Exception as e:
        raise WebDriverError("Failed to get window.") from e


async def go_back(server_url, session, session_http: Union[ClientSession, None] = None):
    """
    This command causes the browser to traverse one step backward
    in the joint session history of the
    current browse. This is equivalent to pressing the back button in the browser.
    """
    try:
        url = f"{server_url}/session/{session}/back"
        await _post(url, {}, session_http=session_http)
        return True
    except Exception as e:
        raise WebDriverError("Failed to go back to page.") from e


async def get_url(server_url, session, session_http: Union[ClientSession, None] = None) -> str:
    """Returns the URL from web page:"""
    try:
        url = f"{server_url}/session/{session}/url"
        response = await _get(url, session_http=session_http)
        return response.get("value", "")
    except Exception as e:
        raise WebDriverError("Failed to get page url.") from e


async def get_timeouts(
    server_url, session, session_http: Union[ClientSession, None] = None
) -> dict:
    """
    Returns the configured timeouts:
        {"implicit": 0, "pageLoad": 300000, "script": 30000}
    """
    try:
        url = f"{server_url}/session/{session}/timeouts"
        response = await _get(url, session_http=session_http)
        return response.get("value", {})
    except Exception as e:
        raise WebDriverError("Failed to get timeouts.") from e


async def get_status(server_url, session_http: Union[ClientSession, None] = None) -> dict:
    """Returns the status and details of the WebDriver"""
    try:
        url = f"{server_url}/status"
        response = await _get(url, session_http=session_http)
        return response
    except Exception as e:
        raise WebDriverError("Failed to get status.") from e


async def get_title(server_url, session, session_http: Union[ClientSession, None] = None) -> str:
    """Get the page title"""
    try:
        url = f"{server_url}/session/{session}/title"
        response = await _get(url, session_http=session_http)
        return response.get("value", "")
    except Exception as e:
        raise WebDriverError("Failed to get page title.") from e


async def find_elements(
    server_url: str,
    session: str,
    locator_type: str,
    locator_value: str,
    session_http: Union[ClientSession, None] = None,
) -> List[Any]:
    """Search the DOM elements by 'locator', for example, 'xpath'"""
    locator_type, locator_value = convert_locator_to_css_selector(locator_type, locator_value)
    try:
        payload = {"using": locator_type, "value": locator_value}
        url = f"{server_url}/session/{session}/elements"
        response = await _post(url, payload, session_http=session_http)
        return [x.get(ELEMENT_W3C) for x in response.get("value")]
    except Exception as e:
        raise WebDriverError(
            f"Failed to find element by '{locator_type}'-'{locator_value}'."
        ) from e


async def find_elements_jsonwire(
    server_url: str,
    session: str,
    locator_type: str,
    locator_value: str,
    session_http: Union[ClientSession, None] = None,
) -> List[Any]:
    """Search the DOM elements by 'locator', for example, 'xpath'"""
    locator_type, locator_value = convert_locator_to_css_selector(locator_type, locator_value)
    try:
        payload = {"using": locator_type, "value": locator_value}
        url = f"{server_url}/session/{session}/elements"
        response = await _post(url, payload, session_http=session_http)
        return [x.get(ELEMENT_JSONWIRE) for x in response.get("value")]
    except Exception as e:
        raise WebDriverError(
            f"Failed to find element by '{locator_type}'-'{locator_value}'."
        ) from e


async def get_property(
    server_url, session, element, property, session_http: Union[ClientSession, None] = None
) -> Any:
    """Get the given HTML property of an element, for example, 'href'"""
    try:
        url = f"{server_url}/session/{session}/element/{element}/property/{property}"
        response = await _get(url, session_http=session_http)
        return response.get("value")
    except Exception as e:
        raise WebDriverError("Failed to get value from element.") from e


async def get_attribute(
    server_url, session, element, attribute, session_http: Union[ClientSession, None] = None
) -> str:
    """Get the given HTML attribute of an element, for example, 'aria-valuenow'"""
    try:
        url = f"{server_url}/session/{session}/element/{element}/attribute/{attribute}"
        response = await _get(url, session_http=session_http)
        if response.get("value") is None:
            return ""
        return response.get("value", "")
    except Exception as e:
        raise WebDriverError("Failed to get value from element.") from e


async def get_text(
    server_url, session, element, session_http: Union[ClientSession, None] = None
) -> str:
    """Get the text of an element"""
    try:
        url = f"{server_url}/session/{session}/element/{element}/text"
        response = await _get(url, session_http=session_http)
        return response.get("value", "")
    except Exception as e:
        raise WebDriverError("Failed to get text from element.") from e


async def get_cookies(
    server_url: str, session: str, session_http: Union[ClientSession, None] = None
) -> list:
    """Get the page cookies"""
    try:
        url = f"{server_url}/session/{session}/cookie"
        response = await _get(url, session_http=session_http)
        return response.get("value", [])
    except Exception as e:
        raise WebDriverError("Failed to get page cookies.") from e


async def close_session(server_url, session, session_http: Union[ClientSession, None] = None):
    """Close an opened session and close the browser"""
    try:
        url = f"{server_url}/session/{session}"
        await _delete(url, session_http=session_http)
        return True
    except Exception as e:
        raise WebDriverError("Failed to close session.") from e


async def get(server_url, session, page_url, session_http: Union[ClientSession, None] = None):
    """Does the same of 'go_to_page'. Added to be compatible with selenium method name'"""
    return go_to_page(server_url, session, page_url, session_http=session_http)


async def go_to_page(
    server_url, session, page_url, session_http: Union[ClientSession, None] = None
):
    """Navigate to 'page_url'"""
    try:
        url = f"{server_url}/session/{session}/url"
        payload = {"url": page_url}
        await _post(url, payload, session_http=session_http)
        return True
    except Exception as e:
        raise WebDriverError(f"Failed to navigate to page '{page_url}'.") from e


async def send_keys(
    server_url, session, element, text, session_http: Union[ClientSession, None] = None
):
    """Fill an editable element, for example a textarea, with a given text"""
    try:
        url = f"{server_url}/session/{session}/element/{element}/value"
        payload = {"text": text, "value": [*text], "id": element}
        await _post(url, payload, session_http=session_http)
        return True
    except Exception as e:
        raise WebDriverError(f"Failed to send key '{text}'.") from e


async def click(server_url, session, element, session_http: Union[ClientSession, None] = None):
    """Click on an element"""
    try:
        payload = {"id": element}
        url = f"{server_url}/session/{session}/element/{element}/click"
        await _post(url, payload, session_http=session_http)
        return True
    except Exception as e:
        raise WebDriverError("Failed to click on element.") from e


async def find_element(
    server_url: str,
    session: str,
    locator_type: str,
    locator_value: str,
    session_http: Union[ClientSession, None] = None,
) -> str:
    """Find an element by a 'locator', for example 'xpath'"""
    locator_type, locator_value = convert_locator_to_css_selector(locator_type, locator_value)
    try:
        payload = {"using": locator_type, "value": locator_value}
        url = f"{server_url}/session/{session}/element"
        response = await _post(url, payload, session_http=session_http)

        # Firefox does not support id locator, so it prints the error message to the user
        # It helps on debug
        if response.get("value").get("error"):
            raise WebDriverError(f"Failed to find element. {response}")
        return get_element(response)
    except Exception as e:
        raise WebDriverError(
            f"Failed to find element by '{locator_type}'-'{locator_value}'."
        ) from e


async def find_element_jsonwire(
    server_url: str,
    session: str,
    locator_type: str,
    locator_value: str,
    session_http: Union[ClientSession, None] = None,
) -> str:
    """Find an element by a 'locator', for example 'xpath'"""
    locator_type, locator_value = convert_locator_to_css_selector(locator_type, locator_value)
    try:
        payload = {"using": locator_type, "value": locator_value}
        url = f"{server_url}/session/{session}/element"
        response = await _post(url, payload, session_http=session_http)

        # Firefox does not support id locator, so it prints the error message to the user
        # It helps on debug
        if response.get("value").get("error"):
            raise WebDriverError(f"Failed to find element. {response}")
        return get_element_jsonwire(response)
    except Exception as e:
        raise WebDriverError(
            f"Failed to find element by '{locator_type}'-'{locator_value}'."
        ) from e


async def get_session(
    server_url: str,
    capabilities: Optional[dict] = None,
    session_http: Union[ClientSession, None] = None,
) -> str:
    """
    Opens a browser and a session.
    This session is used for all functions to perform events in the page
    """
    try:
        if not capabilities:
            capabilities = {}
        url = f"{server_url}/session"
        response = await _post(url, capabilities, session_http=session_http)
        return response.get("sessionId")
    except Exception as e:
        raise WebDriverError("Failed to open session. Check the browser capabilities.") from e
