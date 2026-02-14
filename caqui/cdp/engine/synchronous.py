# Copyright (C) 2023 Caqui - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://github.com/douglasdcm/caqui

import datetime
import json
import threading
import urllib.request
from typing import Any, Dict, List, Optional
from urllib.parse import urlparse

from bs4 import BeautifulSoup

from caqui._vendor.chrome_devtools_protocol.cdp import (
    accessibility,
    browser,
    dom,
    emulation,
    input_,
    network,
    page,
    runtime,
    storage,
    target,
)
from caqui.cdp.by import By
from caqui.cdp.connection import SyncCDPConnection
from caqui.constants import TIME_FORMAT_MICROSECONDS, TIMEOUT
from caqui.exceptions import WebDriverError
from caqui.helper import convert_locator_to_css_selector_or_xpath, save_picture


class GlobalValues:
    _doc: Optional[dom.Node] = None
    conn: SyncCDPConnection = None

    def get_document_node(refresh=False) -> dom.Node:
        if refresh:
            GlobalValues._doc = None
        if not GlobalValues.conn:
            raise WebDriverError("No connection")
        if not GlobalValues._doc:
            GlobalValues._doc = GlobalValues.conn.execute(dom.get_document(depth=-1, pierce=True))
        return GlobalValues._doc


def _get_element_center(conn, element):
    box_model = conn.execute(dom.get_box_model(node_id=element))
    content_box = box_model.content
    center_x = (content_box[0] + content_box[2]) / 2
    center_y = (content_box[1] + content_box[5]) / 2
    return center_x, center_y


def _find_element_by_xpath(
    conn: SyncCDPConnection,
    xpath: str,
    root_id: Optional[dom.NodeId] = None,
) -> dom.NodeId:
    if root_id:
        remote_root = conn.execute(dom.resolve_node(node_id=root_id))
    else:
        node = GlobalValues.get_document_node()
        remote_root = conn.execute(dom.resolve_node(node_id=node.node_id))
    object_id = remote_root.object_id
    call_res = conn.execute(
        runtime.call_function_on(
            object_id=object_id,
            function_declaration=f"""
            function() {{
                const doc = this.ownerDocument || this;
                const r = doc.evaluate(
                    `{xpath}`,
                    this,
                    null,
                    XPathResult.FIRST_ORDERED_NODE_TYPE,
                    null
                );
                return r.singleNodeValue;
            }}
            """,
            return_by_value=False,
        )
    )
    remote = call_res[0]
    if not remote.object_id:
        raise WebDriverError("XPath returned no element")
    node = conn.execute(dom.request_node(object_id=remote.object_id))
    if node == 0:
        raise WebDriverError("Resolved object is not a DOM node")
    return node


def _find_all_elements_by_xpath(
    conn: SyncCDPConnection,
    xpath: str,
    root_id: Optional[dom.NodeId] = None,
) -> List[dom.NodeId]:
    if root_id:
        remote_root = conn.execute(dom.resolve_node(node_id=root_id))
    else:
        node = GlobalValues.get_document_node()
        remote_root = conn.execute(dom.resolve_node(node_id=node.node_id))

    object_id = remote_root.object_id

    call_res = conn.execute(
        runtime.call_function_on(
            object_id=object_id,
            function_declaration=f"""
            function () {{
                const doc = this.ownerDocument || this;
                const snapshot = doc.evaluate(
                    `{xpath}`,
                    this,
                    null,
                    XPathResult.ORDERED_NODE_SNAPSHOT_TYPE,
                    null
                );

                const results = [];
                for (let i = 0; i < snapshot.snapshotLength; i++) {{
                    results.push(snapshot.snapshotItem(i));
                }}
                return results;
            }}
            """,
            return_by_value=False,
        )
    )

    remote_array = call_res[0]

    if not remote_array.object_id:
        raise WebDriverError("XPath returned no elements")

    properties = conn.execute(
        runtime.get_properties(object_id=remote_array.object_id, own_properties=True)
    )

    nodes: List[dom.NodeId] = []

    for prop in properties[0]:
        if not prop.name.isdigit():
            continue

        remote_node = prop.value
        if not remote_node or not remote_node.object_id:
            continue

        node_id = conn.execute(dom.request_node(object_id=remote_node.object_id))

        if node_id != 0:
            nodes.append(node_id)

    if not nodes:
        raise WebDriverError("Resolved objects are not DOM nodes")

    return nodes


def describe_node_id(conn: SyncCDPConnection, node_id: dom.NodeId):
    if not node_id:
        raise WebDriverError(f"Invalid node id '{node_id}'")
    return conn.execute(dom.describe_node(node_id))


def _find_element_by_css_selector(
    conn: SyncCDPConnection, root_id: dom.NodeId, depth: int, pierce: bool, selector: str
):
    if root_id:
        node = conn.execute(dom.describe_node(root_id))
    else:
        node = GlobalValues.get_document_node()
    node_id = conn.execute(dom.query_selector(node_id=node.node_id, selector=selector))
    if not node_id:
        raise WebDriverError()
    return node_id


