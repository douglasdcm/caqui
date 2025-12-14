# Copyright (C) 2023 Caqui - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://github.com/douglasdcm/caqui

import os
from typing import TYPE_CHECKING, Dict, List, Tuple

from caqui.cdp import asynchronous

if TYPE_CHECKING:
    from caqui.easy.cdp.drivers import AsyncDriver


class Element:
    def __init__(self, element: str, driver: "AsyncDriver") -> None:
        self._element: str = element
        self._conn: str = driver.conn
        self._driver: "AsyncDriver" = driver
        self._locator_type: str = ""
        self._locator_value: str = ""

    def __str__(self) -> str:
        return f"type: Element. NodeId: {self._element}"

    @property
    def element_id(self) -> str:
        return self._element

    # TODO test it
    @property
    def locator(self) -> Tuple[str, str]:
        return (self._locator_type, self._locator_value)

    # TODO test it
    @locator.setter
    def locator(self, locator: Tuple[str, str]) -> None:
        """
        Stores the locator type and values

        Args:
            value: the locator type and value, for example, ('xpath', '//a')
        """
        self._locator_type, self._locator_value = locator

    # TODO test it
    async def get_rect(self) -> Dict[str, float]:
        """Returns the rectangle that enclosed the element
        For example: {"height": 23, "width": 183, "x": 10, "y": 9652.12}
        """
        return await asynchronous.get_rect(self._conn, self._element)

    # TODO test it
    async def tag_name(self) -> str:
        """Returns the tag name of the element"""
        return await asynchronous.get_tag_name(self._conn, self._element)

    # TODO test it
    async def active_element(self) -> "Element":
        """Returns the active element"""
        self._element = await asynchronous.get_active_element(self._conn)
        return Element(self._element, driver=self._driver)

    @property
    def shadow_root(self) -> "ShadowElement":
        return ShadowElement(self._element, self._driver)

    async def describe_element(self):
        return await asynchronous.describe_node_id(self._conn, self._element)

    # TODO test it
    async def value_of_css_property(self, property_name: str) -> str:
        """Returns the desired CSS property of the element"""
        return await asynchronous.get_css_value(
            self._conn,
            self._element,
            property_name,
        )

    async def screenshot(self, file) -> None:
        """Takes a screenshot of the element"""
        path = os.path.dirname(file)
        if not path:
            path = "./"
        file_name = os.path.basename(file)
        await asynchronous.take_screenshot_element(
            self._conn,
            self._element,
            path,
            file_name,
        )

    async def is_selected(self) -> bool:
        """Returns True if the element is selected. Otherwise returns False"""
        return await asynchronous.is_element_selected(
            self._conn,
            self._element,
        )

    async def is_enabled(self) -> bool:
        """Returns True if the element is enabled. Otherwise returns False"""
        return await asynchronous.is_element_enabled(
            self._conn,
            self._element,
        )

    async def get_text(self) -> str:
        """Returns the text of the element"""
        return await asynchronous.get_text(
            self._conn,
            self._element,
        )

    async def get_css_value(self, property_name: str) -> str:
        """Returns the desired CSS property of the element"""
        return await asynchronous.get_css_value(
            self._conn,
            self._element,
            property_name,
        )

    async def submit(self) -> None:
        """Submits a form"""
        await asynchronous.submit(
            self._conn,
            self._element,
        )

    async def get_rect(self) -> Dict[str, float]:
        """Returns the rectangle that enclosed the element"""
        return await asynchronous.get_rect(
            self._conn,
            self._element,
        )

    async def get_tag_name(self) -> str:
        """Returns the element tag name"""
        return await asynchronous.get_tag_name(
            self._conn,
            self._element,
        )

    async def get_computed_label(self) -> str:
        """Get the element tag computed label. Get the accessibility name"""
        return await asynchronous.get_computed_label(
            self._conn,
            self._element,
        )

    async def get_computed_role(self) -> str:
        """Get the element tag computed role (the element role)"""
        return await asynchronous.get_computed_role(
            self._conn,
            self._element,
        )

    async def get_property(self, property: str) -> str:
        """Get the given HTML property of an element, for example, 'href'"""
        return await asynchronous.get_property(
            self._conn,
            self._element,
            property,
        )

    async def get_attribute(self, attribute: str) -> str:
        """Get the given HTML attribute of an element, for example, 'aria-valuenow'"""
        return await asynchronous.get_attribute(
            self._conn,
            self._element,
            attribute,
        )

    async def clear(self) -> None:
        """Clear the element text"""
        await asynchronous.clear_element(
            self._conn,
            self._element,
        )

    async def send_keys(self, text: str) -> None:
        """Fill the element with a text"""
        await asynchronous.send_keys(
            self._conn,
            self._element,
            text,
        )

    async def click(self) -> None:
        """Click on the element

        `Attention`: do not use it with Alerts/Prompts.
        These elements are opened automatically by find_element
        """
        await asynchronous.click(
            self._conn,
            self._element,
        )

    async def find_elements(self, locator: str, value: str) -> List["Element"]:
        """
        Find the children elements by 'locator_type'

        If the 'parent_element' is a shadow element,
         set the 'locator_type' as 'id' or 'css selector'
        """
        elements = await asynchronous.find_children_elements(
            self._conn,
            self._element,
            locator,
            value,
        )
        return [Element(element, self._driver) for element in elements]

    async def find_element(self, locator: str, value: str) -> "Element":
        """Find the element by `locator_type`"""
        element = await asynchronous.find_child_element(
            self._conn,
            self._element,
            locator,
            value,
        )
        return Element(element, self._driver)


class _FindShadowElementW3C:
    async def find_elements(self, element: "Element", locator: str, value: str) -> List["Element"]:
        """
        Find the children elements by 'locator_type'

        If the 'parent_element' is a shadow element,
         set the 'locator_type' as 'id' or 'css selector'
        """
        shadow_element = await asynchronous.get_shadow_elements(
            element._conn,
            element.element_id,
            locator,
            value,
        )
        return [Element(e, element._driver) for e in shadow_element]


class ShadowElement(Element):
    async def find_elements(self, locator, value) -> List[Element]:
        """Find a shadow element by a 'locator', for example 'xpath'"""
        return await _FindShadowElementW3C().find_elements(self, locator, value)

    async def find_element(self, locator, value) -> Element:
        """Find a shadow element by a 'locator', for example 'xpath'"""
        shadow_element = await asynchronous.get_shadow_element(
            self._conn,
            self.element_id,
            locator,
            value,
        )
        return Element(shadow_element, self._driver)
