import os
from caqui import asynchronous, synchronous


class Element:
    def __init__(self, element, driver) -> None:
        self._element = element
        self._remote = driver.remote
        self._session = driver.session
        self._session_http = driver.session_http
        self._driver = driver

    def __str__(self) -> str:
        return self._element

    @property
    def rect(self):
        """Returns the rectangle that enclosed the element
        For example: {"height": 23, "width": 183, "x": 10, "y": 9652.12}
        """
        return synchronous.get_rect(self._remote, self._session, self._element)

    @property
    def tag_name(self):
        """Returns the tag name of the element"""
        return synchronous.get_tag_name(self._remote, self._session, self._element)

    @property
    def text(self):
        """Returns the text of the element"""
        return synchronous.get_text(self._remote, self._session, self._element)

    @property
    def active_element(self):
        """Returns the active element"""
        self._element = synchronous.get_active_element(self._driver, self._session)
        return self._element

    async def value_of_css_property(self, property_name):
        """Returns the desired CSS property of the element"""
        return await asynchronous.get_css_value(
            self._remote,
            self._session,
            self._element,
            property_name,
            session_http=self._session_http,
        )

    async def screenshot(self, file):
        """Takes a screenshot of the element"""
        path = os.path.dirname(file)
        if not path:
            path = "./"
        file_name = os.path.basename(file)
        return await asynchronous.take_screenshot_element(
            self._remote,
            self._session,
            self._element,
            path,
            file_name,
            session_http=self._session_http,
        )

    async def is_selected(self) -> bool:
        """Returns True if the element is selected. Otherwise returns False"""
        return await asynchronous.is_element_selected(
            self._remote, self._session, self._element, session_http=self._session_http
        )

    async def is_enabled(self):
        """Returns True if the element is enabled. Otherwise returns False"""
        return await asynchronous.is_element_enabled(
            self._remote, self._session, self._element, session_http=self._session_http
        )

    async def get_text(self):
        """Returns the text of the element"""
        return await asynchronous.get_text(
            self._remote, self._session, self._element, session_http=self._session_http
        )

    async def get_css_value(self, property_name):
        """Returns the desired CSS property of the element"""
        return await asynchronous.get_css_value(
            self._remote,
            self._session,
            self._element,
            property_name,
            session_http=self._session_http,
        )

    async def submit(self):
        """Submits a form"""
        return await asynchronous.submit(
            self._remote, self._session, self._element, session_http=self._session_http
        )

    async def get_rect(self):
        """Returns the rectangle that enclosed the element"""
        return await asynchronous.get_rect(
            self._remote, self._session, self._element, session_http=self._session_http
        )

    async def get_tag_name(self):
        """Returns the element tag name"""
        return await asynchronous.get_tag_name(
            self._remote, self._session, self._element, session_http=self._session_http
        )

    async def get_computed_label(self):
        """Get the element tag computed label. Get the accessibility name"""
        return await asynchronous.get_computed_label(
            self._remote, self._session, self._element, session_http=self._session_http
        )

    async def get_computed_role(self):
        """Get the element tag computed role (the element role)"""
        return await asynchronous.get_computed_role(
            self._remote, self._session, self._element, session_http=self._session_http
        )

    async def get_property(self, property):
        """Get the given HTML property of an element, for example, 'href'"""
        return await asynchronous.get_property(
            self._remote, self._session, self._element, property, session_http=self._session_http
        )

    async def get_attribute(self, attribute):
        """Get the given HTML attribute of an element, for example, 'aria-valuenow'"""
        return await asynchronous.get_attribute(
            self._remote, self._session, self._element, attribute, session_http=self._session_http
        )

    async def clear(self):
        """Clear the element text"""
        return await asynchronous.clear_element(
            self._remote, self._session, self._element, session_http=self._session_http
        )

    async def send_keys(self, text):
        """Fill the element with a text"""
        return await asynchronous.send_keys(
            self._remote, self._session, self._element, text, session_http=self._session_http
        )

    async def click(self):
        """Click on the element"""
        return await asynchronous.click(
            self._remote, self._session, self._element, session_http=self._session_http
        )

    async def find_elements(self, locator, value):
        """
        Find the children elements by 'locator_type'

        If the 'parent_element' is a shadow element,
         set the 'locator_type' as 'id' or 'css selector'
        """
        result = []
        elements = await asynchronous.find_children_elements(
            self._remote,
            self._session,
            self._element,
            locator,
            value,
            session_http=self._session_http,
        )
        for element in elements:
            result.append(Element(element, self._driver))
        return result

    async def find_element(self, locator, value):
        """Find the element by `locator_type`"""
        element = await asynchronous.find_child_element(
            self._remote,
            self._session,
            self._element,
            locator,
            value,
            session_http=self._session_http,
        )
        return Element(element, self._driver)
