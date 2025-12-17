# Copyright (C) 2023 Caqui - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://github.com/douglasdcm/caqui

import asyncio
import datetime
from typing import Any, Dict, List, Optional, Tuple, Union

from aiohttp import ClientSession
from orjson import dumps

from caqui.by import By
from caqui.cdp.connection import CDPConnection
from caqui.cdp.launcher import get_ws_url
from caqui.constants import (
    ELEMENT_JSONWIRE,
    ELEMENT_W3C,
    HEADERS,
    TIMEOUT,
    TIME_FORMAT_MICROSECONDS,
)
from caqui.exceptions import WebDriverError
from caqui.helper import (
    convert_locator_to_css_selector,
    get_element,
    get_element_jsonwire,
    get_elements,
    save_picture,
)
from bs4 import BeautifulSoup
from cdp import page, dom, browser, input_, target, runtime, network, emulation, accessibility


async def _handle_alert(conn: CDPConnection, alert_element, timeout, function_callback, text=None):
    await conn.execute(page.enable())
    click_task = asyncio.create_task(click(conn, alert_element))
    current_datetime = datetime.datetime.now()
    time_to_add = datetime.timedelta(seconds=timeout)
    new_datetime = current_datetime + time_to_add
    while 1 == 1:  # Used 1==1 and not True to deceive VSCode
        while datetime.datetime.now() < new_datetime:
            event = conn.get_event_nowait()
            if event is None:
                await asyncio.sleep(0)  # yield control
                continue
            if isinstance(event, page.JavascriptDialogOpening):
                await function_callback(conn, text)
                return
        raise TimeoutError()
    await click_task


async def _send_test_to_prompt_alert(conn: CDPConnection, text):
    await conn.execute(page.handle_java_script_dialog(accept=True, prompt_text=text))


async def _accept_alert(conn: CDPConnection, text):
    await conn.execute(page.handle_java_script_dialog(accept=True))


async def _dismiss_alert(conn: CDPConnection, text):
    await conn.execute(page.handle_java_script_dialog(accept=True))


async def _set_screen(conn, screen_type: str = "fullscreen"):
    window_for_target = await conn.execute(browser.get_window_for_target())
    window_id = window_for_target[0]
    bounds = browser.Bounds.from_json({"windowState": screen_type})
    await conn.execute(browser.set_window_bounds(window_id=window_id, bounds=bounds))


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


async def _delete(url):
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


async def _post(url, payload: dict):
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


async def _get(url: str) -> dict:
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


async def _handle_window(conn, session, command):
    """
    Handles window actions (fullscreen, minimize, maximize) for the current session.

    Args:
        conn: (CDPConnection): The WebDriver server URL.
        session (str): The session ID.
        command (str): The window command.
        session_http (ClientSession, optional): An existing aiohttp session.

    Returns:
        bool: True if the window action was successful.
    """
    url = f"{conn: CDPConnection}/session/{session}/window/{command}"
    payload: dict = {}
    await _post(url, payload, session_http=session_http)
    return True


async def get(conn: CDPConnection, page_url: str) -> None:
    """Does the same of 'go_to_page'. Added to be compatible with selenium method name'"""
    try:
        await conn.execute(page.enable())
        await conn.execute(page.navigate(url=page_url))
        await conn.execute(page.enable())
        await conn.execute(dom.enable())
        await conn.execute(runtime.enable())
        await conn.execute(network.enable())
        await conn.execute(
            target.set_auto_attach(auto_attach=True, wait_for_debugger_on_start=False, flatten=True)
        )
    except Exception as e:
        raise WebDriverError(f"Failed to navigate to page '{page_url}'.") from e


async def go_to_page(page_url: str) -> None:
    """Navigate to 'page_url'"""
    get(page_url)


# async def find_element(
#     locator_type, locator_value: str,
# ):
#     """Find an element by a 'selector', for example an 'xpath' like '//div[@id="example"]'"""
#     try:
#         locator_type, selector = convert_locator_to_css_selector(locator_type, locator_value)
#         js_command = f"document.querySelector('{selector}');"
#         async with CDPConnection(get_ws_url()) as conn:
#             element: Tuple[runtime.RemoteObject, None] = await conn.execute(runtime.evaluate(expression=js_command))
#             if not element[0].object_id:
#                 raise WebDriverError(f"Could not find element with selector: {locator_value}")
#             return element[0].object_id
#     except Exception as e:
#         raise WebDriverError(f"Could not find element with selector: {locator_value}") from e


