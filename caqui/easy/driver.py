import os
from caqui import asynchronous, synchronous
from caqui.easy.action_chains import ActionChains
from caqui.easy.window import Window
from caqui.easy.element import Element
from caqui.easy.switch_to import SwitchTo
from caqui.easy.alert import Alert


class AsyncDriver:
    def __init__(self, remote, capabilities, url=None) -> None:
        self.__remote = remote
        self.__session = synchronous.get_session(remote, capabilities)
        if url:
            synchronous.get(
                remote,
                self.__session,
                url,
            )

    @property
    def remote(self):
        return self.__remote

    @property
    def session(self):
        return self.__session

    @property
    def title(self):
        return synchronous.get_title(self.__remote, self.__session)

    @property
    def current_url(self):
        return synchronous.get_url(self.__remote, self.__session)

    @property
    def window(self):
        return Window(self)

    @property
    def actions(self):
        return ActionChains(self)

    @property
    def alert(self):
        return Alert(self)

    @property
    def switch_to(self):
        return SwitchTo(self)

    @property
    def window_handles(self):
        return synchronous.get_window_handles(self.__remote, self.__session)

    @property
    def current_window_handle(self):
        return synchronous.get_window(self.__remote, self.__session)

    def quit(self):
        synchronous.close_session(self.__remote, self.__session)

    async def close(self):
        return asynchronous.close_window(self.__remote, self.__session)

    async def execute_script(self, script, args=[]):
        return await asynchronous.execute_script(
            self.__remote, self.__session, script, args
        )

    async def set_window_position(self, x, y):
        rect = await asynchronous.get_window_rectangle(self.__remote, self.__session)
        return await asynchronous.set_window_rectangle(
            self.__remote, self.__session, rect.get("width"), rect.get("height"), x, y
        )

    async def set_window_size(self, width, height):
        rect = await asynchronous.get_window_rectangle(self.__remote, self.__session)
        return await asynchronous.set_window_rectangle(
            self.__remote, self.__session, width, height, rect.get("x"), rect.get("y")
        )

    async def get_window_position(self):
        return await asynchronous.get_window_rectangle(self.__remote, self.__session)

    async def get_window_size(self):
        return await asynchronous.get_window_rectangle(self.__remote, self.__session)

    async def save_screenshot(self, file):
        path = os.path.dirname(file)
        if not path:
            path = "./"
        file_name = os.path.basename(file)
        return await asynchronous.take_screenshot(
            self.__remote, self.__session, path, file_name
        )

    async def delete_all_cookies(self):
        return await asynchronous.delete_all_cookies(self.__remote, self.__session)

    async def delete_cookie(self, cookie_name):
        return await asynchronous.delete_cookie(
            self.__remote, self.__session, cookie_name
        )

    async def get_cookies(self):
        return await asynchronous.get_cookies(self.__remote, self.__session)

    async def get_cookie(self, cookie_name):
        return await asynchronous.get_named_cookie(
            self.__remote, self.__session, cookie_name
        )

    async def add_cookie(self, cookie):
        return await asynchronous.add_cookie(self.__remote, self.__session, cookie)

    async def implicitly_wait(self, timeouts: int):
        return await asynchronous.set_timeouts(self.__remote, self.__session, timeouts)

    async def back(self):
        return await asynchronous.go_back(self.__remote, self.__session)

    async def forward(self):
        return await asynchronous.go_forward(self.__remote, self.__session)

    async def refresh(self):
        return await asynchronous.refresh_page(self.__remote, self.__session)

    async def fullscreen_window(self):
        return await asynchronous.fullscreen_window(self.__remote, self.__session)

    async def minimize_window(self):
        return await asynchronous.minimize_window(self.__remote, self.__session)

    async def maximize_window(self):
        return await asynchronous.maximize_window(self.__remote, self.__session)

    async def get(self, url):
        await asynchronous.go_to_page(
            self.__remote,
            self.__session,
            url,
        )

    async def find_elements(self, locator, value):
        elements = await asynchronous.find_elements(
            self.__remote, self.__session, locator, value
        )
        result = []
        for element in elements:
            result.append(Element(element, self))
        return result

    async def find_element(self, locator, value):
        element = await asynchronous.find_element(
            self.__remote, self.__session, locator, value
        )
        return Element(element, self)
