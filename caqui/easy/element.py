import os
from caqui import asynchronous, synchronous


class Element:
    def __init__(self, element, driver) -> None:
        self.__element = element
        self.__remote = driver.remote
        self.__session = driver.session
        self.__driver = driver

    def __str__(self) -> str:
        return self.__element

    @property
    def rect(self):
        return synchronous.get_rect(self.__remote, self.__session, self.__element)

    @property
    def tag_name(self):
        return synchronous.get_tag_name(self.__remote, self.__session, self.__element)

    @property
    def text(self):
        return synchronous.get_text(self.__remote, self.__session, self.__element)

    @property
    def active_element(self):
        self.__element = synchronous.get_active_element(self.__driver, self.__session)
        return self.__element

    async def value_of_css_property(self, property_name):
        return await asynchronous.get_css_value(
            self.__remote, self.__session, self.__element, property_name
        )

    async def screenshot(self, file):
        path = os.path.dirname(file)
        if not path:
            path = "./"
        file_name = os.path.basename(file)
        return await asynchronous.take_screenshot_element(
            self.__remote, self.__session, self.__element, path, file_name
        )

    async def is_selected(self):
        return await asynchronous.is_element_selected(
            self.__remote, self.__session, self.__element
        )

    async def is_enabled(self):
        return await asynchronous.is_element_enabled(
            self.__remote, self.__session, self.__element
        )

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

    async def get_computed_label(self):
        return await asynchronous.get_computed_label(
            self.__remote, self.__session, self.__element
        )

    async def get_computed_role(self):
        return await asynchronous.get_computed_role(
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