async def find_element(
    conn: CDPConnection, locator_type, locator_value: str, root_id: dom.NodeId = None
) -> dom.NodeId:
    """Find an element by a 'selector', for example an 'xpath' like '//div[@id="example"]'"""
    try:
        selector = locator_value
        locator_type, selector = convert_locator_to_css_selector(locator_type, locator_value)
        if locator_type == By.CSS_SELECTOR:
            if not root_id:
                node = await conn.execute(dom.get_document())
            else:
                node = root_id
            node_id = await conn.execute(
                dom.query_selector(node_id=node.node_id, selector=selector)
            )
            if not node_id:
                raise WebDriverError(f"Could not find element with selector: {locator_value}")
            return node_id
        await conn.execute(dom.enable())
        search_result = await conn.execute(
            dom.perform_search(query=selector, include_user_agent_shadow_dom=True)
        )
        search_id = search_result[0]
        result_count = search_result[1]

        if result_count == 0:
            raise WebDriverError(f"Could not find element with selector: {locator_value}")

        nodes = await conn.execute(
            dom.get_search_results(search_id=search_id, from_index=0, to_index=result_count)
        )
        return nodes[0]
    except Exception as e:
        raise WebDriverError(f"Could not find element with selector: {locator_value}") from e


async def find_elements(conn: CDPConnection, locator_type, locator_value: str):
    """Find an element by a 'selector', for example an 'xpath' like '//div[@id="example"]'"""
    try:
        locator_type, selector = convert_locator_to_css_selector(locator_type, locator_value)
        node = await conn.execute(dom.get_document())
        node_ids = await conn.execute(
            dom.query_selector_all(node_id=node.node_id, selector=selector)
        )
        if not node_ids:
            raise WebDriverError(f"Could not find element with selector: {locator_value}")
        return node_ids
    except Exception as e:
        raise WebDriverError(f"Could not find element with selector: {locator_value}") from e


# async def click(remote_object):
#     """Click on an element"""
#     try:
#         selector = "#button"
#         js_command = f"document.querySelector('{selector}').click();"
#         async with CDPConnection(get_ws_url()) as conn:
#             remote_object: Tuple[runtime.RemoteObject, None] = await conn.execute(runtime.evaluate(expression=js_command))
#             if not remote_object[0].object_id:
#                 raise WebDriverError("Failed to click on element.")
#             return remote_object[0].object_id
#     except Exception as e:
#         raise WebDriverError("Failed to click on element.") from e


async def click(conn: CDPConnection, element):
    """Click on an element"""
    try:
        box_model = await conn.execute(dom.get_box_model(node_id=element))
        content_box = box_model.content
        center_x = (content_box[0] + content_box[2]) / 2
        center_y = (content_box[1] + content_box[5]) / 2
        commands = []
        mouse_button = input_.MouseButton("left")
        commands.append(
            input_.dispatch_mouse_event(
                "mousePressed", center_x, center_y, button=mouse_button, click_count=1
            )
        )
        commands.append(input_.dispatch_mouse_event(
            'mouseReleased', 
            center_x, 
            center_y, 
            button=mouse_button, 
            click_count=1
        ))
        for command in commands:
            await conn.execute(command)
    except Exception as e:
        raise WebDriverError("Failed to click on element.") from e


async def send_keys(conn: CDPConnection, element, text: str):
    """Send keys to an element"""
    try:
        await conn.execute(dom.focus(node_id=element))
        for char in text:
            await conn.execute(
                input_.dispatch_key_event(
                    "keyDown",
                    text=char,
                    unmodified_text=char,
                    windows_virtual_key_code=ord(char),
                    native_virtual_key_code=ord(char),
                )
            )
            await conn.execute(
                input_.dispatch_key_event(
                    "keyUp",
                    text=char,
                    unmodified_text=char,
                    windows_virtual_key_code=ord(char),
                    native_virtual_key_code=ord(char),
                )
            )
    except Exception as e:
        raise WebDriverError("Failed to send keys to element.") from e


async def get_text(conn: CDPConnection, element) -> str:
    """Get the text of an element"""
    try:
        html_doc = await conn.execute(dom.get_outer_html(node_id=element))
        soup = BeautifulSoup(html_doc, "html.parser")
        return soup.get_text()
    except Exception as e:
        raise WebDriverError("Failed to get text from element.") from e


async def get_attribute(conn: CDPConnection, element, attribute: str) -> str:
    """Get the given HTML attribute of an element, for example, 'aria-valuenow'"""
    try:
        attributes = await conn.execute(dom.get_attributes(node_id=element))
        attr_dict = {attributes[i]: attributes[i + 1] for i in range(0, len(attributes), 2)}
        result = attr_dict.get(attribute)
        if result is None:
            raise WebDriverError("Failed to get value from element.")
        return result
    except Exception as e:
        raise WebDriverError("Failed to get value from element.") from e


async def get_title(conn: CDPConnection) -> str:
    """Get the page title"""
    try:
        root_node = await conn.execute(dom.get_document())
        title_node_id = await conn.execute(
            dom.query_selector(node_id=root_node.node_id, selector="title")
        )
        result = await conn.execute(dom.get_outer_html(node_id=title_node_id))
        return BeautifulSoup(result, "html.parser").get_text()
    except Exception as e:
        raise WebDriverError("Failed to get page title.") from e


