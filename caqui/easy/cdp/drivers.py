# Copyright (C) 2023 Caqui - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://github.com/douglasdcm/caqui

import os
from typing import List, Union

from caqui.by import By
from caqui.cdp import asynchronous
from caqui.easy.cdp.action_chains import ActionChains
from caqui.easy.cdp.alert import Alert
from caqui.easy.cdp.capabilities import BaseCapabilitiesBuilder
from caqui.easy.cdp.element import Element
from caqui.easy.cdp.switch_to import SwitchTo
from caqui.easy.cdp.window import Window

TIMEOUT = 120  # seconds


class AsyncDriver:
    _instance = None

    def __init__(
        self,
        conn,
        capabilities: Union[BaseCapabilitiesBuilder, dict] = dict(),
        port: int = 9222,
    ) -> None:
        """Mimics Selenium methods

        Args:
            capabilities: the configuration to the driver
            conn: a client to make HTTP requests
            port: the port where the remote server is running the driver
            specification: the specification the driver follows.
            Allowed values are "w3c" or "jsonwire"
                For example, ChromeDriver follows JsonWire protocol while
                GeckoDriver works with W3C
        """
        if isinstance(capabilities, BaseCapabilitiesBuilder):
            self.browser = capabilities.__class__.__name__
        self._capabilities: dict = {}
        if isinstance(capabilities, BaseCapabilitiesBuilder):
            self._capabilities = capabilities.to_dict()
        else:
            self._capabilities = capabilities
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
    async def get_current_window_handle(self) -> str:
        """Returns the current window handle"""
        return await asynchronous.get_window(self._conn)

    async def get_page_source(self) -> str:
        return await asynchronous.get_page_source(self._conn)

    async def get_window_handles(self) -> str:
        """Returns the text of the element"""
        return await asynchronous.get_window_handles(
            self._conn,
        )

    async def get_title(self) -> str:
        """Returns the text of the element"""
        return await asynchronous.get_title(
            self._conn,
        )

    async def get_current_url(self) -> str:
        """Returns the text of the element"""
        return await asynchronous.get_url(
            self._conn,
        )

    async def close(self) -> None:
        """Closes the window"""
        await asynchronous.close_window(
            self._conn,
        )

    async def execute_script(self, script: str, args: List = []):
        """
        Execute a JavaScript script on the browser.

        Args:
            script (str): The JavaScript script to execute.
            args (list[str], optional): Variable arguments for the script. Defaults to [].

        Returns:
            result: The result of the executed script.
        """
        element = await asynchronous.find_element(self._conn, By.XPATH, "//body")
        await asynchronous.execute_script(
            self._conn,
            element,
            script,
        )

    # TODO test it
    async def set_window_position(self, x: int, y: int) -> None:
        """Repositions the page"""
        rect = await asynchronous.get_window_rectangle(
            self._conn,
        )
        return await asynchronous.set_window_rectangle(
            self._conn,
            rect.get("width", 0),
            rect.get("height", 0),
            x,
            y,
        )

    async def set_window_size(self, width: int, height: int) -> None:
        """Resizes the page"""
        rect = await asynchronous.get_window_rectangle(
            self._conn,
        )
        return await asynchronous.set_window_rectangle(
            self._conn,
            width,
            height,
            0,
            0,
        )

    # TODO test it
    async def get_window_position(self):
        """Returns the window rectangle"""
        return await asynchronous.get_window_rectangle(
            self._conn,
        )

    async def get_window_size(self) -> dict:
        """Returns the window rectangle"""
        return await asynchronous.get_window_rectangle(
            self._conn,
        )

    async def save_screenshot(self, file: str) -> bool:
        """Takes a scheenshot of the page"""
        path = os.path.dirname(file)
        if not path:
            path = "./"
        file_name = os.path.basename(file)
        return await asynchronous.take_screenshot(
            self._conn,
            path,
            file_name,
        )

    async def delete_all_cookies(self) -> None:
        """Deletes all storaged cookies"""
        await asynchronous.delete_all_cookies(
            self._conn,
        )

    async def delete_cookie(self, cookie_name) -> None:
        """Delete the desired cookie"""
        cookie = await asynchronous.get_named_cookie(self._conn, cookie_name)
        await asynchronous.delete_cookie(
            self._conn, cookie_name, cookie.get("url"), cookie.get("domain")
        )

    async def get_cookies(self) -> List[dict]:
        """Get all cookies"""
        return await asynchronous.get_cookies(
            self._conn,
        )

    async def get_cookie(self, cookie_name: str) -> dict:
        """Get the desired cookie"""
        return await asynchronous.get_named_cookie(
            self._conn,
            cookie_name,
        )

    async def add_cookie(self, cookie: dict) -> None:
        """Add a new cookie"""
        await asynchronous.add_cookie(
            self._conn,
            cookie,
        )

    async def back(self) -> None:
        """This command causes the browser to traverse one step backward
        in the joint session history of the
        current browse. This is equivalent to pressing the back button in the browser."""
        await asynchronous.go_back(
            self._conn,
        )

    async def forward(self) -> None:
        """Go page forward"""
        await asynchronous.go_forward(
            self._conn,
        )

    async def refresh(self) -> None:
        """Refreshs the page"""
        await asynchronous.refresh_page(
            self._conn,
        )

    async def fullscreen_window(self) -> None:
        """Sets the page in fullscreen"""
        await asynchronous.fullscreen_window(
            self._conn,
        )

    async def minimize_window(self) -> None:
        """Minimizes the page"""
        await asynchronous.minimize_window(
            self._conn,
        )

    async def maximize_window(self) -> None:
        """Maximizes the page"""
        await asynchronous.maximize_window(
            self._conn,
        )

    async def get(self, url: str) -> None:
        """Navigates to URL `url`"""
        await asynchronous.get(
            self._conn,
            url,
        )

    async def find_elements(self, locator: str, value: str) -> List[Element]:
        """Search the DOM elements by 'locator', for example, 'xpath'"""
        elements = await asynchronous.find_elements(self._conn, locator, value)
        return [Element(e, self) for e in elements]

    async def find_element(self, locator: str, value: str) -> Element:
        """Find an element by a 'locator', for example 'xpath'

        `Attention`: it opens Alerts/Prompt elements automatically
        Not applicable for elements in iframes.
        """
        element = await asynchronous.find_element(self._conn, locator, value)
        self._current_element = Element(element, self)
        return self._current_element
