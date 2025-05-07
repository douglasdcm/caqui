import os
from typing import Union
from caqui import asynchronous, synchronous
from caqui.easy.action_chains import ActionChains
from caqui.easy.window import Window
from caqui.easy.element import Element
from caqui.easy.switch_to import SwitchTo
from caqui.easy.alert import Alert
from caqui.exceptions import CapabilityNotSupported


class AsyncPage:
    def __init__(
            self, server_url: str,
            capabilities: dict = None,
            url: Union[str, None] = None
        ) -> None:
        """Mimics Selenium methods"""
        if not capabilities:
            capabilities = {}
        if not isinstance(capabilities, dict):
            raise CapabilityNotSupported("Expected dictionary")
        self.__server_url = server_url
        self.__session = synchronous.get_session(server_url, capabilities)
        if url:
            synchronous.get(
                self.__server_url,
                self.__session,
                url,
            )

    @property
    def remote(self) -> str:
        """Returns the Driver Server URL"""
        return self.__server_url

    @property
    def session(self) -> str:
        """Returns tne session id"""
        return self.__session

    @property
    def title(self):
        """Returns the title of the page"""
        return synchronous.get_title(self.__server_url, self.__session)

    @property
    def current_url(self):
        """Returns the current URL of the page"""
        return synchronous.get_url(self.__server_url, self.__session)

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
        return synchronous.get_window_handles(self.__server_url, self.__session)

    @property
    def current_window_handle(self):
        """Returns the current window handle"""
        return synchronous.get_window(self.__server_url, self.__session)

    def quit(self):
        """Closes the session"""
        synchronous.close_session(self.__server_url, self.__session)

    async def close(self):
        """Closes the window"""
        return await asynchronous.close_window(self.__server_url, self.__session)

    async def execute_script(self, script, args=[]):
        return await asynchronous.execute_script(self.__server_url, self.__session, script, args)

    async def set_window_position(self, x, y):
        """Repositions the page"""
        rect = await asynchronous.get_window_rectangle(self.__server_url, self.__session)
        return await asynchronous.set_window_rectangle(
            self.__server_url, self.__session, rect.get("width"), rect.get("height"), x, y
        )

    async def set_window_size(self, width, height):
        """Resizes the page"""
        rect = await asynchronous.get_window_rectangle(self.__server_url, self.__session)
        return await asynchronous.set_window_rectangle(
            self.__server_url, self.__session, width, height, rect.get("x"), rect.get("y")
        )

    async def get_window_position(self):
        """Returns the window rectangle"""
        return await asynchronous.get_window_rectangle(self.__server_url, self.__session)

    async def get_window_size(self):
        """Returns the window rectangle"""
        return await asynchronous.get_window_rectangle(self.__server_url, self.__session)

    async def save_screenshot(self, file):
        """Takes a scheenshot of the page"""
        path = os.path.dirname(file)
        if not path:
            path = "./"
        file_name = os.path.basename(file)
        return await asynchronous.take_screenshot(
            self.__server_url, self.__session, path, file_name
        )

    async def delete_all_cookies(self):
        """Deletes all storaged cookies"""
        return await asynchronous.delete_all_cookies(self.__server_url, self.__session)

    async def delete_cookie(self, cookie_name):
        """Delete the desired cookie"""
        return await asynchronous.delete_cookie(self.__server_url, self.__session, cookie_name)

    async def get_cookies(self):
        """Get all cookies"""
        return await asynchronous.get_cookies(self.__server_url, self.__session)

    async def get_cookie(self, cookie_name):
        """Get the desired cookie"""
        return await asynchronous.get_named_cookie(self.__server_url, self.__session, cookie_name)

    async def add_cookie(self, cookie):
        """Add a new cookie"""
        return await asynchronous.add_cookie(self.__server_url, self.__session, cookie)

    async def implicitly_wait(self, timeouts: int):
        """Set implicty timeouts"""
        return await asynchronous.set_timeouts(self.__server_url, self.__session, timeouts)

    async def back(self):
        """This command causes the browser to traverse one step backward
        in the joint session history of the
        current browse. This is equivalent to pressing the back button in the browser."""
        return await asynchronous.go_back(self.__server_url, self.__session)

    async def forward(self):
        """Go page forward"""
        return await asynchronous.go_forward(self.__server_url, self.__session)

    async def refresh(self):
        """Refreshs the page"""
        return await asynchronous.refresh_page(self.__server_url, self.__session)

    async def fullscreen_window(self):
        """Sets the page in fullscreen"""
        return await asynchronous.fullscreen_window(self.__server_url, self.__session)

    async def minimize_window(self):
        """Minimizes the page"""
        return await asynchronous.minimize_window(self.__server_url, self.__session)

    async def maximize_window(self):
        """Maximizes the page"""
        return await asynchronous.maximize_window(self.__server_url, self.__session)

    async def get(self, url):
        """Navigates to URL `url`"""
        await asynchronous.go_to_page(
            self.__server_url,
            self.__session,
            url,
        )

    async def find_elements(self, locator, value):
        """Search the DOM elements by 'locator', for example, 'xpath'"""
        elements = await asynchronous.find_elements(
            self.__server_url, self.__session, locator, value
        )
        result = []
        for element in elements:
            result.append(Element(element, self))
        return result

    async def find_element(self, locator, value):
        """Find an element by a 'locator', for example 'xpath'"""
        element = await asynchronous.find_element(self.__server_url, self.__session, locator, value)
        return Element(element, self)