async def get_url(conn: CDPConnection) -> str:
    """Returns the URL from web page:"""
    try:
        await conn.execute(page.enable())
        frame_tree = await conn.execute(page.get_frame_tree())
        current_url = frame_tree.frame.url
        return current_url
    except Exception as e:
        raise WebDriverError("Failed to get page url.") from e


async def go_back(conn: CDPConnection):
    try:
        result = await conn.execute(page.get_navigation_history())
        current = result[0]
        if current <= 0:
            return
        entry = result[1][current - 1]
        await conn.execute(page.enable())
        await conn.execute(page.navigate_to_history_entry(entry.id_))
    except Exception as e:
        raise WebDriverError("Failed to go back to page.") from e


async def is_element_selected(conn: CDPConnection, element) -> bool:
    """Check if element is selected"""
    try:
        try:
            get_attribute_value = await get_attribute(conn, element, "checked")
            return get_attribute_value.lower() == ""
        except WebDriverError:
            pass
        try:
            get_attribute_value = await get_attribute(conn, element, "selected")
            return get_attribute_value.lower() == ""
        except WebDriverError:
            pass
        return False
    except Exception as e:
        raise WebDriverError("Failed to check if element is selected.") from e


async def get_css_value(conn: CDPConnection, element, property_name) -> str:
    """Get CSS value"""
    try:
        styles = await get_attribute(conn, element, "style")
        styles = styles.split(";")
        for s in styles:
            items = s.split(":")
            if len(items) == 2:
                if items[0].strip() == property_name:
                    return items[1].strip()
        raise WebDriverError("Failed to get css value.")
    except Exception as e:
        raise WebDriverError("Failed to get css value.") from e


async def add_cookie(conn: CDPConnection, cookie: Dict[str, Any]):
    """Add cookie

    This function adds a cookie to the WebDriver session.
    Based on W3C WebDriver Specification.

    Args:
        conn: The CDP connection object
        cookie: A dictionary representing the cookie to add
        Example:{
            "domain": ".example.org",
            "httpOnly": True,
            "name": "NID",
            "path": "/",
            "sameSite": "Lax",
            "secure": True,
            "value": "523=Sc0_gs..."
        }
    Returns:
        None

    """
    same_time = (
        network.CookieSameSite.from_json(cookie.get("sameSite")) if cookie.get("sameSite") else None
    )
    try:
        await conn.execute(
            network.set_cookie(
                name=cookie.get("name"),
                value=cookie.get("value"),
                domain=cookie.get("domain"),
                path=cookie.get("path", "/"),
                secure=cookie.get("secure", False),
                http_only=cookie.get("httpOnly", False),
                same_site=same_time,
                expires=cookie.get("expiry"),
            )
        )
    except Exception as e:
        raise WebDriverError("Failed to add cookie.") from e


async def delete_cookie(
    conn: CDPConnection, name: str, url: Optional[str] = None, domanin: Optional[str] = None
):
    """
    Delete cookie by name

    This function deletes a cookie with the specified name from the WebDriver session.
    Based on W3C WebDriver Specification.

    Args:
        conn: CDPConnection: The base URL of the WebDriver server
        name: The name of the cookie to delete

    Returns:
        None

    Raises:
        WebDriverError: If the cookie deletion fails
    """
    try:
        await conn.execute(network.delete_cookies(name=name, url=url, domain=domanin))
    except Exception as e:
        raise WebDriverError(f"Failed to delete cookie '{name}'.") from e


async def refresh_page(conn: CDPConnection):
    """
    Refreshes the current page by making an HTTP POST request to the server URL.

    Args:
        conn: (CDPConnection): The base URL of the server.
    Returns:
        None
    """
    try:
        await conn.execute(page.reload())
    except Exception as e:
        raise WebDriverError("Failed to refresh page.") from e


async def go_forward(conn: CDPConnection):
    """
    Go to page forward.

    This function sends a POST request to the specified URL,
    with an empty payload, and returns True if successful.

    Parameters:
        conn: (CDPConnection): The base URL of the server.

    Returns:
        None
    """
    try:
        result = await conn.execute(page.get_navigation_history())
        current = result[0]
        if current <= 0:
            return
        entry = result[1][current + 1]
        await conn.execute(page.enable())
        await conn.execute(page.navigate_to_history_entry(entry.id_))
    except Exception as e:
        raise WebDriverError("Failed to go to page forward.") from e


async def set_window_rectangle(
    conn: CDPConnection,
    width: int,
    height: int,
    left: Optional[int] = None,
    top: Optional[int] = None,
):
    """
    Set window rectangle.

    This function sets the window size and position based on W3C WebDriver Specification.

    Args:
        conn: CDPConnection: The base URL of the WebDriver server
        width: The desired window width in pixels
        height: The desired window height in pixels
        left: The desired window x coordinate
        top: The desired window y coordinate

    Returns:
        None

    Raises:
        WebDriverError: If the window rectangle setting fails
    """
    try:
        window_for_target = await conn.execute(browser.get_window_for_target())
        window_id = window_for_target[0]
        bounds: Dict[str, Any] = {}
        if left is not None:
            bounds["left"] = left
        if top is not None:
            bounds["top"] = top
        bounds = browser.Bounds.from_json({"width": width, "height": height})
        await conn.execute(browser.set_window_bounds(window_id=window_id, bounds=bounds))
    except Exception as e:
        raise WebDriverError("Failed to set window rectangle.") from e


