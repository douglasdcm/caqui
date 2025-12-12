# Copyright (C) 2023 Caqui - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://github.com/douglasdcm/caqui

import os
from typing import TYPE_CHECKING, Callable, Dict, List, Optional, Tuple

from aiohttp import ClientSession

from caqui import asynchronous, synchronous
from caqui.constants import Specification

if TYPE_CHECKING:
    from caqui.easy.drivers import AsyncDriver


class _FindShadowElement:
    async def find_element(self, element: "Element", locator: str, value: str) -> "Element":
        raise NotImplementedError("Not implemented by subclass")

    async def find_elements(self, element: "Element", locator, value) -> List["Element"]:
        raise NotImplementedError("Not implemented by subclass")


class _FindShadowElementW3C(_FindShadowElement):
    async def find_elements(self, element: "Element", locator: str, value: str) -> List["Element"]:
        """
        Find the children elements by 'locator_type'

        If the 'parent_element' is a shadow element,
         set the 'locator_type' as 'id' or 'css selector'
        """
        shadow_root = await asynchronous.get_shadow_root(
            element._server_url, element._session, element._element, element._session_http
        )
        shadow_element = await asynchronous.get_shadow_elements(
            element._server_url,
            element._session,
            shadow_root,
            locator,
            value,
            element._session_http,
        )
        return [Element(e, element._driver) for e in shadow_element]

    async def find_element(self, element: "Element", locator: str, value: str) -> "Element":
        """
        Find the children elements by 'locator_type'

        If the 'parent_element' is a shadow element,
         set the 'locator_type' as 'id' or 'css selector'
        """
        shadow_root = await asynchronous.get_shadow_root(
            element._server_url, element._session, element._element, element._session_http
        )
        shadow_element = await asynchronous.get_shadow_element(
            element._server_url,
            element._session,
            shadow_root,
            locator,
            value,
            element._session_http,
        )
        return Element(shadow_element, element._driver)


class _FindShadowElementJsonWire:
    async def find_elements(self, element: "Element", locator: str, value: str) -> List["Element"]:
        """
        Find the children elements by 'locator_type'

        If the 'parent_element' is a shadow element,
         set the 'locator_type' as 'id' or 'css selector'
        """
        shadow_root = await asynchronous.get_shadow_root(
            element._server_url, element._session, element._element, element._session_http
        )
        shadow_element = await asynchronous.get_shadow_elements_jsonwire(
            element._server_url,
            element._session,
            shadow_root,
            locator,
            value,
            element._session_http,
        )
        return [Element(e, element._driver) for e in shadow_element]

    async def find_element(self, element: "Element", locator: str, value: str) -> "Element":
        """
        Find the children elements by 'locator_type'

        If the 'parent_element' is a shadow element,
         set the 'locator_type' as 'id' or 'css selector'
        """
        shadow_root = await asynchronous.get_shadow_root(
            element._server_url, element._session, element._element, element._session_http
        )
        shadow_element = await asynchronous.get_shadow_element_jsonwire(
            element._server_url,
            element._session,
            shadow_root,
            locator,
            value,
            element._session_http,
        )
        return Element(shadow_element, element._driver)


FIND_ELEMENT_SHADOW_IMPLEMENTATIONS: Dict[str, Callable] = {
    Specification.FIREFOX: _FindShadowElementW3C,
    Specification.CHROME: _FindShadowElementJsonWire,
    Specification.EDGE: _FindShadowElementJsonWire,
    Specification.OPERA: _FindShadowElementJsonWire,
    Specification.JSONWIRE: _FindShadowElementJsonWire,
    Specification.W3C: _FindShadowElementW3C,
}


