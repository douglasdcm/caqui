# Copyright (C) 2023 Caqui - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://github.com/douglasdcm/caqui

import os
from typing import Dict, List, Union

from aiohttp import ClientSession

from caqui import asynchronous, synchronous
from caqui.constants import Specification
from caqui.easy.action_chains import ActionChainsJsonWire, ActionChainsW3C
from caqui.easy.alert import Alert
from caqui.easy.capabilities import BaseCapabilitiesBuilder
from caqui.easy.element import Element
from caqui.easy.switch_to import SwitchToJsonWire, SwitchToW3C
from caqui.easy.window import Window
from caqui.exceptions import WebDriverError

TIMEOUT = 120  # seconds


SWITCHTO_IMPLEMENTATIONS = {
    Specification.FIREFOX: SwitchToW3C,
    Specification.CHROME: SwitchToJsonWire,
    Specification.EDGE: SwitchToJsonWire,
    Specification.OPERA: SwitchToJsonWire,
    Specification.JSONWIRE: SwitchToJsonWire,
    Specification.W3C: SwitchToW3C,
}

ACTION_CHAINS_IMPLEMENTATIONS = {
    Specification.FIREFOX: ActionChainsW3C,
    Specification.CHROME: ActionChainsJsonWire,
    Specification.EDGE: ActionChainsJsonWire,
    Specification.OPERA: ActionChainsJsonWire,
    Specification.JSONWIRE: ActionChainsJsonWire,
    Specification.W3C: ActionChainsW3C,
}


class _FindElement:
    async def find_element(self, async_driver: "AsyncDriver", locator, value) -> Element:
        raise NotImplementedError("Not implemented by subclass")


class _FindElementW3C(_FindElement):
    async def find_elements(self, async_driver: "AsyncDriver", locator, value) -> list:
        """Search the DOM elements by 'locator', for example, 'xpath'"""
        elements = await asynchronous.find_elements(
            async_driver._server_url,
            async_driver._session,
            locator,
            value,
            session_http=async_driver.session_http,
        )
        result = []
        for element in elements:
            el = Element(element, async_driver)
            el.locator = (locator, value)
            result.append(el)
        async_driver._elements_pool.extend(result)
        async_driver._elements_pool = list(set(async_driver._elements_pool))
        return result

    async def find_element(self, async_driver: "AsyncDriver", locator, value) -> Element:
        """Find an element by a 'locator', for example 'xpath'"""
        elements_filtered: List[Element] = [
            e for e in async_driver._elements_pool if e.locator == (locator, value)
        ]
        if elements_filtered:
            return elements_filtered[0]
        element = await asynchronous.find_element(
            async_driver._server_url,
            async_driver._session,
            locator,
            value,
            session_http=async_driver.session_http,
        )
        result = Element(element, async_driver)
        result.locator = (locator, value)
        async_driver._elements_pool.append(result)
        return result


class _FindElementJsonWire:
    async def find_elements(self, async_driver: "AsyncDriver", locator, value) -> List[Element]:
        """Search the DOM elements by 'locator', for example, 'xpath'"""
        elements = await asynchronous.find_elements_jsonwire(
            async_driver._server_url,
            async_driver._session,
            locator,
            value,
            session_http=async_driver.session_http,
        )
        result = []
        for element in elements:
            el = Element(element, async_driver)
            el.locator = (locator, value)
            result.append(el)
        async_driver._elements_pool.extend(result)
        async_driver._elements_pool = list(set(async_driver._elements_pool))
        return result

    async def find_element(self, async_driver: "AsyncDriver", locator, value) -> Element:
        """Find an element by a 'locator', for example 'xpath'"""
        elements_filtered: List[Element] = [
            e for e in async_driver._elements_pool if e.locator == (locator, value)
        ]
        if elements_filtered:
            return elements_filtered[0]
        element = await asynchronous.find_element_jsonwire(
            async_driver._server_url,
            async_driver._session,
            locator,
            value,
            session_http=async_driver.session_http,
        )
        result = Element(element, async_driver)
        result.locator = (locator, value)
        async_driver._elements_pool.append(result)
        return result