async def fullscreen_window(conn: CDPConnection):
    """
    Fullscreen window.

    This function fullscreens the window based on W3C WebDriver Specification.

    Args:
        conn: CDPConnection: The base URL of the WebDriver server

    Returns:
        None

    Raises:
        WebDriverError: If the fullscreen operation fails
    """
    try:
        await _set_screen(conn, "normal")
        await _set_screen(conn, "fullscreen")
    except Exception as e:
        raise WebDriverError("Failed to fullscreen window.") from e


async def minimize_window(conn: CDPConnection):
    """
    Minimize window.

    This function minimizes the window based on W3C WebDriver Specification.

    Args:
        conn: CDPConnection: The base URL of the WebDriver server

    Returns:
        None

    Raises:
        WebDriverError: If the minimize operation fails
    """
    try:
        await _set_screen(conn, "normal")
        await _set_screen(conn, "minimized")
    except Exception as e:
        raise WebDriverError("Failed to minimize window.") from e


async def maximize_window(conn: CDPConnection):
    """
    Maximize window.

    This function maximizes the window based on W3C WebDriver Specification.

    Args:
        conn: CDPConnection: The base URL of the WebDriver server

    Returns:
        None

    Raises:
        WebDriverError: If the maximize operation fails
    """
    try:
        await _set_screen(conn, "normal")
        await _set_screen(conn, "maximized")
    except Exception as e:
        raise WebDriverError("Failed to maximize window.") from e


async def switch_to_window(conn: CDPConnection, handle: browser.target.TargetInfo):
    """
    Switch to window.

    This function switches the WebDriver context to a different window by its handle.
    Based on W3C WebDriver Specification.

    Args:
        conn: CDPConnection: The URL of the WebDriver server.

    Returns:
        None

    Raises:
        WebDriverError: If the switch to window operation fails.
    """
    try:
        attach = await conn.execute(
            target.attach_to_target(target_id=handle.target_id, flatten=True)
        )
        conn.session_id = attach
        await conn.execute(page.enable())
        await conn.execute(runtime.enable())
    except Exception as e:
        raise WebDriverError("Failed to switch to window.") from e


async def new_window(conn) -> str:
    """
    Open a new window.

    This function opens a new window or tab based on W3C WebDriver Specification.

    Args:
        conn: CDPConnection: The base URL of the WebDriver server
        window_type: The type of window to open ('tab' or 'window'). Defaults to 'tab'

    Returns:
        None

    Raises:
        WebDriverError: If the window creation fails
    """
    try:
        await conn.execute(
            target.create_target(
                url="about:blank",
            )
        )
    except Exception as e:
        raise WebDriverError("Failed to open window.") from e


async def switch_to_parent_frame(conn: CDPConnection):
    """
    Switch to parent frame of 'element_frame'.

    This function switches the WebDriver context to the parent frame of the specified frame element.
    Based on W3C WebDriver Specification.

    Args:
        conn: CDPConnection: The base URL of the WebDriver server
        element_frame: The frame element identifier whose parent frame to switch to

    Returns:
        None

    Raises:
        WebDriverError: If the switch to parent frame operation fails
    """
    try:
        doc = await conn.execute(dom.get_document(depth=1))
        return doc.node_id
    except Exception as e:
        raise WebDriverError("Failed to switch to parent frame.") from e


async def switch_to_frame(conn: CDPConnection, element_frame: str) -> dom.Node:
    """
    Switch to frame 'element_frame'.

    This function switches the WebDriver context to the specified frame element.
    Based on W3C WebDriver Specification.

    Args:
        conn: CDPConnection: The base URL of the WebDriver server
        element_frame: The frame element identifier to switch to

    Returns:
        cdp.dom.Node

    Raises:
        WebDriverError: If the switch to frame operation fails
    """
    try:
        desc = await conn.execute(dom.describe_node(node_id=element_frame, depth=1))
        return desc.content_document
    except Exception as e:
        raise WebDriverError("Failed to switch to frame.") from e


async def delete_all_cookies(conn: CDPConnection):
    """
    Delete all cookies for the current session.

    This function removes all cookies associated with the active session,
    following the W3C WebDriver Specification for cookie management.

    Args:
        conn: CDPConnection: The base URL of the WebDriver server.

    Returns:
        None

    Raises:
        WebDriverError: If the cookie deletion request fails or an error occurs
                        during the deletion process.
    """
    try:
        await conn.execute(network.clear_browser_cookies())
    except Exception as e:
        raise WebDriverError("Failed to delete cookies.") from e


