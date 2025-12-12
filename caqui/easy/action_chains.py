# Copyright (C) 2023 Caqui - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://github.com/douglasdcm/caqui

from typing import TYPE_CHECKING, Coroutine, List, Union

from caqui import asynchronous

if TYPE_CHECKING:
    from caqui.easy.drivers import AsyncDriver
    from caqui.easy.element import Element


class ActionChainsW3C:
    def __init__(self, driver: "AsyncDriver") -> None:
        self._server_url = driver.server_url
        self._session = driver.session
        self._session_http = driver.session_http
        self._coroutines: List[Coroutine] = []
        self._element = Union["Element", None]

    def click(self, element: "Element") -> "ActionChainsW3C":
        """
        Clicks on the element `element`
        """
        self._element = element
        coroutine = asynchronous.click(
            self._server_url, self._session, str(element), session_http=self._session_http
        )
        self._coroutines.append(coroutine)
        return self

    def move_to_element(self, element: "Element") -> "ActionChainsW3C":
        """Move the mouse to the element `element`"""
        self._element = element
        coroutine = asynchronous.actions_move_to_element(
            self._server_url, self._session, str(element), session_http=self._session_http
        )
        self._coroutines.append(coroutine)
        return self

    def scroll_to_element(self, element: "Element", delta_y: int = 1000) -> "ActionChainsW3C":
        """Scrolls the screen to the element `element`"""
        self._element = element
        coroutine = asynchronous.actions_scroll_to_element(
            self._server_url,
            self._session,
            str(element),
            delta_y=delta_y,
            session_http=self._session_http,
        )
        self._coroutines.append(coroutine)
        return self

    async def perform(self) -> None:
        """Executes the chain of Coroutines"""
        [await coroutine for coroutine in self._coroutines]


class ActionChainsJsonWire(ActionChainsW3C):
    def __init__(self, driver):
        super().__init__(driver)

    def move_to_element(self, element: "Element") -> "ActionChainsW3C":
        """Move the mouse to the element `element`"""
        self._element = element
        coroutine = asynchronous.actions_move_to_element_jsonwire(
            self._server_url, self._session, str(element), session_http=self._session_http
        )
        self._coroutines.append(coroutine)
        return self

    def scroll_to_element(self, element: "Element", delta_y=1000) -> "ActionChainsW3C":
        """Scrolls the screen to the element `element`"""
        self._element = element
        coroutine = asynchronous.actions_scroll_to_element_jsonwire(
            self._server_url,
            self._session,
            str(element),
            delta_y=delta_y,
            session_http=self._session_http,
        )
        self._coroutines.append(coroutine)
        return self
