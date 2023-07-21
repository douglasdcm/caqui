import os
from caqui import asynchronous, synchronous


class ActionChains:
    def __init__(self, driver) -> None:
        self.__remote = driver.remote
        self.__session = driver.session
        self.__coroutines = []
        self.__element = None

    def click(self, element=None):
        if not element:
            element = self.__element
        coroutine = asynchronous.click(self.__remote, self.__session, str(element))
        self.__coroutines.append(coroutine)
        return self

    def move_to_element(self, element):
        self.__element = element
        coroutine = asynchronous.actions_move_to_element(
            self.__remote, self.__session, str(element)
        )
        self.__coroutines.append(coroutine)
        return self

    def scroll_to_element(self, element):
        self.__element = element
        coroutine = asynchronous.actions_scroll_to_element(
            self.__remote, self.__session, str(element)
        )
        self.__coroutines.append(coroutine)
        return self

    async def perform(self):
        for coroutine in self.__coroutines:
            await coroutine
        return True


class Window:
    def __init__(self, driver) -> None:
        self.__remote = driver.remote
        self.__session = driver.session

    async def new(self, window_type="tab"):
        """
        Open a new window

        :param window_type (str): tab or window

        return (str): window handle
        """
        return await asynchronous.new_window(self.__remote, self.__session, window_type)


class Element:
    def __init__(self, element, driver) -> None:
        self.__element = element
        self.__remote = driver.remote
        self.__session = driver.session
        self.__driver = driver

    def __str__(self) -> str:
        return self.__element

    @property
    def text(self):
        return synchronous.get_text(self.__remote, self.__session, self.__element)

    async def get_text(self):
        return await asynchronous.get_text(
            self.__remote, self.__session, self.__element
        )

    async def get_css_value(self, property_name):
        return await asynchronous.get_css_value(
            self.__remote, self.__session, self.__element, property_name
        )

    async def is_element_selected(self):
        return await asynchronous.is_element_selected(
            self.__remote, self.__session, self.__element
        )

    async def is_element_enabled(self):
        return await asynchronous.is_element_enabled(
            self.__remote, self.__session, self.__element
        )

    async def submit(self):
        return await asynchronous.submit(self.__remote, self.__session, self.__element)

    async def get_rect(self):
        return await asynchronous.get_rect(
            self.__remote, self.__session, self.__element
        )

    async def get_tag_name(self):
        return await asynchronous.get_tag_name(
            self.__remote, self.__session, self.__element
        )

    async def take_screenshot_element(self, path="/tmp", file_name="caqui"):
        return await asynchronous.take_screenshot_element(
            self.__remote, self.__session, self.__element, path, file_name
        )

    async def get_computed_label(self):
        return await asynchronous.get_computed_label(
            self.__remote, self.__session, self.__element
        )

    async def get_computed_role(self):
        return await asynchronous.get_computed_role(
            self.__remote, self.__session, self.__element
        )

    async def get_computed_label(self):
        return await asynchronous.get_computed_label(
            self.__remote, self.__session, self.__element
        )

    async def get_property(self, property):
        return await asynchronous.get_property(
            self.__remote, self.__session, self.__element, property
        )

    async def get_attribute(self, attribute):
        return await asynchronous.get_attribute(
            self.__remote, self.__session, self.__element, attribute
        )

    async def clear(self):
        return await asynchronous.clear_element(
            self.__remote, self.__session, self.__element
        )

    async def send_keys(self, text):
        return await asynchronous.send_keys(
            self.__remote, self.__session, self.__element, text
        )

    async def click(self):
        return await asynchronous.click(self.__remote, self.__session, self.__element)

    async def find_elements(self, locator, value):
        result = []
        elements = await asynchronous.find_children_elements(
            self.__remote, self.__session, self.__element, locator, value
        )
        for element in elements:
            result.append(Element(element, self.__driver))
        return result

    async def find_element(self, locator, value):
        element = await asynchronous.find_child_element(
            self.__remote, self.__session, self.__element, locator, value
        )
        return Element(element, self.__driver)


class AsyncDriver:
    def __init__(self, remote, capabilities, url=None) -> None:
        self.__remote = remote
        self.__session = synchronous.get_session(remote, capabilities)
        if url:
            self.__url = url
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

    def quit(self):
        synchronous.close_session(self.__remote, self.__session)

    def close(self):
        self.quit()

    def window(self):
        return Window(self)

    def actions(self):
        return ActionChains(self)

    async def save_screenshot(self, file):
        path = os.path.dirname(file)
        if not path:
            path = "./"
        file_name = os.path.basename(file)
        return await asynchronous.take_screenshot(
            self.__remote, self.__session, path, file_name
        )

    async def maximize_window(self):
        return await asynchronous.maximize_window(self.__remote, self.__session)

    async def get(self, url):
        self.__url = url
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