async def send_alert_text(
    conn: CDPConnection, alert_element: dom.NodeId, text, timeout: float = TIMEOUT
):
    """
    Send text to an alert dialog.

    This function sends text to the currently open alert dialog.
    Based on W3C WebDriver Specification.

    Args:
        conn: CDPConnection: The base URL of the WebDriver server
        alert_element: the alert element to send text
        text: The text to send to the alert dialog

    Returns:
        None

    Raises:
        WebDriverError: If sending text to the alert fails
    """
    try:
        await _handle_alert(conn, alert_element, timeout, _send_test_to_prompt_alert, text)
    except Exception as e:
        raise WebDriverError("Failed to sent text to alert.") from e


async def accept_alert(conn: CDPConnection, alert_element: dom.NodeId, timeout: float = TIMEOUT):
    """
    Accept alert.

    This function accepts the currently open alert dialog.
    Based on W3C WebDriver Specification.

    Args:
        conn: CDPConnection: The base URL of the WebDriver server
        alert_element: the alert to be accepted

    Returns:
        None

    Raises:
        WebDriverError: If the alert acceptance fails
    """
    try:
        await _handle_alert(conn, alert_element, timeout, _accept_alert)
    except Exception as e:
        raise WebDriverError("Failed to accept alert.") from e


async def dismiss_alert(conn: CDPConnection, alert_element: dom.NodeId, timeout: float = TIMEOUT):
    """Dismiss alert

    This function dismisses the currently open alert dialog.
    Based on W3C WebDriver Specification.

    Args:
        conn: CDPConnection: The base URL of the WebDriver server.
        alert_element: the alert to be dismissed

    Returns:
        None

    Raises:
        WebDriverError: If the alert dismissal fails.
    """
    try:
        await _handle_alert(conn, alert_element, timeout, _dismiss_alert)
    except Exception as e:
        raise WebDriverError("Failed to dismiss alert.") from e


async def take_screenshot_element(
    conn: CDPConnection,
    element,
    path="/tmp",
    file_name="caqui",
):
    """Take screenshot of element

    Args:
        conn: CDPConnection: The base URL of the WebDriver server..
        element: The identifier of the element to take a screenshot of.
        path: The directory path where the screenshot will be saved.
        file_name: The name of the file to save the screenshot as.

    Returns:
        None

    Raises:
        WebDriverError: If taking the screenshot fails.
    """
    try:
        box_model = await conn.execute(dom.get_box_model(node_id=element))
        content_box = box_model.content[
            0:8
        ]  # Get the 8 points (x1, y1, x2, y2... etc) of the content box

        # Determine the clipping region coordinates from the box model points
        # The content_box provides points of a polygon, we need min/max x and y for the clip
        # Simplified assumption for a simple rectangle:
        x_coords = content_box[::2]
        y_coords = content_box[1::2]
        clip_x = min(x_coords)
        clip_y = min(y_coords)
        clip_width = max(x_coords) - clip_x
        clip_height = max(y_coords) - clip_y

        # Define the Clip object
        clip = page.Viewport(
            x=clip_x,
            y=clip_y,
            width=clip_width,
            height=clip_height,
            scale=1.0,  # Use 1.0 for a standard scale
        )

        now = datetime.datetime.now()
        timestamp = now.strftime(TIME_FORMAT_MICROSECONDS)

        # Capture the screenshot with the specified clip
        screenshot_data = await conn.execute(page.capture_screenshot(clip=clip))
        save_picture(timestamp, path, file_name, screenshot_data)
    except Exception as e:
        raise WebDriverError("Failed to take screenshot from element.") from e


async def take_screenshot(
    conn: CDPConnection,
    path: str = "/tmp",
    file_name: str = "caqui",
):
    """Take screenshot

    Args:
        conn: CDPConnection: The base URL of the WebDriver server..
        path: The directory path where the screenshot will be saved.
        file_name: The name of the file to save the screenshot as.

    Returns:
        NOne

    Raises:
        WebDriverError: If taking the screenshot fails.
    """
    try:
        # 2. Get the full layout metrics of the page
        # This command returns the content size of the page, regardless of the current viewport
        metrics = await conn.execute(page.get_layout_metrics())
        content_size = metrics[-1]
        full_width = content_size.width
        full_height = content_size.height

        # 3. Override the device metrics to match the full page size
        # This effectively makes the entire page visible in a single "viewport"
        viewport = page.Viewport(0, 0, full_width, full_height, 1)
        await conn.execute(
            emulation.set_device_metrics_override(
                width=full_width,
                height=full_height,
                device_scale_factor=1,
                mobile=False,
                screen_width=full_width,
                screen_height=full_height,
                position_x=0,
                position_y=0,
                viewport=viewport,
            )
        )

        # 4. Capture the screenshot
        screenshot_data = await conn.execute(page.capture_screenshot(quality=90))

        # 5. Reset viewport emulation (optional, good practice)
        await conn.execute(emulation.clear_device_metrics_override())

        # 6. Save the screenshot data to a file
        now = datetime.datetime.now()
        timestamp = now.strftime(TIME_FORMAT_MICROSECONDS)
        save_picture(timestamp, path, file_name, screenshot_data)
    except Exception as e:
        raise WebDriverError("Failed to take screenshot.") from e