def _find_element(
    conn: SyncCDPConnection,
    locator_type,
    locator_value: str,
    root_id: dom.NodeId = None,
    depth=1,
    pierce=False,
):
    locator_type, selector = convert_locator_to_css_selector_or_xpath(locator_type, locator_value)
    if locator_type == By.XPATH:
        try:
            return _find_element_by_xpath(conn, selector, root_id)
        except Exception:
            raise
    if locator_type == By.CSS_SELECTOR:
        return _find_element_by_css_selector(conn, root_id, depth, pierce, selector)
    raise WebDriverError(f"Could not find element with selector: {locator_value}")


def _find_all_elements(
    conn: SyncCDPConnection,
    locator_type,
    locator_value: str,
    root_id: dom.NodeId = None,
):
    locator_type, locator_value = convert_locator_to_css_selector_or_xpath(
        locator_type, locator_value
    )
    if locator_type == By.XPATH:
        return _find_all_elements_by_xpath(conn, locator_value, root_id)
    if locator_type == By.CSS_SELECTOR:
        if root_id:
            node = conn.execute(dom.describe_node(root_id))
        else:
            node = GlobalValues.get_document_node()
        node_id = conn.execute(dom.query_selector_all(node_id=node.node_id, selector=locator_value))
        if not node_id:
            raise WebDriverError()
        return node_id


def _handle_alert(conn: SyncCDPConnection, alert_element, timeout, function_callback, text=None):
    click_task = threading.Thread(target=click, args=(conn, alert_element))
    click_task.daemon = True
    click_task.start()
    click_task.join()
    current_datetime = datetime.datetime.now()
    time_to_add = datetime.timedelta(seconds=timeout)
    new_datetime = current_datetime + time_to_add
    while 1 == 1:  # Used 1==1 and not True to deceive VSCode
        while datetime.datetime.now() < new_datetime:
            event = conn.get_event_nowait()
            if event is None:
                continue
            if isinstance(event, page.JavascriptDialogOpening):
                function_callback(conn, text)
                return event.message
        raise TimeoutError()
    click_task


def _send_test_to_prompt_alert(conn: SyncCDPConnection, text):
    conn.execute(page.handle_java_script_dialog(accept=True, prompt_text=text))


def _accept_alert(conn: SyncCDPConnection, text):
    conn.execute(page.handle_java_script_dialog(accept=True))


def _dismiss_alert(conn: SyncCDPConnection, text):
    conn.execute(page.handle_java_script_dialog(accept=False))


def _set_screen(conn, screen_type: str = "fullscreen"):
    window_for_target = conn.execute(browser.get_window_for_target())
    window_id = window_for_target[0]
    bounds = browser.Bounds.from_json({"windowState": screen_type})
    conn.execute(browser.set_window_bounds(window_id=window_id, bounds=bounds))


def get(conn: SyncCDPConnection, page_url: str) -> None:
    """Does the same of 'go_to_page'. Added to be compatible with selenium method name'"""
    try:
        conn.execute(page.enable())
        conn.execute(page.navigate(url=page_url))
        conn.execute(
            target.set_auto_attach(auto_attach=True, wait_for_debugger_on_start=False, flatten=True)
        )
        _refresh_agents(conn)
    except Exception as e:
        raise WebDriverError(f"Failed to navigate to page '{page_url}'.") from e


def _refresh_agents(conn: SyncCDPConnection):
    conn.execute(page.enable())
    conn.execute(dom.enable())
    conn.execute(runtime.enable())
    conn.execute(network.enable())
    conn.execute(accessibility.enable()),
    GlobalValues.conn = conn
    GlobalValues.get_document_node(refresh=True)


def go_to_page(conn, page_url: str) -> None:
    """Navigate to 'page_url'"""
    get(conn, page_url)


def find_element(
    conn: SyncCDPConnection, locator_type: str, locator_value: str, root_id: dom.NodeId = None
) -> dom.NodeId:
    """Find an element by a 'selector', for example an 'xpath' like '//div[@id="example"]'

    `Attention`: it opens Alerts/Prompt elements automatically.
    Not applicable for elements in iframes.
    """
    try:
        return _find_element(conn, locator_type, locator_value, root_id)
    except Exception as e:
        raise WebDriverError(f"Could not find element with selector: {locator_value}") from e


def find_elements(conn: SyncCDPConnection, locator_type, locator_value: str):
    """Find an element by a 'selector', for example an 'xpath' like '//div[@id="example"]'"""
    try:
        return _find_all_elements(conn, locator_type, locator_value)
    except Exception as e:
        raise WebDriverError(f"Could not find element with selector: {locator_value}") from e


