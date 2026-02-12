# Copyright (C) 2023 Caqui - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://github.com/douglasdcm/caqui

import os
from typing import List

from caqui.cdp.by import By
from caqui.cdp.engine import synchronous
from caqui.cdp.synchronous.action_chains import ActionChains
from caqui.cdp.synchronous.alert import Alert
from caqui.cdp.synchronous.element import Element
from caqui.cdp.synchronous.switch_to import SwitchTo
from caqui.cdp.synchronous.window import Window
from caqui.helper import deprecated

TIMEOUT = 120  # seconds


class SyncDriverCDP:
    _instance = None

    def __init__(
        self,
        conn,
    ) -> None:
        """Mimics Selenium methods

        Args:
            conn: a client to make HTTP requests
        """
        self._conn = conn
        self._current_element = None

    @property
    def conn(self) -> str:
        """Returns tne websocket connect"""
        return self._conn

    @property
    def window(self) -> Window:
        """Returns the current `Window` object"""
        return Window(self)

    @property
    def actions(self) -> ActionChains:
        """Returns the `ActionChains` object"""
        return ActionChains(self)

    @property
    def alert(self) -> Alert:
        """Returns the `Alert` object"""
        return Alert(self)

    @property
    def switch_to(self) -> SwitchTo:
        """Returns the `SwithTo` object"""
        return SwitchTo(self)


    # TODO test it
    def get_current_window_handle(self) -> str:
        """Returns the current window handle"""
        return synchronous.get_window(self._conn)

    def get_page_source(self) -> str:
        return synchronous.get_page_source(self._conn)

    def get_window_handles(self) -> str:
        """Returns the text of the element"""
        return synchronous.get_window_handles(
            self._conn,
        )

    def get_title(self) -> str:
        """Returns the text of the element"""
        return synchronous.get_title(
            self._conn,
        )

    def get_current_url(self) -> str:
        """Returns the text of the element"""
        return synchronous.get_url(
            self._conn,
        )

    def close(self) -> None:
        """Closes the window"""
        synchronous.close_window(
            self._conn,
        )

    def execute_script(self, script: str, args: List = []):
        """
        Execute a JavaScript script on the browser.

        Args:
            script (str): The JavaScript script to execute.
            args (list[str], optional): Variable arguments for the script. Defaults to [].

        Returns:
            result: The result of the executed script.
        """
        element = synchronous.find_element(self._conn, By.XPATH, "//body")
        synchronous.execute_script(
            self._conn,
            element,
            script,
        )

    # TODO test it
    def set_window_position(self, x: int, y: int) -> None:
        """Repositions the page"""
        rect = synchronous.get_window_rectangle(
            self._conn,
        )
        return synchronous.set_window_rectangle(
            self._conn,
            rect.get("width", 0),
            rect.get("height", 0),
            x,
            y,
        )

    def set_window_size(self, width: int, height: int) -> None:
        """Resizes the page"""
        return synchronous.set_window_rectangle(
            self._conn,
            width,
            height,
            0,
            0,
        )

    # TODO test it
    def get_window_position(self):
        """Returns the window rectangle"""
        return synchronous.get_window_rectangle(
            self._conn,
        )

    def get_window_size(self) -> dict:
        """Returns the window rectangle"""
        return synchronous.get_window_rectangle(
            self._conn,
        )

    def save_screenshot(self, file: str) -> bool:
        """Takes a scheenshot of the page"""
        path = os.path.dirname(file)
        if not path:
            path = "./"
        file_name = os.path.basename(file)
        return synchronous.take_screenshot(
            self._conn,
            path,
            file_name,
        )

    def delete_all_cookies(self) -> None:
        """Deletes all storaged cookies"""
        synchronous.delete_all_cookies(
            self._conn,
        )

    def delete_cookie(self, cookie_name) -> None:
        """Delete the desired cookie"""
        cookie = synchronous.get_named_cookie(self._conn, cookie_name)
        synchronous.delete_cookie(self._conn, cookie_name, cookie.get("url"), cookie.get("domain"))

    def get_cookies(self) -> List[dict]:
        """Get all cookies"""
        return synchronous.get_cookies(
            self._conn,
        )

    def get_cookie(self, cookie_name: str) -> dict:
        """Get the desired cookie"""
        return synchronous.get_named_cookie(
            self._conn,
            cookie_name,
        )

    def add_cookie(self, cookie: dict) -> None:
        """Add a new cookie"""
        synchronous.add_cookie(
            self._conn,
            cookie,
        )

    @deprecated
    def implicitly_wait(self, timeouts: int) -> None:
        """Set implicty timeouts.`Note` Present for backward-compatibility only"""
        pass

    def back(self) -> None:
        """This command causes the browser to traverse one step backward
        in the joint session history of the
        current browse. This is equivalent to pressing the back button in the browser."""
        synchronous.go_back(
            self._conn,
        )

    def forward(self) -> None:
        """Go page forward"""
        synchronous.go_forward(
            self._conn,
        )

    def refresh(self) -> None:
        """Refreshs the page"""
        synchronous.refresh_page(
            self._conn,
        )

    def fullscreen_window(self) -> None:
        """Sets the page in fullscreen"""
        synchronous.fullscreen_window(
            self._conn,
        )

    def minimize_window(self) -> None:
        """Minimizes the page"""
        synchronous.minimize_window(
            self._conn,
        )

    def maximize_window(self) -> None:
        """Maximizes the page"""
        synchronous.maximize_window(
            self._conn,
        )

    def get(self, url: str) -> None:
        """Navigates to URL `url`"""
        synchronous.get(
            self._conn,
            url,
        )

    def find_elements(self, locator: str, value: str) -> List[Element]:
        """Search the DOM elements by 'locator', for example, 'xpath'"""
        elements = synchronous.find_elements(self._conn, locator, value)
        return [Element(e, self) for e in elements]

    def find_element(self, locator: str, value: str) -> Element:
        """Find an element by a 'locator', for example 'xpath'

        `Attention`: it opens Alerts/Prompt elements automatically
        Not applicable for elements in iframes.
        """
        element = synchronous.find_element(self._conn, locator, value)
        self._current_element = Element(element, self)
        return self._current_element
