# Copyright (C) 2023 Caqui - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://github.com/douglasdcm/caqui

from typing import TYPE_CHECKING, List, Union

from caqui.cdp import synchronous

if TYPE_CHECKING:
    from caqui.easy.cdp.synchronous.drivers import SyncDriverCDP
    from caqui.easy.cdp.synchronous.element import Element


class ActionChains:
    def __init__(self, driver: "SyncDriverCDP") -> None:
        self._conn = driver.conn
        self._commands: List = []
        self._element = Union["Element", None]

    def click(self, element: "Element") -> "ActionChains":
        """
        Clicks on the element `element`
        """
        self._element = element
        coroutine = synchronous.click(
            self._conn,
            element.element_id,
        )
        self._commands.append(coroutine)
        return self

    def move_to_element(self, element: "Element") -> "ActionChains":
        """Move the mouse to the element `element`"""
        self._element = element
        coroutine = synchronous.actions_move_to_element(
            self._conn,
            element.element_id,
        )
        self._commands.append(coroutine)
        return self

    def scroll_to_element(self, element: "Element", delta_y: int = 1000) -> "ActionChains":
        """Scrolls the screen to the element `element`"""
        self._element = element
        coroutine = synchronous.actions_scroll_to_element(
            self._conn,
            element.element_id,
        )
        self._commands.append(coroutine)
        return self

    def perform(self) -> None:
        """Executes the chain of Commands"""
        [command for command in self._commands]