class Element:
    def __init__(self, element: str, driver: "AsyncDriver") -> None:
        self._element: str = element
        self._server_url: str = driver.server_url
        self._session: str = driver.session
        self._session_http: Optional[ClientSession] = driver.session_http
        self._driver: "AsyncDriver" = driver
        self._locator_type: str = ""
        self._locator_value: str = ""

    def __str__(self) -> str:
        return self._element

    @property
    def element_id(self) -> str:
        return self._element

    @property
    def locator(self) -> Tuple[str, str]:
        return (self._locator_type, self._locator_value)

    @locator.setter
    def locator(self, locator: Tuple[str, str]) -> None:
        """
        Stores the locator type and values

        Args:
            value: the locator type and value, for example, ('xpath', '//a')
        """
        self._locator_type, self._locator_value = locator

    @property
    def rect(self) -> Dict[str, float]:
        """Returns the rectangle that enclosed the element
        For example: {"height": 23, "width": 183, "x": 10, "y": 9652.12}
        """
        return synchronous.get_rect(self._server_url, self._session, self._element)

    @property
    def tag_name(self) -> str:
        """Returns the tag name of the element"""
        return synchronous.get_tag_name(self._server_url, self._session, self._element)

    @property
    def text(self) -> str:
        """Returns the text of the element"""
        return synchronous.get_text(self._server_url, self._session, self._element)

    @property
    def active_element(self) -> "Element":
        """Returns the active element"""
        self._element = synchronous.get_active_element(self._server_url, self._session)
        return Element(self._element, driver=self._driver)

    @property
    def shadow_root(self) -> "ShadowElement":
        return ShadowElement(self._element, self._driver)

    async def value_of_css_property(self, property_name: str) -> str:
        """Returns the desired CSS property of the element"""
        return await asynchronous.get_css_value(
            self._server_url,
            self._session,
            self._element,
            property_name,
            session_http=self._session_http,
        )

    async def screenshot(self, file) -> None:
        """Takes a screenshot of the element"""
        path = os.path.dirname(file)
        if not path:
            path = "./"
        file_name = os.path.basename(file)
        await asynchronous.take_screenshot_element(
            self._server_url,
            self._session,
            self._element,
            path,
            file_name,
            session_http=self._session_http,
        )

    async def is_selected(self) -> bool:
        """Returns True if the element is selected. Otherwise returns False"""
        return await asynchronous.is_element_selected(
            self._server_url, self._session, self._element, session_http=self._session_http
        )

    async def is_enabled(self) -> bool:
        """Returns True if the element is enabled. Otherwise returns False"""
        return await asynchronous.is_element_enabled(
            self._server_url, self._session, self._element, session_http=self._session_http
        )

    async def get_text(self) -> str:
        """Returns the text of the element"""
        return await asynchronous.get_text(
            self._server_url, self._session, self._element, session_http=self._session_http
        )

    async def get_css_value(self, property_name: str) -> str:
        """Returns the desired CSS property of the element"""
        return await asynchronous.get_css_value(
            self._server_url,
            self._session,
            self._element,
            property_name,
            session_http=self._session_http,
        )

    async def submit(self) -> None:
        """Submits a form"""
        await asynchronous.submit(
            self._server_url, self._session, self._element, session_http=self._session_http
        )

    async def get_rect(self) -> Dict[str, float]:
        """Returns the rectangle that enclosed the element"""
        return await asynchronous.get_rect(
            self._server_url, self._session, self._element, session_http=self._session_http
        )

    async def get_tag_name(self) -> str:
        """Returns the element tag name"""
        return await asynchronous.get_tag_name(
            self._server_url, self._session, self._element, session_http=self._session_http
        )

    async def get_computed_label(self) -> str:
        """Get the element tag computed label. Get the accessibility name"""
        return await asynchronous.get_computed_label(
            self._server_url, self._session, self._element, session_http=self._session_http
        )

    async def get_computed_role(self) -> str:
        """Get the element tag computed role (the element role)"""
        return await asynchronous.get_computed_role(
            self._server_url, self._session, self._element, session_http=self._session_http
        )

    async def get_property(self, property: str) -> str:
        """Get the given HTML property of an element, for example, 'href'"""
        return await asynchronous.get_property(
            self._server_url,
            self._session,
            self._element,
            property,
            session_http=self._session_http,
        )

    async def get_attribute(self, attribute: str) -> str:
        """Get the given HTML attribute of an element, for example, 'aria-valuenow'"""
        return await asynchronous.get_attribute(
            self._server_url,
            self._session,
            self._element,
            attribute,
            session_http=self._session_http,
        )

    async def clear(self) -> None:
        """Clear the element text"""
        await asynchronous.clear_element(
            self._server_url, self._session, self._element, session_http=self._session_http
        )

    async def send_keys(self, text: str) -> None:
        """Fill the element with a text"""
        await asynchronous.send_keys(
            self._server_url, self._session, self._element, text, session_http=self._session_http
        )

    async def click(self) -> None:
        """Click on the element"""
        await asynchronous.click(
            self._server_url, self._session, self._element, session_http=self._session_http
        )

    async def find_elements(self, locator: str, value: str) -> List["Element"]:
        """
        Find the children elements by 'locator_type'

        If the 'parent_element' is a shadow element,
         set the 'locator_type' as 'id' or 'css selector'
        """
        elements = await asynchronous.find_children_elements(
            self._server_url,
            self._session,
            self._element,
            locator,
            value,
            session_http=self._session_http,
        )
        return [Element(element, self._driver) for element in elements]

    async def find_element(self, locator: str, value: str) -> "Element":
        """Find the element by `locator_type`"""
        element = await asynchronous.find_child_element(
            self._server_url,
            self._session,
            self._element,
            locator,
            value,
            session_http=self._session_http,
        )
        return Element(element, self._driver)


class ShadowElement(Element):
    async def find_elements(self, locator, value) -> List[Element]:
        """Find a shadow element by a 'locator', for example 'xpath'"""
        return await FIND_ELEMENT_SHADOW_IMPLEMENTATIONS[self._driver.browser]().find_elements(
            self, locator, value
        )

    async def find_element(self, locator, value) -> Element:
        """Find a shadow element by a 'locator', for example 'xpath'"""
        return await FIND_ELEMENT_SHADOW_IMPLEMENTATIONS[self._driver.browser]().find_element(
            self, locator, value
        )