def click(conn: SyncCDPConnection, element):
    """Click on an element"""
    try:
        center_x, center_y = _get_element_center(conn, element)
        commands = []
        mouse_button = input_.MouseButton("left")
        commands.append(
            input_.dispatch_mouse_event(
                "mousePressed", center_x, center_y, button=mouse_button, click_count=1
            )
        )
        commands.append(
            input_.dispatch_mouse_event(
                "mouseReleased", center_x, center_y, button=mouse_button, click_count=1
            )
        )
        for command in commands:
            conn.execute(command, wait=False)
    except Exception as e:
        raise WebDriverError("Failed to click on element.") from e


def send_keys(conn: SyncCDPConnection, element, text: str):
    """Send keys to an element"""
    try:
        conn.execute(dom.focus(node_id=element))
        for char in text:
            conn.execute(
                input_.dispatch_key_event(
                    "keyDown",
                    text=char,
                    unmodified_text=char,
                    windows_virtual_key_code=ord(char),
                    native_virtual_key_code=ord(char),
                )
            )
            conn.execute(
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


def get_text(conn: SyncCDPConnection, element) -> str:
    """Get the text of an element"""
    try:
        result = execute_script(conn, element, "value")
        if result and result[0].value:
            return result[0].value
        html_doc = conn.execute(dom.get_outer_html(node_id=element))
        soup = BeautifulSoup(html_doc, "html.parser")
        return soup.get_text()
    except Exception as e:
        raise WebDriverError("Failed to get text from element.") from e


def get_attribute(conn: SyncCDPConnection, element, attribute: str) -> str:
    """Get the given HTML attribute of an element, for example, 'aria-valuenow'"""
    try:
        attributes = conn.execute(dom.get_attributes(node_id=element))
        attr_dict = {attributes[i]: attributes[i + 1] for i in range(0, len(attributes), 2)}
        result = attr_dict.get(attribute)
        if result is None:
            raise WebDriverError("Failed to get value from element.")
        return result
    except Exception as e:
        raise WebDriverError("Failed to get value from element.") from e


def get_title(conn: SyncCDPConnection) -> str:
    """Get the page title"""
    try:
        target_info = conn.execute(target.get_target_info())
        return target_info.title if target_info.type_ == "page" else ""
    except Exception:
        pass
    try:
        root_node = GlobalValues.get_document_node()
        title_node_id = conn.execute(
            dom.query_selector(node_id=root_node.node_id, selector="title")
        )
        result = conn.execute(dom.get_outer_html(node_id=title_node_id))
        return BeautifulSoup(result, "html.parser").get_text()
    except Exception as e:
        raise WebDriverError("Failed to get page title.") from e


def get_url(conn: SyncCDPConnection) -> str:
    """Returns the URL from web page:"""
    try:
        frame_tree = conn.execute(page.get_frame_tree())
        current_url = frame_tree.frame.url
        return current_url
    except Exception as e:
        raise WebDriverError("Failed to get page url.") from e


def go_back(conn: SyncCDPConnection):
    try:
        result = conn.execute(page.get_navigation_history())
        current = result[0]
        if current <= 0:
            return
        entry = result[1][current - 1]
        conn.execute(page.navigate_to_history_entry(entry.id_))
        _refresh_agents(conn)
    except Exception as e:
        raise WebDriverError("Failed to go back to page.") from e


def is_element_selected(conn: SyncCDPConnection, element) -> bool:
    """Check if element is selected"""
    try:
        try:
            get_attribute_value = get_attribute(conn, element, "checked")
            return get_attribute_value.lower() == ""
        except WebDriverError:
            pass
        try:
            get_attribute_value = get_attribute(conn, element, "selected")
            return get_attribute_value.lower() == ""
        except WebDriverError:
            pass
        return False
    except Exception as e:
        raise WebDriverError("Failed to check if element is selected.") from e


def get_css_value(conn: SyncCDPConnection, element, property_name) -> str:
    """Get CSS value"""
    try:
        styles = get_attribute(conn, element, "style")
        if styles is None:
            return ""
        styles = styles.split(";")
        for s in styles:
            items = s.split(":")
            if len(items) == 2:
                if items[0].strip() == property_name:
                    return items[1].strip()
        raise WebDriverError("Failed to get css value.")
    except Exception as e:
        raise WebDriverError("Failed to get css value.") from e


def get_property(conn: SyncCDPConnection, element: dom.NodeId, property_name) -> str:
    try:
        result = get_attribute(conn, element, property_name)
        if result is None:
            return ""
        return result
    except Exception as e:
        raise WebDriverError("Failed to get property.") from e


def get_cookies(conn: SyncCDPConnection) -> list:
    """Get the page cookies"""
    try:
        cookies = conn.execute(storage.get_cookies())
        return [c.to_json() for c in cookies]
    except Exception as e:
        raise WebDriverError("Failed to get page cookies.") from e


def add_cookie(conn: SyncCDPConnection, cookie: Dict[str, Any]):
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
        conn.execute(
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


def delete_cookie(
    conn: SyncCDPConnection, name: str, url: Optional[str] = None, domanin: Optional[str] = None
):
    """
    Delete cookie by name

    This function deletes a cookie with the specified name from the WebDriver session.
    Based on W3C WebDriver Specification.

    Args:
        conn: CDPConnectionSync: The connection to the websocket
        name: The name of the cookie to delete

    Returns:
        None

    Raises:
        WebDriverError: If the cookie deletion fails
    """
    try:
        conn.execute(network.delete_cookies(name=name, url=url, domain=domanin))
    except Exception as e:
        raise WebDriverError(f"Failed to delete cookie '{name}'.") from e


def refresh_page(conn: SyncCDPConnection):
    """
    Refreshes the current page by making an HTTP POST request to the server URL.

    Args:
        conn: (CDPConnectionSync): The base URL of the server.
    Returns:
        None
    """
    try:
        conn.execute(page.reload())
        GlobalValues.get_document_node(refresh=True)
    except Exception as e:
        raise WebDriverError("Failed to refresh page.") from e


def go_forward(conn: SyncCDPConnection):
    """
    Go to page forward.

    This function sends a POST request to the specified URL,
    with an empty payload, and returns True if successful.

    Parameters:
        conn: (CDPConnectionSync): The base URL of the server.

    Returns:
        None
    """
    try:
        result = conn.execute(page.get_navigation_history())
        current = result[0]
        entry = result[1][current + 1]
        conn.execute(page.navigate_to_history_entry(entry.id_))
        _refresh_agents(conn)
    except Exception as e:
        raise WebDriverError("Failed to go to page forward.") from e


def set_window_rectangle(
    conn: SyncCDPConnection,
    width: int,
    height: int,
    left: Optional[int] = None,
    top: Optional[int] = None,
):
    """
    Set window rectangle.

    This function sets the window size and position based on W3C WebDriver Specification.

    Args:
        conn: CDPConnectionSync: The connection to the websocket
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
        window_for_target = conn.execute(browser.get_window_for_target())
        window_id = window_for_target[0]
        bounds: Dict[str, Any] = {}
        if left is not None:
            bounds["left"] = left
        if top is not None:
            bounds["top"] = top
        bounds = browser.Bounds.from_json({"width": width, "height": height})
        conn.execute(browser.set_window_bounds(window_id=window_id, bounds=bounds))
    except Exception as e:
        raise WebDriverError("Failed to set window rectangle.") from e


def fullscreen_window(conn: SyncCDPConnection):
    """
    Fullscreen window.

    This function fullscreens the window based on W3C WebDriver Specification.

    Args:
        conn: CDPConnectionSync: The connection to the websocket

    Returns:
        None

    Raises:
        WebDriverError: If the fullscreen operation fails
    """
    try:
        _set_screen(conn, "normal")
        _set_screen(conn, "fullscreen")
    except Exception as e:
        raise WebDriverError("Failed to fullscreen window.") from e


def minimize_window(conn: SyncCDPConnection):
    """
    Minimize window.

    This function minimizes the window based on W3C WebDriver Specification.

    Args:
        conn: CDPConnectionSync: The connection to the websocket

    Returns:
        None

    Raises:
        WebDriverError: If the minimize operation fails
    """
    try:
        _set_screen(conn, "normal")
        _set_screen(conn, "minimized")
    except Exception as e:
        raise WebDriverError("Failed to minimize window.") from e


def maximize_window(conn: SyncCDPConnection):
    """
    Maximize window.

    This function maximizes the window based on W3C WebDriver Specification.

    Args:
        conn: CDPConnectionSync: The connection to the websocket

    Returns:
        None

    Raises:
        WebDriverError: If the maximize operation fails
    """
    try:
        _set_screen(conn, "normal")
        _set_screen(conn, "maximized")
    except Exception as e:
        raise WebDriverError("Failed to maximize window.") from e


def switch_to_window(conn: SyncCDPConnection, handle: target.TargetInfo):
    """
    Switch to window.

    This function switches the WebDriver context to a different window by its handle.
    Based on W3C WebDriver Specification.

    Args:
        conn: CDPConnectionSync: The connection to the websocket.

    Returns:
        new_conn (CDPConnectionSync): The new connection to the websocket.

    Raises:
        WebDriverError: If the switch to window operation fails.
    """
    if not handle:
        raise WebDriverError("Handle not informed")
    try:
        handles = get_window_handles(conn)
        index = 0
        for h in handles:
            if h.target_id == handle.target_id:
                break
            index += 1
        port = urlparse(conn.url).port
        with urllib.request.urlopen(f"http://127.0.0.1:{port}/json") as r:
            targets = json.loads(r.read())
            targets_page = [p for p in targets if p.get("type") == "page"]
            targets_page.reverse()
            ws_url = targets_page[index]["webSocketDebuggerUrl"]
            conn.set_url(ws_url)
            conn.connect()
            new_conn = conn
            _refresh_agents(new_conn)
            return new_conn
    except Exception as e:
        raise WebDriverError("Failed to switch to window.") from e


def new_window(conn: SyncCDPConnection) -> None:
    """
    Open a new window.

    This function opens a new window or tab based on W3C WebDriver Specification.

    Args:
        conn: CDPConnectionSync: The connection to the websocket
        window_type: The type of window to open ('tab' or 'window'). Defaults to 'tab'

    Returns:
        None

    Raises:
        WebDriverError: If the window creation fails
    """
    try:
        conn.execute(
            target.create_target(
                url="about:blank",
            )
        )
    except Exception as e:
        raise WebDriverError("Failed to open window.") from e


def switch_to_parent_frame(conn: SyncCDPConnection):
    """
    Switch to parent frame of 'element_frame'.

    This function switches the WebDriver context to the parent frame of the specified frame element.
    Based on W3C WebDriver Specification.

    Args:
        conn: CDPConnectionSync: The connection to the websocket
        element_frame: The frame element identifier whose parent frame to switch to

    Returns:
        None

    Raises:
        WebDriverError: If the switch to parent frame operation fails
    """
    try:
        doc = conn.execute(dom.get_document(depth=1))
        doc = GlobalValues.get_document_node()
        return doc.node_id
    except Exception as e:
        raise WebDriverError("Failed to switch to parent frame.") from e


def switch_to_frame(conn: SyncCDPConnection, element_frame: str) -> dom.NodeId:
    """
    Switch to frame 'element_frame'.

    This function switches the WebDriver context to the specified frame element.
    Based on W3C WebDriver Specification.

    Args:
        conn: CDPConnectionSync: The connection to the websocket
        element_frame: The frame element identifier to switch to

    Returns:
        cdp.dom.Node

    Raises:
        WebDriverError: If the switch to frame operation fails
    """
    try:
        desc = conn.execute(dom.describe_node(node_id=element_frame, depth=1))
        return desc.content_document.node_id
    except Exception as e:
        raise WebDriverError("Failed to switch to frame.") from e


def delete_all_cookies(conn: SyncCDPConnection):
    """
    Delete all cookies for the current session.

    This function removes all cookies associated with the active session,
    following the W3C WebDriver Specification for cookie management.

    Args:
        conn: CDPConnectionSync: The connection to the websocket.

    Returns:
        None

    Raises:
        WebDriverError: If the cookie deletion request fails or an error occurs
                        during the deletion process.
    """
    try:
        conn.execute(network.clear_browser_cookies())
    except Exception as e:
        raise WebDriverError("Failed to delete cookies.") from e


def get_alert_text(conn: SyncCDPConnection, element: dom.NodeId) -> str:
    """Get the text from an alert"""
    try:
        return _handle_alert(conn, element, timeout=TIMEOUT, function_callback=_accept_alert)
    except Exception as e:
        raise WebDriverError("Failed to get the alert text.") from e


def send_alert_text(
    conn: SyncCDPConnection, alert_element: dom.NodeId, text, timeout: float = TIMEOUT
):
    """
    Send text to an alert dialog.

    This function sends text to the currently open alert dialog and closes it.
    Based on W3C WebDriver Specification.

    Args:
        conn: CDPConnectionSync: The connection to the websocket
        alert_element: the alert element to send text
        text: The text to send to the alert dialog

    Returns:
        None

    Raises:
        WebDriverError: If sending text to the alert fails
    """
    try:
        _handle_alert(conn, alert_element, timeout, _send_test_to_prompt_alert, text)
    except Exception as e:
        raise WebDriverError("Failed to sent text to alert.") from e


def accept_alert(conn: SyncCDPConnection, alert_element: dom.NodeId, timeout: float = TIMEOUT):
    """
    Accept alert.

    This function accepts the currently open alert dialog.
    Based on W3C WebDriver Specification.

    Args:
        conn: CDPConnectionSync: The connection to the websocket
        alert_element: the alert to be accepted

    Returns:
        None

    Raises:
        WebDriverError: If the alert acceptance fails
    """
    try:
        _handle_alert(conn, alert_element, timeout, _accept_alert)
    except Exception as e:
        raise WebDriverError("Failed to accept alert.") from e


def dismiss_alert(conn: SyncCDPConnection, alert_element: dom.NodeId, timeout: float = TIMEOUT):
    """Dismiss alert

    This function dismisses the currently open alert dialog.
    Based on W3C WebDriver Specification.

    Args:
        conn: CDPConnectionSync: The connection to the websocket.
        alert_element: the alert to be dismissed

    Returns:
        None

    Raises:
        WebDriverError: If the alert dismissal fails.
    """
    try:
        _handle_alert(conn, alert_element, timeout, _dismiss_alert)
    except Exception as e:
        raise WebDriverError("Failed to dismiss alert.") from e


def take_screenshot_element(
    conn: SyncCDPConnection,
    element,
    path="/tmp",
    file_name="caqui",
):
    """Take screenshot of element

    Args:
        conn: CDPConnectionSync: The connection to the websocket..
        element: The identifier of the element to take a screenshot of.
        path: The directory path where the screenshot will be saved.
        file_name: The name of the file to save the screenshot as.

    Returns:
        None

    Raises:
        WebDriverError: If taking the screenshot fails.
    """
    try:
        box_model = conn.execute(dom.get_box_model(node_id=element))
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
        screenshot_data = conn.execute(page.capture_screenshot(clip=clip))
        save_picture(timestamp, path, file_name, screenshot_data)
    except Exception as e:
        raise WebDriverError("Failed to take screenshot from element.") from e


def take_screenshot(
    conn: SyncCDPConnection,
    path: str = "/tmp",
    file_name: str = "caqui",
):
    """Take screenshot

    Args:
        conn: CDPConnectionSync: The connection to the websocket..
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
        metrics = conn.execute(page.get_layout_metrics())
        content_size = metrics[-1]
        full_width = content_size.width
        full_height = content_size.height

        # 3. Override the device metrics to match the full page size
        # This effectively makes the entire page visible in a single "viewport"
        viewport = page.Viewport(0, 0, full_width, full_height, 1)
        conn.execute(
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

        screenshot_data = conn.execute(page.capture_screenshot(quality=90))

        # 5. Reset viewport emulation (optional, good practice)
        conn.execute(emulation.clear_device_metrics_override())

        # 6. Save the screenshot data to a file
        now = datetime.datetime.now()
        timestamp = now.strftime(TIME_FORMAT_MICROSECONDS)
        save_picture(timestamp, path, file_name, screenshot_data)
    except Exception as e:
        raise WebDriverError("Failed to take screenshot.") from e


def get_named_cookie(conn, name) -> dict:
    """Get cookie by name.

    This function retrieves a cookie from the WebDriver session based on the specified name.

    Args:
        conn: CDPConnectionSync: The connection to the websocket..
        name: The name of the cookie to retrieve.

    Returns:
        A dictionary representing the cookie if found, otherwise an empty dictionary.

    Raises:
        WebDriverError: If the request to get the cookie fails.
    """
    try:
        cookies = get_cookies(conn)
        return [c for c in cookies if c.get("name") == name][0]
    except Exception as e:
        raise WebDriverError(f"Failed to get cookie '{name}'.") from e


def get_computed_label(conn: SyncCDPConnection, element: dom.NodeId) -> str:
    """Get the element tag computed label. Get the accessibility name.

    Args:
        conn: CDPConnectionSync: The connection to the websocket..
        element: The identifier of the element to retrieve the computed label for.

    Returns:
        The computed label of the element, which represents its accessibility name.

    Raises:
        WebDriverError: If retrieving the computed label fails.
    """
    try:
        # Query the accessibility tree for the specific node
        # The queryAXTree command takes a nodeId (among other possible identifiers)
        ax_nodes_response = conn.execute(accessibility.get_partial_ax_tree(node_id=element))

        # The response contains a list of AXNode objects
        # The target node's info should be in the list
        for ax_node in ax_nodes_response:
            # Check if this is the correct node and extract its name/label
            # The 'name' property holds the computed accessible name
            if ax_node.name.value:
                return ax_node.name.value
        return ""
    except Exception as e:
        raise WebDriverError("Failed to get element computed label.") from e


def get_computed_role(conn: SyncCDPConnection, element: dom.NodeId) -> str:
    """Get the element tag computed role (the element role).

    Args:
        conn: CDPConnectionSync: The connection to the websocket..
        element: The identifier of the element to retrieve the computed role for.

    Returns:
        A string representing the computed role

    Raises:
        WebDriverError: If retrieving the computed role fails.
    """
    try:
        # Get accessibility information for the node, including the role
        # We use getAXNodeAndAncestors to retrieve the AXNode object which holds computed properties
        ax_nodes_response = conn.execute(accessibility.get_ax_node_and_ancestors(node_id=element))

        # The response is a list of nodes, the first one is the target node
        if ax_nodes_response:
            target_ax_node = ax_nodes_response[0]
            computed_role = target_ax_node.role.value
            return computed_role
        return ""
    except Exception as e:
        raise WebDriverError("Failed to get element computed label.") from e


def get_tag_name(conn: SyncCDPConnection, element: dom.NodeId) -> str:
    """
    Get the tag name of a specified element in a WebDriver session.

    Parameters:
        conn: CDPConnectionSync: The connection to the websocket.
        element: The identifier for the specific element whose tag name is to be retrieved.

    Returns:
        A string representing the tag name of the specified element.

    Raises:
        WebDriverError: If there is an error while attempting to retrieve the element's tag name.
    """
    try:
        result = conn.execute(dom.describe_node(node_id=element))
        return result.node_name
    except Exception as e:
        raise WebDriverError("Failed to get element name.") from e


# def get_shadow_element_v1(
#     conn: CDPConnectionSync,
#     shadow_root_locator_type: str,
#     shadoe_root_locator_value: str,
#     locator_type: str,
#     locator_value: str,
# ) -> dom.NodeId:
#     """
#     Get the shadow root element from a web page using the W3C WebDriver Specification.

#     Parameters:
#         conn: CDPConnectionSync: The connection to the websocket.
#         shadow_element: The ID or name of the shadow element to retrieve.
#         locator_type: The type of locator to use (e.g., 'css selector', 'xpath').
#         locator_value: The value of the locator to find the element.

#     Returns:
#         The shadow root element as a string, or an empty string if not found.

#     Raises:
#         WebDriverError: If there is an error retrieving the shadow element.
#     """
#     try:
#         host_node = _find_element(
#             conn, shadow_root_locator_type, shadoe_root_locator_value, depth=-1, pierce=True
#         )
#         host_details = conn.execute(dom.describe_node(node_id=host_node, depth=1))
#         shadow_roots = host_details.shadow_roots
#         return _find_element(conn, locator_type, locator_value, shadow_roots[0].node_id)
#     except Exception as e:
#         raise WebDriverError("Failed to get the element shadow.") from e


def get_shadow_element(
    conn: SyncCDPConnection,
    shadow_element,
    locator_type: str,
    locator_value: str,
) -> dom.NodeId:
    """
    Get the shadow root element from a web page using the W3C WebDriver Specification.

    Parameters:
        conn: CDPConnectionSync: The connection to the websocket.
        shadow_element: The ID or name of the shadow element to retrieve.
        locator_type: The type of locator to use (e.g., 'css selector', 'xpath').
        locator_value: The value of the locator to find the element.

    Returns:
        The shadow root element as a string, or an empty string if not found.

    Raises:
        WebDriverError: If there is an error retrieving the shadow element.
    """
    try:
        host_details = conn.execute(dom.describe_node(node_id=shadow_element, depth=1))
        shadow_roots = host_details.shadow_roots
        return _find_element(conn, locator_type, locator_value, shadow_roots[0].node_id)
    except Exception as e:
        raise WebDriverError("Failed to get the element shadow.") from e


def get_shadow_elements(
    conn: SyncCDPConnection,
    shadow_element: str,
    locator_type: str,
    locator_value: str,
) -> List[str]:
    """
    Get the list of shadow root elements.

    Args:
        conn: CDPConnectionSync: The connection to the websocket.
        shadow_element: The identifier for the shadow element to retrieve.
        locator_type: The type of locator to use (e.g., 'css selector', 'xpath').
        locator_value: The value of the locator to find the element.

    Returns:
        A list of shadow root element identifiers.

    Raises:
        WebDriverError: If there is an error retrieving the shadow elements.
    """
    """Get the list of shadow root elements"""
    try:
        host_details = conn.execute(dom.describe_node(node_id=shadow_element, depth=1))
        shadow_roots = host_details.shadow_roots
        return _find_all_elements(conn, locator_type, locator_value, shadow_roots[0].node_id)
    except Exception as e:
        raise WebDriverError("Failed to get the element shadow.") from e


def get_rect(conn: SyncCDPConnection, element) -> dict:
    """Get the element rectangle"""
    try:
        result = conn.execute(dom.get_box_model(node_id=element))
        # Quad([205, 103.4375, 226.484375, 103.4375, 226.484375, 118.4375, 205, 118.4375])
        content = result.content
        height = abs(content[-1] - content[1])
        width = abs(content[2] - content[0])
        x = content[0]
        y = content[1]
        return {"height": height, "width": width, "x": x, "y": y}
    except Exception as e:
        raise WebDriverError("Failed to get element rect.") from e


def actions_move_to_element(conn: SyncCDPConnection, element: str) -> None:
    """
    Move to an element simulating a mouse movement.

    This function sends a WebDriver Actions command to move the mouse pointer to a
    specified element, following the W3C WebDriver Specification.

    Args:
        conn: CDPConnectionSync: The connection to the websocket..
        element: The element identifier (W3C element reference) to move the pointer to.

    Returns:
        None

    Raises:
        WebDriverError: If the action fails to move to the element.

    Note:
        The mouse movement is performed with zero duration, resulting in an instant
        pointer movement to the element's location. The element reference follows the
        W3C WebDriver specification format.
    """
    """Move to an element simulating a mouse movement"""
    try:
        x, y = _get_element_center(conn, element)
        conn.execute(
            input_.dispatch_mouse_event(
                "mouseMoved",
                x=x,
                y=y,
            )
        )
    except Exception as e:
        raise WebDriverError("Failed to move to element.") from e


def actions_scroll_to_element(
    conn: SyncCDPConnection,
    element,
):
    """Scroll to an element simulating a mouse movement"""
    try:
        remote_object = conn.execute(dom.resolve_node(node_id=element))
        conn.execute(
            runtime.call_function_on(
                function_declaration="""
                    function() {
                        this.scrollIntoView({
                            block: 'center',
                            inline: 'center',
                            behavior: 'instant'
                        });
                    }""",
                object_id=remote_object.object_id,
            )
        )
    except Exception as e:
        raise WebDriverError("Failed to scroll to element.") from e


def submit(conn: SyncCDPConnection, element):
    """Submit a form. It is similar to 'submit' funtion in Seleniu
    It is not part of W3C WebDriver. Just added for convenience
    """
    try:
        remote_object = conn.execute(dom.resolve_node(node_id=element))
        conn.execute(
            runtime.call_function_on(
                function_declaration="""
                    function() {
                        this.submit();
                    }""",
                object_id=remote_object.object_id,
            )
        )
    except Exception as e:
        raise WebDriverError("Failed to submit form.") from e


def find_children_elements(
    conn: SyncCDPConnection,
    parent_element: str,
    locator_type: str,
    locator_value: str,
):
    """Find the children elements by 'locator_type'

    If the 'parent_element' is a shadow element, set the 'locator_type' as 'id' or
    'css selector'
    """
    try:
        return _find_all_elements(conn, locator_type, locator_value, parent_element)
    except Exception as e:
        raise WebDriverError(
            f"Failed to find the children elements from '{parent_element}'."
        ) from e


def find_child_element(
    conn: SyncCDPConnection,
    parent_element: str,
    locator_type: str,
    locator_value: str,
):
    """Find the child element by 'locator_type'"""
    try:
        return find_element(conn, locator_type, locator_value, parent_element)
    except Exception as e:
        raise WebDriverError(f"Failed to find the child element from '{parent_element}'.") from e


def get_page_source(conn: SyncCDPConnection) -> str:
    """Get the page source (all content)"""
    try:
        doc = GlobalValues.get_document_node()
        return conn.execute(dom.get_outer_html(node_id=doc.node_id))
    except Exception as e:
        raise WebDriverError("Failed to get the page source.") from e


def execute_script(
    conn: SyncCDPConnection,
    element: dom.NodeId,
    script: str,
    positive=True,
    return_by_value=False,
):
    """Executes a script, like 'style.background='#000000'' to change
    the background of the element"""
    positive = "" if positive else "!"
    try:
        remote_object = conn.execute(dom.resolve_node(node_id=element))
        return conn.execute(
            runtime.call_function_on(
                function_declaration="""
                    function() {"""
                f"""
                        return {positive}this.{script};
                    """
                """
                    }
                """,
                object_id=remote_object.object_id,
                return_by_value=return_by_value,
            )
        )
    except Exception as e:
        raise WebDriverError("Failed to execute script.") from e


def get_active_element(conn: SyncCDPConnection):
    """Get the active element"""
    try:
        eval_result = conn.execute(runtime.evaluate(expression="document.activeElement"))
        object_id = eval_result[0].object_id
        if not object_id:
            raise WebDriverError("No active element or it is the document body.")
        node_id_response = conn.execute(dom.request_node(object_id=object_id))
        return node_id_response
    except Exception as e:
        raise WebDriverError("Failed to check if element is selected.") from e


def clear_element(conn: SyncCDPConnection, element: dom.NodeId):
    """Clear the element text"""
    try:
        resolved = conn.execute(dom.resolve_node(node_id=element))

        conn.execute(
            runtime.call_function_on(
                object_id=resolved.object_id,
                function_declaration="""
                    function() {
                        this.value = '';
                        this.dispatchEvent(new Event('input', { bubbles: true }));
                        this.dispatchEvent(new Event('change', { bubbles: true }));
                    }
                """,
            )
        )
    except Exception as e:
        raise WebDriverError("Failed to clear the element text.") from e


def is_element_enabled(conn: SyncCDPConnection, element) -> bool:
    """Check if element is enabled"""
    try:
        script = "disabled"
        result = execute_script(conn, element, script, positive=False, return_by_value=True)
        return bool(result[0].value)
    except Exception as e:
        raise WebDriverError("Failed to check if element is enabled.") from e


def get_window_rectangle(conn: SyncCDPConnection) -> dict:
    """Get window rectangle"""
    try:
        _, bounds = conn.execute(browser.get_window_for_target())
        return {
            "x": bounds.left,
            "y": bounds.top,
            "width": bounds.width,
            "height": bounds.height,
        }
    except Exception as e:
        raise WebDriverError("Failed to get window rectangle.") from e


def get_window_handles(conn: SyncCDPConnection) -> List[target.TargetInfo]:
    """Get window handles"""
    try:
        targets = conn.execute(target.get_targets())
        return [t for t in targets if t.type_ == "page"]
    except Exception as e:
        raise WebDriverError("Failed to get window handles.") from e


def close_window(conn: SyncCDPConnection):
    """Close active window"""
    try:
        new_window(conn)
        conn.execute(target.page.close())
    except Exception as e:
        raise WebDriverError("Failed to close active window.") from e


def get_window(conn) -> str:
    """Get window"""
    try:
        result = get_window_handles(conn)
        return result[0].target_id
    except Exception as e:
        raise WebDriverError("Failed to get window.") from e


def get_status(conn: SyncCDPConnection) -> dict:
    """Returns the status and details of the WebDriver"""
    try:
        conn.execute(target.get_targets())
        return {"ready": True}
    except Exception as e:
        raise WebDriverError("Failed to get status.") from e