async def get_named_cookie(conn, name) -> dict:
    """Get cookie by name.

    This function retrieves a cookie from the WebDriver session based on the specified name.

    Args:
        conn: CDPConnection: The base URL of the WebDriver server..
        name: The name of the cookie to retrieve.

    Returns:
        A dictionary representing the cookie if found, otherwise an empty dictionary.

    Raises:
        WebDriverError: If the request to get the cookie fails.
    """
    try:
        cookies = await conn.execute(network.get_all_cookies())
        return [c for c in cookies if c.name == name][0].to_json()
    except Exception as e:
        raise WebDriverError(f"Failed to get cookie '{name}'.") from e


async def get_computed_label(conn: CDPConnection, element: dom.NodeId) -> str:
    """Get the element tag computed label. Get the accessibility name.

    Args:
        conn: CDPConnection: The base URL of the WebDriver server..
        element: The identifier of the element to retrieve the computed label for.

    Returns:
        The computed label of the element, which represents its accessibility name.

    Raises:
        WebDriverError: If retrieving the computed label fails.
    """
    try:
        await conn.execute(accessibility.enable())
        # Query the accessibility tree for the specific node
        # The queryAXTree command takes a nodeId (among other possible identifiers)
        ax_nodes_response = await conn.execute(accessibility.get_partial_ax_tree(node_id=element))

        # The response contains a list of AXNode objects
        # The target node's info should be in the list
        for ax_node in ax_nodes_response:
            # Check if this is the correct node and extract its name/label
            # The 'name' property holds the computed accessible name
            if ax_node.name.value:
                return ax_node.name.value
    except Exception as e:
        raise WebDriverError("Failed to get element computed label.") from e


async def get_computed_role(conn, session, element) -> str:
    """Get the element tag computed role (the element role).

    Args:
        conn: CDPConnection: The base URL of the WebDriver server..
        element: The identifier of the element to retrieve the computed role for.
        session_http: An optional HTTP client session for making requests.
        If not provided, a default session will be used.

    Returns:
        The computed role of the element, which represents its accessibility role.

    Raises:
        WebDriverError: If retrieving the computed role fails.
    """
    try:
        url = f"{conn: CDPConnection}/session/{session}/element/{element}/computedrole"
        response = await _get(url, session_http)
        return response.get("value", "")
    except Exception as e:
        raise WebDriverError("Failed to get element computed label.") from e


async def get_tag_name(conn, session, element) -> str:
    """
    Get the tag name of a specified element in a WebDriver session.

    Parameters:
        conn: CDPConnection: The base URL of the WebDriver server.
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
        url = f"{conn: CDPConnection}/session/{session}/element/{element}/name"
        response = await _get(url, session_http)
        return response.get("value", "")
    except Exception as e:
        raise WebDriverError("Failed to get element name.") from e


async def get_shadow_root(conn: CDPConnection, element: str) -> str:
    """
    Get the shadow root element from a specified web element.

    Args:
        conn: CDPConnection: The URL of the WebDriver server.
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
        url = f"{conn: CDPConnection}/session/{session}/element/{element}/shadow"
        response = await _get(url, session_http)
        return response.get("value", {}).get(root_element)
    except Exception as e:
        raise WebDriverError("Failed to get element shadow.") from e


async def get_shadow_element(
    conn: CDPConnection,
    shadow_element: str,
    locator_type: str,
    locator_value: str,
    session_http: Union[ClientSession, None] = None,
) -> str:
    """Get the shadow root element"""
    """
    Get the shadow root element from a web page using the W3C WebDriver Specification.

    Parameters:
        conn: CDPConnection: The base URL of the WebDriver server.
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
        url: str = f"{conn: CDPConnection}/session/{session}/shadow/{shadow_element}/element"
        payload: Dict[str, str] = {"using": locator_type, "value": locator_value}
        response: Dict[str, Any] = await _post(url, payload, session_http)
        return response.get("value", {}).get(ELEMENT_W3C, "")
    except Exception as e:
        raise WebDriverError("Failed to get the element shadow.") from e


async def get_shadow_elements(
    conn: CDPConnection,
    shadow_element: str,
    locator_type: str,
    locator_value: str,
    session_http: Union[ClientSession, None] = None,
) -> List[str]:
    """
    Get the list of shadow root elements.

    Args:
        conn: CDPConnection: The base URL of the WebDriver server.
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
        url: str = f"{conn: CDPConnection}/session/{session}/shadow/{shadow_element}/elements"
        payload: Dict[str, str] = {"using": locator_type, "value": locator_value}
        response: Dict[str, Any] = await _post(url, payload, session_http)
        return [x.get(ELEMENT_W3C) for x in response.get("value", {})]
    except Exception as e:
        raise WebDriverError("Failed to get the element shadow.") from e