FIND_ELEMENT_IMPLEMENTATIONS: Dict[str, _FindElement] = {
    Specification.FIREFOX: _FindElementW3C,
    Specification.CHROME: _FindElementJsonWire,
    Specification.EDGE: _FindElementJsonWire,
    Specification.OPERA: _FindElementJsonWire,
    Specification.JSONWIRE: _FindElementJsonWire,
    Specification.W3C: _FindElementW3C,
}


class AsyncDriver:
    _instance = None

    def __init__(
        self,
        server_url: str,
        capabilities: Union[BaseCapabilitiesBuilder, dict, None] = None,
        session_http: Union[ClientSession, None] = None,
        port: int = 9999,
        specification: str = "",
    ) -> None:
        """Mimics Selenium methods

        Args:
            server_url: the URL of the remote server running the driver
            capabilities: the configuration to the driver
            session_http: a client to make HTTP requests
            port: the port where the remote server is running the driver
            specification: the specification the driver follows.
            Allowed values are "w3c" or "jsonwire"
                For example, ChromeDriver follows JsonWire protocol while
                GeckoDriver works with W3C
        """
        if isinstance(capabilities, BaseCapabilitiesBuilder):
            self.browser = capabilities.__class__.__name__
        elif specification.lower() in ["w3c", "jsonwire"]:
            self.browser = specification.lower()
        else:
            raise WebDriverError("No valid specification or capabilities")
        self._port = port
        self.session_http = session_http
        self._capabilities: dict = {}
        if isinstance(capabilities, BaseCapabilitiesBuilder):
            self._capabilities = capabilities.to_dict()
        else:
            self._capabilities: dict = capabilities
        self._server_url: str = server_url
        self._session: str = synchronous.get_session(self._server_url, self._capabilities)
        self._elements_pool: List[Element] = []

    @property
    def server_url(self) -> str:
        """Returns the Driver Server URL"""
        return self._server_url

    @property
    def session(self) -> str:
        """Returns tne session id"""
        return self._session

    @property
    def title(self):
        """Returns the title of the page"""
        return synchronous.get_title(self._server_url, self._session)

    @property
    def current_url(self):
        """Returns the current URL of the page"""
        return synchronous.get_url(self._server_url, self._session)

    @property
    def window(self):
        """Returns the current `Window` object"""
        return Window(self)

    @property
    def actions(self) -> ActionChainsW3C:
        """Returns the `ActionChains` object"""
        return ACTION_CHAINS_IMPLEMENTATIONS[self.browser](self)

    @property
    def alert(self):
        """Returns the `Alert` object"""
        return Alert(self)

    @property
    def switch_to(self) -> SwitchToW3C:
        """Returns the `SwithTo` object"""
        return SWITCHTO_IMPLEMENTATIONS[self.browser](self)

    @property
    def window_handles(self):
        """Returns the window handles"""
        return synchronous.get_window_handles(self._server_url, self._session)

    @property
    def current_window_handle(self):
        """Returns the current window handle"""
        return synchronous.get_window(self._server_url, self._session)

    @property
    def page_source(self):
        return synchronous.get_page_source(self._server_url, self._session)

    def cleanup_cache(self):
        self._elements_pool = []

    def quit(self):
        """Closes the session"""
        self.cleanup_cache()
        synchronous.close_session(self._server_url, self._session)

    async def close(self):
        """Closes the window"""
        self.cleanup_cache()
        return await asynchronous.close_window(
            self._server_url, self._session, session_http=self.session_http
        )

    async def execute_script(self, script, args=[]):
        return await asynchronous.execute_script(
            self._server_url, self._session, script, args, session_http=self.session_http
        )

    async def set_window_position(self, x, y):
        """Repositions the page"""
        rect = await asynchronous.get_window_rectangle(
            self._server_url, self._session, session_http=self.session_http
        )
        return await asynchronous.set_window_rectangle(
            self._server_url,
            self._session,
            rect.get("width"),
            rect.get("height"),
            x,
            y,
            session_http=self.session_http,
        )

    async def set_window_size(self, width, height):
        """Resizes the page"""
        rect = await asynchronous.get_window_rectangle(
            self._server_url, self._session, session_http=self.session_http
        )
        return await asynchronous.set_window_rectangle(
            self._server_url,
            self._session,
            width,
            height,
            rect.get("x"),
            rect.get("y"),
            session_http=self.session_http,
        )

    async def get_window_position(self):
        """Returns the window rectangle"""
        return await asynchronous.get_window_rectangle(
            self._server_url, self._session, session_http=self.session_http
        )

    async def get_window_size(self):
        """Returns the window rectangle"""
        return await asynchronous.get_window_rectangle(
            self._server_url, self._session, session_http=self.session_http
        )

    async def save_screenshot(self, file):
        """Takes a scheenshot of the page"""
        path = os.path.dirname(file)
        if not path:
            path = "./"
        file_name = os.path.basename(file)
        return await asynchronous.take_screenshot(
            self._server_url, self._session, path, file_name, session_http=self.session_http
        )

    async def delete_all_cookies(self):
        """Deletes all storaged cookies"""
        return await asynchronous.delete_all_cookies(
            self._server_url, self._session, session_http=self.session_http
        )

    async def delete_cookie(self, cookie_name):
        """Delete the desired cookie"""
        return await asynchronous.delete_cookie(
            self._server_url, self._session, cookie_name, session_http=self.session_http
        )

    async def get_cookies(self):
        """Get all cookies"""
        return await asynchronous.get_cookies(
            self._server_url, self._session, session_http=self.session_http
        )

    async def get_cookie(self, cookie_name) -> dict:
        """Get the desired cookie"""
        return await asynchronous.get_named_cookie(
            self._server_url, self._session, cookie_name, session_http=self.session_http
        )

    async def add_cookie(self, cookie):
        """Add a new cookie"""
        return await asynchronous.add_cookie(
            self._server_url, self._session, cookie, session_http=self.session_http
        )

    async def implicitly_wait(self, timeouts: int):
        """Set implicty timeouts"""
        return await asynchronous.set_timeouts(
            self._server_url, self._session, timeouts, session_http=self.session_http
        )

    async def back(self):
        """This command causes the browser to traverse one step backward
        in the joint session history of the
        current browse. This is equivalent to pressing the back button in the browser."""
        self._elements_pool = []
        return await asynchronous.go_back(
            self._server_url, self._session, session_http=self.session_http
        )

    async def forward(self):
        """Go page forward"""
        self._elements_pool = []
        return await asynchronous.go_forward(
            self._server_url, self._session, session_http=self.session_http
        )

    async def refresh(self):
        """Refreshs the page"""
        self._elements_pool = []
        return await asynchronous.refresh_page(
            self._server_url, self._session, session_http=self.session_http
        )

    async def fullscreen_window(self):
        """Sets the page in fullscreen"""
        return await asynchronous.fullscreen_window(
            self._server_url, self._session, session_http=self.session_http
        )

    async def minimize_window(self):
        """Minimizes the page"""
        return await asynchronous.minimize_window(
            self._server_url, self._session, session_http=self.session_http
        )

    async def maximize_window(self):
        """Maximizes the page"""
        return await asynchronous.maximize_window(
            self._server_url, self._session, session_http=self.session_http
        )

    async def get(self, url):
        """Navigates to URL `url`"""
        self._elements_pool = []
        await asynchronous.go_to_page(
            self._server_url, self._session, url, session_http=self.session_http
        )

    async def find_elements(self, locator, value) -> List[Element]:
        """Search the DOM elements by 'locator', for example, 'xpath'"""
        return await FIND_ELEMENT_IMPLEMENTATIONS[self.browser]().find_elements(
            self, locator, value
        )

    async def find_element(self, locator, value) -> Element:
        """Find an element by a 'locator', for example 'xpath'"""
        return await FIND_ELEMENT_IMPLEMENTATIONS[self.browser]().find_element(self, locator, value)
