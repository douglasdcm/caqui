import os as _os
from caqui import asynchronous as _asynchronous, synchronous as _synchronous


class __Window:
    def __init__(self, driver) -> None:
        self.__remote = driver.remote
        self.__session = driver.session

    async def new(self, window_type="tab"):
        """
        Open a new window

        :param window_type (str): tab or window

        return (str): window handle
        """
        return await _asynchronous.new_window(
            self.__remote, self.__session, window_type
        )


class _Element:
    def __init__(self, element, driver) -> None:
        self.__element = element
        self.__remote = driver.remote
        self.__session = driver.session
        self.__driver = driver

    def __str__(self) -> str:
        return self.__element

    @property
    def rect(self):
        return _synchronous.get_rect(self.__remote, self.__session, self.__element)

    @property
    def tag_name(self):
        return _synchronous.get_tag_name(self.__remote, self.__session, self.__element)

    @property
    def text(self):
        return _synchronous.get_text(self.__remote, self.__session, self.__element)

    @property
    def active_element(self):
        self.__element = _synchronous.get_active_element(self.__driver, self.__session)
        return self.__element

    async def value_of_css_property(self, property_name):
        return await _asynchronous.get_css_value(
            self.__remote, self.__session, self.__element, property_name
        )

    async def screenshot(self, file):
        path = _os.path.dirname(file)
        if not path:
            path = "./"
        file_name = _os.path.basename(file)
        return await _asynchronous.take_screenshot_element(
            self.__remote, self.__session, self.__element, path, file_name
        )

    async def is_selected(self):
        return await _asynchronous.is_element_selected(
            self.__remote, self.__session, self.__element
        )

    async def is_enabled(self):
        return await _asynchronous.is_element_enabled(
            self.__remote, self.__session, self.__element
        )

    async def get_text(self):
        return await _asynchronous.get_text(
            self.__remote, self.__session, self.__element
        )

    async def get_css_value(self, property_name):
        return await _asynchronous.get_css_value(
            self.__remote, self.__session, self.__element, property_name
        )

    async def is_element_selected(self):
        return await _asynchronous.is_element_selected(
            self.__remote, self.__session, self.__element
        )

    async def is_element_enabled(self):
        return await _asynchronous.is_element_enabled(
            self.__remote, self.__session, self.__element
        )

    async def submit(self):
        return await _asynchronous.submit(self.__remote, self.__session, self.__element)

    async def get_rect(self):
        return await _asynchronous.get_rect(
            self.__remote, self.__session, self.__element
        )

    async def get_tag_name(self):
        return await _asynchronous.get_tag_name(
            self.__remote, self.__session, self.__element
        )

    async def get_computed_label(self):
        return await _asynchronous.get_computed_label(
            self.__remote, self.__session, self.__element
        )

    async def get_computed_role(self):
        return await _asynchronous.get_computed_role(
            self.__remote, self.__session, self.__element
        )

    async def get_property(self, property):
        return await _asynchronous.get_property(
            self.__remote, self.__session, self.__element, property
        )

    async def get_attribute(self, attribute):
        return await _asynchronous.get_attribute(
            self.__remote, self.__session, self.__element, attribute
        )

    async def clear(self):
        return await _asynchronous.clear_element(
            self.__remote, self.__session, self.__element
        )

    async def send_keys(self, text):
        return await _asynchronous.send_keys(
            self.__remote, self.__session, self.__element, text
        )

    async def click(self):
        return await _asynchronous.click(self.__remote, self.__session, self.__element)

    async def find_elements(self, locator, value):
        result = []
        elements = await _asynchronous.find_children_elements(
            self.__remote, self.__session, self.__element, locator, value
        )
        for element in elements:
            result.append(_Element(element, self.__driver))
        return result

    async def find_element(self, locator, value):
        element = await _asynchronous.find_child_element(
            self.__remote, self.__session, self.__element, locator, value
        )
        return _Element(element, self.__driver)


class _Alert:
    def __init__(self, driver) -> None:
        self.__remote = driver.remote
        self.__session = driver.session

    @property
    def text(self):
        return _synchronous.get_alert_text(self.__remote, self.__session)

    async def accept(self):
        return await _asynchronous.accept_alert(self.__remote, self.__session)

    async def dismiss(self):
        return await _asynchronous.dismiss_alert(self.__remote, self.__session)

    async def send_keys(self, text):
        return await _asynchronous.send_alert_text(self.__remote, self.__session, text)


class _SwitchTo:
    def __init__(self, driver) -> None:
        self.__driver = driver
        self.__iframe = None
        self.__window_handle = None

    @property
    def active_element(self):
        element = _synchronous.get_active_element(
            self.__driver.remote, self.__driver.session
        )
        return _Element(element, self.__driver)

    @property
    def alert(self):
        return _Alert(self.__driver)

    async def new_window(self, window_type):
        self.__window_handle = await _asynchronous.new_window(
            self.__driver.remote, self.__driver.session, window_type
        )
        self.__window_handle = await _asynchronous.switch_to_window(
            self.__driver.remote, self.__driver.session, self.__window_handle
        )
        return self.__window_handle

    async def window(self, window_handle):
        self.__window_handle = await _asynchronous.switch_to_window(
            self.__driver.remote, self.__driver.session, window_handle
        )
        return self.__window_handle

    async def frame(self, iframe):
        self.__iframe = str(iframe)
        return await _asynchronous.switch_to_frame(
            self.__driver.remote, self.__driver.session, self.__iframe
        )

    async def default_content(self):
        return await _asynchronous.switch_to_parent_frame(
            self.__driver.remote, self.__driver.session, self.__iframe
        )