async def get_rect(conn, session, element) -> dict:
    """Get the element rectangle"""
    try:
        url = f"{conn: CDPConnection}/session/{session}/element/{element}/rect"
        response = await _get(url, session_http)
        return response.get("value", {})
    except Exception as e:
        raise WebDriverError("Failed to get element rect.") from e


async def actions(conn, session, payload):
    url = f"{conn: CDPConnection}/session/{session}/actions"
    await _post(url, payload, session_http=session_http)
    return True


async def actions_move_to_element(conn: CDPConnection, element: str) -> bool:
    """
    Move to an element simulating a mouse movement.

    This function sends a WebDriver Actions command to move the mouse pointer to a
    specified element, following the W3C WebDriver Specification.

    Args:
        conn: CDPConnection: The URL of the WebDriver server..
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
        return await actions(conn, session, payload, session_http=session_http)
    except Exception as e:
        raise WebDriverError("Failed to move to element.") from e


async def actions_scroll_to_element(
    conn: CDPConnection,
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
        return await actions(conn, session, payload, session_http=session_http)
    except Exception as e:
        raise WebDriverError("Failed to scroll to element.") from e


async def submit(conn, session, element):
    """Submit a form. It is similar to 'submit' funtion in Seleniu
    It is not part of W3C WebDriver. Just added for convenience
    """
    try:
        submit_element = await find_child_element(
            conn,
            session,
            element,
            locator_type="xpath",
            locator_value="*[@type='submit']",
            session_http=session_http,
        )
        return await click(conn, session, submit_element, session_http=session_http)
    except Exception as e:
        raise WebDriverError("Failed to submit form.") from e


async def actions_click(conn, session, element):
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
        return await actions(conn, session, payload, session_http=session_http)
    except Exception as e:
        raise WebDriverError("Failed to click the element.") from e


async def set_timeouts(conn, session, timeouts):
    """Set timeouts"""
    try:
        url = f"{conn: CDPConnection}/session/{session}/timeouts"
        payload = {
            "implicit": timeouts,
        }
        await _post(url, payload, session_http=session_http)
        return True
    except Exception as e:
        raise WebDriverError("Failed to set timeouts.") from e


async def find_children_elements(
    conn: CDPConnection,
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
        url = f"{conn: CDPConnection}/session/{session}/element/{parent_element}/elements"
        payload = {"using": locator_type, "value": locator_value, "id": parent_element}
        response = await _post(url, payload, session_http=session_http)
        return get_elements(response)
    except Exception as e:
        raise WebDriverError(
            f"Failed to find the children elements from '{parent_element}'."
        ) from e


async def find_child_element(
    conn: CDPConnection,
    parent_element: str,
    locator_type: str,
    locator_value: str,
    session_http: Union[ClientSession, None] = None,
):
    """Find the child element by 'locator_type'"""
    locator_type, locator_value = convert_locator_to_css_selector(locator_type, locator_value)
    try:
        url = f"{conn: CDPConnection}/session/{session}/element/{parent_element}/element"
        payload = {"using": locator_type, "value": locator_value, "id": parent_element}
        response = await _post(url, payload, session_http=session_http)
        return get_element(response)
    except Exception as e:
        raise WebDriverError(f"Failed to find the child element from '{parent_element}'.") from e


async def get_page_source(conn) -> str:
    """Get the page source (all content)"""
    try:
        url = f"{conn: CDPConnection}/session/{session}/source"
        response = await _get(url, session_http=session_http)
        return response.get("value", "")
    except Exception as e:
        raise WebDriverError("Failed to get the page source.") from e


async def execute_script(
    conn: CDPConnection,
    script: str,
    args: List = [],
    session_http: Union[ClientSession, None] = None,
):
    """Executes a script, like 'alert('something')' to open an alert window"""
    try:
        url = f"{conn: CDPConnection}/session/{session}/execute/async"
        payload = {"script": script, "args": args}
        response = await _post(url, payload, session_http=session_http)
        return response.get("value")
    except Exception as e:
        raise WebDriverError("Failed to execute script.") from e


async def get_alert_text(conn) -> str:
    """Get the text from an alert"""
    try:
        url = f"{conn: CDPConnection}/session/{session}/alert/text"
        response = await _get(url, session_http=session_http)
        return response.get("value", "")
    except Exception as e:
        raise WebDriverError("Failed to get the alert text.") from e


async def get_active_element(conn):
    """Get the active element"""
    try:
        url = f"{conn: CDPConnection}/session/{session}/element/active"
        response = await _get(url, session_http=session_http)
        return get_element(response)
    except Exception as e:
        raise WebDriverError("Failed to check if element is selected.") from e


async def clear_element(conn, session, element):
    """Clear the element text"""
    try:
        url = f"{conn: CDPConnection}/session/{session}/element/{element}/clear"
        payload = {"id": element}
        await _post(url, payload, session_http=session_http)
        return True
    except Exception as e:
        raise WebDriverError("Failed to clear the element text.") from e


async def is_element_enabled(conn, session, element) -> bool:
    """Check if element is enabled"""
    try:
        url = f"{conn: CDPConnection}/session/{session}/element/{element}/enabled"
        response = await _get(url, session_http=session_http)
        return response.get("value", False)
    except Exception as e:
        raise WebDriverError("Failed to check if element is enabled.") from e


# async def get_css_value(
#     conn, session, element, property_name
# ) -> str:
#     """Get CSS value"""
#     try:
#         url = f"{conn: CDPConnection}/session/{session}/element/{element}/css/{property_name}"
#         response = await _get(url, session_http=session_http)
#         return response.get("value", "")
#     except Exception as e:
#         raise WebDriverError("Failed to get css value.") from e


# async def is_element_selected(
#     conn, session, element
# ) -> bool:
#     """Check if element is selected"""
#     try:
#         url = f"{conn: CDPConnection}/session/{session}/element/{element}/selected"
#         response = await _get(url, session_http=session_http)
#         return bool(response.get("value"))
#     except Exception as e:
#         raise WebDriverError("Failed to check if element is selected.") from e


async def get_window_rectangle(conn) -> dict:
    """Get window rectangle"""
    try:
        url = f"{conn: CDPConnection}/session/{session}/window/rect"
        response = await _get(url, session_http=session_http)
        return response.get("value", {})
    except Exception as e:
        raise WebDriverError("Failed to get window rectangle.") from e


async def get_window_handles(conn: CDPConnection) -> list:
    """Get window handles"""
    try:
        targets = await conn.execute(target.get_targets())
        return [t for t in targets if t.type_ == "page"]
    except Exception as e:
        raise WebDriverError("Failed to get window handles.") from e


async def close_window(conn) -> list:
    """Close active window"""
    try:
        url = f"{conn: CDPConnection}/session/{session}/window"
        response = await _delete(url, session_http=session_http)
        return response.get("value")
    except Exception as e:
        raise WebDriverError("Failed to close active window.") from e


async def get_window(conn) -> str:
    """Get window"""
    try:
        url = f"{conn: CDPConnection}/session/{session}/window"
        response = await _get(url, session_http=session_http)
        return response.get("value", "")
    except Exception as e:
        raise WebDriverError("Failed to get window.") from e


# async def go_back(conn):
#     """
#     This command causes the browser to traverse one step backward
#     in the joint session history of the
#     current browse. This is equivalent to pressing the back button in the browser.
#     """
#     try:
#         url = f"{conn: CDPConnection}/session/{session}/back"
#         await _post(url, {}, session_http=session_http)
#         return True
#     except Exception as e:
#         raise WebDriverError("Failed to go back to page.") from e


