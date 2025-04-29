from caqui import asynchronous
from caqui.easy.element import Element


class ActionChains:
    def __init__(self, driver) -> None:
        self.__remote = driver.remote
        self.__session = driver.session
        self.__coroutines = []

    def click(self, element: Element):
        """Clicks on the element `element`"""
        self.__element = element
        coroutine = asynchronous.click(self.__remote, self.__session, str(element))
        self.__coroutines.append(coroutine)
        return self

    def move_to_element(self, element: Element):
        """Move the mouve to the element `element`"""
        self.__element = element
        coroutine = asynchronous.actions_move_to_element(
            self.__remote, self.__session, str(element)
        )
        self.__coroutines.append(coroutine)
        return self

    def scroll_to_element(self, element: Element):
        """Scrolls the screen to the element `element`"""
        self.__element = element
        coroutine = asynchronous.actions_scroll_to_element(
            self.__remote, self.__session, str(element)
        )
        self.__coroutines.append(coroutine)
        return self

    async def perform(self):
        """Executes the chain of Coroutines"""
        for coroutine in self.__coroutines:
            await coroutine
        return True
