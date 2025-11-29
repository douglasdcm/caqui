from caqui import asynchronous
from caqui.easy.element import Element
from typing import Coroutine


class ActionChains:
    def __init__(self, driver) -> None:
        self._remote = driver.remote
        self._session = driver.session
        self._session_http = driver.session_http
        self._coroutines: list[Coroutine] = []
        self._element = None

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

    def scroll_to_element(self, element: Element):
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
