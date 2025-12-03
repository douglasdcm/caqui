# Copyright (C) 2023 Caqui - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://github.com/douglasdcm/caqui

from typing import Coroutine, List, Union

from caqui import asynchronous
from caqui.easy.element import Element


class ActionChains:
    def __init__(self, driver) -> None:
        self._remote = driver.remote
        self._session = driver.session
        self._session_http = driver.session_http
        self._coroutines: List[Coroutine] = []
        self._element = Union[Element, None]

    def click(self, element: Element):
        """
        Clicks on the element `element`
        """
        self._element = element
        coroutine = asynchronous.click(
            self._remote, self._session, str(element), session_http=self._session_http
        )
        self._coroutines.append(coroutine)
        return self

    def move_to_element(self, element: Element):
        """Move the mouve to the element `element`"""
        self._element = element
        coroutine = asynchronous.actions_move_to_element(
            self._remote, self._session, str(element), session_http=self._session_http
        )
        self._coroutines.append(coroutine)
        return self

    def scroll_to_element(self, element: Element) -> "ActionChains":
        """Scrolls the screen to the element `element`"""
        self._element = element
        coroutine = asynchronous.actions_scroll_to_element(
            self._remote, self._session, str(element), session_http=self._session_http
        )
        self._coroutines.append(coroutine)
        return self

    async def perform(self):
        """Executes the chain of Coroutines"""
        [await coroutine for coroutine in self._coroutines]
        return True
