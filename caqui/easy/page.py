import os
from typing import Optional, Union

from aiohttp import ClientSession
from caqui import asynchronous, synchronous
from caqui.easy.action_chains import ActionChains
from caqui.easy.window import Window
from caqui.easy.element import Element
from caqui.easy.switch_to import SwitchTo
from caqui.easy.alert import Alert
from caqui.exceptions import CapabilityNotSupported


class AsyncPage:
    def __init__(
        self,
        server_url: str,
        capabilities: Optional[dict] = None,
        url: Union[str, None] = None,
        session_http: Union[ClientSession, None] = None,
    ) -> None:
        """Mimics Selenium methods"""
        self.session_http = session_http
        if not capabilities:
            capabilities = {}
        if not isinstance(capabilities, dict):
            raise CapabilityNotSupported("Expected dictionary")
        self._server_url = server_url
        self._session = synchronous.get_session(server_url, capabilities)
        if url:
            synchronous.get(
                self._server_url,
                self._session,
                url,
            )

    @property
    def remote(self) -> str:
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
    def actions(self):
        """Returns the `ActionChains` object"""
        return ActionChains(self)

    @property
    def alert(self):
        """Returns the `Alert` object"""
        return Alert(self)

    @property
    def switch_to(self):
        """Returns the `SwithTo` object"""
        return SwitchTo(self)

    @property
    def window_handles(self):
        """Returns the window handles"""
        return synchronous.get_window_handles(self._server_url, self._session)

    @property
    def current_window_handle(self):
        """Returns the current window handle"""
        return synchronous.get_window(self._server_url, self._session)

    def quit(self):
        """Closes the session"""
        synchronous.close_session(self._server_url, self._session)

    async def close(self):
        """Closes the window"""
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
        return await asynchronous.go_back(
            self._server_url, self._session, session_http=self.session_http
        )

    async def forward(self):
        """Go page forward"""
        return await asynchronous.go_forward(
            self._server_url, self._session, session_http=self.session_http
        )

    async def refresh(self):
        """Refreshs the page"""
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
        await asynchronous.go_to_page(
            self._server_url, self._session, url, session_http=self.session_http
        )

    async def find_elements(self, locator, value) -> list:
        """Search the DOM elements by 'locator', for example, 'xpath'"""
        elements = await asynchronous.find_elements(
            self._server_url, self._session, locator, value, session_http=self.session_http
        )
        result = []
        for element in elements:
            result.append(Element(element, self))
        return result

    async def find_element(self, locator, value) -> Element:
        """Find an element by a 'locator', for example 'xpath'"""
        element = await asynchronous.find_element(
            self._server_url, self._session, locator, value, session_http=self.session_http
        )
        return Element(element, self)