class ActionChains:
    def __init__(self, driver) -> None:
        self.__remote = driver.remote
        self.__session = driver.session
        self.__coroutines = []
        self.__element = None

    def click(self, element=None):
        if not element:
            element = self.__element
        coroutine = _asynchronous.click(self.__remote, self.__session, str(element))
        self.__coroutines.append(coroutine)
        return self

    def move_to_element(self, element):
        self.__element = element
        coroutine = _asynchronous.actions_move_to_element(
            self.__remote, self.__session, str(element)
        )
        self.__coroutines.append(coroutine)
        return self

    def scroll_to_element(self, element):
        self.__element = element
        coroutine = _asynchronous.actions_scroll_to_element(
            self.__remote, self.__session, str(element)
        )
        self.__coroutines.append(coroutine)
        return self

    async def perform(self):
        for coroutine in self.__coroutines:
            await coroutine
        return True


class AsyncDriver:
    def __init__(self, remote, capabilities, url=None) -> None:
        self.__remote = remote
        self.__session = _synchronous.get_session(remote, capabilities)
        if url:
            _synchronous.get(
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
        return _synchronous.get_title(self.__remote, self.__session)

    @property
    def current_url(self):
        return _synchronous.get_url(self.__remote, self.__session)

    @property
    def window(self):
        return __Window(self)

    @property
    def actions(self):
        return ActionChains(self)

    @property
    def alert(self):
        return _Alert(self)

    @property
    def switch_to(self):
        return _SwitchTo(self)

    @property
    def window_handles(self):
        return _synchronous.get_window_handles(self.__remote, self.__session)

    @property
    def current_window_handle(self):
        return _synchronous.get_window(self.__remote, self.__session)

    def quit(self):
        _synchronous.close_session(self.__remote, self.__session)

    async def close(self):
        return _asynchronous.close_window(self.__remote, self.__session)

    async def execute_script(self, script, args=[]):
        return await _asynchronous.execute_script(
            self.__remote, self.__session, script, args
        )

    async def set_window_position(self, x, y):
        rect = await _asynchronous.get_window_rectangle(self.__remote, self.__session)
        return await _asynchronous.set_window_rectangle(
            self.__remote, self.__session, rect.get("width"), rect.get("height"), x, y
        )

    async def set_window_size(self, width, height):
        rect = await _asynchronous.get_window_rectangle(self.__remote, self.__session)
        return await _asynchronous.set_window_rectangle(
            self.__remote, self.__session, width, height, rect.get("x"), rect.get("y")
        )

    async def get_window_position(self):
        return await _asynchronous.get_window_rectangle(self.__remote, self.__session)

    async def get_window_size(self):
        return await _asynchronous.get_window_rectangle(self.__remote, self.__session)

    async def save_screenshot(self, file):
        path = _os.path.dirname(file)
        if not path:
            path = "./"
        file_name = _os.path.basename(file)
        return await _asynchronous.take_screenshot(
            self.__remote, self.__session, path, file_name
        )

    async def delete_all_cookies(self):
        return await _asynchronous.delete_all_cookies(self.__remote, self.__session)

    async def delete_cookie(self, cookie_name):
        return await _asynchronous.delete_cookie(
            self.__remote, self.__session, cookie_name
        )

    async def get_cookies(self):
        return await _asynchronous.get_cookies(self.__remote, self.__session)

    async def get_cookie(self, cookie_name):
        return await _asynchronous.get_named_cookie(
            self.__remote, self.__session, cookie_name
        )

    async def add_cookie(self, cookie):
        return await _asynchronous.add_cookie(self.__remote, self.__session, cookie)

    async def implicitly_wait(self, timeouts: int):
        return await _asynchronous.set_timeouts(self.__remote, self.__session, timeouts)

    async def back(self):
        return await _asynchronous.go_back(self.__remote, self.__session)

    async def forward(self):
        return await _asynchronous.go_forward(self.__remote, self.__session)

    async def refresh(self):
        return await _asynchronous.refresh_page(self.__remote, self.__session)

    async def fullscreen_window(self):
        return await _asynchronous.fullscreen_window(self.__remote, self.__session)

    async def minimize_window(self):
        return await _asynchronous.minimize_window(self.__remote, self.__session)

    async def maximize_window(self):
        return await _asynchronous.maximize_window(self.__remote, self.__session)

    async def get(self, url):
        await _asynchronous.go_to_page(
            self.__remote,
            self.__session,
            url,
        )

    async def find_elements(self, locator, value):
        elements = await _asynchronous.find_elements(
            self.__remote, self.__session, locator, value
        )
        result = []
        for element in elements:
            result.append(_Element(element, self))
        return result

    async def find_element(self, locator, value):
        element = await _asynchronous.find_element(
            self.__remote, self.__session, locator, value
        )
        return _Element(element, self)
