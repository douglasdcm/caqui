from caqui import asynchronous, synchronous


class Window:
    def __init__(self, remote, session) -> None:
        self.__remote = remote
        self.__session = session

    async def new(self, window_type="tab"):
        """
        Open a new window

        :param window_type (str): tab or window

        return (str): window handle
        """
        return await asynchronous.new_window(self.__remote, self.__session, window_type)


class Element:
    def __init__(self, element, remote, session) -> None:
        self.__element = element
        self.__remote = remote
        self.__session = session

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
        return await asynchronous.find_children_elements(
            self.__remote, self.__session, self.__element, locator, value
        )

    async def find_element(self, locator, value):
        return await asynchronous.find_child_element(
            self.__remote, self.__session, self.__element, locator, value
        )


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

    def quit(self):
        synchronous.close_session(self.__remote, self.__session)

    def window(self):
        return Window(self.__remote, self.__session)

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
            result.append(Element(element, self.__remote, self.__session))
        return result

    async def find_element(self, locator, value):
        element = await asynchronous.find_element(
            self.__remote, self.__session, locator, value
        )
        return Element(element, self.__remote, self.__session)
