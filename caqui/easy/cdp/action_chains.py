# Copyright (C) 2023 Caqui - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://github.com/douglasdcm/caqui

from typing import TYPE_CHECKING, Coroutine, List, Union

from caqui.cdp import asynchronous

if TYPE_CHECKING:
    from caqui.easy.cdp.drivers import AsyncDriver
    from caqui.easy.cdp.element import Element


class ActionChains:
    def __init__(self, driver: "AsyncDriver") -> None:
        self._conn = driver.conn
        self._coroutines: List[Coroutine] = []
        self._element = Union["Element", None]

    def click(self, element: "Element") -> "ActionChains":
        """
        Clicks on the element `element`
        """
        self._element = element
        coroutine = asynchronous.click(
            self._conn,
            element.element_id,
        )
        self._coroutines.append(coroutine)
        return self

    def move_to_element(self, element: "Element") -> "ActionChains":
        """Move the mouse to the element `element`"""
        self._element = element
        coroutine = asynchronous.actions_move_to_element(
            self._conn,
            element.element_id,
        )
        self._coroutines.append(coroutine)
        return self

    def scroll_to_element(self, element: "Element", delta_y: int = 1000) -> "ActionChains":
        """Scrolls the screen to the element `element`"""
        self._element = element
        coroutine = asynchronous.actions_scroll_to_element(
            self._conn,
            element.element_id,
        )
        self._coroutines.append(coroutine)
        return self

    async def perform(self) -> None:
        """Executes the chain of Coroutines"""
        [await coroutine for coroutine in self._coroutines]