# async def get_url(conn) -> str:
#     """Returns the URL from web page:"""
#     try:
#         url = f"{conn: CDPConnection}/session/{session}/url"
#         response = await _get(url, session_http=session_http)
#         return response.get("value", "")
#     except Exception as e:
#         raise WebDriverError("Failed to get page url.") from e


async def get_timeouts(conn) -> dict:
    """
    Returns the configured timeouts:
        {"implicit": 0, "pageLoad": 300000, "script": 30000}
    """
    try:
        url = f"{conn: CDPConnection}/session/{session}/timeouts"
        response = await _get(url, session_http=session_http)
        return response.get("value", {})
    except Exception as e:
        raise WebDriverError("Failed to get timeouts.") from e


async def get_status(conn: CDPConnection) -> dict:
    """Returns the status and details of the WebDriver"""
    try:
        url = f"{conn: CDPConnection}/status"
        response = await _get(url, session_http=session_http)
        return response
    except Exception as e:
        raise WebDriverError("Failed to get status.") from e


async def get_cookies(conn: CDPConnection) -> list:
    """Get the page cookies"""
    try:
        url = f"{conn: CDPConnection}/session/{session}/cookie"
        response = await _get(url, session_http=session_http)
        return response.get("value", [])
    except Exception as e:
        raise WebDriverError("Failed to get page cookies.") from e


async def close_session(conn):
    """Close an opened session and close the browser"""
    try:
        url = f"{conn: CDPConnection}/session/{session}"
        await _delete(url, session_http=session_http)
        return True
    except Exception as e:
        raise WebDriverError("Failed to close session.") from e


async def get_session(
    conn: CDPConnection,
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
        url = f"{conn: CDPConnection}/session"
        response = await _post(url, capabilities, session_http=session_http)
        return response.get("sessionId")
    except Exception as e:
        raise WebDriverError("Failed to open session. Check the browser capabilities.") from e
